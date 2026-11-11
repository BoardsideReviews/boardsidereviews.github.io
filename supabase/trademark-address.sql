-- Boardside Reviews · trademark (™) + mailing address in the automatic emails (Nov 10, 2026)
-- Paste into Supabase → SQL Editor → Run. Safe to run more than once.
-- Only replaces the four email-template functions and sets the postal address; nothing else changes.
-- (The same changes are already in welcome-email.sql and mailing-list.sql.)

insert into public.mailing_settings (k, v)
values ('postal_address', '5730 N First St Ste 105 #291, Fresno, CA 93710')
on conflict (k) do update set v = excluded.v;

-- welcome email (sent automatically when an account is created)
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

-- mailing-list emails (sent from admin.html)
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
<a href="https://www.boardsidereviews.com/" style="text-decoration:none;"><img src="https://www.boardsidereviews.com/email/logo-tagline.png" width="300" height="54" alt="Boardside Reviews: Where boards meet the bedside" style="display:block;border:0;width:300px;max-width:100%;height:auto;"></a>
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
<p style="margin:0;">Boardside Reviews&trade; &middot; Where boards meet the bedside{{ADDRESS}}<br>You're receiving this because you joined the Boardside Reviews mailing list.<br><br><a href="{{UNSUB_URL}}" style="color:#0d7070;font-weight:600;">Unsubscribe</a></p>
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
    'Boardside Reviews™ · Where boards meet the bedside',
    (select v from public.mailing_settings where k = 'postal_address'),
    'You''re receiving this because you joined the Boardside Reviews mailing list.',
    'Unsubscribe: ' || p_unsub);
$$;
