#!/usr/bin/env node
// Boardside Reviews · Cross-Cover puzzle builder
// Pre-builds daily puzzles into crossword-data/YYYY.json with two hard rules the
// in-browser generator can't enforce on its own (it has no memory of other days):
//   1. No grid ever repeats (including a grid that is another day's grid flipped on its diagonal).
//   2. No answer appears again within RECENT_DAYS days.
// Usage:  node tools/crossword-build.js [daysAhead]     (default 3650 ≈ 10 years ahead)
// Safe to re-run: existing days are never changed; it only appends missing days.
'use strict';
const fs = require('fs'), path = require('path');
const ROOT = path.join(__dirname, '..');
global.window = global;
require(path.join(ROOT, 'crossword-words.js'));
const X = require(path.join(ROOT, 'crossword-engine.js'));
const BANK = global.BOARDSIDE_XWORD_WORDS;
const START = '2026-11-09';          // Cross-Cover No. 1
const RECENT_DAYS = 14;
const DATA = path.join(ROOT, 'crossword-data');
const daysAhead = +(process.argv[2] || 3650);

function laToday() { return X.todayLA(); }
function load() {
  const all = {};
  if (!fs.existsSync(DATA)) fs.mkdirSync(DATA);
  for (const f of fs.readdirSync(DATA)) if (/^\d{4}\.json$/.test(f)) Object.assign(all, JSON.parse(fs.readFileSync(path.join(DATA, f), 'utf8')));
  return all;
}
function save(all) {
  const byYear = {};
  for (const ds of Object.keys(all).sort()) (byYear[ds.slice(0, 4)] = byYear[ds.slice(0, 4)] || {})[ds] = all[ds];
  for (const y of Object.keys(byYear)) {
    const body = '{\n' + Object.keys(byYear[y]).map(d => `"${d}":"${byYear[y][d]}"`).join(',\n') + '\n}\n';
    const f = path.join(DATA, y + '.json');
    if (!fs.existsSync(f) || fs.readFileSync(f, 'utf8') !== body) fs.writeFileSync(f, body);
  }
}
const transpose = g => { let o = ''; for (let c = 0; c < 6; c++) for (let r = 0; r < 6; r++) o += g[r * 6 + c]; return o; };
function answersOf(g) {
  const p = X.fromRows('2000-01-01', g, BANK);
  return p ? p.across.concat(p.down).map(e => e.answer) : [];
}

const all = load();
const seen = new Set();
for (const g of Object.values(all)) { seen.add(g); seen.add(transpose(g)); }
const end = X.dayNum(laToday()) + daysAhead;
let added = 0, t0 = Date.now();
for (let n = X.dayNum(START); n <= end; n++) {
  const ds = X.fromDayNum(n);
  if (all[ds]) continue;
  const exclude = {};
  for (let k = 1; k <= RECENT_DAYS; k++) {
    const prev = all[X.fromDayNum(n - k)];
    if (prev) answersOf(prev).forEach(w => { exclude[w] = 1; });
  }
  const p = X.generate(ds, BANK, { exclude, reject: g => seen.has(g) || seen.has(transpose(g)) });
  const g = p.rows.join('').replace(/#/g, '#');
  all[ds] = g; seen.add(g); seen.add(transpose(g)); added++;
  if (added % 100 === 0) { save(all); console.log(ds, added, 'built', Math.round((Date.now() - t0) / 1000) + 's'); }
}
save(all);
console.log(`Done. Added ${added} day(s). Puzzles now run through ${Object.keys(all).sort().pop()}.`);
