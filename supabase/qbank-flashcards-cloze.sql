-- Boardside Reviews · flashcards return the question's references (Nov 11, 2026). Already applied live; kept for the record.
create or replace function public.qb_flashcards(p_limit integer default 40)
returns json language plpgsql security definer set search_path = public as $$
declare uid uuid := public.qb_require();
begin
  return (
    with pool as (
      select s.question_id from public.qb_status s where s.user_id = uid and s.last_correct = false
      union
      select r.question_id from public.qb_responses r
        join public.qb_status s on s.user_id = r.user_id and s.question_id = r.question_id
       where r.user_id = uid and r.flagged
    ),
    -- latest confidence rating per question (only learners who use confidence ratings have any)
    conf as (
      select distinct on (c.qid) c.qid, c.level, c.correct
        from public.qb_confidence c
       where c.user_id = uid
       order by c.qid, c.updated_at desc
    ),
    -- correct answers that were only a guess are weak spots too; they join the deck once it is unlocked
    lucky as (
      select f.qid as question_id from conf f
        join public.qb_status s on s.user_id = uid and s.question_id = f.qid
       where f.level = 'guess' and s.last_correct
         and f.qid not in (select question_id from pool)
    ),
    deck as (
      select question_id from pool
      union
      select question_id from lucky where (select count(*) from pool) >= 50
    ),
    cards as (
      select p.question_id, coalesce(c.due_at, '-infinity'::timestamptz) as due_at,
             coalesce(c.interval_days, 0) as iv, coalesce(c.reps, 0) as reps, c.question_id is null as is_new,
             f.level as conf,
             -- priority among due cards: sure-but-wrong first (a misconception), then guesses, then unsure
             case when f.level = 'sure' and s.last_correct = false then 0
                  when f.level = 'guess' then 1
                  when f.level = 'unsure' then 2 else 3 end as prio,
             (f.level = 'sure' and s.last_correct = false) as sure_wrong,
             (f.level = 'guess' and s.last_correct) as lucky_guess
        from deck p
        left join public.qb_srs c on c.user_id = uid and c.question_id = p.question_id
        left join conf f on f.qid = p.question_id
        left join public.qb_status s on s.user_id = uid and s.question_id = p.question_id
    ),
    n as (select count(*) as pool from pool)
    select json_build_object(
      'pool', (select pool from n),
      'min_pool', 50,
      'deck', (select count(*) from cards),
      'due_count', case when (select pool from n) < 50 then 0 else (select count(*) from cards where due_at <= now()) end,
      'new_count', (select count(*) from cards where is_new),
      'next_due', (select min(due_at) from cards where due_at > now()),
      'cards', case when (select pool from n) < 50 then '[]'::json else coalesce((
        select json_agg(x) from (
          select q.id, q.num, q.subject, q.body->>'stem' as stem, q.body->'data' as data, q.body->>'exam' as exam, q.body->'tests' as tests, q.body->'notes' as notes, q.body->>'ask' as ask,
                 q.answer, q.body->'choices'->>q.answer as answer_text, q.explain->'reasons'->>q.answer as why,
                 q.explain->>'pearl' as pearl, q.explain->'details'->>q.answer as detail,
                 q.explain->>'references' as refs, q.explain->'ref_links' as ref_links,
                 c.iv as interval_days, c.reps, c.is_new, c.conf, c.sure_wrong, c.lucky_guess
            from cards c join public.qb_questions q on q.id = c.question_id
           where c.due_at <= now()
           order by (c.due_at = '-infinity'::timestamptz) desc, c.prio, c.due_at, random()
           limit greatest(1, least(coalesce(p_limit, 40), 100))
        ) x), '[]'::json) end
    ));
end;
$$;