-- Boardside Reviews · automatic welcome email (sent from hello@boardsidereviews.com via Resend)
-- Paste into Supabase → SQL Editor → Run. Safe to run more than once.
--
-- When someone finishes creating an account (account_ready becomes true), the database sends ONE
-- welcome email. If they ticked the mailing-list box, the email also thanks them for that and has an
-- Unsubscribe link at the bottom (boardsidereviews.com/unsubscribe.html).
--
-- One-time step: the Resend API key lives in Supabase Vault, never in this file. In Resend, create an
-- API key with "Sending access" for boardsidereviews.com, then run (with your key):
--     select vault.create_secret('re_YOUR_KEY', 'resend_api_key', 'Resend key for welcome emails');
-- Until that key exists nothing is sent, and account creation keeps working normally.
-- To send yourself a test:   select public.welcome_send_test(true);   -- true = mailing-list version

create extension if not exists pg_net with schema extensions;

-- who has been sent the welcome email (one per account)
create table if not exists public.email_welcome_log (
  user_id    uuid primary key references auth.users(id) on delete cascade,
  email      text,
  mailing    boolean,
  request_id bigint,
  created_at timestamptz not null default now()
);
-- people who unsubscribed from the mailing list
create table if not exists public.mailing_optouts (
  user_id    uuid primary key references auth.users(id) on delete cascade,
  email      text,
  created_at timestamptz not null default now()
);
alter table public.email_welcome_log enable row level security;
alter table public.mailing_optouts enable row level security;
revoke all on public.email_welcome_log, public.mailing_optouts from anon, authenticated;

-- secret used to sign unsubscribe links (made once, kept in Vault)
do $$
begin
  if not exists (select 1 from vault.secrets where name = 'unsubscribe_secret') then
    perform vault.create_secret(encode(extensions.gen_random_bytes(32), 'hex'), 'unsubscribe_secret', 'Signs unsubscribe links');
  end if;
end $$;

create or replace function public.email_unsub_token(p_user uuid)
returns text language sql stable security definer set search_path = public, extensions as $$
  select encode(extensions.hmac(p_user::text, (select decrypted_secret from vault.decrypted_secrets where name = 'unsubscribe_secret'), 'sha256'), 'hex');
$$;
revoke execute on function public.email_unsub_token(uuid) from public, anon, authenticated;

-- called by boardsidereviews.com/unsubscribe.html
create or replace function public.email_unsubscribe(p_user uuid, p_token text)
returns boolean language plpgsql security definer set search_path = public as $$
begin
  if p_user is null or p_token is null or p_token <> public.email_unsub_token(p_user) then return false; end if;
  insert into public.mailing_optouts (user_id, email)
  select u.id, u.email from auth.users u where u.id = p_user
  on conflict (user_id) do nothing;
  return true;
end;
$$;
revoke execute on function public.email_unsubscribe(uuid, text) from public;
grant execute on function public.email_unsubscribe(uuid, text) to anon, authenticated;

create or replace function public.email_esc(p text)
returns text language sql immutable as $$
  select replace(replace(replace(replace(coalesce(p, ''), '&', '&amp;'), '<', '&lt;'), '>', '&gt;'), '"', '&quot;');
$$;

create or replace function public.welcome_email_html(p_last text, p_mailing boolean, p_unsub text)
returns text language plpgsql immutable as $fn$
declare
  tpl text := $tpl$<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<meta name="supported-color-schemes" content="light">
