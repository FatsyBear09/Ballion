"""ucl088-ucl111: knockout-phase goalscorers (by season, round and club)."""
from ballion.registry import prompt
from prompts.collectors.ucl_matches import matches, scorer_recs
from prompts.collectors.ucl_util import dedupe


def season(y):
    return f"{y}–{y + 1}" if y == 1999 else f"{y}–{str(y + 1)[2:]}"


def ko_page(y):
    word = "stage" if y < 2008 else "phase"
    return f"{season(y)} UEFA Champions League knockout {word}"


def ko_matches(y, stages):
    return [m for m in matches(ko_page(y)) if m["stage"] in stages]


def _scorers(years, stages, label):
    def fn():
        recs = []
        for y in years:
            recs += scorer_recs(ko_matches(y, stages), detail=f"{season(y)} {label}")
        return dedupe(recs)
    return fn


# ---------------------------------------------------------------- by season (ucl088-ucl098)

for _i, _y in enumerate(range(2015, 2026)):
    extra = ", play-offs" if _y >= 2024 else ""
    prompt(f"ucl{88 + _i:03d}",
           f"Name a player who scored in the {season(_y)} Champions League knockout phase "
           f"(round of 16 to semi-finals; own goals{extra} and the final excluded)",
           f"en:{ko_page(_y)} — goals in the round of 16, quarter-finals and semi-finals",
           family="ucl-ko-scorers")(_scorers([_y], {"r16", "qf", "sf"}, "knockout"))

for _pid, _y in (("ucl099", 2024), ("ucl100", 2025)):
    prompt(_pid, f"Name a player who scored in the {season(_y)} Champions League knockout phase play-offs "
                 "(own goals excluded)",
           f"en:{ko_page(_y)} — knockout phase play-off goals", family="ucl-ko-scorers")(
        _scorers([_y], {"po"}, "play-off"))

# ---------------------------------------------------------------- by round

prompt("ucl101", "Name a player who scored in a Champions League semi-final, 2015–16 to 2025–26 (own goals excluded)",
       "en:2015–16 to 2025–26 UEFA Champions League knockout phase pages — semi-final goals",
       family="ucl-ko-round-scorers")(_scorers(range(2015, 2026), {"sf"}, "semi-final"))
prompt("ucl102", "Name a player who scored in a Champions League quarter-final, 2020–21 to 2025–26 (own goals excluded)",
       "en:2020–21 to 2025–26 UEFA Champions League knockout phase pages — quarter-final goals",
       family="ucl-ko-round-scorers")(_scorers(range(2020, 2026), {"qf"}, "quarter-final"))
prompt("ucl103", "Name a player who scored in a Champions League semi-final, 2004–05 to 2014–15 (own goals excluded)",
       "en:2004–05 to 2014–15 UEFA Champions League knockout stage/phase pages — semi-final goals",
       family="ucl-ko-round-scorers")(_scorers(range(2004, 2015), {"sf"}, "semi-final"))

# ---------------------------------------------------------------- against / for a club

KO_STAGES = {"po", "r16", "qf", "sf"}


def _against(club_title, first_year):
    def fn():
        recs = []
        for y in range(first_year, 2026):
            ms = [m for m in ko_matches(y, KO_STAGES) if club_title in (m["home"], m["away"])]
            recs += scorer_recs(ms, lambda m, side: (m["away"] if side == 0 else m["home"]) == club_title,
                                detail=f"v {club_title}, {season(y)}")
        return dedupe(recs)
    return fn


for _pid, _name, _title, _y0 in [
        ("ucl104", "Real Madrid", "Real Madrid CF", 2015), ("ucl105", "Barcelona", "FC Barcelona", 2015),
        ("ucl106", "Bayern Munich", "FC Bayern Munich", 2015), ("ucl107", "Manchester City", "Manchester City F.C.", 2016),
        ("ucl108", "Paris Saint-Germain", "Paris Saint-Germain FC", 2015), ("ucl109", "Arsenal", "Arsenal F.C.", 2015)]:
    prompt(_pid, f"Name a player who has scored against {_name} in a Champions League knockout tie, "
                 f"{season(_y0)} to 2025–26 (own goals and finals excluded)",
           f"en:{season(_y0)} to 2025–26 UEFA Champions League knockout phase pages — goals by {_name}'s opponents "
           "(play-offs to semi-finals)", family="ucl-ko-scored-against")(_against(_title, _y0))


def _for_country(country):
    def fn():
        recs = []
        for y in range(2015, 2026):
            ms = ko_matches(y, KO_STAGES)
            recs += scorer_recs(ms, lambda m, side: (m["hc"] if side == 0 else m["ac"]) == country,
                                detail=f"{season(y)} knockout")
        return dedupe(recs)
    return fn


for _pid, _adj, _c in (("ucl110", "an Italian", "Italy"), ("ucl111", "a German", "Germany")):
    prompt(_pid, f"Name a player who scored for {_adj} club in a Champions League knockout tie, "
                 "2015–16 to 2025–26 (own goals and finals excluded)",
           f"en:2015–16 to 2025–26 UEFA Champions League knockout phase pages — goals for {_c} clubs "
           "(play-offs to semi-finals)", family="ucl-ko-scored-for-country")(_for_country(_c))
