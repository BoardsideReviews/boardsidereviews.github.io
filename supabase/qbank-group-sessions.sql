-- Boardside Reviews · group sessions (live, Kahoot-style question sessions)
-- Paste this whole file into Supabase → SQL Editor → New query → Run.
-- Safe to run more than once.
--
-- How it works
--   • A host creates a room and gets a 6-digit code. People join at boardsidereviews.com/join.
--   • Free sets: anyone with a verified free account can host or join.
--   • Full question bank: only accounts in qb_room_hosts can host (for now just
--     boardsidereviews@gmail.com). Only accounts with full question bank access can join.
--   • The host's screen and the phones ask the server for the room's state about once a second,
--     so it keeps working on hospital Wi-Fi that blocks live connections.
--
-- Privacy: only averages are kept
--   • Answers are added to a running count per answer choice (qb_room_tally). No row ever says
--     who picked what.
--   • While a session is open, the server keeps who is in the room and who has already answered
--     each question (not what they answered), only to stop double votes. Both lists are deleted
--     the moment the session ends, and open rooms close on their own after 4 hours.
--   • Group answers are never saved to anyone's question bank account or stats.
--
-- Who can host full question bank sessions: manage it on the admin page (Group session hosts).
-- boardsidereviews@gmail.com is always a host and can't be removed there.

-- ─────────────────────────────────────────────────────────────
-- 1. TABLES
-- ─────────────────────────────────────────────────────────────
create table if not exists public.qb_room_hosts (
  email    text primary key,
  added_at timestamptz not null default now()
);
insert into public.qb_room_hosts (email) values ('boardsidereviews@gmail.com') on conflict (email) do nothing;
alter table public.qb_room_hosts add column if not exists note text;   -- e.g. 'Chief resident, Example IM program'

create table if not exists public.qb_rooms (
  id          uuid primary key default gen_random_uuid(),
  code        text not null,
  kind        text not null check (kind in ('free', 'bank')),
  title       text not null,
  host        uuid not null,
  qids        text[] not null,
  n           integer not null,
  timed       boolean not null default false,
  secs        integer not null default 90,
  status      text not null default 'lobby' check (status in ('lobby', 'question', 'reveal', 'ended')),
  qi          integer not null default 0,            -- current question, 0-based
  ends_at     timestamptz,                           -- timed question: when time runs out
  paused_left integer,                               -- timed question on pause: seconds left
  ver         integer not null default 0,            -- bumps on every step, so screens know to redraw
  peak        integer not null default 0,            -- most people in the room at once
  created_at  timestamptz not null default now(),
  ended_at    timestamptz
);
create unique index if not exists qb_rooms_open_code on public.qb_rooms (code) where status <> 'ended';
create index if not exists qb_rooms_host on public.qb_rooms (host, created_at desc);

-- running count per answer choice: the only answer data kept
create table if not exists public.qb_room_tally (
  room   uuid not null references public.qb_rooms(id) on delete cascade,
  qi     integer not null,
  choice text not null,
  n      integer not null default 0,
  primary key (room, qi, choice)
);
-- who is in an open room (deleted when it ends)
create table if not exists public.qb_room_members (
  room uuid not null references public.qb_rooms(id) on delete cascade,
  user_id uuid not null,
  primary key (room, user_id)
);
-- who has already answered a question (not what they answered; deleted when the room ends)
create table if not exists public.qb_room_voted (
  room uuid not null references public.qb_rooms(id) on delete cascade,
  qi   integer not null,
  user_id uuid not null,
  primary key (room, qi, user_id)
);

alter table public.qb_room_hosts   enable row level security;
alter table public.qb_rooms        enable row level security;
alter table public.qb_room_tally   enable row level security;
alter table public.qb_room_members enable row level security;
alter table public.qb_room_voted   enable row level security;
revoke all on public.qb_room_hosts, public.qb_rooms, public.qb_room_tally,
              public.qb_room_members, public.qb_room_voted from anon, authenticated;

