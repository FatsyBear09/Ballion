"""ucl001-ucl051: who played in Champions League / European Cup finals."""
from ballion.registry import prompt
from prompts.collectors.ucl_util import dedupe, final_players, played, final_sides, final_match

# ---------------------------------------------------------------- single finals

SINGLE = [
    ("ucl001", 2026, "PSG v Arsenal"), ("ucl002", 2025, "PSG 5–0 Inter"), ("ucl003", 2024, "Dortmund v Real Madrid"),
    ("ucl004", 2023, "Man City v Inter"), ("ucl005", 2022, "Liverpool v Real Madrid"),
    ("ucl006", 2021, "Man City v Chelsea"), ("ucl007", 2020, "PSG v Bayern"),
    ("ucl008", 2019, "Tottenham v Liverpool"), ("ucl009", 2018, "Real Madrid v Liverpool"),
    ("ucl010", 2017, "Juventus v Real Madrid"), ("ucl011", 2016, "Real Madrid v Atlético"),
    ("ucl012", 2015, "Juventus v Barcelona"), ("ucl013", 2014, "Real Madrid v Atlético, Lisbon"),
    ("ucl014", 2012, "Bayern v Chelsea"), ("ucl015", 2008, "Man United v Chelsea, Moscow"),
    ("ucl016", 2005, "Milan v Liverpool, Istanbul"), ("ucl017", 1999, "Man United v Bayern"),
]


def _single(year, tag):
    def fn():
        return dedupe(final_players(year, include_replay=False))
    return fn


for _pid, _y, _tag in SINGLE:
    prompt(_pid, f"Name a player who played in the {_y} Champions League final ({_tag})",
           f"en:{_y} UEFA Champions League final — lineups (starters + used substitutes)",
           family="ucl-final-players")(_single(_y, _tag))

ENGLISH = {"Liverpool F.C.", "Tottenham Hotspur F.C.", "Chelsea F.C.", "Manchester City F.C.", "Arsenal F.C."}


def _eng_since_2018():
    recs = []
    for y in range(2018, 2027):
        if y == 2020:
            continue
        recs += final_players(y, club=ENGLISH, include_replay=False)
    return dedupe([r for r in recs if r["_team"] in ENGLISH])


@prompt("ucl018", "Name a player who played in a Champions League final for an English club, 2018 to 2026",
        "en:2018–2026 UEFA Champions League final pages — English clubs' lineups (starters + used subs)",
        family="ucl-final-players-era")
def eng_finals():
    return _eng_since_2018()


# ---------------------------------------------------------------- club across eras

def club_finals(club_keys, years):
    """club_keys: substrings of the club's article title."""
    def fn():
        recs = []
        for y in years:
            for team, sd in final_sides(y):
                if any(k in team for k in club_keys):
                    for p in sd["players"]:
                        if played(p):
                            recs.append({"answer": p["answer"], "enwiki": p["enwiki"], "detail": f"{y} final"})
        return dedupe(recs)
    return fn


def both_clubs(years):
    def fn():
        recs = []
        for y in years:
            for team, sd in final_sides(y):
                for p in sd["players"]:
                    if played(p):
                        recs.append({"answer": p["answer"], "enwiki": p["enwiki"], "detail": f"{y} final"})
        return dedupe(recs)
    return fn


CLUB_ERA = [
    ("ucl019", "Name a player who played in a Champions League final for Barcelona (2006, 2009 or 2011)",
     "en:2006 / 2009 / 2011 UEFA Champions League final — Barcelona lineup", ["Barcelona"], [2006, 2009, 2011]),
    ("ucl020", "Name a player who played in a Champions League final for Manchester United (1999, 2008, 2009 or 2011)",
     "en:1999 / 2008 / 2009 / 2011 UEFA Champions League final — Man United lineup", ["Manchester United"],
     [1999, 2008, 2009, 2011]),
    ("ucl021", "Name a player who played in a Champions League final for Juventus (1996, 1997, 1998, 2003, 2015 or 2017)",
     "en:Juventus lineups in the 1996, 1997, 1998, 2003, 2015, 2017 UEFA Champions League finals", ["Juventus"],
     [1996, 1997, 1998, 2003, 2015, 2017]),
    ("ucl022", "Name a player who played in a Champions League final for Real Madrid (1998, 2000 or 2002)",
     "en:1998 / 2000 / 2002 UEFA Champions League final — Real Madrid lineup", ["Real Madrid"], [1998, 2000, 2002]),
    ("ucl023", "Name a player who played in a Champions League final for Bayern Munich (1999, 2001, 2010, 2012 or 2013)",
     "en:Bayern lineups in the 1999, 2001, 2010, 2012, 2013 UEFA Champions League finals", ["Bayern"],
     [1999, 2001, 2010, 2012, 2013]),
    ("ucl024", "Name a player who played in a European Cup final for Real Madrid, 1956–1960",
     "en:1956–1960 European Cup final pages — Real Madrid lineups", ["Real Madrid"], range(1956, 1961)),
    ("ucl025", "Name a player who played in a European Cup final for Benfica, Inter or Milan, 1961–1965",
     "en:1961–1965 European Cup final pages — Benfica, Inter and Milan lineups", ["Benfica", "Inter", "Milan"],
     range(1961, 1966)),
    ("ucl027", "Name a player who played in a European Cup final for Ajax, 1971–1973",
     "en:1971–1973 European Cup final pages — Ajax lineups", ["Ajax"], range(1971, 1974)),
    ("ucl028", "Name a player who played in a European Cup final for Bayern Munich, 1974–1976",
     "en:1974–1976 European Cup final pages — Bayern lineups (incl. 1974 replay)", ["Bayern"], range(1974, 1977)),
    ("ucl029", "Name a player who played in a European Cup final for Liverpool (1977, 1978, 1981 or 1984)",
     "en:1977 / 1978 / 1981 / 1984 European Cup final pages — Liverpool lineups", ["Liverpool"],
     [1977, 1978, 1981, 1984]),
    ("ucl030", "Name a player who played in a European Cup final for Nottingham Forest or Aston Villa (1979, 1980 or 1982)",
     "en:1979 / 1980 / 1982 European Cup final pages — Forest and Villa lineups", ["Nottingham Forest", "Aston Villa"],
     [1979, 1980, 1982]),
    ("ucl031", "Name a player who played in a European Cup / Champions League final for AC Milan "
               "(1989, 1990, 1993, 1994 or 1995)",
     "en:AC Milan lineups in the 1989, 1990, 1993, 1994, 1995 finals", ["AC Milan"], [1989, 1990, 1993, 1994, 1995]),
    ("ucl032", "Name a player who played in a Champions League final for Ajax (1995 or 1996)",
     "en:1995 / 1996 UEFA Champions League final — Ajax lineups", ["Ajax"], [1995, 1996]),
]
for _pid, _t, _s, _k, _y in CLUB_ERA:
    prompt(_pid, _t, _s, family="ucl-final-club-era")(club_finals(_k, list(_y)))


@prompt("ucl026", "Name a player who played in the 1967 or 1968 European Cup final",
        "en:1967 and 1968 European Cup final pages — both teams' lineups", family="ucl-final-club-era")
def f6768():
    return both_clubs([1967, 1968])()
