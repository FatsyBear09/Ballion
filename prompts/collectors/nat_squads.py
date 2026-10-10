"""nat: prompts built from the 'YYYY ... squads' articles (squads, coaches, captains, ages, clubs, leagues)."""
from ballion.registry import prompt
from ballion.wiki import resolve
from prompts.collectors.nat_util import country_recs, dedupe, player_recs, squads

WC26 = "2026 FIFA World Cup squads"
WC22 = "2022 FIFA World Cup squads"
WC18 = "2018 FIFA World Cup squads"
EURO24 = "UEFA Euro 2024 squads"
EURO20 = "UEFA Euro 2020 squads"
EURO16 = "UEFA Euro 2016 squads"
COPA24 = "2024 Copa América squads"
COPA21 = "2021 Copa América squads"
AFCON25 = "2025 Africa Cup of Nations squads"
AFCON23 = "2023 Africa Cup of Nations squads"
AFCON21 = "2021 Africa Cup of Nations squads"
ASIA23 = "2023 AFC Asian Cup squads"
GOLD25 = "2025 CONCACAF Gold Cup squads"


def _players(page, teams=None):
    for team, v in squads(page).items():
        if teams is None or team in teams:
            for p in v["players"]:
                yield team, p


def _src(page, what):
    return f"en:{page} — {what}"


# ------------------------------------------------------------------ countries at a tournament
def _teams(page):
    return lambda: country_recs([(t, "") for t in squads(page)])


def _reg_teams(pid, text, page, family="nat-country-at-tournament"):
    prompt(pid, text, _src(page, "one section per team"), family=family)(_teams(page))


_reg_teams("nat001", "Name a country that played at the 2026 World Cup", WC26)
_reg_teams("nat064", "Name a country that played at the 2022 World Cup", WC22)
_reg_teams("nat065", "Name a country that played at Euro 2024", EURO24)
_reg_teams("nat066", "Name a country that played at the 2024 Copa América", COPA24)
_reg_teams("nat067", "Name a country that played at the 2025 Africa Cup of Nations", AFCON25)
_reg_teams("nat068", "Name a country that played at the 2023 AFC Asian Cup", ASIA23)
_reg_teams("nat069", "Name a country that played at the 2025 CONCACAF Gold Cup", GOLD25)


# ------------------------------------------------------------------ squads of one team
def _squad_fn(page, team):
    return lambda: player_recs([p for _, p in _players(page, {team})],
                               lambda p: f"#{p['no']} {p['pos']}, {p['clubtxt']}")


SQUAD_PROMPTS = [
    ("nat016", "Spain's 2026 World Cup-winning squad", WC26, "Spain"),
    ("nat017", "Argentina's 2026 World Cup squad", WC26, "Argentina"),
    ("nat018", "England's 2026 World Cup squad", WC26, "England"),
    ("nat019", "the United States' 2026 World Cup squad", WC26, "United States"),
    ("nat020", "Morocco's 2022 World Cup squad", WC22, "Morocco"),
    ("nat021", "Croatia's 2018 World Cup squad", WC18, "Croatia"),
    ("nat022", "Japan's 2022 World Cup squad", WC22, "Japan"),
    ("nat023", "Italy's Euro 2020-winning squad", EURO20, "Italy"),
    ("nat024", "England's Euro 2024 squad", EURO24, "England"),
    ("nat025", "Portugal's Euro 2016-winning squad", EURO16, "Portugal"),
    ("nat026", "Argentina's 2021 Copa América-winning squad", COPA21, "Argentina"),
    ("nat027", "Colombia's 2024 Copa América squad", COPA24, "Colombia"),
    ("nat028", "Senegal's 2021 Africa Cup of Nations-winning squad", AFCON21, "Senegal"),
    ("nat029", "Ivory Coast's 2023 Africa Cup of Nations-winning squad", AFCON23, "Ivory Coast"),
    ("nat030", "Morocco's 2025 Africa Cup of Nations squad", AFCON25, "Morocco"),
    ("nat031", "Qatar's 2023 AFC Asian Cup-winning squad", ASIA23, "Qatar"),
]
for _pid, _what, _page, _team in SQUAD_PROMPTS:
    prompt(_pid, f"Name a player in {_what}", _src(_page, f"{_team} section"), family="nat-squad")(_squad_fn(_page, _team))