<title>Thank you for joining Boardside Reviews</title>
</head>
<body style="margin:0;padding:0;background:#eef5fc;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">Thank you for creating your Boardside Reviews account. Here's where to start.</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#eef5fc;">
<tr><td align="center" style="padding:28px 12px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:560px;background:#ffffff;border:1px solid #dce3ea;border-radius:16px;">
<tr><td style="padding:32px 32px 8px 32px;">
<a href="https://www.boardsidereviews.com/" style="text-decoration:none;"><img src="https://www.boardsidereviews.com/email/logo-tagline.png" width="300" height="54" alt="Boardside Reviews: Where boards meet the bedside" style="display:block;border:0;width:300px;max-width:100%;height:auto;"></a>
</td></tr>
<tr><td style="padding:20px 32px 0 32px;font-family:'Plus Jakarta Sans',Inter,Arial,Helvetica,sans-serif;color:#0b2545;">
<h1 style="margin:0;font-size:30px;line-height:1.15;font-weight:800;letter-spacing:-0.5px;color:#0b2545;">Thank you for joining.</h1>
</td></tr>
<tr><td style="padding:18px 32px 0 32px;font-family:Inter,Arial,Helvetica,sans-serif;font-size:16px;line-height:1.6;color:#33465f;">
<p style="margin:0 0 14px 0;">{{GREETING}}</p>
<p style="margin:0 0 14px 0;">Thank you for creating a Boardside Reviews&trade; account. Boardside is a small, physician-built project, and it truly means a lot that you'd give it a try. Every question is reviewed and verified personally, and I don't take your time for granted.</p>
</td></tr>
<tr><td style="padding:10px 32px 0 32px;font-family:'Plus Jakarta Sans',Inter,Arial,Helvetica,sans-serif;">
<p style="margin:0 0 12px 0;font-size:17px;font-weight:800;color:#0b2545;">Start here</p>
</td></tr>
<tr><td style="padding:0 32px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="font-family:Inter,Arial,Helvetica,sans-serif;font-size:15px;line-height:1.55;color:#33465f;">
<tr><td width="40" valign="top" style="padding:0 0 14px 0;"><div style="width:28px;height:28px;line-height:28px;border-radius:14px;background:#e2f3f1;color:#0d7070;font-weight:700;font-size:14px;text-align:center;">1</div></td>
<td valign="top" style="padding:2px 0 14px 0;"><b style="color:#0b2545;">Try the free sets.</b> 80 questions across Pulmonary &amp; Critical Care, Cardiology, GI and Nephrology, in learning or exam mode.</td></tr>
<tr><td width="40" valign="top" style="padding:0 0 14px 0;"><div style="width:28px;height:28px;line-height:28px;border-radius:14px;background:#e2f3f1;color:#0d7070;font-weight:700;font-size:14px;text-align:center;">2</div></td>
<td valign="top" style="padding:2px 0 14px 0;"><b style="color:#0b2545;">Read every explanation.</b> Each answer choice is explained, so the wrong ones teach as much as the right one.</td></tr>
<tr><td width="40" valign="top" style="padding:0 0 6px 0;"><div style="width:28px;height:28px;line-height:28px;border-radius:14px;background:#e2f3f1;color:#0d7070;font-weight:700;font-size:14px;text-align:center;">3</div></td>
<td valign="top" style="padding:2px 0 6px 0;"><b style="color:#0b2545;">Play between shifts.</b> ABG Blitz, Vent Lab, Hemodynamic Roulette and more in Gamified Learning.</td></tr>
</table>
</td></tr>
<tr><td align="left" style="padding:20px 32px 6px 32px;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td style="border-radius:10px;background:#0d7070;">
<a href="https://www.boardsidereviews.com/qbank.html?sample" style="display:inline-block;padding:13px 22px;font-family:Inter,Arial,Helvetica,sans-serif;font-size:16px;font-weight:700;color:#ffffff;text-decoration:none;border-radius:10px;">Start practicing &rarr;</a>
</td></tr></table>
</td></tr>
<tr><td style="padding:20px 32px 0 32px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#e2f3f1;border:1px solid #bfe3df;border-radius:12px;">
<tr><td style="padding:16px 18px;font-family:Inter,Arial,Helvetica,sans-serif;font-size:15px;line-height:1.55;color:#33465f;">
<p style="margin:0 0 4px 0;font-family:'Plus Jakarta Sans',Inter,Arial,Helvetica,sans-serif;font-size:16px;font-weight:800;color:#0d7070;">You're on the launch waitlist.</p>
The full question bank (about 1,600 questions) and the Boardside Notes book open soon. I'll email you 48 hours before launch and again when we're live, so you have a chance at the founders price.
</td></tr></table>
</td></tr>
{{MAILING_BLOCK}}
<tr><td style="padding:22px 32px 30px 32px;font-family:Inter,Arial,Helvetica,sans-serif;font-size:15px;line-height:1.6;color:#33465f;">
<p style="margin:0 0 14px 0;">If anything is unclear, wrong, or could be better, just reply to this email. I read every one.</p>
<p style="margin:0;">With gratitude,<br><b style="color:#0b2545;">Khaled M. Abdullah, MD</b><br><span style="color:#52627a;">Founder, Boardside Reviews</span></p>
</td></tr>
<tr><td style="border-top:1px solid #dce3ea;padding:20px 32px 26px 32px;font-family:Inter,Arial,Helvetica,sans-serif;font-size:13px;line-height:1.6;color:#52627a;">
<p style="margin:0 0 10px 0;">Questions? Reply to this email or reach us at <a href="mailto:support@boardsidereviews.com" style="color:#0d7070;text-decoration:none;font-weight:600;">support@boardsidereviews.com</a>.</p>
<p style="margin:0;">Boardside Reviews&trade; &middot; Where boards meet the bedside<br>5730 N First St Ste 105 #291, Fresno, CA 93710<br>You're receiving this because you created an account at <a href="https://www.boardsidereviews.com/" style="color:#52627a;">boardsidereviews.com</a>.{{UNSUB_BLOCK}}</p>
</td></tr>
</table>
</td></tr>
</table>
</body>
</html>
$tpl$;
  mailing_block text := $blk$<tr><td style="padding:12px 32px 0 32px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#fff4dc;border:1px solid #f0d9a6;border-radius:12px;">
