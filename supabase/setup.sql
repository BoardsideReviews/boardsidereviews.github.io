-- Boardside Reviews · leaderboard database
-- Paste this whole file into Supabase → SQL Editor → New query → Run.
-- Safe to run more than once.

-- ─────────────────────────────────────────────────────────────
-- 0. WHO IS ADMIN
-- Only the email addresses in this table can remove names, ban
-- players, and edit the blocked-word list. Sign in on the site
-- with this exact email to use boardsidereviews.com/admin.html
-- ─────────────────────────────────────────────────────────────
create table if not exists public.admins (
  email text primary key
);
insert into public.admins (email) values ('boardsidereviews@gmail.com')
  on conflict do nothing;

-- ─────────────────────────────────────────────────────────────
-- 1. TABLES
-- ─────────────────────────────────────────────────────────────
create table if not exists public.profiles (
  user_id      uuid primary key references auth.users(id) on delete cascade,
  display_name text,
  name_key     text unique,
  banned       boolean not null default false,
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now()
);

create table if not exists public.scores (
  id         bigserial primary key,
  user_id    uuid not null references public.profiles(user_id) on delete cascade,
  game       text not null check (game ~ '^[a-z0-9-]{1,40}$'),
  variant    text not null default 'default' check (variant ~ '^[a-z0-9-]{1,60}$'),
  score      integer not null,
  total      integer not null,
  created_at timestamptz not null default now(),
  constraint score_in_range check (total between 1 and 1000 and score between 0 and total)
);
create index if not exists scores_board_idx on public.scores (game, variant, user_id);
create index if not exists scores_user_idx  on public.scores (user_id, created_at desc);

create table if not exists public.blocked_words (
  word     text primary key check (word ~ '^[a-z]{2,30}$'),
  anywhere boolean not null default false  -- true: blocked even inside a longer word
);

-- Starter list. Names are checked after lowercasing and undoing common
-- swaps (0→o, 1→i, 3→e, 4→a, 5→s, 7→t, 8→b, @→a, $→s).
-- anywhere = true  → blocked even inside a longer word ("xfuckx").
-- anywhere = false → blocked only as a whole word, so real names like
--                    Hancock, Fukuda, Nazir, or Dickson still work.
-- Add more from the admin page at any time.
insert into public.blocked_words (word, anywhere) values
  ('fuck',true),('shit',true),('cunt',true),('bitch',true),('whore',true),('slut',true),
  ('asshole',true),('nigger',true),('nigga',true),('faggot',true),('retard',true),
  ('kike',true),('tranny',true),('wetback',true),('rapist',true),('hitler',true),
  ('porn',true),('dildo',true),('jizz',true),('penis',true),('vagina',true),
  ('boardside',true),('khalemedic',true),('moderator',true),('admin',true),
  ('fuk',false),('dick',false),('cock',false),('pussy',false),('bastard',false),('twat',false),
  ('wank',false),('prick',false),('fag',false),('spic',false),('chink',false),('coon',false),
  ('gook',false),('dyke',false),('nazi',false),('rape',false),('anal',false),('cum',false),
  ('sex',false),('tits',false),('boob',false),('official',false),('staff',false)
on conflict do nothing;

-- ─────────────────────────────────────────────────────────────
-- 2. HELPERS
-- ─────────────────────────────────────────────────────────────
create or replace function public.is_admin()
returns boolean language sql stable security definer set search_path = public as $$
  select exists (
    select 1 from public.admins a
    where lower(a.email) = lower(coalesce(auth.jwt() ->> 'email', ''))
  );
$$;

create or replace function public.name_is_allowed(p_name text)
returns boolean language plpgsql stable security definer set search_path = public as $$
declare
  t text;      -- name with look-alike characters undone
  joined text; -- letters only, all words run together
  toks text[]; -- individual words
begin
  t := translate(lower(p_name), '0134578@$!|', 'oieastbasii');
  joined := regexp_replace(t, '[^a-z]', '', 'g');
  if joined = '' then return false; end if;
  toks := array_remove(regexp_split_to_array(regexp_replace(t, '[^a-z]+', ' ', 'g'), ' '), '');
  return not exists (
    select 1 from public.blocked_words w
    where (w.anywhere and position(w.word in joined) > 0)
       or (not w.anywhere and (w.word = any(toks) or w.word = joined
                               or (w.word || 's') = any(toks)))
  );
end;
$$;

