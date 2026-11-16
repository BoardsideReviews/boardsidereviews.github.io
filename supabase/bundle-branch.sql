-- Boardside Reviews · Bundle Branch (daily medical word search) no-hint leaderboard guard
-- Paste this whole file into Supabase → SQL Editor → New query → Run.
-- Safe to run more than once. Needs setup.sql and cross-cover.sql (for get_time_leaderboard) to have been run first.
--
-- How the board works:
--  • One board per day. variant = the California date, e.g. '2026-11-16'.
--  • score = total = solve time in whole seconds. Lowest time wins; ties go to whoever posted first.
--  • Only solves with no hints can be posted (the game hides the button otherwise).
--  • Each player gets ONE post per day (their first board), so replaying can't improve it.
--  • Only today's board (or yesterday's, for solves that run past midnight) can be posted to.
--  • Times under 15 seconds are rejected as not humanly possible.

create or replace function public.bundle_branch_check()
returns trigger language plpgsql security definer set search_path = public as $$
declare
  d date;
  today date := (now() at time zone 'America/Los_Angeles')::date;
begin
  if new.game <> 'bundle-branch' then return new; end if;
  begin
    d := to_date(new.variant, 'YYYY-MM-DD');
  exception when others then
    raise exception 'stale_puzzle';
  end;
  if new.variant !~ '^\d{4}-\d{2}-\d{2}$' or d > today or d < today - 1 then
    raise exception 'stale_puzzle';
  end if;
  if new.score <> new.total then raise exception 'bad_time'; end if;
  if new.score < 15 then raise exception 'too_quick'; end if;
  if new.score > 86400 then raise exception 'bad_time'; end if;
  if exists (select 1 from public.scores
             where user_id = new.user_id and game = 'bundle-branch' and variant = new.variant) then
    raise exception 'already_posted';
  end if;
  return new;
end;
$$;

drop trigger if exists bundle_branch_check on public.scores;
create trigger bundle_branch_check
  before insert on public.scores
  for each row execute function public.bundle_branch_check();

-- Backstop so two posts sent at the same instant can't both land.
do $$ begin
  create unique index if not exists scores_bundle_branch_once
    on public.scores (user_id, variant) where game = 'bundle-branch';
exception when others then raise notice 'scores_bundle_branch_once not created: %', sqlerrm;
end $$;
