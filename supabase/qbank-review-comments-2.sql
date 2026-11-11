-- Review comments: your own comments, Good/Bad marking (tap again to clear), and the 10 open items from the layout update as comments.
begin;
create or replace function public.admin_rc_add(p_question_id text, p_priority text, p_comment text)
returns json language plpgsql security definer set search_path = public as $$
declare r public.qb_review_comments;
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  if p_priority not in ('high','med','low') then raise exception 'bad_priority'; end if;
  if nullif(btrim(coalesce(p_comment,'')),'') is null then raise exception 'empty_comment'; end if;
  insert into public.qb_review_comments(question_id, priority, comment, source, status, reply, replied_at)
    values (p_question_id, p_priority, btrim(p_comment), 'khaled', 'replied', btrim(p_comment), now())
  returning * into r;
  return row_to_json(r);
end $$;

create or replace function public.admin_rc_edit(p_id bigint, p_comment text)
returns json language plpgsql security definer set search_path = public as $$
declare r public.qb_review_comments;
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  if nullif(btrim(coalesce(p_comment,'')),'') is null then
    delete from public.qb_review_comments where id = p_id and source = 'khaled' returning * into r;
    if r.id is null then raise exception 'comment_not_found'; end if;
    return json_build_object('deleted', true, 'id', p_id);
  end if;
  update public.qb_review_comments set comment = btrim(p_comment), reply = btrim(p_comment), replied_at = now()
   where id = p_id and source = 'khaled' and status <> 'resolved' returning * into r;
  if r.id is null then raise exception 'comment_not_found'; end if;
  return row_to_json(r);
end $$;

create or replace function public.admin_q_mark(p_id text, p_status text)
returns json language plpgsql security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  if p_status not in ('todo','ok','change') then raise exception 'bad_status'; end if;
  insert into public.qb_question_review(id, status) values (p_id, p_status)
    on conflict (id) do update set status = excluded.status, updated_at = now();
  return json_build_object('ok', true);
end $$;

revoke all on function public.admin_rc_add(text, text, text), public.admin_rc_edit(bigint, text) from public, anon;
grant execute on function public.admin_rc_add(text, text, text), public.admin_rc_edit(bigint, text) to authenticated;

-- (the 10 layout-update items were inserted from a private file; question text is not kept in this public repo)
update public.qb_question_review set tags = array_remove(tags, 'decide') where 'decide' = any(tags);
commit;
