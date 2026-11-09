-- Boardside Reviews · live mailing list + sending to it from admin.html
-- Paste into Supabase → SQL Editor → Run. Safe to run more than once. Needs welcome-email.sql first.
--
-- One live list: mailing_prefs holds each account's current choice.
--   • Ticking the box at sign-up puts them on it; the Settings switch in the question bank turns it on/off;
--     the Unsubscribe link in any email turns it off. Every change takes effect immediately.
--   • admin_mailing_send() reads the list at the moment you press Send, so it always goes to the right people.
-- Marketing emails should carry a postal address (CAN-SPAM). Set it once with:
--   insert into public.mailing_settings (k, v) values ('postal_address', 'Boardside Reviews · PO Box …, City, ST 00000')
--   on conflict (k) do update set v = excluded.v;

create table if not exists public.mailing_prefs (
  user_id    uuid primary key references auth.users(id) on delete cascade,
  email      text,
  subscribed boolean not null,
  source     text,
  updated_at timestamptz not null default now()
);
create table if not exists public.mailing_sends (
  id         bigserial primary key,
  subject    text not null,
  body       text not null,
  recipients integer not null,
  test       boolean not null,
  sent_by    text,
  sent_at    timestamptz not null default now()
);
create table if not exists public.mailing_settings (k text primary key, v text);
alter table public.mailing_prefs enable row level security;
alter table public.mailing_sends enable row level security;
alter table public.mailing_settings enable row level security;
revoke all on public.mailing_prefs, public.mailing_sends, public.mailing_settings from anon, authenticated;

-- one-time fill: everyone with an account, from their sign-up choice and any unsubscribes so far
insert into public.mailing_prefs (user_id, email, subscribed, source, updated_at)
select u.id, u.email,
       coalesce((u.raw_user_meta_data ->> 'marketing_opt_in')::boolean, false)
         and not exists (select 1 from public.mailing_optouts o where o.user_id = u.id),
       case when exists (select 1 from public.mailing_optouts o where o.user_id = u.id) then 'unsubscribe link' else 'sign-up' end,
       coalesce((select o.created_at from public.mailing_optouts o where o.user_id = u.id), u.created_at)
from auth.users u
where coalesce((u.raw_user_meta_data ->> 'account_ready')::boolean, false)
on conflict (user_id) do nothing;

create or replace function public.mailing_is_subscribed(p_user uuid)
returns boolean language sql stable security definer set search_path = public as $$
  select coalesce((select p.subscribed from public.mailing_prefs p where p.user_id = p_user), false);
$$;
revoke execute on function public.mailing_is_subscribed(uuid) from public, anon, authenticated;

-- new account: record their sign-up choice (fires before the welcome email trigger: names sort first)
create or replace function public.mailing_on_account_ready()
returns trigger language plpgsql security definer set search_path = public as $$
begin
  if coalesce(new.raw_user_meta_data ->> 'account_ready', '') = 'true'
     and coalesce(old.raw_user_meta_data ->> 'account_ready', '') <> 'true' then
    insert into public.mailing_prefs (user_id, email, subscribed, source)
    values (new.id, new.email, coalesce((new.raw_user_meta_data ->> 'marketing_opt_in')::boolean, false), 'sign-up')
    on conflict (user_id) do nothing;
  end if;
  return new;
exception when others then
  raise warning 'mailing pref not saved for %: %', new.id, sqlerrm;
  return new;
end;
$$;
drop trigger if exists boardside_mailing_pref on auth.users;
create trigger boardside_mailing_pref
  after update of raw_user_meta_data on auth.users
  for each row execute function public.mailing_on_account_ready();

-- welcome email now reads the live list
create or replace function public.welcome_on_account_ready()
returns trigger language plpgsql security definer set search_path = public as $$
declare
  mailing boolean;
  rid bigint;
begin
  if coalesce(new.raw_user_meta_data ->> 'account_ready', '') <> 'true'
     or coalesce(old.raw_user_meta_data ->> 'account_ready', '') = 'true'
     or exists (select 1 from public.email_welcome_log where user_id = new.id) then
    return new;
  end if;
  begin
    mailing := coalesce((select p.subscribed from public.mailing_prefs p where p.user_id = new.id),
                        coalesce((new.raw_user_meta_data ->> 'marketing_opt_in')::boolean, false));
    rid := public.welcome_send(new.id, new.email, new.raw_user_meta_data ->> 'last_name', mailing);
    if rid is not null then
      insert into public.email_welcome_log (user_id, email, mailing, request_id) values (new.id, new.email, mailing, rid)
      on conflict (user_id) do nothing;
    end if;
  exception when others then
    raise warning 'welcome email not sent for %: %', new.id, sqlerrm;
  end;
  return new;
