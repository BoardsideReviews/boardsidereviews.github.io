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
    not_admin: "This page is for the site owner."
  };
  function friendly(err) {
    if (!err) return "";
    var m = err.message || String(err);
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
  async function rpc(name, args) {
    need();
    var r = await sb.rpc(name, args || {});
    if (r.error) throw r.error;
    return r.data;
  }
  async function signOut() { if (sb) await sb.auth.signOut(); }

  // ── Sign-in dialog: email → 6-digit code → display name ──
  var css = '\
.blb-back{position:fixed;inset:0;z-index:1000;background:rgba(8,16,30,.62);display:flex;align-items:center;justify-content:center;padding:16px}\
.blb-card{width:min(420px,100%);background:#fff;color:#0b2545;border-radius:18px;padding:24px;box-shadow:0 24px 60px rgba(0,0,0,.35);font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;display:flex;flex-direction:column;gap:14px;text-align:left}\
.blb-card h2{margin:0;font-family:"Plus Jakarta Sans",Inter,system-ui,sans-serif;font-weight:800;font-size:22px;letter-spacing:-.01em}\
.blb-card p{margin:0;font-size:15px;line-height:22px;color:#52627a}\
.blb-card label{font-size:13px;font-weight:600;color:#33465f;display:flex;flex-direction:column;gap:6px}\
.blb-card input{font:inherit;font-size:16px;padding:12px 14px;border:1px solid #c9d5e2;border-radius:10px;color:#0b2545;background:#fff;width:100%;box-sizing:border-box}\
.blb-card input:focus{outline:2px solid #0d7070;outline-offset:1px;border-color:#0d7070}\
.blb-code{letter-spacing:.4em;font-variant-numeric:tabular-nums;text-align:center;font-size:22px!important}\
.blb-row{display:flex;gap:10px;flex-wrap:wrap;align-items:center}\
.blb-btn{font:inherit;font-weight:600;font-size:15px;border:0;border-radius:10px;padding:12px 18px;cursor:pointer;background:#0b2545;color:#fff}\
.blb-btn:disabled{opacity:.55;cursor:default}\
.blb-link{font:inherit;font-size:14px;background:none;border:0;color:#0d7070;font-weight:600;cursor:pointer;padding:6px 0}\
.blb-err{color:#b9432c;font-size:14px;min-height:0}\
.blb-err:empty{display:none}\
.blb-fine{font-size:12px!important;color:#7a8799!important}';

  function dialog(opts) {
    // opts.title, opts.intro; resolves with display name, or null if closed
    return new Promise(function (resolve) {
      if (!document.getElementById("blb-css")) {
        var st = document.createElement("style"); st.id = "blb-css"; st.textContent = css; document.head.appendChild(st);
      }
      var back = document.createElement("div"); back.className = "blb-back";
      back.innerHTML = '<div class="blb-card" role="dialog" aria-modal="true" aria-labelledby="blb-title"></div>';
      var card = back.firstChild, email = "";
      document.body.appendChild(back);
      function close(v) { back.remove(); document.removeEventListener("keydown", esc); resolve(v); }
      function esc(e) { if (e.key === "Escape") close(null); }
      document.addEventListener("keydown", esc);
      back.addEventListener("mousedown", function (e) { if (e.target === back) close(null); });

      function stepEmail() {
        card.innerHTML = '<h2 id="blb-title">' + (opts.title || "Join the leaderboard") + '</h2>' +
          '<p>' + (opts.intro || "We'll email you a 6-digit code. No password needed.") + '</p>' +
          '<form class="blb-f" novalidate><label>Email<input id="blb-email" type="email" autocomplete="email" required></label>' +
          '<div class="blb-err"></div><div class="blb-row"><button class="blb-btn" type="submit">Email me a code</button>' +
          '<button class="blb-link" type="button" data-x>Not now</button></div>' +
          '<p class="blb-fine">Only your display name is shown publicly. Your email stays private.</p></form>';
        var f = card.querySelector("form"), inp = card.querySelector("#blb-email"), er = card.querySelector(".blb-err");
        card.querySelector("[data-x]").onclick = function () { close(null); };
        inp.focus();
        f.onsubmit = async function (e) {
          e.preventDefault(); er.textContent = "";
          var v = inp.value.trim();
          if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) { er.textContent = "Enter a valid email address."; return; }
          var b = f.querySelector(".blb-btn"); b.disabled = true; b.textContent = "Sending…";
          try { await sendCode(v); email = v; stepCode(); }
          catch (x) { er.textContent = friendly(x); b.disabled = false; b.textContent = "Email me a code"; }
        };
      }
      function stepCode() {
        card.innerHTML = '<h2 id="blb-title">Check your email</h2>' +
          '<p>Enter the 6-digit code sent to <b></b>. It can take a minute; check spam too.</p>' +
          '<form class="blb-f" novalidate><label>Code<input id="blb-code" class="blb-code" inputmode="numeric" autocomplete="one-time-code" maxlength="10"></label>' +
          '<div class="blb-err"></div><div class="blb-row"><button class="blb-btn" type="submit">Verify</button>' +
          '<button class="blb-link" type="button" data-back>Use a different email</button></div></form>';
        card.querySelector("p b").textContent = email;
        var f = card.querySelector("form"), inp = card.querySelector("#blb-code"), er = card.querySelector(".blb-err");
        card.querySelector("[data-back]").onclick = stepEmail;
        inp.focus();
        f.onsubmit = async function (e) {
          e.preventDefault(); er.textContent = "";
          var v = inp.value.replace(/\D/g, "");
          if (v.length < 6) { er.textContent = "Enter the full code from the email."; return; }
          var b = f.querySelector(".blb-btn"); b.disabled = true; b.textContent = "Checking…";
          try {
            await verify(email, v);
            var p = await profile();
            if (p && p.banned) { er.textContent = MESSAGES.banned; b.disabled = false; b.textContent = "Verify"; return; }
            if (p && p.display_name && !opts.rename) close(p.display_name); else stepName(p && p.display_name);
          } catch (x) { er.textContent = friendly(x); b.disabled = false; b.textContent = "Verify"; }
        };
      }
      function stepName(current) {
        card.innerHTML = '<h2 id="blb-title">' + (current ? "Change your display name" : "Pick a display name") + '</h2>' +
          '<p>This is what appears on the leaderboard. 3 to 20 characters.</p>' +
          '<form class="blb-f" novalidate><label>Display name<input id="blb-name" maxlength="20" autocomplete="nickname"></label>' +
          '<div class="blb-err"></div><div class="blb-row"><button class="blb-btn" type="submit">Save name</button>' +
          '<button class="blb-link" type="button" data-x>Cancel</button></div>' +
          '<p class="blb-fine">Inappropriate names are blocked and can be removed.</p></form>';
        var f = card.querySelector("form"), inp = card.querySelector("#blb-name"), er = card.querySelector(".blb-err");
        if (current) inp.value = current;
        card.querySelector("[data-x]").onclick = function () { close(current || null); };
        inp.focus();
        f.onsubmit = async function (e) {
          e.preventDefault(); er.textContent = "";
          var b = f.querySelector(".blb-btn"); b.disabled = true; b.textContent = "Saving…";
          try { close(await setName(inp.value)); }
          catch (x) { er.textContent = friendly(x); b.disabled = false; b.textContent = "Save name"; }
        };
      }

      (async function () {
        try {
          var p = await profile();
          if (p && p.banned) { stepEmail(); card.querySelector(".blb-err").textContent = MESSAGES.banned; return; }
          if (p && opts.rename) return stepName(p.display_name);
          if (p && p.display_name) return close(p.display_name);
          if (p) return stepName(null);
        } catch (x) {}
        stepEmail();
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
    board: board, boardPoints: boardPoints, rpc: rpc, signOut: signOut, dialog: dialog,
    onAuth: function (fn) { if (sb) sb.auth.onAuthStateChange(function () { fn(); }); }
  };
})();
