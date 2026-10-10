"""ucl033-ucl051: finals, roles, nationalities, records."""
from collections import defaultdict

from ballion.registry import prompt
from ballion.wiki import resolve
from prompts.collectors.ucl_finals_parse import country_rec, final_events, final_motm
from prompts.collectors.ucl_util import dedupe, final_match, final_sides, played


def _all(years, pred=None, include_replay=False):
    recs = []
    for y in years:
        for team, sd in final_sides(y, include_replay):
            for p in sd["players"]:
                if played(p) and (pred is None or pred(p)):
                    recs.append({"answer": p["answer"], "enwiki": p["enwiki"], "detail": f"{y} final", "_p": p})
    return recs


def nat_prompt(pid, adj, flag):
    prompt(pid, f"Name {adj} player who played in a Champions League final, 2010 to 2026",
           "en:2010–2026 UEFA Champions League final pages — lineups, nationality from the flag icon "
           "(starters + used subs)",
           family="ucl-final-nationality")(lambda: dedupe(_all(range(2010, 2027), lambda p: p["country"] == flag)))


for _pid, _adj, _flag in [("ucl033", "a Brazilian", "Brazil"), ("ucl034", "an English", "England"),
                          ("ucl035", "a French", "France"), ("ucl036", "a German", "Germany"),
                          ("ucl037", "a Spanish", "Spain")]:
    nat_prompt(_pid, _adj, _flag)

CAF = {"Algeria", "Angola", "Benin", "Burkina Faso", "Cameroon", "Cape Verde", "Central African Republic", "Chad",
       "Comoros", "Congo", "DR Congo", "Democratic Republic of the Congo", "Egypt", "Equatorial Guinea", "Gabon",
       "Gambia", "The Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Ivory Coast", "Côte d'Ivoire", "Kenya", "Liberia",
       "Libya", "Mali", "Mauritania", "Morocco", "Mozambique", "Namibia", "Nigeria", "Senegal", "Sierra Leone",
       "South Africa", "Togo", "Tunisia", "Zambia", "Zimbabwe", "Uganda", "Tanzania", "Madagascar"}
CONMEBOL = {"Argentina", "Bolivia", "Chile", "Colombia", "Ecuador", "Paraguay", "Peru", "Uruguay", "Venezuela"}


@prompt("ucl038", "Name an African international who played in a Champions League final, 2010 to 2026",
        "en:2010–2026 UEFA Champions League final pages — lineups, CAF nation by flag icon (starters + used subs)",
        family="ucl-final-nationality")
def african_finals():
    return dedupe(_all(range(2010, 2027), lambda p: p["country"] in CAF))


@prompt("ucl039", "Name a South American player (not Brazilian) who played in a Champions League final, 2010 to 2026",
        "en:2010–2026 UEFA Champions League final pages — lineups, CONMEBOL nation by flag icon (starters + used subs)",
        family="ucl-final-nationality")
def sa_finals():
    return dedupe(_all(range(2010, 2027), lambda p: p["country"] in CONMEBOL))


@prompt("ucl040", "Name a country that had a player appear in a Champions League final, 2015 to 2026",
        "en:2015–2026 UEFA Champions League final pages — lineup flag icons (starters + used subs)",
        family="ucl-final-countries")
def final_countries():
    seen = defaultdict(set)
    import re
    for r in _all(range(2015, 2027)):
        if r["_p"]["country"]:
            seen[re.sub(r"\s*\(.*\)$", "", r["_p"]["country"])].add(r["detail"].split()[0])
    return dedupe([{**country_rec(c), "detail": "players in " + ", ".join(sorted(ys))} for c, ys in seen.items()])


@prompt("ucl041", "Name a player who came on as a substitute in a Champions League final, 2015 to 2026",
        "en:2015–2026 UEFA Champions League final pages — lineups, substitutes marked as coming on",
        family="ucl-final-roles")
def bench_finals():
    return dedupe([r for r in _all(range(2015, 2027), lambda p: p["subon"])])


@prompt("ucl042", "Name a goalkeeper who played in a Champions League final, 2010 to 2026",
        "en:2010–2026 UEFA Champions League final pages — lineups, GK rows (starters + used subs)",
        family="ucl-final-roles")
def gk_new():
    return dedupe(_all(range(2010, 2027), lambda p: p["pos"] == "GK"))


@prompt("ucl043", "Name a goalkeeper who played in a Champions League final, 1993 to 2009",
        "en:1993–2009 UEFA Champions League final pages — lineups, GK rows (starters + used subs)",
        family="ucl-final-roles")
def gk_old():
    return dedupe(_all(range(1993, 2010), lambda p: p["pos"] == "GK"))


@prompt("ucl044", "Name a player who captained a side in a Champions League final, 2010 to 2026",
        "en:2010–2026 UEFA Champions League final pages — lineups, starting captain marked (c)",
        family="ucl-final-roles")
def captains_new():
    return dedupe(_all(range(2010, 2027), lambda p: p["captain"] and p["started"]))