end;
$$;

-- Unsubscribe link (any email): off, immediately
create or replace function public.email_unsubscribe(p_user uuid, p_token text)
returns boolean language plpgsql security definer set search_path = public as $$
begin
  if p_user is null or p_token is null or p_token <> public.email_unsub_token(p_user) then return false; end if;
  insert into public.mailing_prefs (user_id, email, subscribed, source, updated_at)
  select u.id, u.email, false, 'unsubscribe link', now() from auth.users u where u.id = p_user
  on conflict (user_id) do update set subscribed = false, source = 'unsubscribe link', updated_at = now();
  insert into public.mailing_optouts (user_id, email)
  select u.id, u.email from auth.users u where u.id = p_user
  on conflict (user_id) do nothing;
  return true;
end;
$$;
revoke execute on function public.email_unsubscribe(uuid, text) from public;
grant execute on function public.email_unsubscribe(uuid, text) to anon, authenticated;

-- question bank Settings switch: read / change your own choice
create or replace function public.qb_mailing_get()
returns boolean language sql stable security definer set search_path = public as $$
  select public.mailing_is_subscribed(auth.uid());
$$;
create or replace function public.qb_mailing_set(p_on boolean)
returns boolean language plpgsql security definer set search_path = public, auth as $$
declare uid uuid := auth.uid();
begin
  if uid is null or not exists (select 1 from auth.users u where u.id = uid and u.email_confirmed_at is not null) then
    raise exception 'not_signed_in';
  end if;
  insert into public.mailing_prefs (user_id, email, subscribed, source, updated_at)
  select u.id, u.email, p_on, 'settings', now() from auth.users u where u.id = uid
  on conflict (user_id) do update set subscribed = excluded.subscribed, source = 'settings', updated_at = now();
  if p_on then delete from public.mailing_optouts where user_id = uid; end if;
  return p_on;
end;
$$;
revoke execute on function public.qb_mailing_get() from public, anon;
revoke execute on function public.qb_mailing_set(boolean) from public, anon;
grant execute on function public.qb_mailing_get() to authenticated;
grant execute on function public.qb_mailing_set(boolean) to authenticated;

-- admin list (admin.html): mailing_list is the live value
drop function if exists public.admin_accounts();
create or replace function public.admin_accounts()
returns table (email text, first_name text, last_name text, verified boolean,
               waitlist boolean, mailing_list boolean, created_at timestamptz, kind text,
               heard_from text, heard_from_other text, mailing_updated_at timestamptz, mailing_source text)
language plpgsql stable security definer set search_path = public, auth as $$
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  return query
    select u.email::text,
           u.raw_user_meta_data ->> 'first_name',
           u.raw_user_meta_data ->> 'last_name',
           u.email_confirmed_at is not null,
           coalesce((u.raw_user_meta_data ->> 'account_ready')::boolean, false),
           coalesce(p.subscribed, false),
           u.created_at,
           case when coalesce((u.raw_user_meta_data ->> 'account_ready')::boolean, false)
                then 'Account' else 'Leaderboard only' end,
           u.raw_user_meta_data ->> 'heard_from',
           u.raw_user_meta_data ->> 'heard_from_other',
           p.updated_at,
           p.source
    from auth.users u
    left join public.mailing_prefs p on p.user_id = u.id
    order by u.created_at desc;
end;
$$;
revoke execute on function public.admin_accounts() from public, anon;
grant execute on function public.admin_accounts() to authenticated;

-- ── sending ──────────────────────────────────────────────────
create or replace function public.mailing_body_html(p_body text)
returns text language sql immutable as $$
  select string_agg(
           '<p style="margin:0 0 14px 0;">' ||
           regexp_replace(replace(public.email_esc(trim(para)), E'\n', '<br>'),
                          '(https?://[^\s<]+[^\s<.,;:!?)])', '<a href="\1" style="color:#0d7070;font-weight:600;">\1</a>', 'g') ||
           '</p>', E'\n' order by n)
  from regexp_split_to_table(replace(coalesce(p_body, ''), E'\r', ''), E'\n\\s*\n') with ordinality as t(para, n)
  where trim(para) <> '';
