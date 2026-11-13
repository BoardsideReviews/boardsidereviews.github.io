TRIALS = []
KEYS = ["id","name","journal","year","title","area","pop","int","ctl","out","ans","res","sum"]
def T(*a):
    assert len(a) == len(KEYS), (a[0], len(a))
    d = dict(zip(KEYS, a))
    assert d["ans"] in ("pos","neu","neg"), d["id"]
    TRIALS.append(d)
