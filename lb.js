// Boardside Reviews leaderboard client.
// Needs lb-config.js and the supabase-js UMD build loaded first.
// Exposes window.BLB with sign-in (email code), display names, score posting,
// leaderboard reads, and admin calls.
(function () {
  var cfg = window.BOARDSIDE_LB || {};
  var enabled = !!(cfg.url && cfg.key && window.supabase && window.supabase.createClient);
  var sb = enabled ? window.supabase.createClient(cfg.url, cfg.key, {
    auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: false }
  }) : null;

  var MESSAGES = {
    name_length: "Use 3 to 20 characters.",
    name_chars: "Use letters, numbers, spaces, dots, dashes, or underscores.",
    name_blocked: "That name isn't allowed. Try another.",
    too_fast: "Posted a moment ago. Wait a few seconds and try again.",
    no_name: "Pick a display name first.",
    banned: "This account can't post to the leaderboard.",
    not_signed_in: "Sign in first.",
    not_admin: "This page is for the site owner.",
    already_posted: "You've already posted a time for this puzzle. Your first clean solve is the one that counts.",
    stale_puzzle: "This puzzle's board is closed. Times post for today's puzzle only.",
    too_quick: "That time is too fast to post.",
    bad_time: "That time couldn't be posted.",
    copay_once: "You've already posted today's streak. Your first run of the day is the one that counts.",
    endemic_once: "You've already posted today's score. Your first pin of the day is the one that counts."
  };
  function friendly(err) {
    if (!err) return "";
    var m = err.message || String(err);
    if (/scores_cross_cover_once/.test(m)) return MESSAGES.already_posted;
    if (/scores_copay_once|copay_once/.test(m)) return MESSAGES.copay_once;
    if (/scores_endemic_once|endemic_once/.test(m)) return MESSAGES.endemic_once;
    if (/profiles_name_key_key|duplicate key/.test(m)) return "Someone already has that name. Try another.";
    if (/Token has expired|invalid|otp/i.test(m) && /token|otp|code/i.test(m)) return "That code didn't work. Check it, or send a new one.";
    if (/rate limit|security purposes|seconds/i.test(m)) return "Too many codes requested. Wait a minute, then try again.";
    if (/Failed to fetch|NetworkError/i.test(m)) return "Couldn't reach the leaderboard. Check your connection.";
    for (var k in MESSAGES) if (m.indexOf(k) !== -1) return MESSAGES[k];
    return m;
  }
  function need() { if (!sb) throw new Error("Leaderboard is not set up yet."); }

  async function user() {
    if (!sb) return null;
    var r = await sb.auth.getSession();
    return r.data && r.data.session ? r.data.session.user : null;
  }
  async function profile() {
    var u = await user(); if (!u) return null;
    var r = await sb.from("profiles").select("display_name,banned").eq("user_id", u.id).maybeSingle();
    if (r.error) throw r.error;
    return r.data || { display_name: null, banned: false, missing: true };
  }
  async function sendCode(email) {
    need();
    var r = await sb.auth.signInWithOtp({ email: email, options: { shouldCreateUser: true } });
    if (r.error) throw r.error;
  }
  async function verify(email, code) {
    need();
    var r = await sb.auth.verifyOtp({ email: email, token: code, type: "email" });
    if (r.error) throw r.error;
    return r.data.user;
  }
  async function setName(name) {
    var u = await user(); if (!u) throw new Error("not_signed_in");
    var p = await profile();
    var r = p && !p.missing
      ? await sb.from("profiles").update({ display_name: name }).eq("user_id", u.id).select("display_name")
      : await sb.from("profiles").insert({ user_id: u.id, display_name: name }).select("display_name");
    if (r.error) throw r.error;
    if (!r.data || !r.data.length) throw new Error("banned");
    return r.data[0].display_name;
  }
  async function submit(game, variant, score, total) {
    need();
    var r = await sb.rpc("submit_score", { p_game: game, p_variant: variant, p_score: score, p_total: total });
    if (r.error) throw r.error;
  }
  async function board(game, variant, days, limit) {
    need();
    var r = await sb.rpc("get_leaderboard", { p_game: game, p_variant: variant, p_days: days || null, p_limit: limit || 50 });
    if (r.error) throw r.error;
    return r.data || [];
  }
  async function boardPoints(game, variant, days, limit) {
    need();
    var r = await sb.rpc("get_points_leaderboard", { p_game: game, p_variant: variant, p_days: days || null, p_limit: limit || 50 });
    if (r.error) throw r.error;
    return r.data || [];
  }
  async function boardTime(game, variant, limit) {
    need();
    var r = await sb.rpc("get_time_leaderboard", { p_game: game, p_variant: variant, p_limit: limit || 50 });
    if (r.error) throw r.error;
    return r.data || [];
  }
  async function rpc(name, args) {
    need();
    var r = await sb.rpc(name, args || {});
    if (r.error) throw r.error;
    return r.data;
  }
  async function signOut() { if (sb) await sb.auth.signOut(); }

  // ── Sign-in dialog ──
  // Games: sign in with a Boardside Reviews account (email + password) or create one
  // (name, email, password, mailing-list choice, then a 6-digit code to verify the email).
  // These are the same accounts as the question bank. Admin pages keep the email-code sign-in.
  var css = '\
.blb-back{position:fixed;inset:0;z-index:1000;background:rgba(8,16,30,.62);display:flex;align-items:flex-start;justify-content:center;padding:24px 16px;overflow-y:auto}\
.blb-card{color-scheme:light;width:min(440px,100%);margin:auto 0;background:#fff;color:#0b2545;border-radius:18px;padding:24px;box-shadow:0 24px 60px rgba(0,0,0,.35);font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;display:flex;flex-direction:column;gap:14px;text-align:left}\
.blb-card h2{margin:0;font-family:"Plus Jakarta Sans",Inter,system-ui,sans-serif;font-weight:800;font-size:22px;letter-spacing:-.01em;color:#0b2545}\
.blb-card p{margin:0;font-size:15px;line-height:22px;color:#52627a}\
.blb-card form{display:flex;flex-direction:column;gap:12px;margin:0}\
.blb-card label{font-size:13px;font-weight:600;color:#33465f;display:flex;flex-direction:column;gap:6px}\
.blb-card input,.blb-card select{font:inherit;font-size:16px;padding:11px 13px;border:1px solid #c9d5e2;border-radius:10px;color:#0b2545;background:#fff;width:100%;box-sizing:border-box}\
.blb-card input:focus,.blb-card select:focus{outline:2px solid #0d7070;outline-offset:1px;border-color:#0d7070}\
.blb-two{display:grid;grid-template-columns:1fr 1fr;gap:10px}\
.blb-code{letter-spacing:.4em;font-variant-numeric:tabular-nums;text-align:center;font-size:22px!important}\
.blb-row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}\
.blb-btn{font:inherit;font-weight:600;font-size:15px;border:0;border-radius:10px;padding:12px 18px;cursor:pointer;background:#0b2545;color:#fff}\
.blb-btn.teal{background:#0d7070}\
.blb-btn.wide{width:100%}\
.blb-btn:disabled{opacity:.55;cursor:default}\
.blb-link{font:inherit;font-size:14px;background:none;border:0;color:#0d7070;font-weight:600;cursor:pointer;padding:4px 0;text-align:left}\
.blb-lblrow{display:flex;justify-content:space-between;align-items:center}\
.blb-lblrow .blb-link{font-size:13px;padding:0}\
.blb-err{color:#b9432c;font-size:14px}\
.blb-err:empty{display:none}\
.blb-fine{font-size:12px!important;line-height:17px!important;color:#7a8799!important}\
.blb-rules{list-style:none;margin:-4px 0 0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:3px 10px;font-size:12.5px;color:#7a8799}\
.blb-rules li::before{content:"○ ";color:#b5c1cf}\
.blb-rules li.ok{color:#1f7a4d}\
.blb-rules li.ok::before{content:"✓ ";color:#1f7a4d}\
.blb-check{flex-direction:row!important;align-items:flex-start;gap:10px!important;font-weight:500!important;font-size:13px!important;line-height:18px;color:#52627a!important}\
.blb-check input{width:18px;height:18px;flex:0 0 18px;margin:1px 0 0;padding:0;accent-color:#0d7070}\
.blb-note{background:#eef5fc;border-radius:10px;padding:10px 12px;font-size:12.5px;line-height:18px;color:#33465f}\
.blb-tabs{display:grid;grid-template-columns:1fr 1fr;background:#eef2f6;border-radius:12px;padding:4px;gap:4px}\
.blb-tabs button{font:inherit;font-size:14px;font-weight:600;border:0;border-radius:9px;padding:9px 6px;background:none;color:#52627a;cursor:pointer}\
.blb-tabs button[aria-pressed=true]{background:#fff;color:#0b2545;box-shadow:0 1px 3px rgba(11,37,69,.15)}\
@media (max-width:420px){.blb-two{grid-template-columns:1fr}.blb-card{padding:20px}}';

  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  function pwRules(a, b) {
    return [
      { ok: a.length >= 8, t: "At least 8 characters" },
      { ok: /[A-Za-z]/.test(a), t: "At least one letter" },
      { ok: /[0-9]/.test(a), t: "At least one number" },
      { ok: a.length > 0 && a === b, t: "Passwords match" }
    ];
  }
  function authFriendly(err) {
    var m = (err && (err.message || String(err))) || "";
    if (/Invalid login credentials/i.test(m)) return "Wrong email or password. New here? Create a free account.";
    if (/Signups not allowed|User not found|not found/i.test(m)) return "We couldn't find an account for that email. Create a free account first.";
    if (/Email not confirmed/i.test(m)) return "Please verify your email first, or sign in with an email code.";
    if (/Password should be|weak/i.test(m)) return "That password is too weak. Use at least 8 characters with letters and numbers.";
    return friendly(err);
  }
  function profileData(first, last, optin) {
    return { first_name: first, last_name: last, marketing_opt_in: !!optin,
             marketing_opt_in_at: optin ? new Date().toISOString() : null, account_ready: true,
             waitlist: true, waitlist_at: new Date().toISOString() };
  }
  var HEARD = ["Instagram", "YouTube", "X (Twitter)", "TikTok", "Google search", "A friend or co-resident",
    "My residency program", "An attending or faculty member", "Reddit", "Other"];
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  function dialog(opts) {
    opts = opts || {};
    var admin = !!opts.admin || /admin/i.test(opts.title || "");
    return new Promise(function (resolve) {
      if (!document.getElementById("blb-css")) {
        var st = document.createElement("style"); st.id = "blb-css"; st.textContent = css; document.head.appendChild(st);
      }
      var back = document.createElement("div"); back.className = "blb-back";
      back.innerHTML = '<div class="blb-card" role="dialog" aria-modal="true" aria-labelledby="blb-title"></div>';
      var card = back.firstChild, email = "";
      document.body.appendChild(back);
      function close(v) { back.remove(); document.removeEventListener("keydown", escKey); resolve(v); }
      function escKey(e) { if (e.key === "Escape") close(null); }
      document.addEventListener("keydown", escKey);
      back.addEventListener("mousedown", function (e) { if (e.target === back) close(null); });
      function wire(onsubmit) {
        var f = card.querySelector("form"), er = card.querySelector(".blb-err");
        card.querySelectorAll("[data-x]").forEach(function (b) { b.onclick = function () { close(null); }; });
        f.addEventListener("input", function () { er.textContent = ""; });
        f.onsubmit = function (e) { e.preventDefault(); er.textContent = ""; onsubmit(f, er, f.querySelector("button[type=submit]")); };
        return f;
      }
      function busy(b, on, label) { b.disabled = on; b.textContent = label; }
      var intro = opts.title && /post/i.test(opts.title)
        ? "Your score goes on the leaderboard under a display name you choose."
        : "Sign in to see where you rank on the leaderboards.";

      // ── account: create ──
      function stepCreate(prefill) {
        card.innerHTML = '<h2 id="blb-title">' + esc(opts.title || "Join the leaderboard") + '</h2>' +
          '<div class="blb-tabs" role="group"><button type="button" aria-pressed="true">Create account</button><button type="button" aria-pressed="false" data-go="in">Sign in</button></div>' +
          '<p>' + intro + ' Create your free Boardside Reviews account. It also unlocks the 80 free board questions.</p>' +
          '<form novalidate><div class="blb-two"><label>First name<input id="blb-f" autocomplete="given-name" maxlength="60"></label>' +
          '<label>Last name<input id="blb-l" autocomplete="family-name" maxlength="60"></label></div>' +
          '<label>Email<input id="blb-e" type="email" autocomplete="email"></label>' +
          '<label>Password<input id="blb-p1" type="password" autocomplete="new-password"></label>' +
          '<label>Confirm password<input id="blb-p2" type="password" autocomplete="new-password"></label>' +
          '<ul class="blb-rules" aria-live="polite"></ul>' +
          '<div class="blb-note"><b>You\'ll be on the launch waitlist.</b> We\'ll email you 48 hours before Boardside Reviews launches and again when it\'s live.</div>' +
          '<label class="blb-check"><input id="blb-o" type="checkbox"><span>Also add me to the Boardside Reviews mailing list for occasional teaching emails and updates. You can unsubscribe anytime.</span></label>' +
          '<div class="blb-err" aria-live="polite"></div>' +
          '<button class="blb-btn teal wide" type="submit">Create free account</button>' +
          '<button class="blb-link" type="button" data-x>Not now</button>' +
          '<p class="blb-fine">We\'ll email a 6-digit code to verify your address. Only your display name is shown publicly.</p></form>';
        card.querySelector("[data-go=in]").onclick = function () { stepSignIn(card.querySelector("#blb-e").value.trim()); };
        var p1 = card.querySelector("#blb-p1"), p2 = card.querySelector("#blb-p2"), list = card.querySelector(".blb-rules");
        function draw() { list.innerHTML = pwRules(p1.value, p2.value).map(function (r) { return '<li class="' + (r.ok ? "ok" : "") + '">' + r.t + '</li>'; }).join(""); }
        p1.oninput = draw; p2.oninput = draw; draw();
        if (prefill) card.querySelector("#blb-e").value = prefill;
        card.querySelector("#blb-f").focus();
        wire(async function (f, er, b) {
          var fn = f.querySelector("#blb-f").value.trim(), ln = f.querySelector("#blb-l").value.trim();
          var em = f.querySelector("#blb-e").value.trim().toLowerCase(), optin = f.querySelector("#blb-o").checked;
          if (!fn || !ln) { er.textContent = "Enter your first and last name."; return; }
          if (!EMAIL_RE.test(em)) { er.textContent = "Enter a valid email address."; return; }
          if (!pwRules(p1.value, p2.value).every(function (r) { return r.ok; })) { er.textContent = "Your password doesn't meet all the rules yet."; return; }
          busy(b, true, "Sending code…");
          var pw = p1.value;
          try { await sendCode(em); }
          catch (x) { er.textContent = authFriendly(x); busy(b, false, "Create free account"); return; }
          email = em;
          stepCode({
            title: "Verify your email", back: function () { stepCreate(em); },
            done: async function () {
              var u = await sb.auth.updateUser({ password: pw, data: profileData(fn, ln, optin) });
              if (u.error) throw u.error;
              stepHeard();
            }
          });
        });
      }

      // ── account: sign in ──
      function stepSignIn(prefill) {
        card.innerHTML = '<h2 id="blb-title">' + esc(opts.title || "Sign in") + '</h2>' +
          '<div class="blb-tabs" role="group"><button type="button" aria-pressed="false" data-go="new">Create account</button><button type="button" aria-pressed="true">Sign in</button></div>' +
          '<p>Sign in with your Boardside Reviews account.</p>' +
          '<form novalidate><label>Email<input id="blb-e" type="email" autocomplete="email"></label>' +
          '<label><span class="blb-lblrow">Password<button class="blb-link" type="button" data-go="code">Forgot password?</button></span><input id="blb-p" type="password" autocomplete="current-password"></label>' +
          '<div class="blb-err" aria-live="polite"></div>' +
          '<button class="blb-btn teal wide" type="submit">Sign in</button>' +
          '<button class="blb-link" type="button" data-go="code">Sign in with an email code instead</button>' +
          '<button class="blb-link" type="button" data-x>Not now</button></form>';
        var ei = card.querySelector("#blb-e"); if (prefill) ei.value = prefill;
        card.querySelector("[data-go=new]").onclick = function () { stepCreate(ei.value.trim()); };
        card.querySelectorAll("[data-go=code]").forEach(function (b) { b.onclick = function () { stepCodeLogin(ei.value.trim()); }; });
        (prefill ? card.querySelector("#blb-p") : ei).focus();
        wire(async function (f, er, b) {
          var em = ei.value.trim().toLowerCase(), pw = f.querySelector("#blb-p").value;
          if (!EMAIL_RE.test(em)) { er.textContent = "Enter a valid email address."; return; }
          if (!pw) { er.textContent = "Enter your password."; return; }
          busy(b, true, "Signing in…");
          var r = await sb.auth.signInWithPassword({ email: em, password: pw });
          if (r.error) { er.textContent = authFriendly(r.error); busy(b, false, "Sign in"); return; }
          email = em; afterSignIn();
        });
      }

      // ── email code (forgot password, older code-only accounts, admin pages) ──
      function stepCodeLogin(prefill) {
        card.innerHTML = '<h2 id="blb-title">' + (admin ? esc(opts.title || "Sign in") : "Sign in with an email code") + '</h2>' +
          '<p>' + (admin ? esc(opts.intro || "We'll email you a 6-digit code.") : "Enter your account email. We'll send a 6-digit code. If you forgot your password, you can set a new one after.") + '</p>' +
          '<form novalidate><label>Email<input id="blb-e" type="email" autocomplete="email"></label>' +
          '<div class="blb-err" aria-live="polite"></div>' +
          '<div class="blb-row"><button class="blb-btn" type="submit">Email me a code</button>' +
          (admin ? '<button class="blb-link" type="button" data-x>Not now</button>' : '<button class="blb-link" type="button" data-go="in">Back to sign in</button>') + '</div></form>';
        var ei = card.querySelector("#blb-e"); if (prefill) ei.value = prefill; ei.focus();
        var g = card.querySelector("[data-go=in]"); if (g) g.onclick = function () { stepSignIn(ei.value.trim()); };
        wire(async function (f, er, b) {
          var em = ei.value.trim().toLowerCase();
          if (!EMAIL_RE.test(em)) { er.textContent = "Enter a valid email address."; return; }
          busy(b, true, "Sending…");
          try {
            var r = await sb.auth.signInWithOtp({ email: em, options: { shouldCreateUser: admin } });
            if (r.error) throw r.error;
          } catch (x) { er.textContent = authFriendly(x); busy(b, false, "Email me a code"); return; }
          email = em;
          stepCode({ title: "Check your email", back: function () { stepCodeLogin(em); }, done: afterSignIn, reset: !admin });
        });
      }

      function stepCode(o) {
        card.innerHTML = '<h2 id="blb-title">' + esc(o.title) + '</h2>' +
          '<p>Enter the 6-digit code sent to <b></b>. It can take a minute; check spam too.</p>' +
          '<form novalidate><label>Code<input id="blb-code" class="blb-code" inputmode="numeric" autocomplete="one-time-code" maxlength="10"></label>' +
          '<div class="blb-err" aria-live="polite"></div><div class="blb-row"><button class="blb-btn" type="submit">Verify</button>' +
          '<button class="blb-link" type="button" data-back>Go back</button></div></form>';
        card.querySelector("p b").textContent = email;
        card.querySelector("[data-back]").onclick = o.back;
        var inp = card.querySelector("#blb-code"); inp.focus();
        wire(async function (f, er, b) {
          var v = inp.value.replace(/\D/g, "");
          if (v.length < 6) { er.textContent = "Enter the full code from the email."; return; }
          busy(b, true, "Checking…");
          try { await verify(email, v); await o.done(); }
          catch (x) { er.textContent = authFriendly(x); busy(b, false, "Verify"); }
        });
      }

      // Signed in. Accounts made before passwords (email-code only) finish setting up first.
      async function afterSignIn() {
        var u = await user();
        var md = (u && u.user_metadata) || {};
        if (!admin && !md.account_ready) return stepFinish(md);
        return stepProfile();
      }
      function stepFinish(md) {
        card.innerHTML = '<h2 id="blb-title">Finish setting up your account</h2>' +
          '<p>You\'re signed in as <b></b>. Add your name and choose a password for next time.</p>' +
          '<form novalidate><div class="blb-two"><label>First name<input id="blb-f" autocomplete="given-name" maxlength="60"></label>' +
          '<label>Last name<input id="blb-l" autocomplete="family-name" maxlength="60"></label></div>' +
          '<label>Password<input id="blb-p1" type="password" autocomplete="new-password"></label>' +
          '<label>Confirm password<input id="blb-p2" type="password" autocomplete="new-password"></label>' +
          '<ul class="blb-rules" aria-live="polite"></ul>' +
          '<div class="blb-note"><b>You\'ll be on the launch waitlist.</b> We\'ll email you 48 hours before Boardside Reviews launches and again when it\'s live.</div>' +
          '<label class="blb-check"><input id="blb-o" type="checkbox"><span>Also add me to the Boardside Reviews mailing list for occasional teaching emails and updates. You can unsubscribe anytime.</span></label>' +
          '<div class="blb-err" aria-live="polite"></div><button class="blb-btn teal wide" type="submit">Finish setting up</button></form>';
        card.querySelector("p b").textContent = email;
        card.querySelector("#blb-f").value = md.first_name || ""; card.querySelector("#blb-l").value = md.last_name || "";
        var p1 = card.querySelector("#blb-p1"), p2 = card.querySelector("#blb-p2"), list = card.querySelector(".blb-rules");
        function draw() { list.innerHTML = pwRules(p1.value, p2.value).map(function (r) { return '<li class="' + (r.ok ? "ok" : "") + '">' + r.t + '</li>'; }).join(""); }
        p1.oninput = draw; p2.oninput = draw; draw();
        card.querySelector("#blb-f").focus();
        wire(async function (f, er, b) {
          var fn = f.querySelector("#blb-f").value.trim(), ln = f.querySelector("#blb-l").value.trim();
          if (!fn || !ln) { er.textContent = "Enter your first and last name."; return; }
          if (!pwRules(p1.value, p2.value).every(function (r) { return r.ok; })) { er.textContent = "Your password doesn't meet all the rules yet."; return; }
          busy(b, true, "Saving…");
          var r = await sb.auth.updateUser({ password: p1.value, data: profileData(fn, ln, f.querySelector("#blb-o").checked) });
          if (r.error) { er.textContent = authFriendly(r.error); busy(b, false, "Finish setting up"); return; }
          stepHeard();
        });
      }
      // One question after a new account: how did you hear about Boardside Reviews? (Skip saves nothing.)
      function stepHeard() {
        card.innerHTML = '<h2 id="blb-title">Your account is ready</h2><p>One quick question: how did you hear about Boardside Reviews?</p>' +
          '<form novalidate><label>Choose one<select id="blb-h"><option value="">Select…</option>' +
          HEARD.map(function (o) { return '<option>' + o + '</option>'; }).join("") + '</select></label>' +
          '<label id="blb-ow" hidden>Where?<input id="blb-other" maxlength="120"></label>' +
          '<div class="blb-err" aria-live="polite"></div><div class="blb-row"><button class="blb-btn teal" type="submit">Continue</button>' +
          '<button class="blb-link" type="button" data-skip>Skip</button></div></form>';
        var sel = card.querySelector("#blb-h"), ow = card.querySelector("#blb-ow");
        sel.onchange = function () { ow.hidden = sel.value !== "Other"; };
        async function save(choice) {
          var data = { heard_asked: true, heard_at: new Date().toISOString() };
          if (choice) { data.heard_from = choice; data.heard_from_other = choice === "Other" ? card.querySelector("#blb-other").value.trim().slice(0, 120) : null; }
          try { await sb.auth.updateUser({ data: data }); } catch (e) {}
          stepProfile();
        }
        card.querySelector("[data-skip]").onclick = function () { save(null); };
        wire(function (f, er) { if (!sel.value) { er.textContent = "Pick one, or tap Skip."; return; } save(sel.value); });
      }

      async function stepProfile() {
        var p = null; try { p = await profile(); } catch (x) {}
        if (p && p.banned) { close(null); alert(MESSAGES.banned); return; }
        if (p && p.display_name && !opts.rename) return close(p.display_name);
        stepName(p && p.display_name);
      }
      function stepName(current) {
        card.innerHTML = '<h2 id="blb-title">' + (current ? "Change your display name" : "Pick a display name") + '</h2>' +
          '<p>This is what appears on the leaderboard. 3 to 20 characters.</p>' +
          '<form novalidate><label>Display name<input id="blb-name" maxlength="20" autocomplete="nickname"></label>' +
          '<div class="blb-err" aria-live="polite"></div><div class="blb-row"><button class="blb-btn" type="submit">Save name</button>' +
          '<button class="blb-link" type="button" data-cancel>Cancel</button></div>' +
          '<p class="blb-fine">Inappropriate names are blocked and can be removed.</p></form>';
        var inp = card.querySelector("#blb-name"); if (current) inp.value = current; inp.focus();
        card.querySelector("[data-cancel]").onclick = function () { close(current || null); };
        wire(async function (f, er, b) {
          busy(b, true, "Saving…");
          try { close(await setName(inp.value)); }
          catch (x) { er.textContent = friendly(x); busy(b, false, "Save name"); }
        });
      }

      (async function () {
        try {
          var u = await user();
          if (u) {
            if (!email) email = u.email || "";
            if (opts.rename) return stepProfile();
            return afterSignIn();
          }
        } catch (x) {}
        if (admin) stepCodeLogin(); else if (opts.start === "signin") stepSignIn(); else stepCreate();
      })();
    });
  }

  // Unhide leaderboard-only elements once the leaderboard is configured.
  function reveal() {
    if (!(cfg.url && cfg.key)) return;
    document.querySelectorAll("[data-lb]").forEach(function (el) { el.hidden = false; });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", reveal); else reveal();

  window.BLB = {
    enabled: enabled, friendly: friendly, user: user, profile: profile,
    sendCode: sendCode, verify: verify, setName: setName, submit: submit,
    board: board, boardPoints: boardPoints, boardTime: boardTime, rpc: rpc, signOut: signOut, dialog: dialog,
    onAuth: function (fn) { if (sb) sb.auth.onAuthStateChange(function () { fn(); }); }
  };
})();