$$;

create or replace function public.mailing_email_html(p_subject text, p_body text, p_last text, p_unsub text)
returns text language plpgsql stable as $fn$
declare
  tpl text := $tpl$<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<meta name="supported-color-schemes" content="light">
<title>{{SUBJECT}}</title>
</head>
<body style="margin:0;padding:0;background:#eef5fc;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">{{PREHEADER}}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#eef5fc;">
<tr><td align="center" style="padding:28px 12px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:560px;background:#ffffff;border:1px solid #dce3ea;border-radius:16px;">
<tr><td style="padding:32px 32px 8px 32px;">
<a href="https://www.boardsidereviews.com/" style="text-decoration:none;"><img src="https://www.boardsidereviews.com/email/logo.png" width="220" height="38" alt="Boardside Reviews" style="display:block;border:0;width:220px;height:auto;"></a>
</td></tr>
<tr><td style="padding:18px 32px 0 32px;font-family:Inter,Arial,Helvetica,sans-serif;font-size:16px;line-height:1.6;color:#33465f;">
<p style="margin:0 0 14px 0;">{{GREETING}}</p>
{{BODY}}
</td></tr>
<tr><td style="padding:8px 32px 30px 32px;font-family:Inter,Arial,Helvetica,sans-serif;font-size:15px;line-height:1.6;color:#33465f;">
<p style="margin:0;">With gratitude,<br><b style="color:#0b2545;">Khaled M. Abdullah, MD</b><br><span style="color:#52627a;">Founder, Boardside Reviews</span></p>
</td></tr>
<tr><td style="border-top:1px solid #dce3ea;padding:20px 32px 26px 32px;font-family:Inter,Arial,Helvetica,sans-serif;font-size:13px;line-height:1.6;color:#52627a;">
<p style="margin:0 0 10px 0;">Questions? Reply to this email or reach us at <a href="mailto:support@boardsidereviews.com" style="color:#0d7070;text-decoration:none;font-weight:600;">support@boardsidereviews.com</a>.</p>
<p style="margin:0;">Boardside Reviews &middot; Where boards meet the bedside{{ADDRESS}}<br>You're receiving this because you joined the Boardside Reviews mailing list.<br><br><a href="{{UNSUB_URL}}" style="color:#0d7070;font-weight:600;">Unsubscribe</a></p>
</td></tr>
</table>
</td></tr>
</table>
</body>
</html>
$tpl$;
  addr text := (select v from public.mailing_settings where k = 'postal_address');
  greet text := case when nullif(trim(p_last), '') is null then 'Hello,' else 'Dear Dr. ' || public.email_esc(trim(p_last)) || ',' end;
begin
  return replace(replace(replace(replace(replace(replace(tpl,
    '{{SUBJECT}}', public.email_esc(p_subject)),
    '{{PREHEADER}}', public.email_esc(left(regexp_replace(coalesce(p_body, ''), '\s+', ' ', 'g'), 120))),
    '{{GREETING}}', greet),
    '{{BODY}}', coalesce(public.mailing_body_html(p_body), '')),
    '{{ADDRESS}}', case when nullif(trim(addr), '') is null then '' else '<br>' || public.email_esc(addr) end),
    '{{UNSUB_URL}}', public.email_esc(p_unsub));
end;
$fn$;

create or replace function public.mailing_email_text(p_body text, p_last text, p_unsub text)
returns text language sql stable as $$
  select concat_ws(E'\n',
    case when nullif(trim(p_last), '') is null then 'Hello,' else 'Dear Dr. ' || trim(p_last) || ',' end, '',
    trim(p_body), '',
    'With gratitude,', 'Khaled M. Abdullah, MD', 'Founder, Boardside Reviews', '', '---',
    'Questions? Reply to this email or reach us at support@boardsidereviews.com.',
    'Boardside Reviews · Where boards meet the bedside',
    (select v from public.mailing_settings where k = 'postal_address'),
    'You''re receiving this because you joined the Boardside Reviews mailing list.',
    'Unsubscribe: ' || p_unsub);
$$;

