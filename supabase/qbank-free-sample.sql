-- Boardside Reviews · free sample (80 questions) + free accounts + Cardiology notes download
-- Paste this whole file into Supabase → SQL Editor → New query → Run.
-- Safe to run more than once.
--
-- What it does
--   1. Builds 4 free sets of 20 questions from the question bank:
--        Pulmonary & Critical Care (10 Pulm + 10 Crit Care, alternating), Cardiology,
--        Gastroenterology, Nephrology. Questions are picked AT RANDOM from across all of the
--        subject's sets, skipping image questions and hidden (inactive) ones.
--      The random picks are saved once in qb_free_items and then stay fixed, so free users
--      can't keep re-rolling their way through the paid bank. (The order is shuffled for each
--      learner every time they start a set.) To re-roll all 80:
--        delete from public.qb_free_items;   then run this file again.
--      To swap one question:
--        update public.qb_free_items set question_id = 'Cardiology-2-04'
--         where set_key = 'cardiology' and ord = 7;
--   2. Anyone (no account) can load the first 10 questions of each set.
--      Signed-in accounts with a verified email get all 20 of every set.
--      Free accounts do NOT get the full question bank: that still needs paid access.
--   3. A private storage bucket "free-samples" that only verified accounts can download from.
--      After running this, upload the PDF:
--        Storage → free-samples → Upload file → "boardside-notes-cardiology-sample.pdf"
--      (use exactly that file name).
--   4. admin_accounts(): the account list (waitlist + mailing-list choice) for admin.html.

-- ─────────────────────────────────────────────────────────────
-- 1. FREE SETS
-- ─────────────────────────────────────────────────────────────
create table if not exists public.qb_free_sets (
  set_key text primary key,
  title   text not null,
  blurb   text not null default '',
  sort    integer not null default 0
);
create table if not exists public.qb_free_items (
  set_key     text not null references public.qb_free_sets(set_key) on delete cascade,
  ord         integer not null,
  question_id text not null references public.qb_questions(id) on delete cascade,
  primary key (set_key, ord)
);
alter table public.qb_free_sets enable row level security;
alter table public.qb_free_items enable row level security;
revoke all on public.qb_free_sets, public.qb_free_items from anon, authenticated;

insert into public.qb_free_sets (set_key, title, blurb, sort) values
  ('pulm-crit',  'Pulmonary & Critical Care', '10 pulmonary and 10 critical care questions.', 1),
  ('cardiology', 'Cardiology',                '20 questions from the Cardiology sets.', 2),
  ('gi',         'Gastroenterology',          '20 questions from the Gastroenterology sets.', 3),
  ('renal',      'Nephrology',                '20 questions from the Nephrology sets.', 4)
on conflict (set_key) do nothing;

-- random questions for one subject prefix (e.g. 'Cardiology' matches Cardiology-3-07),
-- from any of its sets; no images, active only
create or replace function public.qb_free_pick(p_prefix text, p_n integer)
returns table (question_id text, rn bigint) language sql volatile security definer set search_path = public as $$
  select x.id, row_number() over ()
  from (
    select q.id
    from public.qb_questions q
    where q.id ~ ('^' || p_prefix || '-[0-9]+-[0-9]+$')
      and q.active
      and coalesce((to_jsonb(q) ->> 'has_image')::boolean, false) = false
    order by random()
    limit p_n
  ) x;
$$;
revoke execute on function public.qb_free_pick(text, integer) from public, anon, authenticated;

-- one-time switch to random picks: clears any earlier first-of-set picks, once
create table if not exists public.qb_free_meta (k text primary key, v text);
alter table public.qb_free_meta enable row level security;
revoke all on public.qb_free_meta from anon, authenticated;
do $$
begin
  if not exists (select 1 from public.qb_free_meta where k = 'random_picks') then
    delete from public.qb_free_items;
    insert into public.qb_free_meta (k, v) values ('random_picks', now()::text);
  end if;
end $$;

-- fill a set only if it is empty (so your manual swaps are never overwritten)
do $$
begin
  if not exists (select 1 from public.qb_free_items where set_key = 'pulm-crit') then
    insert into public.qb_free_items (set_key, ord, question_id)
    select 'pulm-crit', (rn * 2 - 1)::int, question_id from public.qb_free_pick('Pulm', 10)
    union all
    select 'pulm-crit', (rn * 2)::int, question_id from public.qb_free_pick('CritCare', 10);
  end if;
  if not exists (select 1 from public.qb_free_items where set_key = 'cardiology') then
    insert into public.qb_free_items (set_key, ord, question_id)
    select 'cardiology', rn::int, question_id from public.qb_free_pick('Cardiology', 20);
  end if;
  if not exists (select 1 from public.qb_free_items where set_key = 'gi') then
    insert into public.qb_free_items (set_key, ord, question_id)
    select 'gi', rn::int, question_id from public.qb_free_pick('Gastroenterology', 20);
  end if;
  if not exists (select 1 from public.qb_free_items where set_key = 'renal') then
    insert into public.qb_free_items (set_key, ord, question_id)
    select 'renal', rn::int, question_id from public.qb_free_pick('Nephrology', 20);
  end if;
