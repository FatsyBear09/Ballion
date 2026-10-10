"""nat: MLS-based players, future venues, Euro-final venues, frozen current squads, women's / youth / Olympic prompts."""
import re

from ballion.registry import prompt
from ballion.tables import rows, wikitables
from ballion.wiki import resolve
from prompts.collectors.nat_squads import ASIA23, WC26, _players  # noqa: F401
from prompts.collectors.nat_tournaments import _venue_fn, name_from_title, scorers, section_nodes, venues
from prompts.collectors.nat_util import dedupe, player_recs, resolve as _r, soup_noflags, squads, team_titles  # noqa: F401


# ------------------------------------------------------------------ MLS-based players at the 2026 World Cup
@prompt("nat113", "Name a player at the 2026 World Cup who played for a Major League Soccer club (club at the start of the tournament)",
        "en:2026 FIFA World Cup squads — club column, matched against the club table of en:Major League Soccer",
        family="nat-league-at-tournament")
def _nat113():
    mls = []
    for t in wikitables("Major League Soccer"):
        rs = list(rows(t))
        if rs[0][0][:3] == ["Conference", "Club", "Location"]:
            mls = [ln[1][-1] for tx, ln in rs[1:] if ln[1]]
            break
    ps = [p for _, p in _players(WC26) if p["club"]]
    r = resolve(list({p["club"] for p in ps} | set(mls)))
    canon = {r[m]["title"] for m in mls}
    return player_recs([p for p in ps if r[p["club"]]["title"] in canon], lambda p: p["clubtxt"])


# ------------------------------------------------------------------ future venues
@prompt("nat133", "Name a stadium chosen to host a match at the 2030 World Cup or Euro 2028 (planned venues as of October 2026)",
        "en:2030 FIFA World Cup#Proposed venues, en:UEFA Euro 2028#Venues", family="nat-stadium")
def _nat133():
    return _venue_fn([("2030 FIFA World Cup", "Proposed venues"), ("UEFA Euro 2028", "Venues")])()


# ------------------------------------------------------------------ Euro final venues
@prompt("nat138", "Name a stadium that has hosted a men's European Championship final",
        "en:List of UEFA European Championship finals — venue column", family="nat-stadium")
def _nat138():
    t = next(t for t in wikitables("List of UEFA European Championship finals")
             if rows(t) and next(rows(t))[0][:5] == ["Year", "Winners", "Score", "Runners-up", "Venue"])
    out = {}
    for tx, ln in list(rows(t))[1:]:
        if re.fullmatch(r"\d{4}", tx[0]) and ln[4]:
            out.setdefault(ln[4][-1], []).append(tx[0])
    from collections import Counter
    cnt = Counter(name_from_title(l) for l in out)
    recs = [{"answer": name_from_title(l) if cnt[name_from_title(l)] == 1 else l, "enwiki": l,
             "detail": "final " + ", ".join(ys)} for l, ys in out.items()]
    return dedupe(recs)


# ------------------------------------------------------------------ frozen current squads
def _current(page):
    def fn():
        s = soup_noflags(page)
        recs = []
        for sec in ("Current squad", "Recent call-ups"):
            for n in section_nodes(s, sec):
                for t in ([n] if n.name == "table" else n.find_all("table")):
                    rs = list(rows(t))
                    h = [re.sub(r"\s+", " ", c) for c in rs[0][0]]
                    if "Player" not in h:
                        continue
                    pi = h.index("Player")
                    for tx, ln in rs[1:]:
                        ls = [x for x in ln[pi] if "(association football)" not in x]
                        if ls:
                            recs.append({"answer": name_from_title(ls[-1]), "enwiki": ls[-1], "detail": sec.lower()})
        return dedupe(recs)
    return fn