-- ─────────────────────────────────────────────────────────────
-- 2. HELPERS (not callable from the website)
-- ─────────────────────────────────────────────────────────────
create or replace function public.qb_gs_can_host_bank()
returns boolean language sql stable security definer set search_path = public, auth as $$
  select exists (select 1 from auth.users u join public.qb_room_hosts h on lower(h.email) = lower(u.email)
                 where u.id = auth.uid() and u.email_confirmed_at is not null);
$$;

-- close a room and forget who was in it
create or replace function public.qb_gs_close(p_room uuid)
returns void language plpgsql volatile security definer set search_path = public as $$
begin
  update public.qb_rooms set status = 'ended', ended_at = coalesce(ended_at, now()), ends_at = null,
         paused_left = null, ver = ver + 1
   where id = p_room and status <> 'ended';
  delete from public.qb_room_members where room = p_room;
  delete from public.qb_room_voted where room = p_room;
end;
$$;

-- rooms left open for 4 hours close themselves
create or replace function public.qb_gs_sweep()
returns void language plpgsql volatile security definer set search_path = public as $$
declare r record;
begin
  for r in select id from public.qb_rooms where status <> 'ended' and created_at < now() - interval '4 hours' loop
    perform public.qb_gs_close(r.id);
  end loop;
end;
$$;

-- a timed question whose time is up moves to the answer (whoever asks first triggers it)
create or replace function public.qb_gs_tick(p_room uuid)
returns void language plpgsql volatile security definer set search_path = public as $$
begin
  update public.qb_rooms set status = 'reveal', ends_at = null, paused_left = null, ver = ver + 1
   where id = p_room and status = 'question' and timed and ends_at is not null and now() >= ends_at + interval '1 second';
end;
$$;

-- the state every screen polls for: small, no question text
create or replace function public.qb_gs_state(p_room uuid, p_host boolean)
returns json language plpgsql volatile security definer set search_path = public as $$
declare r public.qb_rooms; uid uuid := auth.uid(); res json;
begin
  select * into r from public.qb_rooms where id = p_room;
  select json_build_object(
    'room', r.id, 'code', case when r.status = 'ended' then null else r.code end,
    'kind', r.kind, 'title', r.title, 'n', r.n, 'timed', r.timed, 'secs', r.secs,
    'status', r.status, 'qi', r.qi, 'ver', r.ver,
    'ends_in', case when r.ends_at is null then null else round(extract(epoch from (r.ends_at - now()))::numeric, 2) end,
    'paused', r.paused_left is not null, 'paused_left', r.paused_left,
    'joined', (select count(*) from public.qb_room_members m where m.room = r.id),
    'answered', (select count(*) from public.qb_room_voted v join public.qb_room_members m on m.room = v.room and m.user_id = v.user_id
                 where v.room = r.id and v.qi = r.qi),
    'me_answered', exists (select 1 from public.qb_room_voted v where v.room = r.id and v.qi = r.qi and v.user_id = uid),
    'counts', case when p_host or r.status in ('reveal', 'ended') then
                (select json_object_agg(t.choice, t.n) from public.qb_room_tally t where t.room = r.id and t.qi = r.qi)
              else null end,
    'host', p_host
  ) into res;
  return res;
end;
$$;

revoke execute on function public.qb_gs_can_host_bank(), public.qb_gs_close(uuid), public.qb_gs_sweep(),
  public.qb_gs_tick(uuid), public.qb_gs_state(uuid, boolean) from public, anon, authenticated;

-- ─────────────────────────────────────────────────────────────
-- 3. FOR THE WEBSITE
-- ─────────────────────────────────────────────────────────────
-- can this account host full question bank sessions? (shows the host card on the question bank home)
create or replace function public.qb_room_can_host()
returns boolean language sql stable security definer set search_path = public, auth as $$
  select public.qb_gs_can_host_bank();
$$;