end $$;

-- ─────────────────────────────────────────────────────────────
-- 2. WHO GETS WHAT
-- ─────────────────────────────────────────────────────────────
-- true when the caller is signed in and has verified their email
create or replace function public.qb_email_verified()
returns boolean language sql stable security definer set search_path = public, auth as $$
  select exists (select 1 from auth.users u where u.id = auth.uid() and u.email_confirmed_at is not null);
$$;
revoke execute on function public.qb_email_verified() from public;
grant execute on function public.qb_email_verified() to anon, authenticated;

-- list of free sets: how many questions each has, and how many this visitor can open
create or replace function public.qb_free_sets()
returns json language sql stable security definer set search_path = public as $$
  select coalesce(json_agg(json_build_object(
           'set_key', s.set_key, 'title', s.title, 'blurb', s.blurb,
           'n', (select count(*) from public.qb_free_items i where i.set_key = s.set_key),
           'open', case when public.qb_email_verified()
                        then (select count(*) from public.qb_free_items i where i.set_key = s.set_key)
                        else least(10, (select count(*) from public.qb_free_items i where i.set_key = s.set_key)) end)
         order by s.sort), '[]'::json)
  from public.qb_free_sets s;
$$;

-- one free set with answers and explanations; first 10 only without a verified account
create or replace function public.qb_free_set(p_set text)
returns json language plpgsql stable security definer set search_path = public as $$
declare
  full_access boolean := public.qb_email_verified();
  res json;
begin
  if not exists (select 1 from public.qb_free_sets where set_key = p_set) then raise exception 'bad_set'; end if;
  select json_build_object(
           'set_key', p_set,
           'full', full_access,
           'n_total', (select count(*) from public.qb_free_items i where i.set_key = p_set),
           'questions', coalesce(json_agg(json_build_object(
              'id', q.id, 'subject', q.subject,
              'num', j -> 'num', 'body', j -> 'body', 'answer', j -> 'answer', 'explain', j -> 'explain',
              'has_image', false) order by it.ord), '[]'::json))
    into res
  from (select i.*, row_number() over (order by i.ord) as k from public.qb_free_items i where i.set_key = p_set) it
  join public.qb_questions q on q.id = it.question_id
  cross join lateral (select to_jsonb(q) as j) jj
  where full_access or it.k <= 10;
  return res;
end;
$$;
revoke execute on function public.qb_free_sets() from public;
revoke execute on function public.qb_free_set(text) from public;
grant execute on function public.qb_free_sets() to anon, authenticated;
grant execute on function public.qb_free_set(text) to anon, authenticated;

-- ─────────────────────────────────────────────────────────────
-- 3. CARDIOLOGY NOTES SAMPLE: private bucket, verified accounts only
-- ─────────────────────────────────────────────────────────────
insert into storage.buckets (id, name, public)
values ('free-samples', 'free-samples', false)
on conflict (id) do nothing;

drop policy if exists "free samples: verified accounts can download" on storage.objects;
create policy "free samples: verified accounts can download" on storage.objects
  for select to authenticated
  using (bucket_id = 'free-samples' and public.qb_email_verified());

-- ─────────────────────────────────────────────────────────────
-- 4. ACCOUNT LIST FOR ADMIN.HTML (waitlist + mailing list)
-- ─────────────────────────────────────────────────────────────
-- Everyone who created a question bank account is on the launch waitlist.
-- mailing_list is true only for people who ticked the mailing-list box.
drop function if exists public.admin_accounts();
create or replace function public.admin_accounts()
returns table (email text, first_name text, last_name text, verified boolean,
               waitlist boolean, mailing_list boolean, created_at timestamptz, kind text)
language plpgsql stable security definer set search_path = public, auth as $$
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  return query
    select u.email::text,
           u.raw_user_meta_data ->> 'first_name',
           u.raw_user_meta_data ->> 'last_name',
           u.email_confirmed_at is not null,
           coalesce((u.raw_user_meta_data ->> 'account_ready')::boolean, false),
           coalesce((u.raw_user_meta_data ->> 'marketing_opt_in')::boolean, false),
           u.created_at,
           case when coalesce((u.raw_user_meta_data ->> 'account_ready')::boolean, false)
                then 'Account' else 'Leaderboard only' end
    from auth.users u
    order by u.created_at desc;
end;
$$;
revoke execute on function public.admin_accounts() from public, anon;
grant execute on function public.admin_accounts() to authenticated;

select (select count(*) from public.qb_free_items) as free_questions_ready,
       'Now upload boardside-notes-cardiology-sample.pdf to Storage → free-samples' as next_step;
