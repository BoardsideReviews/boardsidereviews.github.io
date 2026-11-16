"""Bundle Branch puzzle generator.

For each theme: choose a subset of candidate words that, with the bundle word,
fills a 6x8 grid exactly (48 letters). The bundle word must touch two opposite
edges (left+right or top+bottom). Words are paths through 8-neighbours, they
never reuse a cell and their diagonal steps never cross each other.

Writes bundle-data.js: window.BUNDLE = [{t, b, w:[...], p, a, g:"48 letters", path:{word:[cell...]}, x:"hint words"}]
Run: python3 tools/bundle/gen.py
"""
import json, random, sys, os, itertools
sys.path.insert(0, os.path.dirname(__file__))
from themes import THEMES

R, C = 8, 6
N = R * C
NB = {}
for r in range(R):
    for c in range(C):
        i = r * C + c
        NB[i] = [ (r+dr)*C + (c+dc) for dr in (-1,0,1) for dc in (-1,0,1)
                  if (dr or dc) and 0 <= r+dr < R and 0 <= c+dc < C ]

def diag_key(a, b):
    """Return the crossing diagonal (as a frozenset) for a diagonal step a->b, else None."""
    ra, ca = divmod(a, C); rb, cb = divmod(b, C)
    if ra != rb and ca != cb:
        return frozenset((ra*C+cb, rb*C+ca))
    return None

class Board:
    def __init__(self):
        self.cell = [None]*N          # letter
        self.edges = set()            # frozenset(a,b) of used diagonal steps
    def free(self, i): return self.cell[i] is None

def components(board):
    seen = [False]*N; comps = []
    for s in range(N):
        if board.cell[s] is None and not seen[s]:
            stack=[s]; seen[s]=True; n=0
            while stack:
                x=stack.pop(); n+=1
                for y in NB[x]:
                    if board.cell[y] is None and not seen[y]:
                        seen[y]=True; stack.append(y)
            comps.append(n)
    return comps

def subset_sums(lengths):
    sums={0}
    for L in lengths: sums |= {s+L for s in sums}
    return sums

def feasible(board, remaining):
    comps = components(board)
    if not comps: return not remaining
    if not remaining: return False
    ss = subset_sums([len(w) for w in remaining])
    mn = min(len(w) for w in remaining)
    for n in comps:
        if n < mn or n not in ss: return False
    return True

def paths_from(board, start, word, rnd, limit=60):
    """Yield up to `limit` random paths for word starting at `start` (cell must be free)."""
    out = []
    path=[start]; used={start}; newd=[]
    def rec(k):
        if len(out) >= limit: return
        if k == len(word):
            out.append(list(path)); return
        nbrs = NB[path[-1]][:]; rnd.shuffle(nbrs)
        for y in nbrs:
            if y in used or board.cell[y] is not None: continue
            d = diag_key(path[-1], y)
            if d is not None and (d in board.edges or d in newd): continue
            me = frozenset((path[-1], y))
            path.append(y); used.add(y)
            if d is not None: newd.append(me)
            rec(k+1)
            path.pop(); used.discard(y)
            if d is not None: newd.pop()
            if len(out) >= limit: return
    if board.cell[start] is None:
        rec(1)
    return out

def place(board, word, path):
    added=[]
    for k,i in enumerate(path):
        board.cell[i]=word[k]
    for a,b in zip(path, path[1:]):
        if diag_key(a,b) is not None:
            e=frozenset((a,b)); board.edges.add(e); added.append(e)
    return added

def unplace(board, path, added):
    for i in path: board.cell[i]=None
    for e in added: board.edges.discard(e)