-- subjects a full question bank host can pick from (no image questions, hidden ones skipped)
create or replace function public.qb_room_subjects()
returns json language plpgsql stable security definer set search_path = public as $$
begin
  if not public.qb_gs_can_host_bank() then raise exception 'not_host'; end if;
  return (select coalesce(json_agg(json_build_object('subject', subject, 'n', n) order by subject), '[]'::json)
          from (select q.subject, count(*) as n from public.qb_questions q
                where q.active and coalesce((to_jsonb(q) ->> 'has_image')::boolean, false) = false
                group by q.subject) s);
end;
$$;

-- create a room. Free: p_kind 'free' + p_set (a free set key). Full bank: p_kind 'bank' + p_subject
-- (null = all subjects). p_n is 10 or 20; questions are picked at random. p_timed = 90 seconds each.
create or replace function public.qb_room_create(p_kind text, p_set text, p_subject text, p_n integer, p_timed boolean)
returns json language plpgsql volatile security definer set search_path = public as $$
declare uid uuid := auth.uid(); ids text[]; t text; c text; tries integer := 0; rid uuid; old record;
begin
  if uid is null then raise exception 'not_signed_in'; end if;
  if p_n not in (10, 20) then raise exception 'bad_count'; end if;
  if p_kind = 'free' then
    if not public.qb_email_verified() then raise exception 'not_verified'; end if;
    select title into t from public.qb_free_sets where set_key = p_set;
    if t is null then raise exception 'bad_set'; end if;
    ids := array(select i.question_id from public.qb_free_items i join public.qb_questions q on q.id = i.question_id
                 where i.set_key = p_set and q.active order by random() limit p_n);
  elsif p_kind = 'bank' then
    if not public.qb_gs_can_host_bank() then raise exception 'not_host'; end if;
    t := coalesce(nullif(p_subject, ''), 'All subjects');
    ids := array(select q.id from public.qb_questions q
                 where q.active and coalesce((to_jsonb(q) ->> 'has_image')::boolean, false) = false
                   and (nullif(p_subject, '') is null or q.subject = p_subject)
                 order by random() limit p_n);
  else
    raise exception 'bad_kind';
  end if;
  if coalesce(array_length(ids, 1), 0) = 0 then raise exception 'no_questions'; end if;

  perform public.qb_gs_sweep();
  for old in select id from public.qb_rooms where host = uid and status <> 'ended' loop   -- one open room per host
    perform public.qb_gs_close(old.id);
  end loop;

  loop
    c := (100000 + floor(random() * 900000))::int::text;
    exit when not exists (select 1 from public.qb_rooms where code = c and status <> 'ended');
    tries := tries + 1;
    if tries > 50 then raise exception 'try_again'; end if;
  end loop;

  insert into public.qb_rooms (code, kind, title, host, qids, n, timed)
  values (c, p_kind, t, uid, ids, array_length(ids, 1), coalesce(p_timed, false))
  returning id into rid;
  return public.qb_gs_state(rid, true);
end;
$$;

-- the host's open room, if any (so a refreshed projector picks up where it left off)
create or replace function public.qb_room_mine()
returns json language plpgsql volatile security definer set search_path = public as $$
declare uid uuid := auth.uid(); rid uuid;
begin
  if uid is null then raise exception 'not_signed_in'; end if;
  perform public.qb_gs_sweep();
  select id into rid from public.qb_rooms where host = uid and status <> 'ended' order by created_at desc limit 1;
  if rid is null then return null; end if;
  perform public.qb_gs_tick(rid);
  return public.qb_gs_state(rid, true);
end;
$$;

-- join with a code
create or replace function public.qb_room_join(p_code text)
returns json language plpgsql volatile security definer set search_path = public as $$
declare uid uuid := auth.uid(); r public.qb_rooms; k integer;
begin
  if uid is null then raise exception 'not_signed_in'; end if;
  perform public.qb_gs_sweep();
  select * into r from public.qb_rooms where code = regexp_replace(coalesce(p_code, ''), '\D', '', 'g') and status <> 'ended';
  if r.id is null then raise exception 'no_room'; end if;
  if r.kind = 'free' then
    if not public.qb_email_verified() then raise exception 'not_verified'; end if;
  else
    perform public.qb_require();                     -- full question bank access needed (raises no_access)
  end if;
  insert into public.qb_room_members (room, user_id) values (r.id, uid) on conflict do nothing;
  select count(*) into k from public.qb_room_members where room = r.id;
  update public.qb_rooms set peak = greatest(peak, k) where id = r.id;
  perform public.qb_gs_tick(r.id);
  return public.qb_gs_state(r.id, false);
