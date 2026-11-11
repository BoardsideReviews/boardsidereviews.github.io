-- Boardside Reviews · Co-Pay or No Way (daily drug-price higher-or-lower) leaderboard guard
-- Paste this whole file into Supabase → SQL Editor → New query → Run.
-- Safe to run more than once. The board works without it; this makes it fair.
--
-- How the board works:
--  • One board per day. variant = the California date, e.g. '2026-11-10'.
--  • score = streak (longest wins; ties go to whoever posted first). total = max(streak, 1).
--  • Each player gets ONE post per day (their first run), so replaying can't improve it.
--  • Only today's board (or yesterday's, for runs that end just past midnight) can be posted to.

create or replace function public.copay_noway_check()
returns trigger language plpgsql security definer set search_path = public as $$
declare
  d date;
  today date := (now() at time zone 'America/Los_Angeles')::date;
begin
  if new.game <> 'copay-noway' then return new; end if;
  begin
    d := to_date(new.variant, 'YYYY-MM-DD');
  exception when others then
    raise exception 'stale_puzzle';
  end;
  if new.variant !~ '^\d{4}-\d{2}-\d{2}$' or d > today or d < today - 1 then
    raise exception 'stale_puzzle';
  end if;
  if new.score < 0 or new.score > 200 then raise exception 'bad_time'; end if;
  if exists (select 1 from public.scores
             where user_id = new.user_id and game = 'copay-noway' and variant = new.variant) then
    raise exception 'copay_once';
  end if;
  return new;
end;
$$;

drop trigger if exists copay_noway_check on public.scores;
create trigger copay_noway_check
  before insert on public.scores
  for each row execute function public.copay_noway_check();

-- Backstop so two posts sent at the same instant can't both land.
create unique index if not exists scores_copay_once
  on public.scores (user_id, variant) where game = 'copay-noway';