# ------------------------------------------------------------------ squads across several tournaments
def _multi_fn(parts):
    def fn():
        recs = []
        for page, team in parts:
            tag = page.replace(" squads", "")
            recs += [{"answer": p["name"], "enwiki": p["link"], "detail": f"{team}, {tag}"}
                     for _, p in _players(page, {team}) if p["link"]]
        return dedupe(recs)
    return fn


MULTI = [
    ("nat037", "Wales's squad at Euro 2016, Euro 2020 or the 2022 World Cup", "Wales", [EURO16, EURO20, WC22]),
    ("nat038", "Scotland's squad at Euro 2020, Euro 2024 or the 2026 World Cup", "Scotland", [EURO20, EURO24, WC26]),
    ("nat039", "Iceland's squad at Euro 2016 or the 2018 World Cup", "Iceland", [EURO16, WC18]),
    ("nat041", "Canada's squad at the 2022 or 2026 World Cup", "Canada", [WC22, WC26]),
    ("nat042", "Brazil's squad at the 2018, 2022 or 2026 World Cup", "Brazil", [WC18, WC22, WC26]),
    ("nat043", "France's squad at any World Cup or Euro from 2018 to 2026", "France", [WC18, EURO20, WC22, EURO24, WC26]),
    ("nat044", "Germany's squad at any World Cup or Euro from 2018 to 2026", "Germany", [WC18, EURO20, WC22, EURO24, WC26]),
    ("nat045", "the Netherlands' squad at any World Cup or Euro from 2020 to 2026", "Netherlands", [EURO20, WC22, EURO24, WC26]),
]
for _pid, _what, _team, _pages in MULTI:
    prompt(_pid, f"Name a player who was in {_what}", f"en:{', '.join(_pages)} — {_team} sections",
           family="nat-squad-multi")(_multi_fn([(pg, _team) for pg in _pages]))


@prompt("nat040", "Name a player who was in Northern Ireland's or the Republic of Ireland's squad at Euro 2016",
        _src(EURO16, "Northern Ireland and Republic of Ireland sections"), family="nat-squad-multi")
def _nat040():
    return _multi_fn([(EURO16, "Northern Ireland"), (EURO16, "Republic of Ireland")])()


# ------------------------------------------------------------------ head coaches
def _coach_fn(page, foreign_only=False):
    def fn():
        recs = []
        for team, v in squads(page).items():
            for name, link, flag in v["coach"]:
                if foreign_only and not flag:
                    continue
                recs.append({"answer": name, "enwiki": link, "detail": f"{team} head coach"})
        return dedupe(recs)
    return fn


COACH = [
    ("nat008", "Name the head coach of a team at the 2026 World Cup", WC26),
    ("nat079", "Name the head coach of a team at the 2022 World Cup", WC22),
    ("nat080", "Name the head coach of a team at the 2018 World Cup", WC18),
    ("nat081", "Name the head coach of a team at Euro 2024", EURO24),
    ("nat082", "Name the head coach of a team at Euro 2020", EURO20),
    ("nat083", "Name the head coach of a team at the 2023 Africa Cup of Nations", AFCON23),
    ("nat084", "Name the head coach of a team at the 2025 Africa Cup of Nations", AFCON25),
    ("nat085", "Name the head coach of a team at the 2023 AFC Asian Cup", ASIA23),
    ("nat086", "Name the head coach of a team at the 2024 Copa América", COPA24),
    ("nat096", "Name the head coach of a team at the 2025 CONCACAF Gold Cup", GOLD25),
]
for _pid, _text, _page in COACH:
    prompt(_pid, _text, _src(_page, "coach line per team"), family="nat-coach-at-tournament")(_coach_fn(_page))