-- admin preview (exactly what subscribers get)
create or replace function public.admin_mailing_preview(p_subject text, p_body text)
returns json language plpgsql stable security definer set search_path = public, auth as $$
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  return json_build_object(
    'html', public.mailing_email_html(p_subject, p_body, 'Abdullah', 'https://www.boardsidereviews.com/unsubscribe.html'),
    'subscribers', (select count(*) from public.mailing_prefs p join auth.users u on u.id = p.user_id
                    where p.subscribed and u.email_confirmed_at is not null),
    'has_address', exists (select 1 from public.mailing_settings where k = 'postal_address' and nullif(trim(v), '') is not null));
end;
$$;

-- send: p_test = true → only to the admin's own email; false → everyone subscribed right now
create or replace function public.admin_mailing_send(p_subject text, p_body text, p_test boolean)
returns json language plpgsql security definer set search_path = public, extensions as $$
declare
  api_key text := (select decrypted_secret from vault.decrypted_secrets where name = 'resend_api_key' limit 1);
  me text := lower(coalesce(auth.jwt() ->> 'email', ''));
  batch jsonb := '[]'::jsonb; n int := 0; reqs int := 0; r record; unsub text; subj text := trim(coalesce(p_subject, ''));
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  if api_key is null then raise exception 'no_resend_key'; end if;
  if subj = '' or trim(coalesce(p_body, '')) = '' then raise exception 'empty'; end if;
  for r in
    select u.id, u.email, u.raw_user_meta_data ->> 'last_name' as last
    from auth.users u join public.mailing_prefs p on p.user_id = u.id
    where p.subscribed and u.email_confirmed_at is not null and not p_test
    union all
    select '00000000-0000-0000-0000-000000000000'::uuid, me, 'Abdullah' where p_test
  loop
    unsub := 'https://www.boardsidereviews.com/unsubscribe.html?u=' || r.id || '&t=' || public.email_unsub_token(r.id);
    batch := batch || jsonb_build_array(jsonb_build_object(
      'from', 'Boardside Reviews <hello@boardsidereviews.com>',
      'to', jsonb_build_array(r.email),
      'reply_to', 'hello@boardsidereviews.com',
      'subject', case when p_test then '[Test] ' || subj else subj end,
      'html', public.mailing_email_html(subj, p_body, r.last, unsub),
      'text', public.mailing_email_text(p_body, r.last, unsub),
      'headers', jsonb_build_object('List-Unsubscribe', '<' || unsub || '>')));
    n := n + 1;
    if jsonb_array_length(batch) = 100 then        -- Resend takes up to 100 emails per batch call
      perform net.http_post(url := 'https://api.resend.com/emails/batch', body := batch,
        headers := jsonb_build_object('Authorization', 'Bearer ' || api_key, 'Content-Type', 'application/json'), timeout_milliseconds := 20000);
      reqs := reqs + 1; batch := '[]'::jsonb;
    end if;
  end loop;
  if jsonb_array_length(batch) > 0 then
    perform net.http_post(url := 'https://api.resend.com/emails/batch', body := batch,
      headers := jsonb_build_object('Authorization', 'Bearer ' || api_key, 'Content-Type', 'application/json'), timeout_milliseconds := 20000);
    reqs := reqs + 1;
  end if;
  insert into public.mailing_sends (subject, body, recipients, test, sent_by) values (subj, p_body, n, p_test, me);
  return json_build_object('sent', n, 'requests', reqs, 'test', p_test);
end;
$$;

create or replace function public.admin_mailing_history()
returns table (subject text, recipients integer, test boolean, sent_at timestamptz)
language plpgsql stable security definer set search_path = public as $$
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  return query select s.subject, s.recipients, s.test, s.sent_at from public.mailing_sends s order by s.sent_at desc limit 20;
end;
$$;
revoke execute on function public.admin_mailing_preview(text, text) from public, anon;
revoke execute on function public.admin_mailing_send(text, text, boolean) from public, anon;
revoke execute on function public.admin_mailing_history() from public, anon;
grant execute on function public.admin_mailing_preview(text, text) to authenticated;
grant execute on function public.admin_mailing_send(text, text, boolean) to authenticated;
grant execute on function public.admin_mailing_history() to authenticated;

select (select count(*) from public.mailing_prefs) as accounts_tracked,
       (select count(*) from public.mailing_prefs where subscribed) as subscribed_now;
