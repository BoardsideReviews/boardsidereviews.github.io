// Boardside Reviews game gate.
// Every game is free, but playing needs a free Boardside Reviews account.
// Load this right after lb-config.js, the supabase-js UMD build and lb.js:
//   <script src="game-gate.js"></script>
// A visitor who is signed out (or who never finished setting up their account) gets a
// create-account / sign-in card over the page and can't use what is behind it. After they
// sign in the page reloads so the game starts clean, already signed in.
// Optional wording on the <script> tag: data-eyebrow, data-title, data-text, data-intro,
// data-back (link) and data-back-label.
(function () {
  var script = document.currentScript || {};
  var ds = script.dataset || {};
  var cfg = window.BOARDSIDE_LB || {};
  var BLB = window.BLB;
  // No sign-in client (settings missing, or the Supabase library didn't load): nobody could
  // sign in, so leave the page open rather than lock everyone out.
  if (!BLB || !BLB.enabled) return;

  var T = {
    eyebrow: ds.eyebrow || "FREE TO PLAY",
    title: ds.title || "Create a free account to play",
    text: ds.text || "Every Boardside Reviews game is free. A free account lets you play, post your scores to the leaderboards, and unlocks 80 free board questions.",
    intro: ds.intro || "Every game here is free to play once you're signed in.",
    back: ds.back || "games.html",
    backLabel: ds.backLabel || "All games"
  };

  // supabase-js keeps the session in localStorage under this key. Checking it is instant,
  // so a signed-out visitor never sees the game flash before the gate.
  var ref = ""; try { ref = new URL(cfg.url).hostname.split(".")[0]; } catch (e) {}
  var TOKEN_KEY = "sb-" + ref + "-auth-token";
  function hasToken() { try { return !!window.localStorage.getItem(TOKEN_KEY); } catch (e) { return false; } }
  function ready(u) { return !!(u && u.user_metadata && u.user_metadata.account_ready); }
  function track(name) { try { if (typeof window.gtag === "function") window.gtag("event", name, { page_path: location.pathname }); } catch (e) {} }

  var G = "html.bsr-gated .bsr-gate";
  var css =
    'html.bsr-gated{overflow:hidden!important}' +
    'html.bsr-gated::before{content:"";position:fixed;top:0;right:0;bottom:0;left:0;z-index:989;background:rgba(8,16,30,.78);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}' +
    'html.bsr-gated body>*:not(.bsr-gate):not(.blb-back){pointer-events:none!important;-webkit-user-select:none!important;user-select:none!important}' +
    G + ' *:not(svg):not(circle):not(path){all:revert}' +
    G + '{position:fixed;top:0;right:0;bottom:0;left:0;z-index:990;display:flex;align-items:flex-start;justify-content:center;padding:24px 16px;overflow-y:auto;box-sizing:border-box;font-family:Inter,system-ui,-apple-system,"Segoe UI",sans-serif;-webkit-text-size-adjust:100%;text-align:center}' +
    G + '.bsr-behind{visibility:hidden}' +
    G + ' .bsr-card{color-scheme:light;box-sizing:border-box;width:100%;max-width:440px;margin:auto 0;background:#fff;color:#0b2545;border-radius:18px;padding:28px 24px 20px;box-shadow:0 24px 60px rgba(0,0,0,.35);display:flex;flex-direction:column;align-items:center;gap:12px}' +
    G + ' .bsr-mark{display:block;width:52px;height:52px}' +
    G + ' .bsr-eyebrow{display:block;font-size:12px;font-weight:700;letter-spacing:.12em;color:#0d7070}' +
    G + ' .bsr-title{display:block;margin:0;font-family:"Plus Jakarta Sans",Inter,system-ui,sans-serif;font-weight:800;font-size:24px;line-height:30px;letter-spacing:-.01em;color:#0b2545}' +
    G + ' .bsr-text{display:block;margin:0;font-size:15px;line-height:22px;color:#52627a}' +
    G + ' .bsr-acts{display:flex;flex-direction:column;gap:10px;width:100%;margin-top:6px}' +
    G + ' .bsr-btn{display:block;box-sizing:border-box;width:100%;font-family:inherit;font-weight:600;font-size:16px;line-height:22px;border:1.5px solid #0d7070;border-radius:10px;padding:12px 18px;cursor:pointer;background:#0d7070;color:#fff;text-align:center}' +
    G + ' .bsr-btn.ghost{background:#fff;color:#0b2545;border-color:#c9d5e2}' +
    G + ' .bsr-btn:focus-visible,' + G + ' .bsr-link:focus-visible{outline:2px solid #0d7070;outline-offset:2px}' +
    G + ' .bsr-link{display:inline-block;font-family:inherit;font-size:14px;font-weight:600;color:#0d7070;background:none;border:0;padding:6px 4px;cursor:pointer;text-decoration:none}' +
    G + ' .bsr-foot{display:flex;flex-wrap:wrap;justify-content:center;gap:4px 16px}' +
    '@media (max-width:420px){' + G + ' .bsr-card{padding:24px 20px 16px}' + G + ' .bsr-title{font-size:22px;line-height:28px}}';
  var st = document.createElement("style"); st.id = "bsr-gate-css"; st.textContent = css;
  (document.head || document.documentElement).appendChild(st);

  var MARK = '<svg class="bsr-mark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" aria-hidden="true">' +
    '<circle cx="50" cy="50" r="42" style="fill:#fff;stroke:#0B2545;stroke-width:7"/>' +
    '<path style="fill:#0B2545" d="M35.326,27.0 H51.38 A11.5,11.5 0 0 1 51.38,50 H43.008 V73.0 H35.326 Q34.59,73.0 34.59,72.264 V27.736 Q34.59,27.0 35.326,27.0 Z"/>' +
    '<path style="fill:#0D7070" d="M43.008,50 H53.91 A11.5,11.5 0 0 1 53.91,73.0 H43.008 Z"/></svg>';

  var root = document.documentElement;
  var gate = null, gated = false, mode = "", busy = false, inerted = [], watcher = null;

  // Everything on the page except the gate and the sign-in dialog is made inert while gated,
  // including anything a game adds later (score pops, intro screens).
  function inertAll() {
    Array.prototype.forEach.call(document.body.children, function (c) {
      if (c === gate || c.classList.contains("blb-back") || c.inert) return;
      if (c.tagName === "SCRIPT" || c.tagName === "STYLE") return;
      c.inert = true; inerted.push(c);
    });
  }

  // While the gate is up, keys must not reach the game behind it (crossword letters, shortcuts).
  // Typing in the sign-in form still works: this only stops the game's own key handlers.
  function keyBlock(e) {
    if (!gated) return;
    if (e.key === "Escape" && document.querySelector(".blb-back")) return;   // let the sign-in dialog close
    e.stopPropagation();
  }
  ["keydown", "keyup", "keypress"].forEach(function (t) { window.addEventListener(t, keyBlock, true); });

  function el(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; }

  function draw() {
    if (!gated || !document.body) return;
    if (!gate) {
      gate = el("div", "bsr-gate");
      gate.setAttribute("role", "dialog"); gate.setAttribute("aria-modal", "true"); gate.setAttribute("aria-labelledby", "bsr-gate-title");
      document.body.appendChild(gate);
      inertAll();
      if (!watcher && window.MutationObserver) {
        watcher = new MutationObserver(function () { if (gated) inertAll(); });
        watcher.observe(document.body, { childList: true });
      }
    }
    gate.textContent = "";
    var card = el("div", "bsr-card"), acts = el("div", "bsr-acts"), foot = el("div", "bsr-foot");
    var logo = el("div"); logo.innerHTML = MARK;
    var title = el("h2", "bsr-title"); title.id = "bsr-gate-title";
    card.appendChild(logo.firstChild);
    var first;
    if (mode === "finish") {
      card.appendChild(el("span", "bsr-eyebrow", "ALMOST THERE"));
      title.textContent = "Finish setting up your account";
      card.appendChild(title);
      card.appendChild(el("p", "bsr-text", "You're signed in, but your free account isn't finished. Add your name and a password to keep playing."));
      first = el("button", "bsr-btn", "Finish setting up"); first.type = "button"; first.onclick = function () { open(); };
      acts.appendChild(first);
      var other = el("button", "bsr-link", "Use a different account"); other.type = "button";
      other.onclick = async function () { try { await BLB.signOut(); } catch (e) {} check(); };
      foot.appendChild(other);
    } else {
      card.appendChild(el("span", "bsr-eyebrow", T.eyebrow));
      title.textContent = T.title;
      card.appendChild(title);
      card.appendChild(el("p", "bsr-text", T.text));
      first = el("button", "bsr-btn", "Create free account"); first.type = "button"; first.onclick = function () { open(); };
      var signin = el("button", "bsr-btn ghost", "Sign in"); signin.type = "button"; signin.onclick = function () { open("signin"); };
      acts.appendChild(first); acts.appendChild(signin);
    }
    var back = el("a", "bsr-link", T.backLabel); back.href = T.back;
    foot.appendChild(back);
    card.appendChild(acts); card.appendChild(foot);
    gate.appendChild(card);
    if (!busy) { try { first.focus({ preventScroll: true }); } catch (e) {} }
  }

  function lock(m) {
    mode = m;
    if (!gated) { gated = true; root.classList.add("bsr-gated"); track("game_gate_shown"); }
    if (document.body) draw(); else document.addEventListener("DOMContentLoaded", draw);
  }

  function unlock() {
    if (!gated) return;
    track("game_gate_passed");
    // The page loaded signed out. Reload so the game and its leaderboard start clean, signed in.
    // (If this browser can't keep the session, a reload would only show the gate again.)
    if (hasToken()) { location.reload(); return; }
    gated = false; root.classList.remove("bsr-gated");
    if (watcher) { watcher.disconnect(); watcher = null; }
    inerted.forEach(function (c) { c.inert = false; }); inerted = [];
    if (gate) { gate.remove(); gate = null; }
  }

  async function check() {
    if (busy) return;                       // mid sign-up: wait for the dialog to finish
    var u = null; try { u = await BLB.user(); } catch (e) {}
    if (busy) return;
    if (ready(u)) unlock(); else lock(u ? "finish" : "out");
  }

  async function open(start) {
    if (busy || !gate) return;
    busy = true; gate.classList.add("bsr-behind");
    try {
      await BLB.dialog({ createTitle: "Create your free account", signInTitle: "Sign in to play", playIntro: T.intro, start: start });
    } catch (e) {}
    busy = false; if (gate) gate.classList.remove("bsr-behind");
    check();
  }

  if (!hasToken()) lock("out");
  check();
  BLB.onAuth(function () { setTimeout(check, 0); });
  window.addEventListener("pageshow", function (e) { if (e.persisted) check(); });
})();