end;
$$;

-- every screen calls this about once a second
create or replace function public.qb_room_poll(p_room uuid)
returns json language plpgsql volatile security definer set search_path = public as $$
declare uid uuid := auth.uid(); r public.qb_rooms;
begin
  if uid is null then raise exception 'not_signed_in'; end if;
  select * into r from public.qb_rooms where id = p_room;
  if r.id is null then raise exception 'no_room'; end if;
  if r.host <> uid and r.status <> 'ended'
     and not exists (select 1 from public.qb_room_members m where m.room = r.id and m.user_id = uid) then
    raise exception 'not_in_room';
  end if;
  perform public.qb_gs_tick(r.id);
  return public.qb_gs_state(r.id, r.host = uid);
end;
$$;

-- one question of the room. Only the current one or earlier ones; the answer and pearl only after
-- that question is revealed; the full per-choice explanation only for the host.
create or replace function public.qb_room_question(p_room uuid, p_qi integer)
returns json language plpgsql stable security definer set search_path = public as $$
declare uid uuid := auth.uid(); r public.qb_rooms; q public.qb_questions; is_host boolean; shown boolean; j jsonb;
begin
  if uid is null then raise exception 'not_signed_in'; end if;
  select * into r from public.qb_rooms where id = p_room;
  if r.id is null then raise exception 'no_room'; end if;
  is_host := r.host = uid;
  if not is_host and not exists (select 1 from public.qb_room_members m where m.room = r.id and m.user_id = uid) then
    raise exception 'not_in_room';
  end if;
  if r.status = 'lobby' or p_qi < 0 or p_qi >= r.n or (p_qi > r.qi and r.status <> 'ended') then raise exception 'not_yet'; end if;
  select * into q from public.qb_questions where id = r.qids[p_qi + 1];
  j := to_jsonb(q);
  shown := p_qi < r.qi or r.status in ('reveal', 'ended');
  return json_build_object(
    'qi', p_qi, 'subject', q.subject, 'body', j -> 'body',
    'answer', case when shown then q.answer end,
    'pearl', case when shown then j -> 'explain' -> 'pearl' end,
    'details', case when shown and is_host then j -> 'explain' -> 'details' end);
end;
$$;

