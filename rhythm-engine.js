// Boardside Reviews · Rhythm Rush ECG engine
// Draws synthetic two-lead rhythm strips (lead II + V1) from a beat-by-beat model:
// each P, QRS, T (and U) is a smooth wave placed by the rhythm's timing rules, then
// summed per lead with baseline wander and a little noise. Every call randomizes rate,
// intervals, amplitudes and artifact, so no two strips of the same rhythm look alike.
//   BoardsideECG.RHYTHMS               -> list of { id, name, family, clue }
//   BoardsideECG.make(id, rnd)         -> strip { T, fs, II, V1, spikes }
//   BoardsideECG.draw(canvas, strip, opts)
(function (root) {
  'use strict';
  var FS = 500, T = 6; // samples per second, strip length (s)

  // ── Rhythm list (name, family for distractors, one-line teaching clue) ──
  var RHYTHMS = [
    ['nsr', 'Normal sinus rhythm', 'sinus', 'Upright P before every QRS, PR constant, rate 60 to 100.'],
    ['sbrady', 'Sinus bradycardia', 'sinus', 'Normal P-QRS-T, just slow: rate under 60.'],
    ['stach', 'Sinus tachycardia', 'sinus', 'Normal P before each QRS, rate over 100. Look for the P on the T.'],
    ['sarr', 'Sinus arrhythmia', 'sinus', 'Normal P waves, but the R-R interval speeds up and slows down with breathing.'],
    ['spause', 'Sinus pause', 'sinus', 'Sinus rhythm, then a gap with no P wave at all.'],
    ['af_slow', 'AF, slow ventricular response', 'af', 'Irregularly irregular, no P waves, and the rate is under 60.'],
    ['af_ctrl', 'AF, rate controlled', 'af', 'Irregularly irregular, no P waves, fibrillatory baseline, rate 60 to 100.'],
    ['af_rvr', 'AF with RVR', 'af', 'Irregularly irregular, no P waves, rate over 110.'],
    ['fl21', 'Atrial flutter, 2:1', 'flutter', 'Regular narrow rhythm near 150: think flutter. One flutter wave hides in the QRS or T.'],
    ['fl41', 'Atrial flutter, 4:1', 'flutter', 'Sawtooth flutter waves in II, four for every QRS, rate near 75.'],
    ['flvar', 'Atrial flutter, variable block', 'flutter', 'Sawtooth waves throughout, but the ratio changes, so the R-R varies.'],
    ['mat', 'Multifocal atrial tachycardia', 'svt', 'Rate over 100 with at least three different P-wave shapes and varying PR.'],
    ['svt', 'SVT (AVNRT)', 'svt', 'Regular narrow tachycardia, 150 to 220, with no visible P waves.'],
    ['pac', 'Premature atrial contractions', 'svt', 'Early beat with an odd-looking P and a narrow QRS, then a short pause.'],
    ['junc', 'Junctional rhythm', 'svt', 'Narrow QRS at 40 to 60 with no P, or an inverted P right next to the QRS.'],
    ['pvc_big', 'Ventricular bigeminy', 'vent', 'Every other beat is a wide, early PVC.'],
    ['pvc_tri', 'Ventricular trigeminy', 'vent', 'Every third beat is a wide, early PVC.'],
    ['pvc_coup', 'PVC couplets', 'vent', 'Two wide PVCs back to back, then sinus again.'],
    ['aivr', 'Accelerated idioventricular rhythm', 'vent', 'Regular wide complexes at 50 to 110 with no P waves. Classic after reperfusion.'],
    ['vt', 'Monomorphic VT', 'vent', 'Regular wide-complex tachycardia, every QRS the same shape.'],
    ['tdp', 'Torsades de pointes', 'vent', 'Polymorphic VT whose amplitude twists around the baseline. Give magnesium.'],
    ['vf', 'Ventricular fibrillation', 'vent', 'Chaotic baseline with no organized QRS. Shock.'],
    ['asys', 'Asystole', 'vent', 'Flat line. Check leads and gain, then CPR and epinephrine. No shock.'],
    ['avb1', 'First-degree AV block', 'block', 'Every P conducts, but the PR is fixed and longer than 200 ms (a big box).'],
    ['mob1', 'Mobitz I (Wenckebach)', 'block', 'PR lengthens beat by beat until a P drops, so beats come in groups.'],
    ['mob2', 'Mobitz II', 'block', 'PR stays constant, then a P suddenly fails to conduct. Needs a pacemaker.'],
    ['avb21', '2:1 AV block', 'block', 'Every other P conducts, with the same PR each time.'],
    ['chb', 'Complete heart block', 'block', 'P waves and QRS complexes march out independently; PR is all over the place.'],
    ['apace', 'Atrial paced rhythm', 'pace', 'Pacer spike before each P wave, then a normal narrow QRS.'],
    ['vpace', 'Ventricular paced rhythm', 'pace', 'Pacer spike right before a wide QRS at a fixed rate.'],
    ['ftc', 'Pacemaker failure to capture', 'pace', 'Pacer spikes with no QRS after some of them.'],
    ['fts', 'Pacemaker failure to sense', 'pace', 'Spikes fire on a fixed timer, ignoring native beats, some landing on T waves.'],
    ['wpw', 'Wolff-Parkinson-White', 'cond', 'Short PR, delta-wave slur into a slightly wide QRS.'],
    ['lbbb', 'Left bundle branch block', 'cond', 'Wide QRS with a deep, broad QS in V1 and discordant T waves.'],
    ['rbbb', 'Right bundle branch block', 'cond', 'Wide QRS with rSR′ ("rabbit ears") in V1 and a slurred S in II.'],
    ['brugada', 'Brugada pattern (type 1)', 'cond', 'Coved ST elevation in V1 sloping into an inverted T. Sudden-death risk.'],
    ['lqt', 'Long QT', 'cond', 'T wave ends past halfway between beats; QTc over 500 ms risks torsades.'],
    ['peakT', 'Hyperkalemia (peaked T waves)', 'lytes', 'Tall, narrow, tented T waves with flattened P waves.'],
    ['sine', 'Severe hyperkalemia (sine wave)', 'lytes', 'Very wide QRS merging into T: a sine wave. Calcium now.'],
    ['uwave', 'Hypokalemia (U waves)', 'lytes', 'Flat T waves followed by a U wave, with slight ST depression.'],
    ['dig', 'Digoxin effect', 'lytes', 'Scooped "reverse tick" ST depression with a short QT.']
  ].map(function (r) { return { id: r[0], name: r[1], family: r[2], clue: r[3] }; });
  var BY_ID = {}; RHYTHMS.forEach(function (r) { BY_ID[r.id] = r; });

  // ── Wave primitives ──
  function U(rnd, a, b) { return a + (b - a) * rnd(); }
  function addG(arr, mu, s, amp) {
    if (!amp) return;
    var i0 = Math.max(0, Math.floor((mu - 4 * s) * FS)), i1 = Math.min(arr.length - 1, Math.ceil((mu + 4 * s) * FS));
    for (var i = i0; i <= i1; i++) { var x = (i / FS - mu) / s; arr[i] += amp * Math.exp(-0.5 * x * x); }
  }
  function addAG(arr, mu, s1, s2, amp) { // asymmetric (rises over s1, falls over s2)
    var i0 = Math.max(0, Math.floor((mu - 4 * s1) * FS)), i1 = Math.min(arr.length - 1, Math.ceil((mu + 4 * s2) * FS));
    for (var i = i0; i <= i1; i++) { var t = i / FS, s = t < mu ? s1 : s2, x = (t - mu) / s; arr[i] += amp * Math.exp(-0.5 * x * x); }
  }
  function qtFor(rr, k) { return Math.min(0.62, Math.max(0.26, (k || 0.40) * Math.sqrt(Math.min(rr, 2)))); }

  // ── Beat morphologies (q = QRS onset; m = strip-wide variation) ──
  function pWave(L, kind, tp, m, rnd) {
    var II = L.II, V1 = L.V1;
    if (kind === 'sinus') { addG(II, tp, 0.022, 0.13 * m.p); addG(V1, tp - 0.012, 0.013, 0.06 * m.p); addG(V1, tp + 0.018, 0.013, -0.05 * m.p); }
    else if (kind === 'retro') { addG(II, tp, 0.02, -0.11); addG(V1, tp, 0.018, 0.04); }
    else if (kind === 'ectopic') {
      var a = (rnd() < 0.5 ? -1 : 1) * U(rnd, 0.07, 0.18), b = U(rnd, -0.08, 0.08);
      addG(II, tp, U(rnd, 0.014, 0.026), a); addG(V1, tp, 0.016, b);
    }
  }
  function tWave(arr, center, s1, s2, amp) { addAG(arr, center, s1, s2, amp); }

  function beat(L, b, m, rnd) {
    var q = b.q, II = L.II, V1 = L.V1, A = m.r, qt = b.qt, mod = m.mod || {};
    var tAmp = mod.peaked ? 0.85 : mod.flatT ? 0.1 : mod.dig ? 0.09 : 0.3 * m.t;
    var tS1 = mod.peaked ? 0.034 : mod.lqt ? 0.075 : 0.055, tS2 = mod.peaked ? 0.032 : mod.lqt ? 0.055 : 0.036;
    var tC = q + qt - (mod.peaked ? 0.075 : mod.lqt ? 0.11 : 0.085);
    switch (b.kind) {
      case 'N': case 'WPW': case 'BRUG':
        if (b.kind === 'WPW') {
          addAG(II, q + 0.05, 0.032, 0.012, 0.42 * A); addG(II, q + 0.072, 0.011, 0.75 * A); addG(II, q + 0.096, 0.010, -0.12 * A);
          addAG(V1, q + 0.05, 0.032, 0.012, 0.3 * A); addG(V1, q + 0.07, 0.012, 0.35 * A); addG(V1, q + 0.094, 0.012, -0.35 * A);
          tWave(II, q + qt - 0.08, 0.055, 0.036, 0.16 * m.t); tWave(V1, q + qt - 0.09, 0.05, 0.04, 0.04);
          break;
        }
        addG(II, q + 0.012, 0.006, -0.07 * A); addG(II, q + 0.034, 0.010, 1.1 * A); addG(II, q + 0.060, 0.009, -0.2 * A);
        addG(V1, q + 0.024, 0.007, 0.22 * A * m.v1r); addG(V1, q + 0.052, 0.013, -0.95 * A);
        tWave(II, tC, tS1, tS2, tAmp);
        if (b.kind === 'BRUG') {
          addG(V1, q + 0.095, 0.03, 0.34); addG(V1, q + 0.15, 0.045, 0.22); addG(V1, q + 0.27, 0.05, -0.28);
        } else {
          tWave(V1, q + qt - 0.09, 0.05, 0.04, mod.peaked ? 0.5 : 0.06);
        }
        if (mod.uwave) { addG(II, q + 0.17, 0.05, -0.06); addG(II, q + qt + 0.075, 0.04, 0.17); addG(V1, q + qt + 0.075, 0.04, 0.12); }
        if (mod.dig) { addAG(II, q + 0.2, 0.075, 0.028, -0.3); addAG(II, q + 0.255, 0.02, 0.03, 0.1); addAG(V1, q + 0.2, 0.07, 0.03, -0.1); }
        break;
      case 'LB':
        addG(II, q + 0.045, 0.022, 0.72 * A); addG(II, q + 0.098, 0.022, 0.78 * A);
        addG(V1, q + 0.072, 0.033, -1.35 * A);
        tWave(II, q + qt - 0.1, 0.06, 0.04, -0.3); tWave(V1, q + qt - 0.1, 0.06, 0.04, 0.35);
        break;
      case 'RB':
        addG(II, q + 0.012, 0.006, -0.06 * A); addG(II, q + 0.032, 0.010, 0.95 * A); addG(II, q + 0.088, 0.022, -0.32 * A);
        addG(V1, q + 0.022, 0.007, 0.3 * A); addG(V1, q + 0.048, 0.009, -0.45 * A); addG(V1, q + 0.097, 0.019, 0.85 * A);
        tWave(II, tC + 0.02, 0.055, 0.036, 0.25 * m.t); tWave(V1, q + qt - 0.09, 0.05, 0.04, -0.2);
        break;
      case 'V': { // ventricular ectopic / escape / VT: wide, bizarre, discordant T
        var f = b.focus || m.focus;
        addG(II, q + 0.065, 0.03 * f.w, 1.3 * f.a2); addG(II, q + 0.135, 0.024, -0.35 * f.a2);
        addG(V1, q + 0.065, 0.032 * f.w, 1.2 * f.av); addG(V1, q + 0.13, 0.024, -0.3 * f.av);
        if (!b.noT) { tWave(II, q + Math.max(0.3, qt - 0.06), 0.06, 0.05, -0.42 * f.a2); tWave(V1, q + Math.max(0.3, qt - 0.06), 0.06, 0.05, -0.38 * f.av); }
        break;
      }
      case 'PACED':
        addG(II, q + 0.075, 0.03, -1.0 * A); addG(II, q + 0.15, 0.02, 0.15);
        addG(V1, q + 0.075, 0.032, -1.2 * A);
        tWave(II, q + qt - 0.08, 0.06, 0.045, 0.35); tWave(V1, q + qt - 0.08, 0.06, 0.045, 0.3);
        break;
      case 'SINE':
        addG(II, q + 0.11, 0.075, 0.95); addG(II, q + 0.36, 0.095, -0.75);
        addG(V1, q + 0.11, 0.075, -0.85); addG(V1, q + 0.36, 0.095, 0.6);
        break;
    }
  }

  // ── Strip assembly ──
  function blank() { var n = Math.round(T * FS); return { II: new Float32Array(n), V1: new Float32Array(n) }; }
  function variation(rnd) {
    return { r: U(rnd, 0.85, 1.25), t: U(rnd, 0.8, 1.25), p: U(rnd, 0.8, 1.25), v1r: U(rnd, 0.7, 1.4),
      focus: { a2: (rnd() < 0.65 ? 1 : -1) * U(rnd, 0.8, 1.1), av: (rnd() < 0.5 ? 1 : -1) * U(rnd, 0.8, 1.1), w: U(rnd, 0.9, 1.25) } };
  }
  
  // Sinus-driven sequence: returns list of { tp (P peak), q (QRS onset or null) }
  function sinusTrain(rnd, rate, opts) {
    opts = opts || {};
    var out = [], t = -U(rnd, 0.2, 60 / rate + 0.2), base = 60 / rate;
    while (t < T + 1) {
      out.push({ tp: t });
      var rr = base * (1 + U(rnd, -0.02, 0.02));
      if (opts.resp) rr = base * (1 + opts.resp * Math.sin(2 * Math.PI * t / opts.respPeriod + opts.phase));
      t += rr;
    }
    return out;
  }

  function build(id, rnd) {
    var L = blank(), m = variation(rnd), spikes = [], beats = [], i, t, rate, pr;
    var P = function (tp, kind) { pWave(L, kind, tp, m, rnd); };
    var Q = function (q, kind, extra) { var b = { q: q, kind: kind, qt: extra && extra.qt || 0.4 }; if (extra) for (var k in extra) b[k] = extra[k]; beats.push(b); return b; };
    var conductedSinus = function (rate, pr, kind, opts) {
      var train = sinusTrain(rnd, rate, opts), rr = 60 / rate;
      train.forEach(function (s, j) {
        var nextRR = j + 1 < train.length ? train[j + 1].tp - s.tp : rr;
        P(s.tp, 'sinus'); Q(s.tp - 0.045 + pr, kind || 'N', { qt: qtFor(nextRR, opts && opts.qtk) });
      });
    };
    switch (id) {
      case 'nsr': conductedSinus(U(rnd, 64, 96), U(rnd, 0.13, 0.18)); break;
      case 'sbrady': conductedSinus(U(rnd, 36, 52), U(rnd, 0.14, 0.19)); break;
      case 'stach': conductedSinus(U(rnd, 112, 145), U(rnd, 0.12, 0.15)); break;
      case 'sarr': conductedSinus(U(rnd, 62, 78), U(rnd, 0.14, 0.18), 'N', { resp: U(rnd, 0.24, 0.32), respPeriod: U(rnd, 3.4, 4.4), phase: U(rnd, 0, 6.28) }); break;
      case 'spause': {
        rate = U(rnd, 66, 86); pr = U(rnd, 0.14, 0.18);
        var rr0 = 60 / rate, pauseAt = U(rnd, 1.8, 3.0), gap = U(rnd, 2.4, 3.1);
        for (t = -U(rnd, 0.2, rr0); t < T + 1; ) { P(t, 'sinus'); Q(t - 0.045 + pr, 'N', { qt: qtFor(rr0) }); var nx = t + rr0 * (1 + U(rnd, -0.02, 0.02)); if (t < pauseAt && nx >= pauseAt) nx = t + gap; t = nx; }
        break;
      }
      case 'af_slow': case 'af_ctrl': case 'af_rvr': {
        var lo = id === 'af_slow' ? 0.95 : id === 'af_ctrl' ? 0.58 : 0.34, hi = id === 'af_slow' ? 1.75 : id === 'af_ctrl' ? 1.05 : 0.56;
        for (t = -U(rnd, 0, 0.8); t < T + 1; t += U(rnd, lo, hi)) Q(t, 'N', { qt: 0.34 });
        fib(L, rnd, U(rnd, 0.035, 0.07));
        break;
      }
      case 'fl21': case 'fl41': case 'flvar': {
        var fc = U(rnd, 0.195, 0.215), ph = U(rnd, 0, fc);
        flutter(L, fc, ph, rnd);
        var ratios = id === 'fl21' ? [2] : id === 'fl41' ? [4] : null, k = -3;
        while (true) {
          var ratio = ratios ? ratios[0] : [2, 3, 4, 4, 3, 2][Math.floor(rnd() * 6)];
          var fw = ph + k * fc; if (fw > T + 1) break;
          Q(fw + 0.21, 'N', { qt: id === 'fl21' ? 0.3 : 0.36, mute: true });
          k += ratio;
        }
        break;
      }
      case 'mat': {
        var foci = [], nf = 3 + Math.floor(rnd() * 2);
        for (i = 0; i < nf; i++) foci.push({ a: [0.2, -0.13, 0.09, 0.16][i] * U(rnd, 0.85, 1.15), s: [0.026, 0.016, 0.02, 0.012][i], v: U(rnd, -0.08, 0.08), pr: U(rnd, 0.1, 0.22) });
        for (t = -U(rnd, 0, 0.5); t < T + 1; ) {
          var fo = foci[Math.floor(rnd() * nf)];
          addG(L.II, t, fo.s, fo.a); addG(L.V1, t, 0.016, fo.v);
          Q(t - 0.045 + fo.pr, 'N', { qt: 0.32 }); t += U(rnd, 0.4, 0.66);
        }
        break;
      }
      case 'svt': { var r2 = 60 / U(rnd, 155, 210); for (t = -U(rnd, 0, r2); t < T + 1; t += r2) Q(t, 'N', { qt: 0.27 }); break; }
      case 'pac': {
        rate = U(rnd, 64, 82); pr = U(rnd, 0.14, 0.17); var rr1 = 60 / rate, n = 0, early = [3, 7 + Math.floor(rnd() * 2)];
        for (t = -U(rnd, 0, rr1); t < T + 1; n++) {
          var isPac = early.indexOf(n) >= 0;
          P(t, isPac ? 'ectopic' : 'sinus'); Q(t - 0.045 + pr, 'N', { qt: qtFor(rr1) });
          var nextEarly = early.indexOf(n + 1) >= 0;
          t += nextEarly ? rr1 * U(rnd, 0.58, 0.68) : isPac ? rr1 * U(rnd, 1.05, 1.15) : rr1 * U(rnd, 0.98, 1.02);
        }
        break;
      }
      case 'junc': {
        var rj = 60 / U(rnd, 42, 58), retro = rnd();
        for (t = -U(rnd, 0, rj); t < T + 1; t += rj * U(rnd, 0.99, 1.01)) {
          Q(t, 'N', { qt: qtFor(rj) });
          if (retro < 0.4) P(t - 0.06, 'retro'); else if (retro < 0.7) P(t + 0.12, 'retro');
        }
        break;
      }
      case 'pvc_big': case 'pvc_tri': case 'pvc_coup': {
        rate = U(rnd, 66, 84); pr = U(rnd, 0.14, 0.17); var rr2 = 60 / rate, idx = 0;
        var pattern = id === 'pvc_big' ? [0, 1] : id === 'pvc_tri' ? [0, 0, 1] : null;
        var coupAt = [2 + Math.floor(rnd() * 2)];
        t = -U(rnd, 0, rr2);
        while (t < T + 1) {
          var isV = pattern ? pattern[(idx) % pattern.length] === 1 : false;
          if (!pattern && coupAt.indexOf(idx) >= 0) {
            P(t, 'sinus'); Q(t - 0.045 + pr, 'N', { qt: qtFor(rr2) });
            var v1 = t - 0.045 + pr + rr2 * U(rnd, 0.48, 0.56), v2 = v1 + U(rnd, 0.36, 0.44);
            Q(v1, 'V', { qt: 0.4, noT: true }); Q(v2, 'V', { qt: 0.42 });
            t = t + 2 * rr2; idx++; coupAt.push(idx + 4); continue;
          }
          if (isV) { Q(t - 0.045 + pr - rr2 * U(rnd, 0.42, 0.5), 'V', { qt: 0.42 }); t += rr2; }
          else { P(t, 'sinus'); Q(t - 0.045 + pr, 'N', { qt: qtFor(rr2) }); t += rr2 * U(rnd, 0.98, 1.02); }
          idx++;
        }
        break;
      }
      case 'aivr': { var ra = 60 / U(rnd, 58, 100); for (t = -U(rnd, 0, ra); t < T + 1; t += ra * U(rnd, 0.98, 1.02)) Q(t, 'V', { qt: qtFor(ra, 0.42) }); break; }
      case 'vt': { var rv = 60 / U(rnd, 150, 205); for (t = -U(rnd, 0, rv); t < T + 1; t += rv) Q(t, 'V', { qt: Math.min(0.3, rv * 0.85) }); break; }
      case 'tdp': torsades(L, rnd); break;
      case 'vf': fibV(L, rnd); break;
      case 'asys': break;
      case 'avb1': conductedSinus(U(rnd, 60, 84), U(rnd, 0.28, 0.38)); break;
      case 'mob1': {
        var ratrr = 60 / U(rnd, 72, 92), group = rnd() < 0.5 ? 4 : 3, prs = group === 4 ? [0.18, 0.27, 0.32] : [0.18, 0.29];
        var g0 = Math.floor(rnd() * group), j = g0;
        for (t = -U(rnd, 0, ratrr); t < T + 1; t += ratrr, j++) {
          P(t, 'sinus'); var pos = j % group;
          if (pos < group - 1) Q(t - 0.045 + prs[pos] + U(rnd, -0.008, 0.008), 'N', { qt: qtFor(ratrr * 1.2) });
        }
        break;
      }
      case 'mob2': {
        var rm = 60 / U(rnd, 72, 92), every = rnd() < 0.5 ? 4 : 5, j2 = Math.floor(rnd() * every), prm = U(rnd, 0.16, 0.2);
        for (t = -U(rnd, 0, rm); t < T + 1; t += rm, j2++) { P(t, 'sinus'); if (j2 % every !== every - 1) Q(t - 0.045 + prm, 'N', { qt: qtFor(rm) }); }
        break;
      }
      case 'avb21': {
        var r21 = 60 / U(rnd, 80, 104), pr21 = U(rnd, 0.16, 0.24), j3 = Math.floor(rnd() * 2);
        for (t = -U(rnd, 0, r21); t < T + 1; t += r21, j3++) { P(t, 'sinus'); if (j3 % 2 === 0) Q(t - 0.045 + pr21, 'N', { qt: qtFor(2 * r21) }); }
        break;
      }
      case 'chb': {
        var rp = 60 / U(rnd, 72, 100), rq = 60 / U(rnd, 30, 44), wide = rnd() < 0.6;
        for (t = -U(rnd, 0, rp); t < T + 1; t += rp) P(t, 'sinus');
        for (t = U(rnd, 0, rq) - 0.4; t < T + 1; t += rq) Q(t, wide ? 'V' : 'N', { qt: 0.46 });
        break;
      }
      case 'apace': {
        var rap = 60 / [60, 70, 80][Math.floor(rnd() * 3)], prp = U(rnd, 0.16, 0.2);
        for (t = -U(rnd, 0, rap); t < T + 1; t += rap) { spikes.push(t - 0.05); P(t, 'sinus'); Q(t - 0.045 + prp, 'N', { qt: qtFor(rap) }); }
        break;
      }
      case 'vpace': {
        var rvp = 60 / [60, 70, 80][Math.floor(rnd() * 3)];
        for (t = -U(rnd, 0, rvp); t < T + 1; t += rvp) { spikes.push(t); Q(t, 'PACED', { qt: qtFor(rvp, 0.44) }); }
        break;
      }
      case 'ftc': {
        var rf = 60 / [60, 70][Math.floor(rnd() * 2)], n2 = 0, miss = [2 + Math.floor(rnd() * 2), 5 + Math.floor(rnd() * 2)];
        for (t = -U(rnd, 0, rf) + 0.3; t < T + 1; t += rf, n2++) { spikes.push(t); if (miss.indexOf(n2) < 0) Q(t, 'PACED', { qt: qtFor(rf, 0.44) }); }
        break;
      }
      case 'fts': {
        // Native sinus rhythm the pacer fails to see; it fires on its own fixed timer.
        var rn = 60 / U(rnd, 74, 86), prn = U(rnd, 0.14, 0.17), rpc = 60 / 60, natives = [];
        for (t = -U(rnd, 0, rn); t < T + 1; t += rn * U(rnd, 0.98, 1.02)) { P(t, 'sinus'); var qq = t - 0.045 + prn; Q(qq, 'N', { qt: qtFor(rn) }); natives.push(qq); }
        for (t = U(rnd, 0.1, 0.6); t < T + 1; t += rpc) {
          spikes.push(t);
          var refractory = natives.some(function (x) { return t - x > -0.05 && t - x < 0.42; });
          var nextNative = natives.filter(function (x) { return x > t; })[0];
          if (!refractory && (nextNative == null || nextNative - t > 0.12)) Q(t, 'PACED', { qt: 0.4 });
        }
        break;
      }
      case 'wpw': conductedSinus(U(rnd, 62, 92), U(rnd, 0.085, 0.105), 'WPW'); break;
      case 'lbbb': conductedSinus(U(rnd, 60, 92), U(rnd, 0.15, 0.19), 'LB', { qtk: 0.43 }); break;
      case 'rbbb': conductedSinus(U(rnd, 60, 92), U(rnd, 0.14, 0.18), 'RB', { qtk: 0.42 }); break;
      case 'brugada': conductedSinus(U(rnd, 60, 88), U(rnd, 0.15, 0.19), 'BRUG'); break;
      case 'lqt': m.mod = { lqt: 1 }; conductedSinus(U(rnd, 56, 72), U(rnd, 0.14, 0.18), 'N', { qtk: U(rnd, 0.56, 0.62) }); break;
      case 'peakT': m.mod = { peaked: 1 }; m.p = 0.45; conductedSinus(U(rnd, 62, 90), U(rnd, 0.16, 0.2)); break;
      case 'sine': { var rs = 60 / U(rnd, 52, 72); for (t = -U(rnd, 0, rs); t < T + 1; t += rs * U(rnd, 0.98, 1.02)) Q(t, 'SINE', { qt: 0.5 }); break; }
      case 'uwave': m.mod = { uwave: 1, flatT: 1 }; conductedSinus(U(rnd, 60, 84), U(rnd, 0.14, 0.18)); break;
      case 'dig': m.mod = { dig: 1 }; conductedSinus(U(rnd, 60, 82), U(rnd, 0.16, 0.2), 'N', { qtk: 0.36 }); break;
      default: throw new Error('Unknown rhythm ' + id);
    }
    beats.forEach(function (b) { beat(L, b, m, rnd); });
    wander(L, rnd);
    return { id: id, T: T, fs: FS, II: L.II, V1: L.V1, spikes: spikes.filter(function (s) { return s > 0.05 && s < T - 0.02; }) };
  }

  // ── Continuous atrial / ventricular activity ──
  function fib(L, rnd, amp) {
    var comps = [];
    for (var k = 0; k < 5; k++) comps.push({ f: U(rnd, 4.2, 7.5), ph: U(rnd, 0, 6.28), a: U(rnd, 0.4, 1) });
    for (var i = 0; i < L.II.length; i++) {
      var t = i / FS, v = 0;
      for (var c = 0; c < comps.length; c++) v += comps[c].a * Math.sin(2 * Math.PI * comps[c].f * t + comps[c].ph);
      v *= amp / 2.2 * (0.75 + 0.25 * Math.sin(2 * Math.PI * 0.7 * t));
      L.II[i] += v; L.V1[i] += v * 1.5;
    }
  }
  function flutter(L, fc, ph, rnd) {
    var a = U(rnd, 0.16, 0.24);
    for (var i = 0; i < L.II.length; i++) {
      var t = i / FS, x = ((t - ph) / fc) % 1; if (x < 0) x += 1;
      // sawtooth: slow downslope, quick return (negative in II), small discrete positive waves in V1
      var saw = x < 0.72 ? -x / 0.72 : -(1 - (x - 0.72) / 0.28);
      L.II[i] += a * (saw + 0.5);
      L.V1[i] += 0.07 * Math.exp(-0.5 * Math.pow((x - 0.35) / 0.12, 2));
    }
  }
  function torsades(L, rnd) {
    var f = U(rnd, 3.4, 4.2), per = U(rnd, 2.2, 3.0), ph = U(rnd, 0, 6.28), ph2 = U(rnd, 0, 6.28);
    for (var i = 0; i < L.II.length; i++) {
      var t = i / FS, env = 1.35 * Math.cos(2 * Math.PI * t / per + ph);
      var w = Math.sin(2 * Math.PI * f * t + 0.6 * Math.sin(2 * Math.PI * 0.9 * t + ph2));
      L.II[i] += env * Math.sign(w) * Math.pow(Math.abs(w), 0.7);
      L.V1[i] += -0.8 * env * Math.sign(w) * Math.pow(Math.abs(w), 0.7);
    }
  }
  function fibV(L, rnd) {
    var comps = [], coarse = U(rnd, 0.25, 0.7);
    for (var k = 0; k < 6; k++) comps.push({ f: U(rnd, 3.5, 7.5), ph: U(rnd, 0, 6.28), a: U(rnd, 0.3, 1), m: U(rnd, 0.2, 0.9) });
    for (var i = 0; i < L.II.length; i++) {
      var t = i / FS, v = 0;
      for (var c = 0; c < comps.length; c++) v += comps[c].a * Math.sin(2 * Math.PI * comps[c].f * t + comps[c].ph) * (0.6 + 0.4 * Math.sin(2 * Math.PI * comps[c].m * t));
      L.II[i] += v * coarse / 2; L.V1[i] += v * coarse / 2.4;
    }
  }
  function wander(L, rnd) {
    var f1 = U(rnd, 0.12, 0.3), a1 = U(rnd, 0.02, 0.07), p1 = U(rnd, 0, 6.28), f2 = U(rnd, 0.15, 0.35), p2 = U(rnd, 0, 6.28);
    var noise = U(rnd, 0.004, 0.012), prevA = 0, prevB = 0;
    for (var i = 0; i < L.II.length; i++) {
      var t = i / FS;
      prevA = 0.6 * prevA + 0.4 * (rnd() - 0.5) * 2 * noise; prevB = 0.6 * prevB + 0.4 * (rnd() - 0.5) * 2 * noise;
      L.II[i] += a1 * Math.sin(2 * Math.PI * f1 * t + p1) + prevA;
      L.V1[i] += a1 * 0.8 * Math.sin(2 * Math.PI * f2 * t + p2) + prevB;
    }
  }

  // ── Drawing (25 mm/s, 10 mm/mV, pink ECG paper) ──
  function draw(cv, strip, opts) {
    opts = opts || {};
    var dpr = Math.min(window.devicePixelRatio || 1, 3), W = cv.clientWidth, mm = W / (strip.T * 25 + 6);
    var rowH = 36 * mm, H = Math.round(rowH * 2 + 2 * mm);
    cv.style.height = H + 'px'; cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
    var g = cv.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.fillStyle = opts.paper || '#fff5f3'; g.fillRect(0, 0, W, H);
    var x0 = 6 * mm, lineMinor = opts.minor || 'rgba(232,120,120,.22)', lineMajor = opts.major || 'rgba(214,72,72,.5)';
    for (var x = 0, k = 0; x <= W + 0.5; x += mm, k++) { g.strokeStyle = k % 5 ? lineMinor : lineMajor; g.lineWidth = k % 5 ? 0.5 : 1; g.beginPath(); g.moveTo(Math.round(x) + 0.5, 0); g.lineTo(Math.round(x) + 0.5, H); g.stroke(); }
    for (var y = 0, k2 = 0; y <= H + 0.5; y += mm, k2++) { g.strokeStyle = k2 % 5 ? lineMinor : lineMajor; g.lineWidth = k2 % 5 ? 0.5 : 1; g.beginPath(); g.moveTo(0, Math.round(y) + 0.5); g.lineTo(W, Math.round(y) + 0.5); g.stroke(); }
    var progress = opts.progress == null ? 1 : opts.progress;
    [['II', 18 * mm], ['V1', rowH + 16 * mm]].forEach(function (row) {
      var arr = strip[row[0]], base = row[1], top = row[0] === 'II' ? 0 : rowH, bottom = top + rowH;
      g.fillStyle = '#222'; g.font = '700 ' + Math.max(10, 3.6 * mm) + 'px ui-monospace, Menlo, Consolas, monospace'; g.fillText(row[0], 0.8 * mm, top + 4.6 * mm);
      // 1 mV calibration pulse
      g.strokeStyle = '#111'; g.lineWidth = Math.max(1.2, 0.32 * mm); g.lineJoin = 'round';
      g.beginPath(); g.moveTo(0.8 * mm, base); g.lineTo(1.8 * mm, base); g.lineTo(1.8 * mm, base - 10 * mm); g.lineTo(4.3 * mm, base - 10 * mm); g.lineTo(4.3 * mm, base); g.lineTo(5.6 * mm, base); g.stroke();
      g.save(); g.beginPath(); g.rect(x0, top, W - x0, rowH); g.clip();
      g.beginPath();
      var n = Math.floor(arr.length * progress);
      for (var i = 0; i < n; i++) {
        var px = x0 + (i / strip.fs) * 25 * mm, py = base - arr[i] * 10 * mm;
        py = Math.max(top + 1, Math.min(bottom - 1, py));
        if (i === 0) g.moveTo(px, py); else g.lineTo(px, py);
      }
      g.stroke();
      // pacer spikes
      strip.spikes.forEach(function (s) {
        if (s / strip.T > progress) return;
        var px = x0 + s * 25 * mm; g.lineWidth = Math.max(1, 0.25 * mm); g.beginPath(); g.moveTo(px, base + 1.5 * mm); g.lineTo(px, base - (row[0] === 'II' ? 9 : 7) * mm); g.stroke();
      });
      g.restore();
    });
    g.fillStyle = 'rgba(40,20,20,.55)'; g.font = '600 ' + Math.max(9, 2.6 * mm) + 'px ui-monospace, Menlo, Consolas, monospace';
    var lbl = '25 mm/s  10 mm/mV'; g.fillText(lbl, W - g.measureText(lbl).width - 1.5 * mm, H - 1.6 * mm);
  }

  var api = { RHYTHMS: RHYTHMS, byId: BY_ID, make: build, draw: draw };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.BoardsideECG = api;
})(typeof window !== 'undefined' ? window : globalThis);
