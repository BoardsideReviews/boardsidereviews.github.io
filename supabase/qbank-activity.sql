-- Boardside Reviews · activity calendar (Anki-style heat map of questions + flashcards per day)
-- Paste into Supabase → SQL Editor → Run. Safe to run more than once.
--
-- Records one row each time a question is answered (counted) or a flashcard is rated, so the
-- question bank can show a day-by-day heat map, streaks and per-day totals in the learner's time zone.
-- On first install it fills in what can be recovered from existing answers and flashcards.

create table if not exists public.qb_activity (
  id      bigserial primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  kind    text not null check (kind in ('q', 'card')),
  correct boolean,
  at      timestamptz not null default now()
);
create index if not exists qb_activity_user_at on public.qb_activity (user_id, at);
alter table public.qb_activity enable row level security;
revoke all on public.qb_activity from anon, authenticated;

-- a question counts once, when it is scored (learning: on submit; exam: when the set ends)
create or replace function public.qb_activity_on_response()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  if new.counted and (tg_op = 'INSERT' or not coalesce(old.counted, false)) then
    insert into public.qb_activity (user_id, kind, correct) values (new.user_id, 'q', new.correct);
  end if;
  return new;
end;
$$;
drop trigger if exists qb_activity_response on public.qb_responses;
create trigger qb_activity_response after insert or update on public.qb_responses
  for each row execute function public.qb_activity_on_response();

-- every flashcard rating is one review ("repeat" counts as not yet remembered)
create or replace function public.qb_activity_on_card()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  if tg_op = 'INSERT' or new.updated_at is distinct from old.updated_at then
    insert into public.qb_activity (user_id, kind, correct) values (new.user_id, 'card', coalesce(new.last_rating, '') <> 'repeat');
  end if;
  return new;
end;
$$;
drop trigger if exists qb_activity_card on public.qb_srs;
create trigger qb_activity_card after insert or update on public.qb_srs
  for each row execute function public.qb_activity_on_card();

-- first install only: recover past activity (each answer's last-saved time; each card's latest review)
do $$
begin
  if not exists (select 1 from public.qb_activity) then
    insert into public.qb_activity (user_id, kind, correct, at)
    select r.user_id, 'q', r.correct, r.updated_at from public.qb_responses r where r.counted and r.updated_at is not null;
    insert into public.qb_activity (user_id, kind, correct, at)
    select c.user_id, 'card', coalesce(c.last_rating, '') <> 'repeat', c.updated_at from public.qb_srs c where c.updated_at is not null;
  end if;
end $$;

-- the signed-in learner's last ~13 months, one row per active day, in their own time zone
create or replace function public.qb_activity(p_tz text default 'UTC')
returns json language plpgsql stable security definer set search_path = public as $$
declare
  uid uuid := public.qb_require();
  tz text := case when exists (select 1 from pg_timezone_names where name = p_tz) then p_tz else 'UTC' end;
  res json;
begin
  select coalesce(json_agg(json_build_object('d', d, 'q', q, 'qc', qc, 'f', f) order by d), '[]'::json) into res
  from (
    select (a.at at time zone tz)::date as d,
           count(*) filter (where a.kind = 'q') as q,
           count(*) filter (where a.kind = 'q' and a.correct) as qc,
           count(*) filter (where a.kind = 'card') as f
    from public.qb_activity a
    where a.user_id = uid and a.at > now() - interval '400 days'
    group by 1
  ) x;
  return json_build_object('tz', tz, 'days', res);
end;
$$;
revoke execute on function public.qb_activity(text) from public, anon;
grant execute on function public.qb_activity(text) to authenticated;

select (select count(*) from public.qb_activity) as activity_rows;
