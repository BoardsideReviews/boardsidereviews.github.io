-- Boardside Reviews · Cross-Cover (daily crossword) leaderboard
-- Paste this whole file into Supabase → SQL Editor → New query → Run.
-- Safe to run more than once. Needs setup.sql to have been run first.
--
-- How the board works:
--  • One board per puzzle. variant = the puzzle's California date, e.g. '2026-11-10'.
--  • score = total = solve time in whole seconds. Lowest time wins; ties go to whoever posted first.
--  • Each player gets ONE post per puzzle (their first clean solve), so replaying can't improve it.
--  • Only today's puzzle (or yesterday's, for solves that run past midnight) can be posted to.
--  • Times under 8 seconds are rejected as not humanly possible.

-- ─────────────────────────────────────────────────────────────
-- 1. Rules checked on every Cross-Cover post
-- ─────────────────────────────────────────────────────────────
create or replace function public.cross_cover_check()
returns trigger language plpgsql security definer set search_path = public as $$
declare
  d date;
  today date := (now() at time zone 'America/Los_Angeles')::date;
begin
  if new.game <> 'cross-cover' then return new; end if;
  begin
    d := to_date(new.variant, 'YYYY-MM-DD');
  exception when others then
    raise exception 'stale_puzzle';
  end;
  if new.variant !~ '^\d{4}-\d{2}-\d{2}$' or d > today or d < today - 1 then
    raise exception 'stale_puzzle';
  end if;
  if new.score <> new.total then raise exception 'bad_time'; end if;
  if new.score < 8 then raise exception 'too_quick'; end if;
  if new.score > 86400 then raise exception 'bad_time'; end if;
  if exists (select 1 from public.scores
             where user_id = new.user_id and game = 'cross-cover' and variant = new.variant) then
    raise exception 'already_posted';
  end if;
  return new;
end;
$$;

drop trigger if exists cross_cover_check on public.scores;
create trigger cross_cover_check
  before insert on public.scores
  for each row execute function public.cross_cover_check();

-- Backstop so two posts sent at the same instant can't both land.
create unique index if not exists scores_cross_cover_once
  on public.scores (user_id, variant) where game = 'cross-cover';

-- ─────────────────────────────────────────────────────────────
-- 2. Public board: fastest time first
-- ─────────────────────────────────────────────────────────────
create or replace function public.get_time_leaderboard(p_game text, p_variant text, p_limit integer default 50)
returns table (rank bigint, display_name text, seconds integer, achieved_at timestamptz, is_me boolean)
language sql stable security definer set search_path = public as $$
  with s as (
    select distinct on (sc.user_id) sc.user_id, sc.score, sc.created_at
    from public.scores sc
    join public.profiles pr on pr.user_id = sc.user_id
    where sc.game = p_game and sc.variant = p_variant
      and pr.display_name is not null and not pr.banned
    order by sc.user_id, sc.created_at asc
  )
  select rank() over (order by s.score asc, s.created_at asc),
         pr.display_name, s.score, s.created_at, (s.user_id = auth.uid())
  from s
  join public.profiles pr on pr.user_id = s.user_id
  order by s.score asc, s.created_at asc
  limit least(greatest(coalesce(p_limit, 50), 1), 200);
$$;

revoke execute on function public.get_time_leaderboard(text, text, integer) from public;
grant execute on function public.get_time_leaderboard(text, text, integer) to anon, authenticated;
