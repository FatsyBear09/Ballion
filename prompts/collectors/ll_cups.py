"""Cup finals: ll021, ll068-ll083, ll186, ll200 (+ ll075-ll077 scorers)."""
import re

from ballion.registry import prompt
from prompts.collectors.ll_util import clean, dedupe, matches


def nm(title):
    return re.sub(r"\s*\([^)]*\)$", "", title)


def _is(team, *needles):
    name, title = team
    s = f"{name} {title}"
    return any(n in s for n in needles)


def appeared(page, team_filter=None, detail=""):
    """Starters + used substitutes of the (first) match on `page`, optionally only for teams passing team_filter."""
    ms = matches(page)
    if not ms:
        raise LookupError(f"{page}: no match box")
    m = ms[0]
    if not m["lineups"]:
        raise LookupError(f"{page}: no line-ups")
    out = []
    for side, lu in zip(("home", "away"), m["lineups"]):
        team = m[side]
        if team_filter and not team_filter(team):
            continue
        for title, name in lu["starters"] + lu["used"]:
            out.append({"answer": clean(name), "enwiki": title, "detail": f"{team[0]}, {detail}"})
    return out


def scorers(page, only_final=False, detail=""):
    out = []
    ms = matches(page)
    for m in ms[-1:] if only_final else ms:
        for side in ("hg", "ag"):
            for g in m[side]:
                if not g["og"]:
                    out.append({"answer": nm(g["title"]), "enwiki": g["title"],
                                "detail": f"{m['home'][0]} {m['score']} {m['away'][0]}, {detail}"})
    return out


# ---------------------------------------------------------------- single Copa del Rey finals (all players who appeared)
COPA = {  # prompt id: (final year, blurb)
    "ll200": (2013, "Atlético Madrid v Real Madrid"),
    "ll186": (2019, "Barcelona v Valencia"),
    "ll068": (2020, "Real Sociedad v Athletic Club, played April 2021"),
    "ll069": (2021, "Barcelona v Athletic Club"),
    "ll070": (2022, "Real Betis v Valencia"),
    "ll071": (2023, "Real Madrid v Osasuna"),
    "ll072": (2024, "Athletic Club v Mallorca"),
    "ll073": (2025, "Barcelona v Real Madrid"),
    "ll074": (2026, "Atlético Madrid v Real Sociedad"),
}


def _copa_final(pid, year, blurb):
    @prompt(pid, f"Name a player who appeared in the {year} Copa del Rey final ({blurb})",
            f"en:{year} Copa del Rey final — line-ups (starters + used substitutes)", family="ll-copa-final")
    def fn():
        return dedupe(appeared(f"{year} Copa del Rey final", detail=f"{year} Copa del Rey final"))
    return fn


for _pid, (_y, _b) in COPA.items():
    _copa_final(_pid, _y, _b)


@prompt("ll075", "Name a player who has scored in a Copa del Rey final since 2000 (own goals excluded)",
        "en:2000 Copa del Rey final … 2026 Copa del Rey final — goalscorers")
def ll075():
    out = []
    for y in range(2000, 2027):
        out += scorers(f"{y} Copa del Rey final", detail=f"{y} final")
    return dedupe(out)


# ---------------------------------------------------------------- Supercopa

@prompt("ll076", "Name a player who has scored in a Supercopa de España final since 2020 (own goals excluded)",
        "en:2020 Supercopa de España final … 2026 Supercopa de España final — goalscorers")
def ll076():
    out = []
    for y in range(2020, 2027):
        out += scorers(f"{y} Supercopa de España final", detail=f"{y} final")
    return dedupe(out)


@prompt("ll021", "Name a player who appeared in a Real Madrid v Barcelona Supercopa de España final between 2023 and 2026",
        "en:2023–2026 Supercopa de España final pages — line-ups (starters + used substitutes)")
def ll021():
    out = []
    for y in (2023, 2024, 2025, 2026):
        page = f"{y} Supercopa de España final"
        m = matches(page)[0]
        names = {m["home"][1], m["away"][1]}
        if names != {"Real Madrid CF", "FC Barcelona"}:
            continue
        out += appeared(page, detail=f"{y} Supercopa final")
    return dedupe(out)


@prompt("ll077", "Name a player who has scored in a Supercopa de España match from 2020 to 2026 (own goals excluded)",
        "en:2020 Supercopa de España … 2026 Supercopa de España — goalscorers in all matches")
def ll077():
    out = []
    for y in range(2020, 2027):
        out += scorers(f"{y} Supercopa de España", detail=str(y))
    return dedupe(out)


# ---------------------------------------------------------------- European finals for Spanish clubs

def _euro(pid, text, pages, club_needle, club_title, fam):
    @prompt(pid, text, "en:" + ", ".join(pages) + " — line-ups (starters + used substitutes)", family=fam)
    def fn():
        out = []
        for p in pages:
            out += appeared(p, lambda t: t[1] == club_title, detail=p[:4] + " final")
        return dedupe(out)
    return fn


_euro("ll078", "Name a player who appeared for Sevilla in a Europa League final (2014, 2015, 2016, 2020 or 2023)",
      [f"{y} UEFA Europa League final" for y in (2014, 2015, 2016, 2020, 2023)], "Sevilla", "Sevilla FC", "ll-euro-final")
_euro("ll079", "Name a player who appeared for Atlético Madrid in a Europa League final (2010, 2012 or 2018)",
      [f"{y} UEFA Europa League final" for y in (2010, 2012, 2018)], "Atl", "Atlético Madrid", "ll-euro-final")
_euro("ll080", "Name a player who appeared for Villarreal in the 2021 Europa League final",
      ["2021 UEFA Europa League final"], "Villarreal", "Villarreal CF", "ll-euro-final")
_euro("ll081", "Name a player who appeared for Real Betis in the 2025 Conference League final",
      ["2025 UEFA Conference League final"], "Betis", "Real Betis", "ll-euro-final")


def _copa_won(pid, text, years, club_title, fam):
    @prompt(pid, text, "en:" + ", ".join(f"{y} Copa del Rey final" for y in years) + " — line-ups of the winning club",
            family=fam)
    def fn():
        out = []
        for y in years:
            out += appeared(f"{y} Copa del Rey final", lambda t: t[1] == club_title, detail=f"{y} Copa del Rey final")
        return dedupe(out)
    return fn


_copa_won("ll082", "Name a player who appeared in a Copa del Rey final that Barcelona won (2015, 2016, 2017, 2018, 2021 or 2025)",
          (2015, 2016, 2017, 2018, 2021, 2025), "FC Barcelona", "ll-copa-won")
_copa_won("ll083", "Name a player who appeared in a Copa del Rey final that Real Madrid won (2011, 2014 or 2023)",
          (2011, 2014, 2023), "Real Madrid CF", "ll-copa-won")
