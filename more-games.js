// Boardside Reviews: "Try another game?" strip for the end/leaderboard screens.
// Shows 3 other Gamified Learning games, picked at random, each as a themed thumbnail.
//   BoardsideMore.mount(containerEl, 'abg-blitz')  → appends a fresh random strip
//   BoardsideMore.html('night-float', roundKey)     → HTML string (same picks while roundKey is unchanged)
(function () {
  var GAMES = [
    { id: 'night-float', name: 'IM Night Float', tag: 'Overnight cross-cover simulator', href: 'night-float.html',
      bg: '#1b1e25', fg: '#f0b54a', art:
      '<div class="bmg-lcd"><span>19:15 · PAGE 1 OF 8</span><b>4B-12: K 6.9. PLS CALL<i>_</i></b></div>' },
    { id: 'abg-blitz', name: 'ABG Blitz', tag: '3-minute acid–base challenge', href: 'abg-blitz.html',
      bg: '#0c1630', fg: '#2ec4b6', art:
      '<div class="bmg-abg"><b>pH 7.24</b><span>PaCO₂ 39 · HCO₃⁻ 16</span></div>' },
    { id: 'hemo-roulette', name: 'Hemodynamic Roulette', tag: '60-second shock challenge', href: 'hemodynamic-roulette.html',
      bg: '#050b1a', fg: '#ff6b78', art:
      '<svg viewBox="0 0 120 50" width="100%" height="56" fill="none" stroke="#ff6b78" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 38h16l7-28 10 36 7-20h12l7-10 7 22h12l7-28 10 36 6-14h17"/></svg>' },
    { id: 'bug-drug', name: "Don't Shrug the Bug", tag: 'Match the bug to the drug', href: 'bug-drug.html',
      bg: 'linear-gradient(135deg,#E6DEFF,#FDE1EC)', fg: '#5C2EC4', light: true, art:
      '<svg viewBox="0 0 30 30" width="64" height="64" aria-hidden="true"><circle cx="15" cy="15" r="13" fill="#F3EEE2" stroke="#3a4a45" stroke-width="2"/><circle cx="15" cy="15" r="7" fill="#fff" stroke="#1F9D63" stroke-width="1" stroke-dasharray="2 2"/><circle cx="15" cy="15" r="2.2" fill="#fff" stroke="#8a8272"/><circle cx="7" cy="10" r="1.6" fill="#5C2EC4"/><circle cx="9" cy="8.2" r="1.6" fill="#5C2EC4"/><rect x="20" y="19" width="5" height="2.2" rx="1.1" fill="#E64078" transform="rotate(-30 22 20)"/><rect x="6" y="20" width="5" height="2.2" rx="1.1" fill="#E64078" transform="rotate(20 8 21)"/><circle cx="22" cy="8" r="1.5" fill="#5C2EC4"/></svg>' },
    { id: 'titrate-tonight', name: 'Titrate Tonight', tag: 'Sleep apnea CPAP night shift', href: 'titrate-tonight.html',
      bg: 'linear-gradient(180deg,#0c1033,#1d2a6b)', fg: '#5ef2e6', art:
      '<svg viewBox="0 0 26 26" width="64" height="64" aria-hidden="true"><circle cx="11" cy="11" r="7" fill="#fff4c9"/><circle cx="14.5" cy="8.5" r="6.2" fill="#121845"/><path d="M2 21q3-4 6 0t6 0 6 0 4-2" fill="none" stroke="#5ef2e6" stroke-width="1.6" stroke-linecap="round"/><text x="17" y="9" font-family="sans-serif" font-weight="700" font-size="6" fill="#cfd6ff">z</text></svg>' },
    { id: 'vent-lab', name: 'Vent Lab', tag: '1-minute asynchrony challenge', href: 'vent-lab.html#game',
      bg: '#05090f', fg: '#3fe0d0', art:
      '<svg viewBox="0 0 30 20" width="96" height="56" fill="none" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 14h4v-9h7v9h3" stroke="#ffc94a" stroke-width="1.6"/><path d="M16 14h2l1.5-9 2 9h6.5" stroke="#3fe0d0" stroke-width="1.6"/></svg>' }
  ];
  // Pages name some games differently from their leaderboard ids.
  var ALIAS = { 'hemodynamic-roulette': 'hemo-roulette', 'shrug-the-bug': 'bug-drug' };

  var css = '\
.bmg{margin:22px auto 4px;width:100%;max-width:720px;text-align:center;box-sizing:border-box}\
.bmg h3{margin:0 0 12px;font:800 20px/1.2 "Plus Jakarta Sans",Inter,system-ui,sans-serif;letter-spacing:-.01em;color:inherit}\
.bmg-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}\
.bmg a.bmg-t{display:flex;flex-direction:column;border-radius:14px;overflow:hidden;text-decoration:none;text-align:left;box-shadow:0 6px 18px rgba(0,0,0,.25);transition:transform .15s ease,box-shadow .15s ease;outline-offset:3px}\
.bmg a.bmg-t:hover,.bmg a.bmg-t:focus-visible{transform:translateY(-3px);box-shadow:0 12px 26px rgba(0,0,0,.32)}\
.bmg-art{height:96px;display:flex;align-items:center;justify-content:center;padding:10px;box-sizing:border-box}\
.bmg-cap{padding:10px 12px 12px;display:flex;flex-direction:column;gap:3px;background:rgba(0,0,0,.28);flex:1}\
.bmg-t.light .bmg-cap{background:rgba(255,255,255,.55)}\
.bmg-cap b{font:700 15px/1.25 "Plus Jakarta Sans",Inter,system-ui,sans-serif}\
.bmg-cap small{font:400 12.5px/1.35 Inter,system-ui,sans-serif;opacity:.8;color:#fff}\
.bmg-t.light .bmg-cap small{color:#33465f}\
.bmg-lcd{width:100%;background:#1a1608;border:1px solid #f0b54a55;border-radius:8px;padding:8px 10px;font:600 11px/1.4 ui-monospace,"SF Mono",Menlo,Consolas,monospace;color:#f0b54a;display:flex;flex-direction:column;gap:3px}\
.bmg-lcd span{opacity:.6;font-size:10px}\
.bmg-lcd i{font-style:normal;animation:bmgBlink 1s steps(1) infinite}\
.bmg-abg{display:flex;flex-direction:column;align-items:center;gap:4px;font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace}\
.bmg-abg b{font-size:28px;color:#2ec4b6;border-bottom:3px solid #f0b54a;padding-bottom:2px}\
.bmg-abg span{font-size:11px;color:#cfe3ff;opacity:.75}\
@keyframes bmgBlink{50%{opacity:0}}\
@media (max-width:560px){.bmg-grid{grid-template-columns:1fr}.bmg a.bmg-t{flex-direction:row}.bmg-art{width:112px;height:auto;min-height:76px;flex:0 0 112px}.bmg-lcd{font-size:9px;padding:6px}.bmg-lcd span{display:none}.bmg-abg b{font-size:20px}.bmg-abg span{display:none}.bmg-art svg{max-width:80px;max-height:48px}.bmg-cap{justify-content:center}}\
@media (prefers-reduced-motion:reduce){.bmg a.bmg-t{transition:none}.bmg-lcd i{animation:none}}';

  function injectCss() {
    if (document.getElementById('bmg-css')) return;
    var st = document.createElement('style'); st.id = 'bmg-css'; st.textContent = css; document.head.appendChild(st);
  }
  function pick(current) {
    var cur = ALIAS[current] || current;
    var pool = GAMES.filter(function (g) { return g.id !== cur; });
    for (var i = pool.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = pool[i]; pool[i] = pool[j]; pool[j] = t; }
    return pool.slice(0, 3);
  }
  function build(games) {
    return '<section class="bmg" aria-label="Try another game"><h3>Try another game?</h3><div class="bmg-grid">' +
      games.map(function (g) {
        return '<a class="bmg-t' + (g.light ? ' light' : '') + '" href="' + g.href + '" style="background:' + g.bg + '">' +
          '<div class="bmg-art">' + g.art + '</div>' +
          '<div class="bmg-cap"><b style="color:' + g.fg + '">' + g.name + '</b><small>' + g.tag + '</small></div></a>';
      }).join('') + '</div></section>';
  }

  var lastKey, lastHtml;
  window.BoardsideMore = {
    html: function (current, key) {
      injectCss();
      if (key !== undefined && key === lastKey && lastHtml) return lastHtml;
      lastKey = key; lastHtml = build(pick(current));
      return lastHtml;
    },
    mount: function (el, current) {
      if (!el) return;
      injectCss();
      var old = el.querySelector(':scope > .bmg'); if (old) old.remove();
      var wrap = document.createElement('div'); wrap.innerHTML = build(pick(current));
      el.appendChild(wrap.firstChild);
    }
  };
})();
