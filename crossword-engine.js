// Boardside Reviews · Cross-Cover puzzle engine
// Builds one 6x6 medical crossword per calendar date. The same date always gives the
// same puzzle on every device (own seeded random generator; no Math.random, no
// engine-dependent sorting), and each date gets its own grid shape and fill.
// Day to day, the site reads pre-built puzzles from crossword-data/YYYY.json
// (made by tools/crossword-build.js, which also guarantees no repeats); this live
// generator is the backup if a day isn't in those files.
//
//   BoardsideXword.generate("2026-11-10", window.BOARDSIDE_XWORD_WORDS)
//   BoardsideXword.todayLA()           -> "YYYY-MM-DD" in California (America/Los_Angeles)
//   BoardsideXword.msUntilNextLA()     -> milliseconds until the next California midnight
(function (root) {
  'use strict';
  var N = 6, CELLS = N * N;
  var SALT = 'boardside-cross-cover-v1';

  // ── Seeded randomness ───────────────────────────────────────────────
  function hash4(str) { // cyrb128 → four 32-bit seeds
    var h1 = 1779033703, h2 = 3144134277, h3 = 1013904242, h4 = 2773480762;
    for (var i = 0, k; i < str.length; i++) {
      k = str.charCodeAt(i);
      h1 = h2 ^ Math.imul(h1 ^ k, 597399067);
      h2 = h3 ^ Math.imul(h2 ^ k, 2869860233);
      h3 = h4 ^ Math.imul(h3 ^ k, 951274213);
      h4 = h1 ^ Math.imul(h4 ^ k, 2716044179);
    }
    h1 = Math.imul(h3 ^ (h1 >>> 18), 597399067);
    h2 = Math.imul(h4 ^ (h2 >>> 22), 2869860233);
    h3 = Math.imul(h1 ^ (h3 >>> 17), 951274213);
    h4 = Math.imul(h2 ^ (h4 >>> 19), 2716044179);
    h1 ^= (h2 ^ h3 ^ h4); h2 ^= h1; h3 ^= h1; h4 ^= h1;
    return [h1 >>> 0, h2 >>> 0, h3 >>> 0, h4 >>> 0];
  }
  function sfc32(s) {
    var a = s[0], b = s[1], c = s[2], d = s[3];
    function next() {
      a >>>= 0; b >>>= 0; c >>>= 0; d >>>= 0;
      var t = (a + b) | 0;
      a = b ^ (b >>> 9); b = (c + (c << 3)) | 0;
      c = (c << 21) | (c >>> 11); d = (d + 1) | 0;
      t = (t + d) | 0; c = (c + t) | 0;
      return (t >>> 0) / 4294967296;
    }
    for (var i = 0; i < 15; i++) next();
    return next;
  }
  function shuffle(arr, rnd) {
    for (var i = arr.length - 1; i > 0; i--) {
      var j = Math.floor(rnd() * (i + 1)), t = arr[i]; arr[i] = arr[j]; arr[j] = t;
    }
    return arr;
  }

  // ── Dates (California time) ─────────────────────────────────────────
  function dayNum(ds) { var p = ds.split('-'); return Math.round(Date.UTC(+p[0], +p[1] - 1, +p[2]) / 864e5); }
  function fromDayNum(n) { var d = new Date(n * 864e5); return d.toISOString().slice(0, 10); }
  function laParts(t) {
    var f = new Intl.DateTimeFormat('en-US', { timeZone: 'America/Los_Angeles', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hourCycle: 'h23' });
    var o = {}; f.formatToParts(new Date(t)).forEach(function (p) { o[p.type] = p.value; });
    return o;
  }
  function todayLA(t) { var o = laParts(t == null ? Date.now() : t); return o.year + '-' + o.month + '-' + o.day; }
  function msUntilNextLA(t) {
    t = t == null ? Date.now() : t;
    var o = laParts(t), today = o.year + '-' + o.month + '-' + o.day;
    var secs = (+o.hour) * 3600 + (+o.minute) * 60 + (+o.second);
    var guess = t + (86400 - secs) * 1000 - (t % 1000);
    // Handle daylight-saving days (23- or 25-hour days): step until the date flips.
    for (var k = 0; k < 4 && todayLA(guess) === today; k++) guess += 3600e3;
    for (var j = 0; j < 4 && todayLA(guess - 3600e3) !== today; j++) guess -= 3600e3;
    return Math.max(1000, guess - t);
  }

  // ── Word bank ──────────────────────────────────────────────────────
  var bankCache = {};
  function parseBank(text) {
    if (bankCache.text === text) return bankCache.rows;
    var rows = [], from = -1e9;
    text.split(/\r?\n/).forEach(function (line) {
      line = line.trim();
      if (!line || line.charAt(0) === '#') return;
      if (line.charAt(0) === '@') { from = dayNum(line.slice(1).trim()); return; }
      var parts = line.split('|');
      var w = (parts[0] || '').trim().toUpperCase();
      var clue = (parts[1] || '').trim();
      if (!/^[A-Z]{3,6}$/.test(w) || !clue) return;
      var retire = 1e9;
      for (var i = 2; i < parts.length; i++) {
        var m = /^retire=(\d{4}-\d{2}-\d{2})$/.exec(parts[i].trim());
        if (m) retire = dayNum(m[1]);
      }
      rows.push({ w: w, clue: clue, from: from, retire: retire, abbr: /\(abbr\.\)/i.test(clue) });
    });
    // First line wins if a word is accidentally listed twice.
    var seen = {}, out = [];
    rows.forEach(function (r) { if (!seen[r.w]) { seen[r.w] = 1; out.push(r); } });
    bankCache = { text: text, rows: out };
    return out;
  }
  function wordsFor(text, ds) {
    var n = dayNum(ds);
    return parseBank(text).filter(function (r) { return r.from <= n && n < r.retire; });
  }

  // ── Grid shapes ────────────────────────────────────────────────────
  // Black squares are placed with 180° rotational symmetry. Rules:
  //  • no 2-letter runs; every answer is 3+ letters
  //  • every white square belongs to at least one answer
  //  • a white square that belongs to only one answer ("unchecked") is allowed, but
  //    capped (a fully interlocked 6x6 can't be filled with medical terms alone)
  //  • all white squares connect
  function runsOf(black) {
    var slots = [];
    for (var dir = 0; dir < 2; dir++) {
      for (var a = 0; a < N; a++) {
        var b = 0;
        while (b < N) {
          var idx = dir === 0 ? a * N + b : b * N + a;
          if (black[idx]) { b++; continue; }
          var cells = [];
          while (b < N) {
            var id2 = dir === 0 ? a * N + b : b * N + a;
            if (black[id2]) break;
            cells.push(id2); b++;
          }
          slots.push({ dir: dir, cells: cells });
        }
      }
    }
    return slots;
  }
  var CFG = { minWhite: 22, maxWhite: 30, maxUnchecked: 6, candidates: 6, maxAttempts: 6000, subset: 0.6, nodeLimit: 2500 };
  var LIMIT = { unchecked: 6, subset: 0.6 };
  function validShape(black) {
    var runs = runsOf(black), cover = new Uint8Array(CELLS), slots = [];
    for (var i = 0; i < runs.length; i++) {
      var r = runs[i];
      if (r.cells.length === 2) return null;
      if (r.cells.length < 3) continue;
      slots.push(r);
      for (var j = 0; j < r.cells.length; j++) cover[r.cells[j]]++;
    }
    var whites = 0, unchecked = 0, first = -1;
    for (var c = 0; c < CELLS; c++) {
      if (black[c]) continue;
      whites++; if (first < 0) first = c;
      if (!cover[c]) return null;
      if (cover[c] === 1) unchecked++;
    }
    if (whites < CFG.minWhite || whites > CFG.maxWhite || unchecked > LIMIT.unchecked) return null;
    var seen = new Uint8Array(CELLS), stack = [first], count = 0; seen[first] = 1;
    while (stack.length) {
      var x = stack.pop(); count++;
      var rr = Math.floor(x / N), cc = x % N;
      var nb = [rr > 0 ? x - N : -1, rr < N - 1 ? x + N : -1, cc > 0 ? x - 1 : -1, cc < N - 1 ? x + 1 : -1];
      for (var k = 0; k < 4; k++) { var y = nb[k]; if (y >= 0 && !black[y] && !seen[y]) { seen[y] = 1; stack.push(y); } }
    }
    if (count !== whites) return null;
    slots.whites = whites; slots.unchecked = unchecked;
    return slots;
  }
  function randomShape(rnd) {
    var black = new Uint8Array(CELLS);
    var pairs = 3 + Math.floor(rnd() * 4); // 6–12 black squares
    var half = []; for (var i = 0; i < CELLS / 2; i++) half.push(i);
    shuffle(half, rnd);
    for (var p = 0; p < pairs; p++) { black[half[p]] = 1; black[CELLS - 1 - half[p]] = 1; }
    return black;
  }

  // ── Fill (backtracking with bitset candidate filtering) ────────────
  function popcount(x) { x -= (x >>> 1) & 0x55555555; x = (x & 0x33333333) + ((x >>> 2) & 0x33333333); return (((x + (x >>> 4)) & 0x0F0F0F0F) * 0x01010101) >>> 24; }

  function buildIndex(words, rnd) {
    var byLen = {};
    for (var L = 3; L <= N; L++) {
      var list = words.filter(function (r) { return r.w.length === L; });
      shuffle(list, rnd);
      var nW = Math.ceil(list.length / 32) || 1;
      var pos = [];
      for (var p = 0; p < L; p++) {
        var letters = [];
        for (var ch = 0; ch < 26; ch++) letters.push(new Uint32Array(nW));
        pos.push(letters);
      }
      var all = new Uint32Array(nW);
      list.forEach(function (r, i) {
        all[i >>> 5] |= (1 << (i & 31));
        for (var p2 = 0; p2 < L; p2++) pos[p2][r.w.charCodeAt(p2) - 65][i >>> 5] |= (1 << (i & 31));
      });
      byLen[L] = { list: list, pos: pos, all: all, nW: nW };
    }
    return byLen;
  }

  function solve(slots, index, nodeLimit) {
    var grid = new Int8Array(CELLS).fill(-1), assigned = new Array(slots.length), used = {};
    var nodes = 0;
    function cand(s) {
      var ix = index[s.cells.length], out = new Uint32Array(ix.all);
      for (var p = 0; p < s.cells.length; p++) {
        var g = grid[s.cells[p]];
        if (g >= 0) { var m = ix.pos[p][g]; for (var k = 0; k < ix.nW; k++) out[k] &= m[k]; }
      }
      return out;
    }
    function rec() {
      if (++nodes > nodeLimit) return false;
      var best = -1, bestSet = null, bestCnt = 1e9;
      for (var i = 0; i < slots.length; i++) {
        if (assigned[i]) continue;
        var set = cand(slots[i]), cnt = 0;
        for (var k = 0; k < set.length; k++) cnt += popcount(set[k]);
        if (cnt === 0) return false;
        if (cnt < bestCnt) { bestCnt = cnt; best = i; bestSet = set; }
      }
      if (best < 0) return true;
      var s = slots[best], list = index[s.cells.length].list;
      for (var w = 0; w < bestSet.length; w++) {
        var bits = bestSet[w];
        while (bits) {
          var low = bits & -bits, bitIdx = 31 - Math.clz32(low);
          bits ^= low;
          var r = list[w * 32 + bitIdx];
          if (used[r.w]) continue;
          var changed = [];
          for (var p = 0; p < s.cells.length; p++) {
            var c = s.cells[p];
            if (grid[c] < 0) { grid[c] = r.w.charCodeAt(p) - 65; changed.push(c); }
          }
          used[r.w] = 1; assigned[best] = r;
          if (rec()) return true;
          used[r.w] = 0; assigned[best] = undefined;
          for (var q = 0; q < changed.length; q++) grid[changed[q]] = -1;
          if (nodes > nodeLimit) return false;
        }
      }
      return false;
    }
    return rec() ? assigned : null;
  }

  // ── Puzzle assembly ────────────────────────────────────────────────
  // Each day, build several valid candidates and keep the best one, so every
  // puzzle is as interlocked, roomy, and plain-English as the bank allows.
  function quality(slots, fill) {
    var abbr = 0, short = 0, long = 0;
    fill.forEach(function (r) { if (r.abbr) abbr++; if (r.w.length === 3) short++; if (r.w.length >= 5) long++; });
    var checked = slots.whites - slots.unchecked;
    return 3 * checked + slots.whites - 4 * slots.unchecked - 3 * abbr - short + 2 * long;
  }
  // opts.exclude: { WORD: 1 } answers not allowed today (builder uses recent days' answers)
  // opts.reject(rowsKey): return true to refuse a finished grid (builder refuses repeats)
  function generate(ds, bankText, opts) {
    opts = opts || {};
    if (!/^\d{4}-\d{2}-\d{2}$/.test(ds)) throw new Error('Date must be YYYY-MM-DD');
    var all = wordsFor(bankText, ds);
    // Safety net: if a day can't be built under the strict rules, loosen them one notch
    // at a time (more unchecked squares allowed, more of the bank in play). In testing
    // the strict tier always succeeds; the later tiers only exist so a day never fails.
    var tiers = [[CFG.maxUnchecked, CFG.subset], [CFG.maxUnchecked + 2, 0.8], [CFG.maxUnchecked + 4, 1]];
    for (var t = 0; t < tiers.length; t++) {
      LIMIT.unchecked = tiers[t][0]; LIMIT.subset = tiers[t][1];
      var out = tryBuild(ds, all, t, opts);
      if (out) return out;
    }
    throw new Error('Could not build a puzzle for ' + ds);
  }
  function tryBuild(ds, all, tier, opts) {
    var tag = tier ? '|t' + tier : '';
    // Each day draws its own random share of the bank, so no two days lean on the same words.
    var pick = sfc32(hash4(SALT + '|subset|' + ds + tag));
    var words = all.filter(function (r) { return pick() < LIMIT.subset && !(opts.exclude && opts.exclude[r.w]); });
    var best = null, found = 0;
    for (var attempt = 0; attempt < CFG.maxAttempts && found < CFG.candidates; attempt++) {
      var rnd = sfc32(hash4(SALT + '|' + ds + tag + '|' + attempt));
      var black = randomShape(rnd);
      var slots = validShape(black);
      if (!slots) continue;
      var index = buildIndex(words, rnd);
      var fill = solve(slots, index, CFG.nodeLimit);
      if (!fill) continue;
      if (opts.reject && opts.reject(gridKey(black, slots, fill))) continue;
      found++;
      var q = quality(slots, fill);
      if (!best || q > best.q) best = { q: q, black: black, slots: slots, fill: fill, attempt: attempt };
    }
    if (!best) return null;
    var res = assemble(ds, best.black, best.slots, best.fill, best.attempt);
    res.tier = tier;
    return res;
  }

  function gridKey(black, slots, fill) {
    var g = [];
    for (var c = 0; c < CELLS; c++) g.push(black[c] ? '#' : '');
    slots.forEach(function (s, i) { for (var p = 0; p < s.cells.length; p++) g[s.cells[p]] = fill[i].w.charAt(p); });
    return g.join('');
  }

  // Rebuild a puzzle from its 36-character grid (row by row, '#' = black square),
  // as stored in crossword-data/YYYY.json. Clues come from the word bank.
  function fromRows(ds, key, bankText) {
    if (!/^[A-Z#]{36}$/.test(key)) return null;
    var clueOf = {};
    parseBank(bankText).forEach(function (r) { clueOf[r.w] = r; });
    var black = new Uint8Array(CELLS);
    for (var c = 0; c < CELLS; c++) black[c] = key.charAt(c) === '#' ? 1 : 0;
    var slots = runsOf(black).filter(function (r) { return r.cells.length >= 3; });
    var fill = [];
    for (var i = 0; i < slots.length; i++) {
      var w = slots[i].cells.map(function (x) { return key.charAt(x); }).join('');
      if (!clueOf[w]) return null; // word no longer in the bank → caller falls back to live generation
      fill.push(clueOf[w]);
    }
    return assemble(ds, black, slots, fill, -1);
  }

  function assemble(ds, black, slots, fill, attempt) {
    var letters = [];
    for (var c = 0; c < CELLS; c++) letters.push(black[c] ? null : '');
    slots.forEach(function (s, i) { for (var p = 0; p < s.cells.length; p++) letters[s.cells[p]] = fill[i].w.charAt(p); });
    // Standard numbering: a square gets a number if it starts an Across or Down answer.
    var startNum = {}, n = 0;
    for (var c2 = 0; c2 < CELLS; c2++) {
      if (black[c2]) continue;
      var starts = slots.some(function (s) { return s.cells[0] === c2; });
      if (starts) startNum[c2] = ++n;
    }
    var across = [], down = [];
    slots.forEach(function (s, i) {
      var e = { num: startNum[s.cells[0]], dir: s.dir === 0 ? 'across' : 'down', cells: s.cells.slice(), answer: fill[i].w, clue: fill[i].clue, abbr: fill[i].abbr };
      (s.dir === 0 ? across : down).push(e);
    });
    across.sort(function (a, b) { return a.num - b.num; });
    down.sort(function (a, b) { return a.num - b.num; });
    var rows = [];
    for (var r = 0; r < N; r++) rows.push(letters.slice(r * N, r * N + N).map(function (x) { return x === null ? '#' : x; }).join(''));
    return {
      date: ds, size: N, rows: rows, letters: letters, numbers: startNum,
      across: across, down: down, attempt: attempt,
      number: dayNum(ds) - dayNum('2026-11-08') // No. 1 = 2026-11-09 (launch)
    };
  }

  var api = { _cfg: CFG, generate: generate, fromRows: fromRows, todayLA: todayLA, msUntilNextLA: msUntilNextLA, dayNum: dayNum, fromDayNum: fromDayNum, wordsFor: wordsFor };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.BoardsideXword = api;
})(typeof window !== 'undefined' ? window : globalThis);
