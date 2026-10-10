"""nat: country-answer prompts (tournament participants, members, medallists, qualifiers)."""
import re

from ballion.registry import prompt
from ballion.tables import rows, wikitables
from prompts.collectors.nat_tournaments import box_teams, boxes, section_nodes
from prompts.collectors.nat_util import country_recs, dedupe, links_in, soup, team_titles


def _team_link(ls):
    return next((x for x in ls if "national" in x and ("football team" in x or "soccer team" in x)), None)


def _recs_from_links(pairs):
    """[(display, team article link, detail)] -> deduped country answers."""
    return dedupe([{"answer": a, "enwiki": l, "detail": d} for a, l, d in pairs if l])


def _display(link):
    name = re.sub(r" (men's )?national (football|soccer) team$", "", link)
    return {"United States": "United States"}.get(name, name)


# ------------------------------------------------------------------ 2026 knockout teams
@prompt("nat002", "Name a country that reached the knockout stage (round of 32) of the 2026 World Cup",
        "en:2026 FIFA World Cup knockout stage — round-of-32 match boxes", family="nat-country-at-tournament")
def _nat002():
    out = []
    for head, b in boxes("2026 FIFA World Cup knockout stage"):
        if re.search(r"round of 32", head, re.I):
            for name, link in box_teams(b):
                out.append((name, link, "round of 32"))
    return _recs_from_links(out)


# ------------------------------------------------------------------ Nations League A
@prompt("nat070", "Name a country that played in League A of the 2024–25 UEFA Nations League",
        "en:2024–25 UEFA Nations League A — group tables", family="nat-country-competition")
def _nat070():
    out = []
    for t in wikitables("2024–25 UEFA Nations League A"):
        rs = list(rows(t))
        if rs[0][0][:2] == ["Pos", "Team v t e"]:
            for tx, ln in rs[1:]:
                out.append((re.sub(r"\s*\(.*", "", tx[1]), _team_link(ln[1]), "League A"))
    return _recs_from_links(out)


# ------------------------------------------------------------------ AFCON winners
@prompt("nat071", "Name a country that has won the Africa Cup of Nations",
        "en:Africa Cup of Nations — titles by team table", family="nat-country-competition")
def _nat071():
    t = next(t for t in wikitables("Africa Cup of Nations") if rows_hdr(t)[:3] == ["Team", "Winners", "Runners-up"])
    out = []
    for tx, ln in list(rows(t))[1:]:
        if re.match(r"[1-9]", tx[1]) and ln[0]:
            out.append((tx[0], ln[0][-1] if "national" in ln[0][-1] else None, "Winners " + re.sub(r"\s+", " ", tx[1])))
    return _recs_from_links(out)


def rows_hdr(t):
    return next(rows(t))[0]


# ------------------------------------------------------------------ penalty shoot-outs
@prompt("nat072", "Name a country that has taken part in a World Cup penalty shoot-out",
        "en:List of FIFA World Cup penalty shoot-outs — team summary table", family="nat-country-history")
def _nat072():
    t = next(t for t in wikitables("List of FIFA World Cup penalty shoot-outs") if rows_hdr(t)[:3] == ["Team", "Played", "Win"])
    out = []
    for tx, ln in list(rows(t))[1:]:
        if ln[0] and tx[1].isdigit():
            out.append((_display(ln[0][-1]), ln[0][-1], f"{tx[1]} shoot-outs"))
    return _recs_from_links(out)


# ------------------------------------------------------------------ confederation members
def _members(heading):
    s = soup("List of men's national association football teams")
    out = []
    for n in section_nodes(s, heading):
        for a, l in links_in(n):
            tl = _team_link([l])
            if tl:
                out.append((_display(tl), tl, heading.split(" ")[0]))
    return _recs_from_links(out)


prompt("nat074", "Name a member nation of CONCACAF",
       "en:List of men's national association football teams — CONCACAF section",
       family="nat-confederation-member")(lambda: _members("CONCACAF ( North America )"))
prompt("nat075", "Name a member nation of the Asian Football Confederation (AFC)",
       "en:List of men's national association football teams — AFC section",
       family="nat-confederation-member")(lambda: _members("AFC ( Asia )"))


# ------------------------------------------------------------------ Olympic medallists
@prompt("nat076", "Name a country that won a men's football medal at the Olympics from 2000 to 2024",
        "en:Football at the Summer Olympics — men's results table (gold/silver/bronze)", family="nat-country-history")
def _nat076():
    t = next(t for t in wikitables("Football at the Summer Olympics")
             if len(list(rows(t))) > 20 and "Gold medalists" in list(rows(t))[1][0])
    rs = list(rows(t))
    names = {}
    for tx, ln in rs[2:]:
        if re.fullmatch(r"\d{4}", tx[1]) and 2000 <= int(tx[1]) <= 2024:
            for i, medal in ((3, "gold"), (5, "silver"), (6, "bronze")):
                names.setdefault(tx[i], []).append(f"{medal} {tx[1]}")
    tt = team_titles(list(names))
    return _recs_from_links([(n, tt[n], ", ".join(d)) for n, d in names.items()])


# ------------------------------------------------------------------ UEFA play-offs
@prompt("nat077", "Name a country that played in the UEFA play-offs for the 2026 World Cup",
        "en:2026 FIFA World Cup qualification (UEFA) — play-off path brackets", family="nat-country-competition")
def _nat077():
    out = []
    for t in wikitables("2026 FIFA World Cup qualification (UEFA)"):
        if rows_hdr(t)[:3] == ["Home team", "Score", "Away team"]:
            for tx, ln in list(rows(t))[1:]:
                for i in (0, 2):
                    tl = _team_link(ln[i])
                    if tl:
                        out.append((tx[i], tl, "play-offs"))
    return _recs_from_links(out)


# ------------------------------------------------------------------ one World Cup appearance
@prompt("nat078", "Name a country that has played at exactly one men's World Cup (2026 included)",
        "en:National team appearances in the FIFA World Cup — appearances table", family="nat-country-history")
def _nat078():
    t = next(t for t in wikitables("National team appearances in the FIFA World Cup")
             if rows_hdr(t)[:2] == ["Team", "Appearances"])
    out = []
    for tx, ln in list(rows(t))[1:]:
        if tx[1] == "1" and ln[0]:
            out.append((_display(ln[0][-1]), ln[0][-1], f"debut {tx[4]}"))
    return _recs_from_links(out)
