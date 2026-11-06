-- Boardside Reviews · question bank confidence ratings
-- Paste this whole file into Supabase → SQL Editor → New query → Run.
-- Safe to run more than once.
--
-- Until this runs, confidence ratings still work but are saved only in the
-- learner's browser. After it runs, they also save to the database and
-- follow the learner to any device.

create table if not exists public.qb_confidence (
  user_id    uuid not null default auth.uid() references auth.users(id) on delete cascade,
  block_id   text not null,
  qid        text not null,
  level      text not null check (level in ('sure', 'unsure', 'guess')),
  correct    boolean,
  updated_at timestamptz not null default now(),
  primary key (user_id, block_id, qid)
);

alter table public.qb_confidence enable row level security;

-- Each learner can see and change only their own ratings.
drop policy if exists qb_confidence_select on public.qb_confidence;
create policy qb_confidence_select on public.qb_confidence
  for select using (user_id = auth.uid());

drop policy if exists qb_confidence_insert on public.qb_confidence;
create policy qb_confidence_insert on public.qb_confidence
  for insert with check (user_id = auth.uid());

drop policy if exists qb_confidence_update on public.qb_confidence;
create policy qb_confidence_update on public.qb_confidence
  for update using (user_id = auth.uid()) with check (user_id = auth.uid());

drop policy if exists qb_confidence_delete on public.qb_confidence;
create policy qb_confidence_delete on public.qb_confidence
  for delete using (user_id = auth.uid());

grant select, insert, update, delete on public.qb_confidence to authenticated;


-- Spaced-repetition flashcards built from each learner's missed and flagged questions.
create table if not exists public.qb_srs (
  user_id       uuid not null references auth.users(id) on delete cascade,
  question_id   text not null references public.qb_questions(id) on delete cascade,
  interval_days real not null default 0,
  reps          integer not null default 0,
  due_at        timestamptz not null default now(),
  last_rating   text,
  updated_at    timestamptz not null default now(),
  primary key (user_id, question_id)
);
alter table public.qb_srs enable row level security;
revoke all on public.qb_srs from anon, authenticated;

-- Pool = questions the learner has answered and either got wrong last time or flagged.
-- Cards are only returned once the pool reaches 50.
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
          select q.id, q.num, q.subject, q.body->>'stem' as stem, q.body->'data' as data, q.body->>'ask' as ask,
                 q.answer, q.body->'choices'->>q.answer as answer_text, q.explain->'reasons'->>q.answer as why,
                 q.explain->>'pearl' as pearl, q.explain->'details'->>q.answer as detail,
                 c.iv as interval_days, c.reps, c.is_new, c.conf, c.sure_wrong, c.lucky_guess
            from cards c join public.qb_questions q on q.id = c.question_id
           where c.due_at <= now()
           order by (c.due_at = '-infinity'::timestamptz) desc, c.prio, c.due_at, random()
           limit greatest(1, least(coalesce(p_limit, 40), 100))
        ) x), '[]'::json) end
    ));
end;
$$;

-- repeat: show again in 10 minutes and halve the interval (more frequent)
-- good:   keep the same interval (minimum 1 day)
-- great:  stretch the interval 2.5x (new card: 4 days), capped at 180 days
create or replace function public.qb_flashcard_rate(p_qid text, p_rating text)
returns json language plpgsql security definer set search_path = public as $$
declare uid uuid := public.qb_require(); iv real; nv real; due timestamptz;
begin
  if p_rating not in ('repeat', 'good', 'great') then raise exception 'bad_rating'; end if;
  if not exists (select 1 from public.qb_status where user_id = uid and question_id = p_qid) then raise exception 'not_in_pool'; end if;
  select interval_days into iv from public.qb_srs where user_id = uid and question_id = p_qid;
  iv := coalesce(iv, 0);
  if p_rating = 'repeat' then
    nv := iv / 2; due := now() + interval '10 minutes';
  elsif p_rating = 'good' then
    nv := greatest(iv, 1); due := now() + make_interval(secs => nv * 86400);
  else
    nv := case when iv = 0 then 4 else least(greatest(iv, 1) * 2.5, 180) end;
    -- confidence-aware: a card the learner was sure about and still missed stretches more slowly
    if exists (select 1 from public.qb_status s where s.user_id = uid and s.question_id = p_qid and not s.last_correct)
       and coalesce((select c.level from public.qb_confidence c where c.user_id = uid and c.qid = p_qid order by c.updated_at desc limit 1), '') = 'sure'
    then nv := case when iv = 0 then 3 else least(greatest(iv, 1) * 2, 180) end; end if;
    due := now() + make_interval(secs => nv * 86400);
  end if;
  insert into public.qb_srs (user_id, question_id, interval_days, reps, due_at, last_rating, updated_at)
  values (uid, p_qid, nv, 1, due, p_rating, now())
  on conflict (user_id, question_id) do update set interval_days = excluded.interval_days, reps = public.qb_srs.reps + 1,
    due_at = excluded.due_at, last_rating = excluded.last_rating, updated_at = now();
  return json_build_object('interval_days', nv, 'due_at', due);
end;
$$;

revoke all on function public.qb_flashcards(integer) from public, anon;
revoke all on function public.qb_flashcard_rate(text, text) from public, anon;
grant execute on function public.qb_flashcards(integer) to authenticated;
grant execute on function public.qb_flashcard_rate(text, text) to authenticated;
select 'confidence + flashcards ready' as status, to_regclass('public.qb_confidence') is not null as conf_table, (select count(*) from pg_proc where proname in ('qb_flashcards','qb_flashcard_rate')) as functions;