prompt("nat009", "Name a head coach at the 2026 World Cup who was coaching a country other than his own",
       _src(WC26, "coach lines marked with a flag icon (coach of a different nationality)"),
       family="nat-coach-foreign")(_coach_fn(WC26, foreign_only=True))


# ------------------------------------------------------------------ captains
def _captain_fn(page):
    def fn():
        return player_recs([p for _, p in _players(page) if p["captain"]], lambda p: "captain")
    return fn


CAPT = [
    ("nat010", "Name the captain of a team at the 2026 World Cup", WC26),
    ("nat093", "Name the captain of a team at the 2022 World Cup", WC22),
    ("nat094", "Name the captain of a team at Euro 2024", EURO24),
    ("nat098", "Name the captain of a team at Euro 2020", EURO20),
    ("nat099", "Name the captain of a team at the 2024 Copa América", COPA24),
    ("nat100", "Name the captain of a team at the 2025 Africa Cup of Nations", AFCON25),
    ("nat101", "Name the captain of a team at the 2023 AFC Asian Cup", ASIA23),
]
for _pid, _text, _page in CAPT:
    prompt(_pid, _text, _src(_page, "captain marker in squad tables"), family="nat-captain-at-tournament")(_captain_fn(_page))


# ------------------------------------------------------------------ ages, caps, shirt numbers, positions
def _filter_fn(page, pred, detail):
    return lambda: player_recs([p for _, p in _players(page) if pred(p)], detail)


def _reg(pid, text, page, what, pred, detail, family):
    prompt(pid, text, _src(page, what), family=family)(_filter_fn(page, pred, detail))


_reg("nat011", "Name a player who went to the 2026 World Cup with 100 or more caps", WC26, "caps >= 100",
     lambda p: (p["caps"] or 0) >= 100, lambda p: f"{p['caps']} caps", "nat-squad-caps")
_reg("nat012", "Name a player born in 2005 or later who was in a 2026 World Cup squad", WC26, "birth year",
     lambda p: (p["born"] or 0) >= 2005, lambda p: f"born {p['born']}", "nat-squad-age")
_reg("nat013", "Name a player born in 1990 or earlier who was in a 2026 World Cup squad", WC26, "birth year",
     lambda p: p["born"] and p["born"] <= 1990, lambda p: f"born {p['born']}", "nat-squad-age")
_reg("nat124", "Name a player born in 2001 or later who was in a 2022 World Cup squad", WC22, "birth year",
     lambda p: (p["born"] or 0) >= 2001, lambda p: f"born {p['born']}", "nat-squad-age")
_reg("nat125", "Name a player born in 1987 or earlier who was in a 2022 World Cup squad", WC22, "birth year",
     lambda p: p["born"] and p["born"] <= 1987, lambda p: f"born {p['born']}", "nat-squad-age")
_reg("nat126", "Name a player born in 2003 or later who was in a Euro 2024 squad", EURO24, "birth year",
     lambda p: (p["born"] or 0) >= 2003, lambda p: f"born {p['born']}", "nat-squad-age")
_reg("nat014", "Name a player who wore the No. 10 shirt at the 2026 World Cup", WC26, "no=10",
     lambda p: p["no"] == "10", lambda p: "No. 10", "nat-squad-number")
_reg("nat015", "Name a player who wore the No. 7 shirt at the 2026 World Cup", WC26, "no=7",
     lambda p: p["no"] == "7", lambda p: "No. 7", "nat-squad-number")
_reg("nat127", "Name a player who wore the No. 9 shirt at the 2022 World Cup", WC22, "no=9",
     lambda p: p["no"] == "9", lambda p: "No. 9", "nat-squad-number")
_reg("nat128", "Name a player who wore the No. 10 shirt at Euro 2024", EURO24, "no=10",
     lambda p: p["no"] == "10", lambda p: "No. 10", "nat-squad-number")
_reg("nat129", "Name a goalkeeper in a Euro 2024 squad", EURO24, "pos=GK",
     lambda p: p["pos"] == "GK", lambda p: "GK", "nat-squad-goalkeeper")
