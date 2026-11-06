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