<tr><td style="padding:16px 18px;font-family:Inter,Arial,Helvetica,sans-serif;font-size:15px;line-height:1.55;color:#33465f;">
<p style="margin:0 0 4px 0;font-family:'Plus Jakarta Sans',Inter,Arial,Helvetica,sans-serif;font-size:16px;font-weight:800;color:#0b2545;">Thank you for joining the mailing list, too.</p>
Expect an occasional teaching email: high-yield pearls and new free material. No spam, and you can unsubscribe anytime at the bottom of any email.
</td></tr></table>
</td></tr>$blk$;
  unsub_block text := $blk$<br><br>Don't want mailing-list emails? <a href="{{UNSUB_URL}}" style="color:#0d7070;font-weight:600;">Unsubscribe</a>.$blk$;
  greet text := case when nullif(trim(p_last), '') is null then 'Hello,' else 'Dear Dr. ' || public.email_esc(trim(p_last)) || ',' end;
begin
  return replace(replace(replace(tpl, '{{GREETING}}', greet),
                 '{{MAILING_BLOCK}}', case when p_mailing then mailing_block else '' end),
                 '{{UNSUB_BLOCK}}', case when p_mailing then replace(unsub_block, '{{UNSUB_URL}}', public.email_esc(p_unsub)) else '' end);
end;
$fn$;

create or replace function public.welcome_email_text(p_last text, p_mailing boolean, p_unsub text)
returns text language sql immutable as $fn$
  select concat_ws(E'\n',
    case when nullif(trim(p_last), '') is null then 'Hello,' else 'Dear Dr. ' || trim(p_last) || ',' end, '',
    'Thank you for creating a Boardside Reviews™ account. Boardside is a small, physician-built project, and it truly means a lot that you''d give it a try. Every question is reviewed and verified personally, and I don''t take your time for granted.', '',
    'Start here:',
    '1. Try the free sets. 80 questions across Pulmonary & Critical Care, Cardiology, GI and Nephrology, in learning or exam mode.',
    '2. Read every explanation. Each answer choice is explained, so the wrong ones teach as much as the right one.',
    '3. Play between shifts. ABG Blitz, Vent Lab, Hemodynamic Roulette and more in Gamified Learning.', '',
    'Start practicing: https://www.boardsidereviews.com/qbank.html?sample', '',
    'You''re on the launch waitlist. The full question bank (about 1,600 questions) and the Boardside Notes book open soon. I''ll email you 48 hours before launch and again when we''re live, so you have a chance at the founders price.', '',
    case when p_mailing then 'Thank you for joining the mailing list, too. Expect an occasional teaching email: high-yield pearls and new free material. No spam, and you can unsubscribe anytime.' || E'\n' end,
    'If anything is unclear, wrong, or could be better, just reply to this email. I read every one.', '',
    'With gratitude,', 'Khaled M. Abdullah, MD', 'Founder, Boardside Reviews', '',
    '---', 'Questions? Reply to this email or reach us at support@boardsidereviews.com.',
    'Boardside Reviews™ · Where boards meet the bedside',
    '5730 N First St Ste 105 #291, Fresno, CA 93710',
    'You''re receiving this because you created an account at boardsidereviews.com.',
    case when p_mailing then 'Unsubscribe from the mailing list: ' || p_unsub end);
