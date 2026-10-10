"""ll097, ll148-ll180: foreign players in La Liga by nationality (and by club)."""
import re

from ballion.registry import prompt
from ballion.wiki import resolve
from prompts.collectors.ll_foreign import sections
from prompts.collectors.ll_util import clean, dedupe

FOREIGN = "List of foreign La Liga players"
ARG = "List of Argentine footballers in La Liga"
BRA = "List of Brazilian footballers in La Liga"

CLUB = {"rm": "Real Madrid CF", "fcb": "FC Barcelona", "atm": "Atlético Madrid", "sev": "Sevilla FC", "val": "Valencia CF"}


def entries(page, names):
    out = []
    S = sections(page)
    for n in names:
        if n not in S:
            raise LookupError(f"{page}: no section {n!r}")
        out += S[n]
    return out


def letters(page):
    return [k for k in sections(page) if re.fullmatch(r"[A-Z]", k)]


def _recs(ents, since=None, club=None):
    sel = []
    for e in ents:
        if since is not None and (e["last"] is None or e["last"] < since):
            continue
        sel.append(e)
    if club:
        titles = {t for e in sel for t, _ in e["clubs"]} | {club}
        res = resolve(list(titles))
        sel = [e for e in sel if any(res[t]["title"] == club for t, _ in e["clubs"])]
    return dedupe([{"answer": clean(e["name"]), "enwiki": e["title"], "detail": re.sub(r"^.*? – ", "", e["text"])[:80]} for e in sel])


def _nat(pid, text, page, names, since, fam="ll-nationality", club=None, src=None):
    sec = "; ".join(names) if len(names) < 6 else f"{len(names)} sections"
    @prompt(pid, text, src or f"en:{page} — {sec}" + (f" (La Liga seasons from {since}–{str(since + 1)[2:]})" if since else ""), family=fam)
    def fn():
        nm = names if page == FOREIGN else letters(page)
        return _recs(entries(page, nm), since, club)
    return fn


# ---------------------------------------------------------------- by nationality
for pid, text, page, names, since in [
    ("ll148", "Name a Uruguayan who has played in La Liga since 2015–16", FOREIGN, ["Uruguay"], 2015),
    ("ll149", "Name a French player who has played in La Liga since 2015–16", FOREIGN, ["France"], 2015),
    ("ll150", "Name a Portuguese player who has played in La Liga since 2015–16", FOREIGN, ["Portugal"], 2015),
    ("ll151", "Name an Argentine who has played in La Liga since 2020–21", ARG, ["A–Z"], 2020),
    ("ll152", "Name a Brazilian who has played in La Liga since 2018–19", BRA, ["A–Z"], 2018),
    ("ll153", "Name a Moroccan who has played in La Liga", FOREIGN, ["Morocco"], None),
    ("ll154", "Name a Dutch player who has played in La Liga since 2000–01", FOREIGN, ["Netherlands"], 2000),
    ("ll155", "Name an Italian who has played in La Liga since 2000–01", FOREIGN, ["Italy"], 2000),
    ("ll156", "Name a Colombian who has played in La Liga since 2010–11", FOREIGN, ["Colombia"], 2010),
    ("ll157", "Name a Mexican who has played in La Liga", FOREIGN, ["Mexico"], None),
    ("ll158", "Name a Nigerian who has played in La Liga", FOREIGN, ["Nigeria"], None),
    ("ll159", "Name a Senegalese player who has played in La Liga", FOREIGN, ["Senegal"], None),
    ("ll160", "Name a player from England, Scotland, Wales, Northern Ireland or the Republic of Ireland who has played in La Liga",
     FOREIGN, ["England", "Scotland", "Wales", "Northern Ireland", "Republic of Ireland"], None),
    ("ll161", "Name a Danish, Swedish, Norwegian, Finnish or Icelandic player who has played in La Liga since 2010–11",
     FOREIGN, ["Denmark", "Sweden", "Norway", "Finland", "Iceland"], 2010),
    ("ll163", "Name an American or Canadian who has played in La Liga", FOREIGN, ["United States of America", "Canada"], None),
    ("ll164", "Name a Belgian who has played in La Liga", FOREIGN, ["Belgium"], None),
    ("ll165", "Name a Serbian, Montenegrin or Bosnian player who has played in La Liga since 2010–11",
     FOREIGN, ["Serbia", "Montenegro", "Bosnia and Herzegovina"], 2010),
    ("ll166", "Name a Croatian who has played in La Liga since 2000–01", FOREIGN, ["Croatia"], 2000),
    ("ll167", "Name a Ukrainian, Georgian or Russian player who has played in La Liga since 2015–16",
     FOREIGN, ["Ukraine", "Georgia", "Russia"], 2015),
]:
    _nat(pid, text, page, names, since)