-- Validate names on every insert/update
create or replace function public.profiles_check_name()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  new.updated_at := now();
  if new.display_name is null then
    new.name_key := null;
    return new;
  end if;
  new.display_name := regexp_replace(btrim(new.display_name), '\s+', ' ', 'g');
  if char_length(new.display_name) < 3 or char_length(new.display_name) > 20 then
    raise exception 'name_length' using hint = 'Use 3 to 20 characters.';
  end if;
  if new.display_name !~ '^[A-Za-z0-9 ._-]+$' then
    raise exception 'name_chars' using hint = 'Use letters, numbers, spaces, dots, dashes, or underscores.';
  end if;
  if not public.name_is_allowed(new.display_name) then
    raise exception 'name_blocked' using hint = 'That name is not allowed. Try another.';
  end if;
  new.name_key := lower(new.display_name);
  return new;
end;
$$;

drop trigger if exists profiles_check_name on public.profiles;
create trigger profiles_check_name
  before insert or update of display_name on public.profiles
  for each row execute function public.profiles_check_name();

-- ─────────────────────────────────────────────────────────────
-- 3. ROW LEVEL SECURITY AND PERMISSIONS
-- Players can read and set only their own name. Nobody can write
-- scores directly; scores go through submit_score().
-- ─────────────────────────────────────────────────────────────
alter table public.admins        enable row level security;
alter table public.profiles      enable row level security;
alter table public.scores        enable row level security;
alter table public.blocked_words enable row level security;

revoke all on public.admins, public.profiles, public.scores, public.blocked_words from anon, authenticated;
grant select on public.profiles to authenticated;
grant insert (user_id, display_name) on public.profiles to authenticated;
grant update (display_name) on public.profiles to authenticated;

drop policy if exists "read own profile"   on public.profiles;
drop policy if exists "create own profile" on public.profiles;
drop policy if exists "rename own profile" on public.profiles;
create policy "read own profile" on public.profiles
  for select to authenticated using (user_id = auth.uid());
create policy "create own profile" on public.profiles
  for insert to authenticated with check (user_id = auth.uid());
create policy "rename own profile" on public.profiles
  for update to authenticated using (user_id = auth.uid() and not banned)
  with check (user_id = auth.uid() and not banned);

-- ─────────────────────────────────────────────────────────────
-- 4. PLAYER FUNCTIONS
-- ─────────────────────────────────────────────────────────────
create or replace function public.submit_score(p_game text, p_variant text, p_score integer, p_total integer)
returns void language plpgsql security definer set search_path = public as $$
declare
  p public.profiles;
begin
  if auth.uid() is null then raise exception 'not_signed_in'; end if;
  select * into p from public.profiles where user_id = auth.uid();
  if found and p.banned then raise exception 'banned'; end if;
  if not found or p.display_name is null then raise exception 'no_name'; end if;
  if exists (select 1 from public.scores
             where user_id = auth.uid() and created_at > now() - interval '30 seconds') then
    raise exception 'too_fast' using hint = 'Wait a few seconds before posting again.';
  end if;
  insert into public.scores (user_id, game, variant, score, total)
  values (auth.uid(), p_game, coalesce(p_variant, 'default'), p_score, p_total);
end;
$$;

-- Public leaderboard: each player's best result, ranked by percent.
create or replace function public.get_leaderboard(p_game text, p_variant text, p_days integer default null, p_limit integer default 50)
returns table (rank bigint, display_name text, best_pct integer, best_score integer, total integer, plays bigint, achieved_at timestamptz, is_me boolean)
language sql stable security definer set search_path = public as $$
  with s as (
    select sc.*, round(100.0 * sc.score / sc.total)::int as pct
    from public.scores sc
    join public.profiles pr on pr.user_id = sc.user_id
    where sc.game = p_game and sc.variant = p_variant
      and pr.display_name is not null and not pr.banned
      and (p_days is null or sc.created_at > now() - make_interval(days => p_days))
  ),
  best as (
    select distinct on (user_id) user_id, pct, score, total, created_at
    from s order by user_id, pct desc, created_at asc
  ),
  counts as (select user_id, count(*) as plays from s group by user_id)
  select rank() over (order by b.pct desc, b.created_at asc),
         pr.display_name, b.pct, b.score, b.total, c.plays, b.created_at,
         (b.user_id = auth.uid())
  from best b
  join public.profiles pr on pr.user_id = b.user_id
  join counts c on c.user_id = b.user_id
  order by b.pct desc, b.created_at asc
  limit least(greatest(coalesce(p_limit, 50), 1), 200);
$$;

