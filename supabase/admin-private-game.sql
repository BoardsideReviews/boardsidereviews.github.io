-- Boardside Reviews · private file storage for the admin page (Nov 14, 2026)
-- Paste into Supabase → SQL Editor → Run. Safe to run more than once.
-- Holds a personal file (Khaled's game) that only admin accounts can read or replace.
-- The file itself is NOT in this repo: it is uploaded from the admin page and lives only in this table.

create table if not exists public.admin_private_files (
  name       text primary key,
  body       text not null,
  updated_at timestamptz not null default now()
);

-- Row level security on, and no policies: nobody can read or write this table directly.
-- The only way in is through the two admin-checked functions below.
alter table public.admin_private_files enable row level security;
revoke all on public.admin_private_files from anon, authenticated;

create or replace function public.admin_get_private_file(p_name text)
returns text language plpgsql stable security definer set search_path = public as $$
declare v text;
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  select body into v from public.admin_private_files where name = p_name;
  return v;
end $$;

create or replace function public.admin_private_file_info(p_name text)
returns table (bytes int, updated_at timestamptz) language plpgsql stable security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  return query select octet_length(f.body), f.updated_at from public.admin_private_files f where f.name = p_name;
end $$;

create or replace function public.admin_set_private_file(p_name text, p_body text)
returns void language plpgsql volatile security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  if p_name !~ '^[a-z0-9-]{1,40}$' then raise exception 'bad_name'; end if;
  if p_body is null or octet_length(p_body) > 5000000 then raise exception 'too_big'; end if;
  insert into public.admin_private_files (name, body, updated_at) values (p_name, p_body, now())
  on conflict (name) do update set body = excluded.body, updated_at = now();
end $$;

revoke all on function public.admin_get_private_file(text) from public, anon;
revoke all on function public.admin_private_file_info(text) from public, anon;
revoke all on function public.admin_set_private_file(text, text) from public, anon;
grant execute on function public.admin_get_private_file(text) to authenticated;
grant execute on function public.admin_private_file_info(text) to authenticated;
grant execute on function public.admin_set_private_file(text, text) to authenticated;
