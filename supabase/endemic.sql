-- Boardside Reviews · Endemic (daily one-pin map game) leaderboard guard
-- Paste this whole file into Supabase → SQL Editor → New query → Run.
-- Safe to run more than once. The board works without it; this makes it fair.
--
-- How the board works:
--  • One board per day. variant = the California date, e.g. '2026-11-12'.
--  • score = points (0 to 5000, highest wins; ties go to whoever posted first). total = 5000.
--  • Each player gets ONE post per day (their first pin), so replaying can't improve it.
--  • Only today's board (or yesterday's, for guesses locked in just before midnight) can be posted to.

create or replace function public.endemic_check()
returns trigger language plpgsql security definer set search_path = public as $$
declare
  d date;
  today date := (now() at time zone 'America/Los_Angeles')::date;
begin
  if new.game <> 'endemic' then return new; end if;
  begin
    d := to_date(new.variant, 'YYYY-MM-DD');
  exception when others then
    raise exception 'stale_puzzle';
  end;
  if new.variant !~ '^\d{4}-\d{2}-\d{2}$' or d > today or d < today - 1 then
    raise exception 'stale_puzzle';
  end if;
  if new.score < 0 or new.score > 5000 or new.total <> 5000 then raise exception 'bad_time'; end if;
  if exists (select 1 from public.scores
             where user_id = new.user_id and game = 'endemic' and variant = new.variant) then
    raise exception 'endemic_once';
  end if;
  return new;
end;
$$;

drop trigger if exists endemic_check on public.scores;
create trigger endemic_check
  before insert on public.scores
  for each row execute function public.endemic_check();

-- Backstop so two posts sent at the same instant can't both land.
create unique index if not exists scores_endemic_once
  on public.scores (user_id, variant) where game = 'endemic';