-- ─────────────────────────────────────────────────────────────
-- 5. ADMIN FUNCTIONS (refuse anyone not in public.admins)
-- ─────────────────────────────────────────────────────────────
create or replace function public.admin_list_players()
returns table (user_id uuid, email text, display_name text, banned boolean, plays bigint, last_played timestamptz, joined timestamptz)
language plpgsql stable security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  return query
    select pr.user_id, u.email::text, pr.display_name, pr.banned,
           count(sc.id), max(sc.created_at), pr.created_at
    from public.profiles pr
    join auth.users u on u.id = pr.user_id
    left join public.scores sc on sc.user_id = pr.user_id
    group by pr.user_id, u.email, pr.display_name, pr.banned, pr.created_at
    order by max(sc.created_at) desc nulls last, pr.created_at desc;
end;
$$;

-- Remove a name. The player must pick a new one before posting again.
-- With p_ban = true they are also hidden from the leaderboard and can't post.
create or replace function public.admin_remove_name(p_user uuid, p_ban boolean default false)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  update public.profiles set display_name = null, banned = (banned or p_ban) where user_id = p_user;
end;
$$;

create or replace function public.admin_unban(p_user uuid)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  update public.profiles set banned = false where user_id = p_user;
end;
$$;

create or replace function public.admin_clear_scores(p_user uuid)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  delete from public.scores where user_id = p_user;
end;
$$;

create or replace function public.admin_list_blocked_words()
returns table (word text, anywhere boolean) language plpgsql stable security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  return query select w.word, w.anywhere from public.blocked_words w order by w.word;
end;
$$;

create or replace function public.admin_add_blocked_word(p_word text, p_anywhere boolean default false)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  insert into public.blocked_words (word, anywhere) values (lower(btrim(p_word)), p_anywhere)
    on conflict (word) do update set anywhere = excluded.anywhere;
  -- Clear any existing names that now match
  update public.profiles set display_name = null
  where display_name is not null and not public.name_is_allowed(display_name);
end;
$$;

create or replace function public.admin_remove_blocked_word(p_word text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  delete from public.blocked_words where word = lower(btrim(p_word));
end;
$$;

-- Function permissions
revoke execute on all functions in schema public from public, anon, authenticated;
grant execute on function public.get_leaderboard(text, text, integer, integer) to anon, authenticated;
grant execute on function public.is_admin() to authenticated;
grant execute on function public.submit_score(text, text, integer, integer) to authenticated;
grant execute on function public.admin_list_players(), public.admin_remove_name(uuid, boolean),
  public.admin_unban(uuid), public.admin_clear_scores(uuid), public.admin_list_blocked_words(),
  public.admin_add_blocked_word(text, boolean), public.admin_remove_blocked_word(text) to authenticated;

-- ─────────────────────────────────────────────────────────────
-- 6. POINTS-RANKED BOARDS (ABG Blitz)
-- ABG Blitz posts raw points (score = total = points), so it is
-- ranked by best points instead of percent. Night Float is unchanged.
-- ─────────────────────────────────────────────────────────────
alter table public.scores drop constraint if exists score_in_range;
alter table public.scores add constraint score_in_range
  check (total between 1 and 100000 and score between 0 and total);

-- No realistic 3-minute run gets near this; blocks obviously fake posts.
alter table public.scores drop constraint if exists abg_blitz_cap;
alter table public.scores add constraint abg_blitz_cap
  check (game <> 'abg-blitz' or score <= 15000);

create or replace function public.get_points_leaderboard(p_game text, p_variant text, p_days integer default null, p_limit integer default 50)
returns table (rank bigint, display_name text, best_score integer, plays bigint, achieved_at timestamptz, is_me boolean)
language sql stable security definer set search_path = public as $$
  with s as (
    select sc.*
    from public.scores sc
    join public.profiles pr on pr.user_id = sc.user_id
    where sc.game = p_game and sc.variant = p_variant
      and pr.display_name is not null and not pr.banned
      and (p_days is null or sc.created_at > now() - make_interval(days => p_days))
  ),
  best as (
    select distinct on (user_id) user_id, score, created_at
    from s order by user_id, score desc, created_at asc
  ),
  counts as (select user_id, count(*) as plays from s group by user_id)
  select rank() over (order by b.score desc, b.created_at asc),
         pr.display_name, b.score, c.plays, b.created_at,
         (b.user_id = auth.uid())
  from best b
  join public.profiles pr on pr.user_id = b.user_id
  join counts c on c.user_id = b.user_id
  order by b.score desc, b.created_at asc
  limit least(greatest(coalesce(p_limit, 50), 1), 200);
$$;
revoke execute on function public.get_points_leaderboard(text, text, integer, integer) from public;
grant execute on function public.get_points_leaderboard(text, text, integer, integer) to anon, authenticated;