def spans(path):
    cols={p%C for p in path}; rows={p//C for p in path}
    return (0 in cols and C-1 in cols) or (0 in rows and R-1 in rows)

def ham_path(rnd, tries=200):
    """Random Hamiltonian path over the 6x8 king-move grid with no crossing diagonals."""
    for _ in range(tries):
        start=rnd.randrange(N)
        path=[start]; used={start}; diag=set()
        ok=True
        while len(path)<N:
            last=path[-1]
            opts=[]
            for y in NB[last]:
                if y in used: continue
                d=diag_key(last,y)
                if d is not None and d in diag: continue
                deg=sum(1 for z in NB[y] if z not in used and z!=y)
                opts.append((deg,y,d))
            if not opts: ok=False; break
            m=min(o[0] for o in opts)
            # mostly Warnsdorff (fewest onward moves), sometimes random, to keep shapes varied
            pool=[o for o in opts if o[0]==m] if rnd.random()<0.85 else opts
            deg,y,d=rnd.choice(pool)
            path.append(y); used.add(y)
            if d is not None: diag.add(frozenset((last,y)))
        if ok: return path
    return None

def solve(bundle, words, rnd, budget):
    for _ in range(max(1,budget//500)):
        hp=ham_path(rnd)
        if not hp: continue
        allw=[bundle]+list(words)
        for _ in range(60):
            rnd.shuffle(allw)
            pos=0; sol={}
            for w in allw:
                seg=hp[pos:pos+len(w)]; pos+=len(w)
                if rnd.random()<.5: seg=seg[::-1]
                sol[w]=seg
            if not spans(sol[bundle]): continue
            # avoid too many dead-straight words
            straight=sum(1 for w in allw if len({p//C for p in sol[w]})==1 or len({p%C for p in sol[w]})==1)
            if straight>2: continue
            board=Board()
            for w,seg in sol.items():
                for k,i in enumerate(seg): board.cell[i]=w[k]
            return board, sol
    return None

def choose_sets(bundle, cands, rnd, max_sets=40):
    need = N - len(bundle)
    sets=[]
    for k in range(4, 9):
        for combo in itertools.combinations(cands, k):
            if sum(len(w) for w in combo)==need:
                sets.append(list(combo))
    # prefer more words (5-7) and keep candidate order preference (earlier = more central)
    rnd.shuffle(sets)
    # keep the most important (earliest-listed) words; then prefer about 6 words
    sets.sort(key=lambda s: (-sum(1 for w in s if cands.index(w)<3), -min(len(s),7), -sum(2.0**-cands.index(w) for w in s)))
    return sets[:max_sets]

# ---------- hint-word dictionary ----------
def load_dict():
    from english_words import get_english_words_set
    from wordfreq import zipf_frequency
    from better_profanity import profanity
    base = {w for w in get_english_words_set(['web2'], lower=False, alpha=True) if w.islower() and 4 <= len(w) <= 12}
    bad = set()
    try:
        profanity.load_censor_words()
        bad = {str(w).lower() for w in profanity.CENSOR_WORDSET}
    except Exception: pass
    words = {w.upper() for w in base if zipf_frequency(w,'en') >= 2.6 and w not in bad}
    extra = os.path.join(os.path.dirname(__file__), 'extra_words.txt')
    if os.path.exists(extra):
        words |= {l.strip().upper() for l in open(extra) if l.strip() and not l.startswith('#')}
    return words

def find_words(cells, dictionary, prefixes):
    found=set()
    def dfs(i, s, used):
        if s not in prefixes: return
        if len(s)>=4 and s in dictionary: found.add(s)
        for y in NB[i]:
            if y not in used:
                used.add(y); dfs(y, s+cells[y], used); used.discard(y)
    for i in range(N): dfs(i, cells[i], {i})
    return found

def main():
    only = sys.argv[1:]  # optional theme indexes to rerun
    dictionary = load_dict()
    theme_words = {w for t in THEMES for w in t['w']} | {t['b'] for t in THEMES}
    dictionary |= {w for w in theme_words if len(w) <= 12}
    prefixes=set()
    for w in dictionary:
        for k in range(1,len(w)+1): prefixes.add(w[:k])
    import hashlib, multiprocessing as mp
    cache_f=os.path.join(os.path.dirname(__file__),'cache.json')
    cache=json.load(open(cache_f)) if os.path.exists(cache_f) else {}
    def h(t): return hashlib.md5(json.dumps([t['b'],t['w']]).encode()).hexdigest()
    todo=[i for i,t in enumerate(THEMES) if h(THEMES[i]) not in cache]
    with mp.Pool(min(8, os.cpu_count() or 2)) as pool:
        for i,res in zip(todo, pool.imap(solve_theme, todo)):
            cache[h(THEMES[i])]=res
            print(f"{i:3d} {'ok ' if res else 'FAIL'} {THEMES[i]['b']}", flush=True)
    json.dump(cache, open(cache_f,'w'))
    out=[]; fails=[]
    for idx,t in enumerate(THEMES):
        res=cache[h(t)]
        if not res: fails.append((idx,t['t'])); continue
        cells=list(res['g']); sol={k:v for k,v in res['path'].items()}
        b=t['b']
        theme=set(sol)
        hint=sorted(find_words(cells, dictionary, prefixes) - theme)
        out.append({"t":t['t'],"a":t.get('a',''),"b":b,"w":[w for w in sorted(sol, key=lambda w: min(sol[w])) if w!=b],
                    "p":t['p'],"g":res['g'],"path":sol,"x":' '.join(hint)})
    # Day order is locked in order.json so adding themes never moves a published day.
    # New themes are shuffled and appended to the end.
    order_f=os.path.join(os.path.dirname(__file__),'order.json')
    order=json.load(open(order_f)) if os.path.exists(order_f) else []
    byb={o['b']:o for o in out}
    assert len(byb)==len(out), "bundle words must be unique"
    new=[b for b in byb if b not in order]
    random.Random(len(order)).shuffle(new)
    order=[b for b in order if b in byb]+new
    json.dump(order, open(order_f,'w'), indent=0)
    out=[byb[b] for b in order]
    for f in fails: print("FAIL", f)
    js = "/* Bundle Branch puzzles. Generated by tools/bundle/gen.py. Do not edit by hand. */\nwindow.BUNDLE = " + json.dumps(out, separators=(',',':')) + ";\n"
    root=os.path.join(os.path.dirname(__file__),'..','..')
    open(os.path.join(root,'bundle-data.js'),'w').write(js)
    print(len(out),"puzzles,",len(fails),"failed; bytes",len(js))

def solve_theme(idx):
    t=THEMES[idx]
    if True:
        rnd=random.Random(1000+idx)
        b=t['b']; cands=t['w']
        bad=[w for w in [b]+cands if not w.isalpha() or not w.isupper()]
        assert not bad, (t['t'], bad)
        sets=choose_sets(b, cands, rnd)
        for attempt in range(6):
            for ws in sets[:12]:
                ws=sorted(ws, key=len, reverse=True)
                res=solve(b, ws, random.Random(attempt*7919+idx), budget=6000 if attempt==0 else 25000)
                if res:
                    board, sol = res
                    return {"g":''.join(board.cell), "path":sol}
        return None

if __name__=='__main__':
    main()
