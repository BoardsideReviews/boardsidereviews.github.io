-- Boardside Reviews · Rhythm Rush leaderboard guard
-- Paste into Supabase → SQL Editor → Run. Safe to run more than once.
-- The leaderboard works without this; it just blocks impossible scores.

-- Rhythm Rush (60 seconds of play): cap obviously fake posts.
alter table public.scores drop constraint if exists rhythm_rush_cap;
alter table public.scores add constraint rhythm_rush_cap
  check (game <> 'rhythm-rush' or score <= 20000);
