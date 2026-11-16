import sys, itertools
sys.path.insert(0, __import__('os').path.dirname(__file__))
from themes import THEMES
from collections import Counter
c = Counter(t['b'] for t in THEMES)
for b, n in c.items():
    if n > 1: print("DUP bundle", b)
for t in THEMES:
    b = t['b']; need = 48 - len(b)
    if len(b) < 6: print("SHORT bundle", b); continue
    ok = any(sum(map(len, combo)) == need for k in range(3, 9) for combo in itertools.combinations(t['w'], k))
    if not ok: print("NOFIT", b, need, [(w, len(w)) for w in t['w']])