$fn$;

-- queue the email through Resend; returns the pg_net request id (null if no API key yet)
create or replace function public.welcome_send(p_user uuid, p_email text, p_last text, p_mailing boolean)
returns bigint language plpgsql security definer set search_path = public, extensions as $$
declare
  api_key text := (select decrypted_secret from vault.decrypted_secrets where name = 'resend_api_key' limit 1);
  unsub text := 'https://www.boardsidereviews.com/unsubscribe.html?u=' || p_user || '&t=' || public.email_unsub_token(p_user);
  body jsonb;
begin
  if api_key is null or p_email is null then return null; end if;
  body := jsonb_build_object(
    'from', 'Boardside Reviews <hello@boardsidereviews.com>',
    'to', jsonb_build_array(p_email),
    'reply_to', 'hello@boardsidereviews.com',
    'subject', 'Thank you for joining Boardside Reviews',
    'html', public.welcome_email_html(p_last, p_mailing, unsub),
    'text', public.welcome_email_text(p_last, p_mailing, unsub));
  if p_mailing then body := body || jsonb_build_object('headers', jsonb_build_object('List-Unsubscribe', '<' || unsub || '>')); end if;
  return net.http_post(url := 'https://api.resend.com/emails', body := body,
    headers := jsonb_build_object('Authorization', 'Bearer ' || api_key, 'Content-Type', 'application/json'),
    timeout_milliseconds := 10000);
end;
$$;
revoke execute on function public.welcome_send(uuid, text, text, boolean) from public, anon, authenticated;

-- fires when an account is finished (account_ready turns true); never blocks the sign-up itself
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
    mailing := coalesce((new.raw_user_meta_data ->> 'marketing_opt_in')::boolean, false)
               and not exists (select 1 from public.mailing_optouts o where o.user_id = new.id);
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
drop trigger if exists boardside_welcome_email on auth.users;
create trigger boardside_welcome_email
  after update of raw_user_meta_data on auth.users
  for each row execute function public.welcome_on_account_ready();

-- send a test to the admin inbox (boardsidereviews@gmail.com); run from the SQL editor
create or replace function public.welcome_send_test(p_mailing boolean default true, p_to text default 'boardsidereviews@gmail.com')
returns bigint language sql security definer set search_path = public as $$
  select public.welcome_send('00000000-0000-0000-0000-000000000000'::uuid, p_to, 'Abdullah', p_mailing);
$$;
revoke execute on function public.welcome_send_test(boolean, text) from public, anon, authenticated;

-- admin list: mailing_list is false once someone unsubscribes
drop function if exists public.admin_accounts();
create or replace function public.admin_accounts()
returns table (email text, first_name text, last_name text, verified boolean,
               waitlist boolean, mailing_list boolean, created_at timestamptz, kind text,
               heard_from text, heard_from_other text)
language plpgsql stable security definer set search_path = public, auth as $$
begin
  if not public.is_admin() then raise exception 'not_admin'; end if;
  return query
    select u.email::text,
           u.raw_user_meta_data ->> 'first_name',
           u.raw_user_meta_data ->> 'last_name',
           u.email_confirmed_at is not null,
           coalesce((u.raw_user_meta_data ->> 'account_ready')::boolean, false),
           coalesce((u.raw_user_meta_data ->> 'marketing_opt_in')::boolean, false)
             and not exists (select 1 from public.mailing_optouts o where o.user_id = u.id),
           u.created_at,
           case when coalesce((u.raw_user_meta_data ->> 'account_ready')::boolean, false)
                then 'Account' else 'Leaderboard only' end,
           u.raw_user_meta_data ->> 'heard_from',
           u.raw_user_meta_data ->> 'heard_from_other'
    from auth.users u
    order by u.created_at desc;
end;
$$;
revoke execute on function public.admin_accounts() from public, anon;
grant execute on function public.admin_accounts() to authenticated;

select (select count(*) from vault.secrets where name = 'resend_api_key') as resend_key_saved,
       (select count(*) from vault.secrets where name = 'unsubscribe_secret') as unsubscribe_secret_saved;