_reg("nat130", "Name a goalkeeper in a 2022 World Cup squad", WC22, "pos=GK",
     lambda p: p["pos"] == "GK", lambda p: "GK", "nat-squad-goalkeeper")


# ------------------------------------------------------------------ club / league representation
def _canon(titles):
    r = resolve(list(titles))
    return {t: r[t]["title"] for t in titles}


def _club_fn(page, club_title):
    def fn():
        ps = [p for _, p in _players(page) if p["club"]]
        cm = _canon({p["club"] for p in ps} | {club_title})
        return player_recs([p for p in ps if cm[p["club"]] == cm[club_title]], lambda p: f"{p['clubtxt']}")
    return fn


CLUBS = [
    ("nat102", "Manchester City", "Manchester City F.C.", WC26, "the 2026 World Cup"),
    ("nat103", "Bayern Munich", "FC Bayern Munich", WC26, "the 2026 World Cup"),
    ("nat104", "Paris Saint-Germain", "Paris Saint-Germain F.C.", WC26, "the 2026 World Cup"),
    ("nat105", "Arsenal", "Arsenal F.C.", WC26, "the 2026 World Cup"),
    ("nat106", "Barcelona", "FC Barcelona", WC26, "the 2026 World Cup"),
    ("nat107", "Crystal Palace", "Crystal Palace F.C.", WC26, "the 2026 World Cup"),
    ("nat108", "Real Madrid", "Real Madrid CF", WC22, "the 2022 World Cup"),
    ("nat109", "Manchester United", "Manchester United F.C.", WC22, "the 2022 World Cup"),
    ("nat110", "Al Sadd", "Al Sadd SC", WC22, "the 2022 World Cup"),
    ("nat111", "Inter Milan", "Inter Milan", EURO24, "Euro 2024"),
    ("nat117", "Al Hilal", "Al Hilal SFC", WC26, "the 2026 World Cup"),
    ("nat118", "Atlético Madrid", "Atlético Madrid", WC26, "the 2026 World Cup"),
]
for _pid, _club, _title, _page, _tour in CLUBS:
    art = "an" if _club[0] in "AEIO" else "a"
    prompt(_pid, f"Name {art} {_club} player who went to {_tour} (club at the start of the tournament)",
           _src(_page, f"club column = {_title}"), family="nat-club-at-tournament")(_club_fn(_page, _title))


def _nat_fn(page, flags, club_filter=None):
    def fn():
        ps = [p for _, p in _players(page) if p["clubnat"] in flags]
        if club_filter:
            ps = club_filter(ps)
        return player_recs(ps, lambda p: p["clubtxt"])
    return fn


LEAGUE = [
    ("nat112", "Name a player at the 2026 World Cup who played for a Saudi Arabian club", WC26, {"Saudi Arabia"}),
    ("nat114", "Name a player at the 2026 World Cup who played for a Turkish club", WC26, {"Turkey"}),
    ("nat115", "Name a player at the 2026 World Cup who played for a Brazilian club", WC26, {"Brazil"}),
    ("nat116", "Name a player at the 2022 World Cup who played for a Qatari club", WC22, {"Qatar"}),
    ("nat119", "Name a player at the 2026 World Cup who played for a Scottish club", WC26, {"Scotland"}),
    ("nat120", "Name a player at the 2026 World Cup who played for a Mexican club", WC26, {"Mexico"}),
    ("nat121", "Name a player at the 2026 World Cup who played for a Dutch club", WC26, {"Netherlands"}),
    ("nat122", "Name a player at Euro 2024 who played for a Turkish club", EURO24, {"Turkey"}),
    ("nat123", "Name a player at Euro 2024 who played for a Saudi Arabian club", EURO24, {"Saudi Arabia"}),
]
for _pid, _text, _page, _flags in LEAGUE:
    prompt(_pid, _text + " (club at the start of the tournament)", _src(_page, "club's flag in squad tables"),
           family="nat-league-at-tournament")(_nat_fn(_page, _flags))
