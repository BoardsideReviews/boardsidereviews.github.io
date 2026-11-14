-- Boardside Reviews · group sessions TEST HELPER: pretend residents
-- For testing only. Adds pretend people to an open group session; they answer each question on their own
-- within a few seconds (about half to three quarters correct), so the live answers and class results fill in.
-- No accounts are created and nothing touches the waitlist or mailing list.
--
-- Use: run this whole file once in Supabase → SQL Editor, then:
--   select public.qb_room_add_bots('123456', 9);      -- the room code on the host screen, how many people
--
-- Remove it all later: run supabase/qbank-group-sessions.sql again (restores the normal timer check),
-- then:  drop function if exists public.qb_room_add_bots(text, integer);
--        drop function if exists public.qb_gs_bots_step(uuid);
--        drop table if exists public.qb_room_bots;

create table if not exists public.qb_room_bots (
  room    uuid not null references public.qb_rooms(id) on delete cascade,
  user_id uuid not null,
  primary key (room, user_id)
);
alter table public.qb_room_bots enable row level security;
revoke all on public.qb_room_bots from anon, authenticated;

-- add pretend people to an open room (SQL editor only: not callable from the website)
create or replace function public.qb_room_add_bots(p_code text, p_n integer)
returns text language plpgsql volatile security definer set search_path = public as $$
declare r public.qb_rooms; i integer; b uuid; k integer;
begin
  select * into r from public.qb_rooms where code = regexp_replace(coalesce(p_code, ''), '\D', '', 'g') and status <> 'ended';
  if r.id is null then return 'No open session with code ' || coalesce(p_code, ''); end if;
  for i in 1 .. least(greatest(coalesce(p_n, 0), 0), 60) loop
    b := gen_random_uuid();
    insert into public.qb_room_bots (room, user_id) values (r.id, b);
    insert into public.qb_room_members (room, user_id) values (r.id, b);
  end loop;
  select count(*) into k from public.qb_room_members where room = r.id;
  update public.qb_rooms set peak = greatest(peak, k) where id = r.id;
  return 'Added ' || least(greatest(coalesce(p_n, 0), 0), 60) || ' pretend people to ' || r.title || ' (code ' || r.code || '). ' || k || ' people in the room now.';
end;
$$;

-- each time a screen checks in (about once a second), every pretend person who hasn't answered yet
-- has a 1-in-4 chance to answer now, so answers trickle in over a few seconds
create or replace function public.qb_gs_bots_step(p_room uuid)
returns void language plpgsql volatile security definer set search_path = public as $$
declare r public.qb_rooms; b record; ans text; ch text[]; pick text; acc numeric; k integer; m integer;
begin
  if not exists (select 1 from public.qb_room_bots where room = p_room) then return; end if;
  select * into r from public.qb_rooms where id = p_room for update;
  if r.status <> 'question' then return; end if;
  select q.answer, array(select key from jsonb_each(case when jsonb_typeof(to_jsonb(q) -> 'body') = 'string'
                                                         then ((to_jsonb(q) ->> 'body')::jsonb) else to_jsonb(q) -> 'body' end -> 'choices') order by key)
    into ans, ch from public.qb_questions q where q.id = r.qids[r.qi + 1];
  acc := 0.45 + (abs(hashtext(r.id::text || r.qi::text)) % 35) / 100.0;       -- this question: 45–79% get it right
  for b in select x.user_id from public.qb_room_bots x
           join public.qb_room_members m2 on m2.room = x.room and m2.user_id = x.user_id
           where x.room = r.id
             and not exists (select 1 from public.qb_room_voted v where v.room = r.id and v.qi = r.qi and v.user_id = x.user_id) loop
    if random() < 0.25 then
      pick := case when random() < acc or coalesce(array_length(ch, 1), 0) < 2 then ans
                   else (select c from unnest(ch) c where c <> ans order by random() limit 1) end;
      insert into public.qb_room_voted (room, qi, user_id) values (r.id, r.qi, b.user_id) on conflict do nothing;
      if found then
        insert into public.qb_room_tally (room, qi, choice, n) values (r.id, r.qi, pick, 1)
        on conflict (room, qi, choice) do update set n = public.qb_room_tally.n + 1;
      end if;
    end if;
  end loop;
  select count(*) into k from public.qb_room_voted v join public.qb_room_members x on x.room = v.room and x.user_id = v.user_id
   where v.room = r.id and v.qi = r.qi;
  select count(*) into m from public.qb_room_members where room = r.id;
  if k >= m then
    update public.qb_rooms set status = 'reveal', ends_at = null, paused_left = null, ver = ver + 1 where id = r.id;
  end if;
end;
$$;

-- the normal timer check, plus the pretend people's turn
create or replace function public.qb_gs_tick(p_room uuid)
returns void language plpgsql volatile security definer set search_path = public as $$
begin
  perform public.qb_gs_bots_step(p_room);
  update public.qb_rooms set status = 'reveal', ends_at = null, paused_left = null, ver = ver + 1
   where id = p_room and status = 'question' and timed and ends_at is not null and now() >= ends_at + interval '1 second';
end;
$$;

revoke execute on function public.qb_room_add_bots(text, integer), public.qb_gs_bots_step(uuid), public.qb_gs_tick(uuid)
  from public, anon, authenticated;

select 'Test helper ready. Now run: select public.qb_room_add_bots(''CODE'', 9);' as status;
