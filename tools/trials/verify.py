#!/usr/bin/env python3
"""Verify every Trial and Error entry against PubMed and build trial-data.js.

For each trial: find the article on PubMed by title + journal + year, record the
PMID, exact title, journal, year and DOI, and check that every number in the
result line appears in the PubMed abstract. Anything that doesn't match is
reported; the build stops if a trial can't be found.

Run:  python3 tools/trials/verify.py
"""
import difflib, json, re, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _t import TRIALS
import t1_critical, t2_cardio, t3_other  # noqa: F401  (register trials)

EU = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
CACHE = os.path.join(HERE, ".pubmed-cache.json")
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

def get(url):
    for k in range(4):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return r.read().decode("utf-8")
        except Exception as e:
            time.sleep(1.5 * (k + 1))
    raise RuntimeError("fetch failed: " + url)

def esearch(term):
    if term in cache: return cache[term]
    time.sleep(0.36)
    j = json.loads(get(EU + "esearch.fcgi?db=pubmed&retmode=json&retmax=12&term=" + urllib.parse.quote(term)))
    ids = j["esearchresult"]["idlist"]
    cache[term] = ids
    return ids

def clean_title(t):
    return re.sub(r"[\[\]():;,'\"?]", " ", t)

def find(tr):
    t = clean_title(tr["title"])
    tries = [
        f'{t}[ti] AND "{tr["journal"]}"[ta] AND {tr["year"]}[dp]',
        f'{t}[ti] AND "{tr["journal"]}"[ta]',
        f'{t}[ti]',
    ]
    for q in tries:
        ids = esearch(q)
        if ids: return ids, q
    return [], None

def efetch(ids):
    out = {}
    need = [i for i in ids if "x" + i not in cache]
    for k in range(0, len(need), 40):
        time.sleep(0.4)
        xml = get(EU + "efetch.fcgi?db=pubmed&retmode=xml&id=" + ",".join(need[k:k+40]))
        root = ET.fromstring(xml)
        for art in root.findall(".//PubmedArticle"):
            pmid = art.findtext(".//MedlineCitation/PMID")
            title = "".join(art.find(".//ArticleTitle").itertext()) if art.find(".//ArticleTitle") is not None else ""
            jt = art.findtext(".//Journal/ISOAbbreviation") or art.findtext(".//MedlineTA") or ""
            yr = art.findtext(".//JournalIssue/PubDate/Year") or (art.findtext(".//JournalIssue/PubDate/MedlineDate") or "")[:4]
            abst = " ".join("".join(a.itertext()) for a in art.findall(".//Abstract/AbstractText"))
            doi = ""
            for aid in art.findall(".//PubmedData/ArticleIdList/ArticleId"):
                if aid.get("IdType") == "doi": doi = aid.text or ""
            ptypes = [p.text for p in art.findall(".//PublicationType")]
            cache["x" + pmid] = {"title": title, "journal": jt, "year": yr, "abstract": abst, "doi": doi, "ptypes": ptypes}
    for i in ids: out[i] = cache.get("x" + i)
    return out

def norm(s):
    s = s.replace("\u00b7", ".").replace("−", "-").replace(" ", " ").replace(" ", " ")
    s = re.sub(r"(\d),(\d{3})", r"\1\2", s)
    return s

# Hand-checked PubMed IDs where the title search is ambiguous or picks a comment/letter.
OVERRIDE = {"6s":"22738085","ttm":"24237006","bougie":"34879143","proppr":"25647203","cast":"2473403",
            "cabana":"30874766","erspc":"19297566","albios":"24635772","basics":"34375394","hot-icu":"33471452",
            "flow":"38785209"}
problems = []
found = {}
for tr in TRIALS:
    if tr["id"] in OVERRIDE:
        found[tr["id"]] = [OVERRIDE[tr["id"]]]; continue
    ids, q = find(tr)
    if not ids:
        problems.append((tr["id"], "NOT FOUND on PubMed")); continue
    found[tr["id"]] = ids
json.dump(cache, open(CACHE, "w"))

allids = sorted({i for v in found.values() for i in v})
meta = efetch(allids)
json.dump(cache, open(CACHE, "w"))

