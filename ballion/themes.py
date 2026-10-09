"""Themes: every prompt belongs to exactly one, picked in the game's Free Play menu.

New prompts carry their theme in the id prefix (gen001, pl001, ll001, ucl001, nat001).
The original p001-p103 keep their ids and are assigned here (see prompts/themes/existing.md).
"""
import re

THEMES = [  # (key, id prefix, display name)
    ("general", "gen", "General"),
    ("premier_league", "pl", "Premier League"),
    ("laliga", "ll", "La Liga"),
    ("champions_league", "ucl", "Champions League"),
    ("national", "nat", "National Teams"),
]
_BY_PREFIX = {prefix: key for key, prefix, _ in THEMES}

EXISTING = {
    "p003": "general", "p004": "general", "p005": "general", "p006": "general", "p007": "general", "p014": "general",
    "p015": "general", "p016": "general", "p017": "general", "p019": "general", "p020": "general", "p021": "general",
    "p025": "general", "p026": "general", "p027": "general", "p040": "general", "p066": "general", "p068": "general",
    "p069": "general", "p070": "general", "p072": "general", "p073": "general", "p077": "general", "p078": "general",
    "p079": "general", "p080": "general", "p081": "general", "p082": "general", "p086": "general", "p088": "general",
    "p099": "general", "p100": "general", "p102": "general", "p103": "general",
    "p001": "premier_league", "p008": "premier_league", "p009": "premier_league", "p010": "premier_league", "p011": "premier_league", "p024": "premier_league",
    "p032": "premier_league", "p033": "premier_league", "p038": "premier_league", "p041": "premier_league", "p042": "premier_league", "p064": "premier_league",
    "p065": "premier_league", "p074": "premier_league", "p075": "premier_league", "p083": "premier_league", "p085": "premier_league", "p089": "premier_league",
    "p090": "premier_league", "p093": "premier_league", "p094": "premier_league", "p096": "premier_league", "p097": "premier_league", "p098": "premier_league",
    "p101": "premier_league",
    "p002": "laliga", "p018": "laliga", "p067": "laliga", "p076": "laliga", "p087": "laliga", "p091": "laliga",
    "p092": "laliga", "p095": "laliga",
    "p022": "champions_league", "p028": "champions_league", "p037": "champions_league", "p043": "champions_league", "p062": "champions_league", "p071": "champions_league",
    "p084": "champions_league",
    "p012": "national", "p013": "national", "p023": "national", "p029": "national", "p030": "national", "p031": "national",
    "p034": "national", "p035": "national", "p036": "national", "p039": "national", "p044": "national", "p045": "national",
    "p046": "national", "p047": "national", "p048": "national", "p049": "national", "p050": "national", "p051": "national",
    "p052": "national", "p053": "national", "p054": "national", "p055": "national", "p056": "national", "p057": "national",
    "p058": "national", "p059": "national", "p060": "national", "p061": "national", "p063": "national",
}

# Original prompts that are siblings of each other (or of new families) share a family,
# so a game never draws two of them.
EXISTING_FAMILY = {
    **{f"p{n:03d}": "wc-winning-squad" for n in range(52, 59)},
    **{f"p{n:03d}": "played-for-both" for n in range(95, 104)},
    **{f"p{n:03d}": "club-played-in-league" for n in range(64, 71)},
    **{f"p{n:03d}": "manager-won-league" for n in range(85, 89)},
    **{f"p{n:03d}": "100-league-goals" for n in (2, 24, 25, 26, 27)},
    **{f"p{n:03d}": "league-top-scorer" for n in (18, 19, 20, 21)},
}


def theme_of(pid):
    if pid in EXISTING:
        return EXISTING[pid]
    m = re.match(r"[a-z]+", pid)
    return _BY_PREFIX[m.group()]