@prompt("ll162", "Name a player from Asia or Australia who has played in La Liga",
        "en:List of foreign La Liga players — Asia (AFC) sections", family="ll-nationality")
def ll162():
    S = sections(FOREIGN)
    keys = list(S)
    i = next(i for i, k in enumerate(keys) if k.startswith("Asia"))
    j = next(j for j, k in enumerate(keys) if j > i and (k.startswith(("Europe", "North America", "Oceania", "South America")) and not k.startswith("Asia")))
    out = []
    for k in keys[i + 1:j]:
        out += S[k]
    return _recs(out)


# ---------------------------------------------------------------- nationality at a club
for pid, text, page, names, club in [
    ("ll168", "Name a Brazilian who has played for Real Madrid", BRA, ["A–Z"], "rm"),
    ("ll169", "Name a Brazilian who has played for Barcelona", BRA, ["A–Z"], "fcb"),
    ("ll170", "Name a Brazilian who has played for Atlético Madrid", BRA, ["A–Z"], "atm"),
    ("ll171", "Name an Argentine who has played for Atlético Madrid", ARG, ["A–Z"], "atm"),
    ("ll172", "Name an Argentine who has played for Real Madrid", ARG, ["A–Z"], "rm"),
    ("ll173", "Name an Argentine who has played for Barcelona", ARG, ["A–Z"], "fcb"),
    ("ll174", "Name an Argentine who has played for Sevilla", ARG, ["A–Z"], "sev"),
    ("ll175", "Name an Argentine who has played for Valencia", ARG, ["A–Z"], "val"),
    ("ll176", "Name a French player who has played for Barcelona", FOREIGN, ["France"], "fcb"),
    ("ll177", "Name a French player who has played for Real Madrid", FOREIGN, ["France"], "rm"),
    ("ll178", "Name a French player who has played for Sevilla", FOREIGN, ["France"], "sev"),
    ("ll179", "Name a Uruguayan who has played for Atlético Madrid", FOREIGN, ["Uruguay"], "atm"),
    ("ll180", "Name a Dutch player who has played for Barcelona", FOREIGN, ["Netherlands"], "fcb"),
]:
    _nat(pid, text, page, names, None, fam="ll-nationality-club", club=CLUB[club],
         src=f"en:{page} — {'; '.join(names)}, clubs list includes {CLUB[club]}")


# ---------------------------------------------------------------- African countries

@prompt("ll097", "Name an African country that has had a player in La Liga",
        "en:List of foreign La Liga players — Africa (CAF) country sections (national football team articles)")
def ll097():
    S = sections(FOREIGN)
    keys = list(S)
    i = keys.index("Africa (CAF)")
    j = next(j for j, k in enumerate(keys) if j > i and k.startswith(("Asia", "Europe", "North America", "South America", "Oceania")))
    recs = []
    for k in keys[i + 1:j]:
        if S[k]:
            recs.append({"answer": k, "enwiki": f"{k} national football team", "detail": f"{len(S[k])} players"})
    return dedupe(recs)