CURRENT = [
    ("nat139", "England", "England national football team"),
    ("nat140", "France", "France national football team"),
    ("nat141", "Brazil", "Brazil national football team"),
    ("nat142", "Argentina", "Argentina national football team"),
    ("nat143", "Spain", "Spain national football team"),
    ("nat144", "Germany", "Germany national football team"),
    ("nat145", "Portugal", "Portugal national football team"),
    ("nat146", "Italy", "Italy national football team"),
    ("nat147", "the Netherlands", "Netherlands national football team"),
    ("nat148", "the United States", "United States men's national soccer team"),
]
for _pid, _name, _page in CURRENT:
    poss = _name + ("'" if _name.endswith("s") else "'s")
    prompt(_pid, f"Name a player in {poss} current squad or recent call-ups (as of October 2026)",
           f"en:{_page} — Current squad + Recent call-ups (snapshot October 2026)", family="nat-current-squad")(_current(_page))


# ------------------------------------------------------------------ women's / youth / Olympic
WWC23 = "2023 FIFA Women's World Cup squads"
WEURO25 = "UEFA Women's Euro 2025 squads"
U21_23 = "2023 UEFA European Under-21 Championship squads"
OLY24 = "Football at the 2024 Summer Olympics – Men's team squads"


def _team_squad(page, team):
    return lambda: player_recs([p for _, p in _players(page, {team})],
                               lambda p: f"#{p['no']} {p['pos']}, {p['clubtxt']}")


prompt("nat192", "Name a player in Spain's 2023 Women's World Cup-winning squad",
       f"en:{WWC23} — Spain section", family="nat-squad")(_team_squad(WWC23, "Spain"))
prompt("nat193", "Name a player in England's Women's Euro 2025-winning squad",
       f"en:{WEURO25} — England section", family="nat-squad")(_team_squad(WEURO25, "England"))
prompt("nat194", "Name a player in England's 2023 UEFA European Under-21 Championship-winning squad",
       f"en:{U21_23} — England section", family="nat-squad")(_team_squad(U21_23, "England"))
prompt("nat195", "Name a player in Spain's 2024 Olympic gold-medal squad (men's tournament)",
       f"en:{OLY24} — Spain section", family="nat-squad")(_team_squad(OLY24, "Spain"))

prompt("nat196", "Name a player who scored at the 2023 Women's World Cup (own goals excluded)",
       "en:2023 FIFA Women's World Cup — Goalscorers section", family="nat-scorer-at-tournament")(
    lambda: dedupe([{"answer": name_from_title(l), "enwiki": l, "detail": f"{n} goals"}
                    for a, l, n in scorers("2023 FIFA Women's World Cup")]))
prompt("nat198", "Name a player who scored at Women's Euro 2025 (own goals excluded)",
       "en:UEFA Women's Euro 2025 — Goalscorers section", family="nat-scorer-at-tournament")(
    lambda: dedupe([{"answer": name_from_title(l), "enwiki": l, "detail": f"{n} goals"}
                    for a, l, n in scorers("UEFA Women's Euro 2025")]))


def _women_team(name):
    cands = [f"{name} women's national football team", f"{name} women's national soccer team"]
    r = resolve(cands)
    for c in cands:
        if not r[c]["missing"]:
            return r[c]["title"]
    raise LookupError(name)


def _women_countries(page):
    def fn():
        return dedupe([{"answer": n, "enwiki": _women_team(n), "detail": ""} for n in squads(page)])
    return fn


prompt("nat197", "Name a country that played at Women's Euro 2025", f"en:{WEURO25} — team sections",
       family="nat-country-at-tournament")(_women_countries(WEURO25))
prompt("nat199", "Name a country that played at the 2023 Women's World Cup", f"en:{WWC23} — team sections",
       family="nat-country-at-tournament")(_women_countries(WWC23))


@prompt("nat200", "Name a country that played in the men's football tournament at the 2024 Olympics",
        f"en:{OLY24} — team sections (answers link to the senior men's national team)", family="nat-country-at-tournament")
def _nat200():
    tt = team_titles(list(squads(OLY24)))
    return dedupe([{"answer": n, "enwiki": t, "detail": "Olympics 2024"} for n, t in tt.items()])
