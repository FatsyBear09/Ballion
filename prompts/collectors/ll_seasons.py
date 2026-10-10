"""ll040-ll067, ll124, ll189, ll192-ll197: club-season squads and scorers."""
import re

from ballion.registry import prompt
from prompts.collectors.ll_util import club_scorers, dedupe, season_label, squad

PAGE = {  # club key -> season-page format
    "rm": "{s} Real Madrid CF season", "fcb": "{s} FC Barcelona season", "atm": "{s} Atlético Madrid season",
    "gir": "{s} Girona FC season", "vil": "{s} Villarreal CF season", "sev": "{s} Sevilla FC season",
    "bet": "{s} Real Betis season", "ath": "{s} Athletic Bilbao season", "rso": "{s} Real Sociedad season",
    "val": "{s} Valencia CF season",
}
SQUAD_EXTRA = ("Squad information", "Squad", "First team squad", "Players and staff")


def squad_union(club, years, women=None):
    recs = []
    for y in years:
        s = season_label(y)
        page = (women or PAGE[club]).format(s=s)
        got = squad(page, SQUAD_EXTRA)
        if not got:
            raise LookupError(f"{page}: empty squad")
        for name, title, pos in got:
            recs.append({"answer": name, "enwiki": title, "detail": f"{s} squad ({pos})"})
    return dedupe(recs)


def _squad(pid, text, club, years, src):
    @prompt(pid, text, src, family="ll-squad")
    def fn():
        return squad_union(club, years)
    return fn


def _src(club, years):
    pg = [PAGE[club].format(s=season_label(y)) for y in years]
    return "en:" + (pg[0] if len(pg) == 1 else f"{pg[0]} … {pg[-1]}") + " — first-team squad table"


for pid, text, club, years in [
    ("ll040", "Name a player in a Real Madrid squad that won La Liga in 2016–17, 2019–20, 2021–22 or 2023–24", "rm", (2016, 2019, 2021, 2023)),
    ("ll041", "Name a player in Real Madrid's 2024–25 first-team squad", "rm", (2024,)),
    ("ll042", "Name a player in a Barcelona squad that won La Liga in 2014–15, 2015–16, 2017–18 or 2018–19", "fcb", (2014, 2015, 2017, 2018)),
    ("ll043", "Name a player in Barcelona's 2024–25 first-team squad", "fcb", (2024,)),
    ("ll044", "Name a player in a Barcelona squad under Pep Guardiola (2008–09 to 2011–12)", "fcb", (2008, 2009, 2010, 2011)),
    ("ll045", "Name a player in an Atlético Madrid squad that won La Liga in 2013–14 or 2020–21", "atm", (2013, 2020)),
    ("ll046", "Name a player in Atlético Madrid's 2024–25 first-team squad", "atm", (2024,)),
    ("ll047", "Name a player in Girona's 2023–24 squad (third in La Liga, first Champions League qualification)", "gir", (2023,)),
    ("ll048", "Name a player in Villarreal's 2020–21 squad (Europa League winners)", "vil", (2020,)),
    ("ll049", "Name a player in Sevilla's 2019–20 squad (Europa League winners)", "sev", (2019,)),
    ("ll050", "Name a player in Sevilla's 2022–23 squad (Europa League winners)", "sev", (2022,)),
    ("ll051", "Name a player in Real Betis's 2021–22 squad (Copa del Rey winners)", "bet", (2021,)),
    ("ll052", "Name a player in Athletic Club's 2023–24 squad (Copa del Rey winners)", "ath", (2023,)),
    ("ll053", "Name a player in an Athletic Club first-team squad from 2020–21 to 2025–26", "ath", tuple(range(2020, 2026))),
    ("ll054", "Name a player in Real Sociedad's 2022–23 squad (fourth in La Liga)", "rso", (2022,)),
    ("ll055", "Name a player in Real Sociedad's 2019–20 squad (Copa del Rey winners, played in 2021)", "rso", (2019,)),
    ("ll056", "Name a player in Valencia's 2018–19 squad (Copa del Rey winners)", "val", (2018,)),
    ("ll057", "Name a player in a Barcelona squad under Xavi (2021–22 to 2023–24)", "fcb", (2021, 2022, 2023)),
    # ll124 dropped: the 2021–22 Valencia season page has no squad table.
]:
    _squad(pid, text, club, years, _src(club, years))


@prompt("ll189", "Name a player in Real Madrid Femenino's 2024–25 squad", "en:2024–25 Real Madrid Femenino season — squad table",
        family="ll-squad")
def ll189():
    return squad_union(None, (2024,), women="{s} Real Madrid Femenino season")


# ---------------------------------------------------------------- scorers for a club in a season

def _scorers(pid, club_name, club, y, extra=""):
    s = season_label(y)
    page = PAGE[club].format(s=s)

    @prompt(pid, f"Name a player who scored for {club_name} in {s} in any competition{extra}",
            f"en:{page} — goalscorers / squad statistics (goals > 0)", family="ll-club-scorers")
    def fn():
        return dedupe([{"answer": n, "enwiki": t, "detail": f"{g} goal{'s' if g != 1 else ''}, {s}"}
                       for n, t, g in club_scorers(page)])
    return fn


for pid, cn, club, y, ex in [
    ("ll058", "Real Madrid", "rm", 2016, ""), ("ll059", "Real Madrid", "rm", 2024, ""),
    ("ll060", "Real Madrid", "rm", 2025, ""), ("ll196", "Real Madrid", "rm", 2021, ""),
    ("ll061", "Barcelona", "fcb", 2024, ""), ("ll062", "Barcelona", "fcb", 2025, ""),
    ("ll197", "Barcelona", "fcb", 2014, " (the MSN treble season)"),
    ("ll063", "Atlético Madrid", "atm", 2020, ""), ("ll192", "Atlético Madrid", "atm", 2024, ""),
    ("ll064", "Villarreal", "vil", 2024, ""), ("ll065", "Real Sociedad", "rso", 2022, ""),
    ("ll066", "Real Betis", "bet", 2024, ""), ("ll067", "Girona", "gir", 2023, ""),
    ("ll193", "Athletic Club", "ath", 2024, ""),
]:
    _scorers(pid, cn, club, y, ex)