-- a member answers the current question (counted once; only the tally remembers the choice)
create or replace function public.qb_room_answer(p_room uuid, p_qi integer, p_choice text)
returns json language plpgsql volatile security definer set search_path = public as $$
declare uid uuid := auth.uid(); r public.qb_rooms; ch text := upper(coalesce(p_choice, '')); k integer; m integer; bj jsonb;
begin
  if uid is null then raise exception 'not_signed_in'; end if;
  select * into r from public.qb_rooms where id = p_room for update;
  if r.id is null then raise exception 'no_room'; end if;
  if not exists (select 1 from public.qb_room_members x where x.room = r.id and x.user_id = uid) then raise exception 'not_in_room'; end if;
  if r.status <> 'question' or r.qi <> p_qi
     or (r.timed and r.ends_at is not null and now() > r.ends_at + interval '1 second') then
    raise exception 'closed';
  end if;
  select to_jsonb(q) -> 'body' into bj from public.qb_questions q where q.id = r.qids[p_qi + 1];
  if jsonb_typeof(bj) = 'string' then bj := (bj #>> '{}')::jsonb; end if;      -- body stored as text
  if ch !~ '^[A-E]$' or not coalesce(bj -> 'choices' ? ch, false) then
    raise exception 'bad_choice';
  end if;
  insert into public.qb_room_voted (room, qi, user_id) values (r.id, p_qi, uid) on conflict do nothing;
  if not found then raise exception 'already'; end if;
  insert into public.qb_room_tally (room, qi, choice, n) values (r.id, p_qi, ch, 1)
  on conflict (room, qi, choice) do update set n = public.qb_room_tally.n + 1;
  -- everyone in the room has answered: show the answer
  select count(*) into k from public.qb_room_voted v join public.qb_room_members x on x.room = v.room and x.user_id = v.user_id
   where v.room = r.id and v.qi = p_qi;
  select count(*) into m from public.qb_room_members where room = r.id;
  if k >= m then
    update public.qb_rooms set status = 'reveal', ends_at = null, paused_left = null, ver = ver + 1 where id = r.id;
  end if;
  return public.qb_gs_state(r.id, false);
end;
$$;

-- a member leaves (answers they already gave stay in the counts)
create or replace function public.qb_room_leave(p_room uuid)
returns void language plpgsql volatile security definer set search_path = public as $$
begin
  delete from public.qb_room_members where room = p_room and user_id = auth.uid();
end;
$$;

-- host controls: start, reveal, next, pause, resume, end
create or replace function public.qb_room_control(p_room uuid, p_action text)
returns json language plpgsql volatile security definer set search_path = public as $$
declare uid uuid := auth.uid(); r public.qb_rooms;
begin
  if uid is null then raise exception 'not_signed_in'; end if;
  select * into r from public.qb_rooms where id = p_room for update;
  if r.id is null or r.host <> uid then raise exception 'not_host'; end if;
  if p_action = 'start' and r.status = 'lobby' then
    if not exists (select 1 from public.qb_room_members m where m.room = r.id) then raise exception 'empty_room'; end if;
    update public.qb_rooms set status = 'question', qi = 0, ver = ver + 1,
           ends_at = case when timed then now() + make_interval(secs => secs) end where id = r.id;
  elsif p_action = 'reveal' and r.status = 'question' then
    update public.qb_rooms set status = 'reveal', ends_at = null, paused_left = null, ver = ver + 1 where id = r.id;
  elsif p_action = 'next' and r.status = 'reveal' then
    if r.qi + 1 >= r.n then
      perform public.qb_gs_close(r.id);
    else
      update public.qb_rooms set status = 'question', qi = qi + 1, paused_left = null, ver = ver + 1,
             ends_at = case when timed then now() + make_interval(secs => secs) end where id = r.id;
    end if;
  elsif p_action = 'pause' and r.status = 'question' and r.timed and r.ends_at is not null then
    update public.qb_rooms set paused_left = greatest(1, ceil(extract(epoch from (ends_at - now())))::int), ends_at = null, ver = ver + 1
     where id = r.id;
  elsif p_action = 'resume' and r.status = 'question' and r.paused_left is not null then
    update public.qb_rooms set ends_at = now() + make_interval(secs => paused_left), paused_left = null, ver = ver + 1 where id = r.id;
  elsif p_action = 'end' then
    perform public.qb_gs_close(r.id);
  end if;
  return public.qb_gs_state(r.id, true);
end;
$$;

-- class results for the host: per question, how many answered and how many got it right
create or replace function public.qb_room_summary(p_room uuid)
returns json language plpgsql stable security definer set search_path = public as $$
declare uid uuid := auth.uid(); r public.qb_rooms;
begin
  select * into r from public.qb_rooms where id = p_room;
  if r.id is null or r.host <> uid then raise exception 'not_host'; end if;
  return json_build_object(
    'title', r.title, 'kind', r.kind, 'n', r.n, 'peak', r.peak, 'status', r.status,
    'questions', (select coalesce(json_agg(json_build_object(
                    'qi', g.i - 1, 'subject', q.subject,
                    'answered', (select coalesce(sum(t.n), 0) from public.qb_room_tally t where t.room = r.id and t.qi = g.i - 1),
                    'correct', (select coalesce(sum(t.n), 0) from public.qb_room_tally t where t.room = r.id and t.qi = g.i - 1 and t.choice = q.answer))
                  order by g.i), '[]'::json)
                  from generate_subscripts(r.qids, 1) as g(i)
                  join public.qb_questions q on q.id = r.qids[g.i]
                  where g.i - 1 < r.qi or (g.i - 1 = r.qi and r.status in ('reveal', 'ended'))));
end;
$$;

revoke execute on function public.qb_room_can_host(), public.qb_room_subjects(),
  public.qb_room_create(text, text, text, integer, boolean), public.qb_room_mine(), public.qb_room_join(text),
  public.qb_room_poll(uuid), public.qb_room_question(uuid, integer), public.qb_room_answer(uuid, integer, text),
  public.qb_room_leave(uuid), public.qb_room_control(uuid, text), public.qb_room_summary(uuid) from public, anon;
grant execute on function public.qb_room_can_host(), public.qb_room_subjects(),
  public.qb_room_create(text, text, text, integer, boolean), public.qb_room_mine(), public.qb_room_join(text),
  public.qb_room_poll(uuid), public.qb_room_question(uuid, integer), public.qb_room_answer(uuid, integer, text),
  public.qb_room_leave(uuid), public.qb_room_control(uuid, text), public.qb_room_summary(uuid) to authenticated;


-- ─────────────────────────────────────────────────────────────
-- 4. ADMIN PAGE: who can host full question bank sessions
-- ─────────────────────────────────────────────────────────────
create or replace function public.admin_room_hosts()
returns json language plpgsql stable security definer set search_path = public, auth as $$
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  return (select coalesce(json_agg(json_build_object(
            'email', h.email, 'note', h.note, 'added_at', h.added_at,
            'has_account', exists (select 1 from auth.users u where lower(u.email) = lower(h.email)),
            'owner', lower(h.email) = 'boardsidereviews@gmail.com',
            'sessions', (select count(*) from public.qb_rooms r join auth.users u on u.id = r.host
                         where lower(u.email) = lower(h.email) and r.kind = 'bank'))
          order by (lower(h.email) = 'boardsidereviews@gmail.com') desc, h.added_at), '[]'::json)
          from public.qb_room_hosts h);
end;
$$;

create or replace function public.admin_room_host_add(p_email text, p_note text)
returns json language plpgsql volatile security definer set search_path = public as $$
declare e text := lower(trim(coalesce(p_email, '')));
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  if e !~ '^[^@\s]+@[^@\s]+\.[^@\s]+$' or length(e) > 254 then raise exception 'bad_email'; end if;
  insert into public.qb_room_hosts (email, note) values (e, nullif(trim(coalesce(p_note, '')), ''))
  on conflict (email) do update set note = coalesce(excluded.note, public.qb_room_hosts.note);
  return public.admin_room_hosts();
end;
$$;

-- removing a host also ends any full question bank session they have open
create or replace function public.admin_room_host_remove(p_email text)
returns json language plpgsql volatile security definer set search_path = public, auth as $$
declare e text := lower(trim(coalesce(p_email, ''))); r record;
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  if e = 'boardsidereviews@gmail.com' then raise exception 'owner_protected'; end if;
  delete from public.qb_room_hosts where lower(email) = e;
  for r in select x.id from public.qb_rooms x join auth.users u on u.id = x.host
           where lower(u.email) = e and x.kind = 'bank' and x.status <> 'ended' loop
    perform public.qb_gs_close(r.id);
  end loop;
  return public.admin_room_hosts();
end;
$$;

revoke execute on function public.admin_room_hosts(), public.admin_room_host_add(text, text),
  public.admin_room_host_remove(text) from public, anon;
grant execute on function public.admin_room_hosts(), public.admin_room_host_add(text, text),
  public.admin_room_host_remove(text) to authenticated;

select 'Group sessions are ready' as status,
       (select string_agg(email, ', ') from public.qb_room_hosts) as full_bank_hosts;
