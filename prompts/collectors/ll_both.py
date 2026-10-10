"""ll136-ll147: players who played for both of two clubs (category intersection, verified against the infobox).

A candidate is in both clubs' Wikipedia categories; it counts only if the infobox senior career lists
the club (first team, not a B team) with at least 1 league appearance. Loans count.
"""
import re
from functools import lru_cache

from ballion.registry import prompt
from ballion.wiki import api, resolve
from prompts.collectors.ll_util import dedupe

CAT = {
    "rm": ("Real Madrid CF players", "Real Madrid CF", "Real Madrid"),
    "fcb": ("FC Barcelona players", "FC Barcelona", "Barcelona"),
    "atm": ("Atlético Madrid footballers", "Atlético Madrid", "Atlético Madrid"),
    "val": ("Valencia CF players", "Valencia CF", "Valencia"),
    "sev": ("Sevilla FC players", "Sevilla FC", "Sevilla"),
    "bet": ("Real Betis players", "Real Betis", "Real Betis"),
    "vil": ("Villarreal CF players", "Villarreal CF", "Villarreal"),
    "ath": ("Athletic Bilbao footballers", "Athletic Bilbao", "Athletic Club"),
    "rso": ("Real Sociedad footballers", "Real Sociedad", "Real Sociedad"),
    "gir": ("Girona FC players", "Girona FC", "Girona"),
    "get": ("Getafe CF footballers", "Getafe CF", "Getafe"),
}


@lru_cache(None)
def members(cat):
    out, cont = [], {}
    while True:
        d = api("en", action="query", list="categorymembers", cmtitle=f"Category:{cat}", cmlimit=500, cmnamespace=0, **cont)
        out += [m["title"] for m in d["query"]["categorymembers"]]
        if "continue" not in d:
            break
        cont = dict(d["continue"])
    return frozenset(out)


@lru_cache(None)
def career(title):
    """[(team link target, apps or None)] from the infobox wikitext of an article."""
    return _careers([title])[title]


_CACHE = {}


def _careers(titles):
    need = [t for t in titles if t not in _CACHE]
    for i in range(0, len(need), 50):
        chunk = need[i:i + 50]
        d = api("en", action="query", prop="revisions", rvprop="content", rvslots="main", titles="|".join(chunk), redirects=1)
        alias = {}
        for k in ("normalized", "redirects"):
            for m in d["query"].get(k, []):
                alias[m["from"]] = m["to"]
        text = {}
        for p in d["query"]["pages"]:
            if p.get("revisions"):
                text[p["title"]] = p["revisions"][0]["slots"]["main"]["content"]
        for t in chunk:
            c = t
            while c in alias:
                c = alias[c]
            _CACHE[t] = _parse(text.get(c, ""))
    return {t: _CACHE[t] for t in titles}


def _parse(wt):
    rows = {}
    for m in re.finditer(r"\|\s*(clubs|caps|years)(\d+)\s*=\s*([^\n|]*(?:\[\[[^\]]*\]\][^\n|]*)*)", wt):
        rows.setdefault(int(m.group(2)), {})[m.group(1)] = m.group(3)
    out = []
    for n in sorted(rows):
        r = rows[n]
        lk = re.search(r"\[\[([^\]|#]+)", r.get("clubs", ""))
        if not lk:
            continue
        cap = re.match(r"\s*(\d+)", re.sub(r"<[^>]*>|\{\{[^}]*\}\}", "", r.get("caps", "")))
        out.append((lk.group(1).strip(), int(cap.group(1)) if cap else None))
    return out


def both(a, b):
    cat_a, canon_a, _ = CAT[a]
    cat_b, canon_b, _ = CAT[b]
    cands = sorted(members(cat_a) & members(cat_b))
    careers = _careers(cands)
    targets = {t for c in careers.values() for t, _ in c} | {canon_a, canon_b}
    res = resolve(list(targets))
    ca, cb = res[canon_a]["title"], res[canon_b]["title"]
    out = []
    for p in cands:
        got = {}
        for t, apps in careers[p]:
            ct = res[t]["title"]
            if apps and apps > 0:
                got[ct] = got.get(ct, 0) + apps
        if ca in got and cb in got:
            out.append({"answer": re.sub(r"\s*\([^)]*\)$", "", p), "enwiki": p,
                        "detail": f"{got[ca]} apps for {CAT[a][2]}, {got[cb]} for {CAT[b][2]}"})
    return dedupe(out)


def _pair(pid, a, b, src):
    @prompt(pid, f"Name a player who has played for both {CAT[a][2]} and {CAT[b][2]}",
            f"en:Category:{CAT[a][0]} ∩ Category:{CAT[b][0]} — verified by infobox (1+ league appearance for each senior team)",
            family="ll-played-for-both")
    def fn():
        return both(a, b)
    return fn


for pid, a, b in [
    ("ll136", "rm", "atm"), ("ll137", "fcb", "atm"), ("ll138", "fcb", "val"), ("ll139", "fcb", "sev"),
    ("ll140", "rm", "sev"), ("ll141", "rm", "bet"), ("ll142", "fcb", "bet"), ("ll143", "atm", "sev"),
    ("ll144", "val", "vil"), ("ll145", "ath", "rso"), ("ll146", "fcb", "gir"), ("ll147", "rm", "get"),
]:
    _pair(pid, a, b, None)
