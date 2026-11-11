-- Boardside Reviews · review comments on questions (Claude's audit comments + Khaled's replies), Nov 11, 2026.
-- Admin-only: the table has row level security with no policies; everything goes through admin-checked functions.
-- Safe to run more than once.

create table if not exists public.qb_review_comments (
  id          bigserial primary key,
  question_id text not null references public.qb_questions(id) on delete cascade,
  priority    text not null check (priority in ('high', 'med', 'low')),
  category    text,
  comment     text not null,
  suggestion  text,
  source      text not null default 'audit',
  status      text not null default 'open' check (status in ('open', 'replied', 'resolved')),
  reply       text,
  replied_at  timestamptz,
  created_at  timestamptz not null default now(),
  resolved_at timestamptz,
  resolution  text
);
create index if not exists qb_review_comments_open on public.qb_review_comments (question_id) where status <> 'resolved';
alter table public.qb_review_comments enable row level security;
revoke all on public.qb_review_comments from anon, authenticated;

-- Per-question counts of comments that aren't resolved yet (for the editor's filters and stats).
create or replace function public.admin_rc_index()
returns json language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  return coalesce((
    select json_agg(x) from (
      select question_id,
             count(*) filter (where priority = 'high') as high,
             count(*) filter (where priority = 'med')  as med,
             count(*) filter (where priority = 'low')  as low,
             count(*) filter (where status = 'replied') as waiting
        from public.qb_review_comments
       where status <> 'resolved'
       group by question_id) x), '[]'::json);
end;
$$;

-- The unresolved comments for a set of questions, highest priority first.
create or replace function public.admin_rc_for(p_ids text[])
returns json language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  return coalesce((
    select json_agg(c order by c.question_id, case c.priority when 'high' then 0 when 'med' then 1 else 2 end, c.id)
      from public.qb_review_comments c
     where c.question_id = any(p_ids) and c.status <> 'resolved'), '[]'::json);
end;
$$;

-- Khaled's reply. An empty reply puts the comment back to open.
create or replace function public.admin_rc_reply(p_id bigint, p_reply text)
returns json language plpgsql security definer set search_path = public as $$
declare r public.qb_review_comments;
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  update public.qb_review_comments
     set reply = nullif(btrim(coalesce(p_reply, '')), ''),
         status = case when nullif(btrim(coalesce(p_reply, '')), '') is null then 'open' else 'replied' end,
         replied_at = case when nullif(btrim(coalesce(p_reply, '')), '') is null then null else now() end
   where id = p_id and status <> 'resolved'
  returning * into r;
  if r.id is null then raise exception 'comment_not_found'; end if;
  return row_to_json(r);
end;
$$;

revoke all on function public.admin_rc_index() from public, anon;
revoke all on function public.admin_rc_for(text[]) from public, anon;
revoke all on function public.admin_rc_reply(bigint, text) from public, anon;
grant execute on function public.admin_rc_index() to authenticated;
grant execute on function public.admin_rc_for(text[]) to authenticated;
grant execute on function public.admin_rc_reply(bigint, text) to authenticated;