out = []
for tr in TRIALS:
    if tr["id"] not in found: continue
    ids = found[tr["id"]]
    # prefer the candidate whose journal/year match and that has an abstract
    def score(i):
        m = meta.get(i) or {}
        s = 10 * difflib.SequenceMatcher(None, re.sub(r"\W+"," ",tr["title"].lower()), re.sub(r"\W+"," ",m.get("title","").lower())).ratio()
        pt = m.get("ptypes") or []
        if any(x in pt for x in ("Letter","Comment","Editorial","Published Erratum","News")): s -= 8
        if any("Trial" in x for x in pt): s += 3
        if m.get("abstract"): s += 4
        if str(tr["year"]) == m.get("year"): s += 2
        if tr["journal"].replace(".", "").lower() in m.get("journal", "").replace(".", "").lower(): s += 2
        if "Comment" in (m.get("ptypes") or []) or "Editorial" in (m.get("ptypes") or []): s -= 6
        return s
    best = max(ids, key=score)
    m = meta[best]
    if len(ids) > 1 and difflib.SequenceMatcher(None, tr["title"].lower(), m["title"].lower().rstrip(".")).ratio() < 0.9:
        problems.append((tr["id"], f"{len(ids)} PubMed matches; chose {best}: {m['title'][:90]}"))
    if str(tr["year"]) != m["year"]:
        problems.append((tr["id"], f"year {tr['year']} vs PubMed {m['year']}"))
    jn = m["journal"].replace(".", "").lower()
    if tr["journal"].replace(".", "").lower() not in jn:
        problems.append((tr["id"], f"journal {tr['journal']} vs PubMed {m['journal']}"))
    ab = norm(m["abstract"] + " " + m["title"])
    nums = re.findall(r"(?<![\w.])\d+(?:\.\d+)?", norm(tr["res"]))
    missing = [n for n in nums if not re.search(r"(?<![\d.])" + re.escape(n) + r"(?![\d])", ab)]
    if missing:
        problems.append((tr["id"], "numbers not in abstract: " + ", ".join(missing)))
    out.append({**tr, "pmid": best, "doi": m["doi"], "pmTitle": m["title"].rstrip("."), "pmJournal": m["journal"], "pmYear": m["year"]})

SHOW = set(sys.argv[1:])
for o in out:
    if o["id"] in SHOW:
        print("=== ", o["id"], o["pmid"], o["pmTitle"]); print(cache["x"+o["pmid"]]["abstract"]); print("RES:", o["res"]); print()
for p in problems: print("•", p[0], "—", p[1])
print(f"\n{len(out)} of {len(TRIALS)} trials matched; {len(problems)} notes.")
json.dump(out, open(os.path.join(HERE, ".verified.json"), "w"), indent=1)

# ---------- build trial-data.js (schedule order) ----------
if problems and any("NOT FOUND" in p[1] or "journal" in p[1] or "year" in p[1] for p in problems):
    sys.exit("Fix the problems above before building.")
ORDER = os.path.join(HERE, "order.json")
order = json.load(open(ORDER)) if os.path.exists(ORDER) else []
known = set(order)
new = [o["id"] for o in out if o["id"] not in known]
# place new trials in a shuffled order that avoids the same subject twice in a row
rnd = random.Random("trial-and-error:" + str(len(order)))
byid = {o["id"]: o for o in out}
rnd.shuffle(new)
seq = list(order)
pool = new[:]
while pool:
    last = byid[seq[-1]] if seq else None
    pick = next((i for i in pool if not last or (byid[i]["area"] != last["area"] and not (len(seq) > 1 and byid[seq[-2]]["ans"] == last["ans"] == byid[i]["ans"]))), pool[0])
    pool.remove(pick); seq.append(pick)
seq = [i for i in seq if i in byid]
json.dump(seq, open(ORDER, "w"), indent=0)
keep = ["id","name","journal","year","area","pop","int","ctl","out","ans","res","sum","pmid","doi","pmTitle"]
data = [{k: byid[i][k] for k in keep} for i in seq]
js = "// Trial and Error: generated by tools/trials/verify.py from the PubMed-verified bank. Do not edit by hand.\n"
js += "// Day N of the game shows TRIALS[(N-1) % TRIALS.length]. New trials are appended so past days never change.\n"
js += "window.TRIALS = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"
open(os.path.join(HERE, "..", "..", "trial-data.js"), "w").write(js)
print("wrote trial-data.js with", len(data), "trials")
