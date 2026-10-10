"""pl035-pl073: players with Premier League appearances for a club in a season or a run of seasons.

Rule: >= 1 Premier League appearance (starts + substitute appearances) in the club season article's
squad-statistics table.  Season articles for 1990s seasons lack appearance data; those prompts fall
back to the article's first-team squad list (see SQUAD_LIST).
"""
from ballion.registry import prompt
from prompts.collectors.pl_util import Acc, club_season, season_squad, squad_list

C = {
    "ARS": ("Arsenal F.C.", "Arsenal"), "CHE": ("Chelsea F.C.", "Chelsea"), "LIV": ("Liverpool F.C.", "Liverpool"),
    "MCI": ("Manchester City F.C.", "Manchester City"), "MUN": ("Manchester United F.C.", "Manchester United"),
    "TOT": ("Tottenham Hotspur F.C.", "Tottenham"), "LEI": ("Leicester City F.C.", "Leicester City"),
    "AVL": ("Aston Villa F.C.", "Aston Villa"), "EVE": ("Everton F.C.", "Everton"),
    "BLA": ("Blackburn Rovers F.C.", "Blackburn Rovers"), "NEW": ("Newcastle United F.C.", "Newcastle United"),
    "BRE": ("Brentford F.C.", "Brentford"), "NFO": ("Nottingham Forest F.C.", "Nottingham Forest"),
    "BHA": ("Brighton & Hove Albion F.C.", "Brighton"), "BOU": ("AFC Bournemouth", "Bournemouth"),
    "WOL": ("Wolverhampton Wanderers F.C.", "Wolves"), "LEE": ("Leeds United F.C.", "Leeds United"),
    "LUT": ("Luton Town F.C.", "Luton Town"), "IPS": ("Ipswich Town F.C.", "Ipswich Town"),
    "SUN": ("Sunderland A.F.C.", "Sunderland"), "SOU": ("Southampton F.C.", "Southampton"),
    "CRY": ("Crystal Palace F.C.", "Crystal Palace"),
}


def squad_union(code, seasons):
    club = C[code][0]
    acc = Acc()
    for y in seasons:
        page = club_season(club, y)
        try:
            for name, title, apps in season_squad(page):
                acc.add(title, name, f"{apps} apps, {sname(y)}")
        except LookupError:
            for name, title in squad_list(page):
                acc.add(title, name, f"{sname(y)} squad")
    return acc.out()


def sname(y):
    return f"{y}–{(y + 1) % 100:02d}"


# ------------------------------------------------------------ single seasons
SINGLE = [
    ("pl035", "LEI", 2015, "Leicester City's title-winning season"),
    ("pl036", "CHE", 2016, "Conte's title-winning season"),
    ("pl037", "MCI", 2017, "the 100-point Centurions season"),
    ("pl038", "MCI", 2018, "the domestic treble season"),
    ("pl039", "LIV", 2018, "97 points, runners-up"),
    ("pl040", "LIV", 2019, "Liverpool's title-winning season"),
    ("pl041", "MCI", 2022, "the treble season"),
    ("pl042", "ARS", 2023, "89 points, runners-up"),
    ("pl043", "AVL", 2023, "Champions League qualification"),
    ("pl044", "LIV", 2024, "Liverpool's title-winning season"),
    ("pl045", "ARS", 2025, "Arsenal's title-winning season"),
    ("pl046", "ARS", 2003, "the unbeaten Invincibles season"),
    ("pl047", "CHE", 2004, "Mourinho's first title"),
    ("pl048", "MUN", 2007, "title and Champions League winners"),
    ("pl049", "MCI", 2011, "the Agüero title-clinching season"),
    ("pl050", "MUN", 1998, "the treble season"),
    ("pl051", "ARS", 1997, "Wenger's first double"),
    ("pl052", "BLA", 1994, "Blackburn's title-winning season"),
    ("pl053", "EVE", 2024, "their final season at Goodison Park"),
    ("pl054", "NEW", 1995, "Keegan's Entertainers"),
]
SQUAD_LIST = {"pl052", "pl054"}  # also pl049 if its article lacks stats  # stats-less 1990s articles: use first-team squad lists


def _make_single(pid, code, y, note):
    club, short = C[code]
    text = f"Name a player who played in the Premier League for {short} in {sname(y)} ({note})"
    if pid in SQUAD_LIST:
        text = f"Name a player in the {sname(y)} {short} squad ({note})"

    @prompt(pid, text, f"en:{club_season(club, y)} — squad statistics, >= 1 Premier League appearance",
            family="pl-season-squad")
    def f():
        return squad_union(code, [y])
    return f


for _s in SINGLE:
    _make_single(*_s)

# ------------------------------------------------------------ eras
ERAS = [
    ("pl055", "LIV", range(2016, 2024), "for Liverpool between 2016–17 and 2023–24 (the Klopp years)"),
    ("pl056", "ARS", range(2020, 2026), "for Arsenal between 2020–21 and 2025–26 (the Arteta years)"),
    ("pl057", "MUN", [2022, 2023], "for Manchester United in 2022–23 or 2023–24 (Ten Hag's full seasons)"),
    ("pl058", "MUN", [2024, 2025], "for Manchester United in 2024–25 or 2025–26"),
    ("pl059", "TOT", [2023, 2024], "for Tottenham in 2023–24 or 2024–25 (Postecoglou's seasons)"),
    ("pl060", "CHE", range(2022, 2026), "for Chelsea between 2022–23 and 2025–26 (the BlueCo ownership years)"),
    ("pl061", "NEW", range(2021, 2026), "for Newcastle between 2021–22 and 2025–26 (the Saudi PIF ownership years)"),
    ("pl062", "BRE", range(2021, 2026), "for Brentford between 2021–22 and 2025–26"),
    ("pl063", "NFO", range(2022, 2026), "for Nottingham Forest between 2022–23 and 2025–26"),
    ("pl064", "BHA", range(2017, 2026), "for Brighton between 2017–18 and 2025–26"),
    ("pl065", "BOU", range(2022, 2026), "for Bournemouth between 2022–23 and 2025–26"),
    ("pl066", "WOL", range(2018, 2026), "for Wolves between 2018–19 and 2025–26"),
    ("pl067", "LEE", [2020, 2021, 2022, 2025], "for Leeds United in 2020–21, 2021–22, 2022–23 or 2025–26"),
    ("pl068", "LUT", [2023], "for Luton Town in 2023–24"),
    ("pl069", "IPS", [2024], "for Ipswich Town in 2024–25"),
    ("pl070", "SUN", [2025], "for Sunderland in 2025–26"),
    ("pl071", "AVL", range(2019, 2026), "for Aston Villa between 2019–20 and 2025–26"),
    ("pl072", "SOU", [2024], "for Southampton in 2024–25"),
    ("pl073", "CRY", range(2023, 2026), "for Crystal Palace between 2023–24 and 2025–26"),
]


def _make_era(pid, code, seasons, desc):
    seasons = list(seasons)
    club = C[code][0]
    text = f"Name a player who played in the Premier League {desc}" if "(" not in desc else \
        f"Name a player who played in the Premier League {desc}"
    first, last = seasons[0], seasons[-1]

    @prompt(pid, text, f"en:{club_season(club, first)}" + (f" … {club_season(club, last)}" if len(seasons) > 1 else "")
            + " — squad statistics, >= 1 Premier League appearance in any listed season",
            family="pl-club-era" if len(seasons) > 2 else "pl-season-squad")
    def f():
        return squad_union(code, seasons)
    return f


for _e in ERAS:
    _make_era(*_e)