def managers(years):
    recs = []
    for y in years:
        m = final_match(y)
        for team, sd in zip(m["teams"], m["sides"]):
            if sd["manager"]:
                recs.append({"answer": sd["manager"][0], "enwiki": sd["manager"][1], "detail": f"{team}, {y} final"})
    return dedupe(recs)


@prompt("ucl045", "Name a manager who has managed in a Champions League final, 2015 to 2026",
        "en:2015–2026 UEFA Champions League final pages — lineups, manager rows (both benches)",
        family="ucl-final-managers")
def managers_new():
    return managers(range(2015, 2027))


@prompt("ucl046", "Name a manager who managed in a Champions League final, 1993 to 2014",
        "en:1993–2014 UEFA Champions League final pages — lineups, manager rows (both benches)",
        family="ucl-final-managers")
def managers_old():
    return managers(range(1993, 2015))


@prompt("ucl047", "Name a player who took a penalty in a Champions League final shoot-out, 2000 to 2026",
        "en:2000–2026 UEFA Champions League final pages — penalty shoot-out takers (scored or missed)",
        family="ucl-final-shootout")
def shootout_takers():
    recs = []
    for y in range(2000, 2027):
        for ev in final_events(y):
            for side, name, title in ev["pens"]:
                recs.append({"answer": name, "enwiki": title, "detail": f"{ev['teams'][side]}, {y} final shoot-out"})
    return dedupe(recs)


@prompt("ucl048", "Name a player who was named Player of the Match in a Champions League final, 2001 to 2026",
        "en:2001–2026 UEFA Champions League final pages — Man of the Match", family="ucl-final-roles")
def motm():
    recs = []
    for y in range(2001, 2027):
        m = final_motm(y)
        if m:
            recs.append({"answer": m[0], "enwiki": m[1], "detail": f"{y} final"})
    return dedupe(recs)


@prompt("ucl049", "Name a player who scored in a European Cup final, 1956 to 1992",
        "en:1956–1992 European Cup final pages — goalscorers (own goals excluded; replay included)",
        family="ucl-final-scorers")
def ec_scorers():
    recs = []
    for y in range(1956, 1993):
        for ev in final_events(y):
            for side, name, title, og in ev["goals"]:
                if not og:
                    recs.append({"answer": name, "enwiki": title, "detail": f"{y} final"})
    return dedupe(recs)


WINNERS = {1956: "Real Madrid", 1957: "Real Madrid", 1958: "Real Madrid", 1959: "Real Madrid", 1960: "Real Madrid",
           1961: "Benfica", 1962: "Benfica", 1963: "AC Milan", 1964: "Inter", 1965: "Inter", 1966: "Real Madrid",
           1967: "Celtic", 1968: "Manchester United", 1969: "AC Milan", 1970: "Feyenoord", 1971: "AFC Ajax",
           1972: "AFC Ajax", 1973: "AFC Ajax", 1974: "Bayern", 1975: "Bayern", 1976: "Bayern", 1977: "Liverpool",
           1978: "Liverpool", 1979: "Nottingham Forest", 1980: "Nottingham Forest", 1981: "Liverpool",
           1982: "Aston Villa", 1983: "Hamburger", 1984: "Liverpool", 1985: "Juventus", 1986: "Steaua",
           1987: "Porto", 1988: "PSV", 1989: "AC Milan", 1990: "AC Milan", 1991: "Red Star", 1992: "Barcelona"}


@prompt("ucl050", "Name a captain who lifted the European Cup, 1956 to 1992",
        "en:1956–1992 European Cup final pages — lineups, captain of the winning side",
        family="ucl-final-roles")
def winning_captains():
    recs = []
    for y, club in WINNERS.items():
        for team, sd in final_sides(y, include_replay=(y == 1974)):
            if club in team:
                for p in sd["players"]:
                    if p["captain"] and p["started"]:
                        recs.append({"answer": p["answer"], "enwiki": p["enwiki"], "detail": f"{team}, {y}"})
    return dedupe(recs)


@prompt("ucl051", "Name a player who has played in three or more Champions League finals (1993 to 2026)",
        "en:1993–2026 UEFA Champions League final pages — lineups; players counted across finals "
        "(starters + used subs)",
        family="ucl-final-roles")
def three_finals():
    cnt, ex = defaultdict(set), {}
    for r in _all(range(1993, 2027)):
        cnt[r["enwiki"]].add(int(r["detail"].split()[0]))
        ex[r["enwiki"]] = r
    res = resolve(list(cnt))
    agg = {}
    for t, ys in cnt.items():
        k = res[t]["title"]
        a = agg.setdefault(k, [set(), ex[t]])
        a[0] |= ys
    return dedupe([{"answer": r["answer"], "enwiki": r["enwiki"],
                    "detail": f"{len(ys)} finals: " + ", ".join(map(str, sorted(ys)))}
                   for k, (ys, r) in agg.items() if len(ys) >= 3])
