-- Boardside Reviews · "Delete account" (Profile info → Delete account, confirmed by typing DELETE)
-- Paste into Supabase → SQL Editor → Run. Safe to run more than once.
--
-- Deletes the signed-in learner's account for good: their login, question bank progress, flashcards,
-- confidence ratings, activity calendar, mailing-list record (all cascade from auth.users), their
-- leaderboard scores, and any purchased access tied to their email (purchases become void).
-- The admin account (boardsidereviews@gmail.com) can't be deleted this way.

create or replace function public.qb_delete_account(p_confirm text)
returns boolean language plpgsql security definer set search_path = public, auth as $$
declare
  uid uuid := auth.uid();
  em text;
begin
  if uid is null then raise exception 'not_signed_in'; end if;
  if coalesce(p_confirm, '') <> 'DELETE' then raise exception 'confirm_required'; end if;
  if public.is_admin() then raise exception 'admin_protected'; end if;
  select lower(u.email) into em from auth.users u where u.id = uid;
  delete from public.scores where user_id = uid;
  if em is not null then delete from public.qb_access where lower(email) = em; end if;
  delete from auth.users where id = uid;          -- everything else cascades
  return true;
end;
$$;
revoke execute on function public.qb_delete_account(text) from public, anon;
grant execute on function public.qb_delete_account(text) to authenticated;

select has_table_privilege('auth.users', 'DELETE') as can_delete_users;
