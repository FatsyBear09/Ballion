"""Shared helpers for the Champions League (ucl) collectors."""
import re
from functools import lru_cache
from urllib.parse import unquote

from bs4 import BeautifulSoup

from ballion.wiki import page_html, resolve


# ---------------------------------------------------------------- generic

def soup_of(title):
    s = BeautifulSoup(page_html(title), "lxml")
    for sup in s.select("sup.reference"):
        sup.decompose()
    return s


def link_title(a):
    href = a.get("href", "")
    if not href.startswith("/wiki/") or ":" in href[6:]:
        return None
    return unquote(href[6:].split("#")[0]).replace("_", " ")


def clean(name):
    name = re.sub(r"\((?:c|captain|a|b|c)\)", "", name)
    name = re.sub(r"[*†‡§#\[\]]+", "", name)
    return re.sub(r"\s+", " ", name).strip()


def dedupe(recs):
    """Merge records whose enwiki titles resolve to one article; drop red links; join details."""
    res = resolve([r["enwiki"] for r in recs])
    out = {}
    for r in recs:
        info = res[r["enwiki"]]
        if info["missing"]:
            continue
        key = info["title"]
        if key in out:
            if r["detail"] and r["detail"] not in out[key]["detail"]:
                out[key]["detail"] += "; " + r["detail"]
        else:
            out[key] = {k: v for k, v in r.items() if not k.startswith('_')}
    # two different articles with the same display name (e.g. two "Red Bull Arena"): show the full title
    names = {}
    for k, r in out.items():
        names.setdefault(r["answer"].casefold(), []).append(k)
    for ks in names.values():
        if len(ks) > 1:
            for k in ks:
                out[k]["answer"] = out[k]["enwiki"]
    return list(out.values())


def season_label(y):
    """2015 -> '2015–16'"""
    return f"{y}–{str(y + 1)[2:]}"


def season_label_full(y):
    """1999 -> '1999–2000' style used by some page titles (2000–01 uses 2-digit)."""
    return season_label(y)


# ---------------------------------------------------------------- finals

def final_title(year):
    """Title of the final played in calendar `year`."""
    if year >= 1993:
        return f"{year} UEFA Champions League final"
    return f"{year} European Cup final"


def _flag(el):
    f = el.select_one(".flagicon img")
    return f.get("alt", "").strip() if f else ""


def _team_of(th):
    for a in th.find_all("a"):
        if a.find_parent(class_="flagicon"):
            continue
        t = link_title(a)
        if t:
            return t
    return th.get_text(" ", strip=True)


def _lineup_tables(s):
    out = []
    for tb in s.select("table"):
        if tb.find("table"):
            continue
        trs = tb.find_all("tr")
        first = [tr.find("td") for tr in trs]
        if any(td is not None and td.get_text(strip=True) in ("GK", "G") and len(tr.find_all("td")) >= 3
               for tr, td in zip(trs, first)):
            out.append(tb)
    return out


def _parse_lineup(tb):
    players, manager, mode = [], None, "start"
    for tr in tb.find_all("tr"):
        tds = tr.find_all(["td", "th"], recursive=False)
        txt = tr.get_text(" ", strip=True)
        if re.match(r"Substitut", txt):
            mode = "sub"
            continue
        if re.match(r"(Manager|Coach|Head coach|Managers?)\b", txt):
            mode = "mgr"
            continue
        if mode == "mgr":
            a = [x for x in tr.find_all("a") if link_title(x) and not x.find_parent(class_="flagicon")]
            if a and manager is None:
                manager = (clean(a[0].get_text()), link_title(a[0]))
            continue
        if len(tds) < 3:
            continue
        pos = tds[0].get_text(strip=True)
        if not re.fullmatch(r"[A-Z]{1,3}", pos):
            continue
        nm = tds[2]
        links = [a for a in nm.find_all("a") if link_title(a) and not a.find_parent(class_="flagicon")
                 and link_title(a) != "Captain (association football)"]
        if not links:
            continue
        a = links[0]
        alts = [i.get("alt", "") for i in tr.find_all("img") if "Flag" not in (i.get("src") or "")]
        imgs = " ".join(alts)
        players.append({
            "answer": clean(a.get_text()), "enwiki": link_title(a), "pos": pos, "country": _flag(nm),
            "started": mode == "start",
            "subon": mode == "sub" and "green arrow" in imgs,
            "captain": bool(re.search(r"\(\s*c\s*\)", nm.get_text(" ", strip=True))),
        })
    return {"players": players, "manager": manager}


@lru_cache(maxsize=None)
def final_match(year):
    """Parsed final: {'teams': [t1, t2], 'sides': [lineup1, lineup2], 'year', 'title',
    'replay': [..] optional}. Each lineup is {'players': [...], 'manager': (name, title)}.
    Players have: answer, enwiki, pos, country, started, subon, captain."""
    title = final_title(year)
    s = soup_of(title)
    teams = []
    for ev in s.select("table.fevent"):
        h, a = ev.select_one("th.fhome"), ev.select_one("th.faway")
        if h and a:
            teams.append([_team_of(h), _team_of(a)])
    lts = _lineup_tables(s)
    if len(lts) < 2:
        raise LookupError(f"{title}: lineups not found ({len(lts)})")
    sides = [_parse_lineup(t) for t in lts]
    first = teams[0]
    out = {"year": year, "title": title, "teams": first, "sides": sides[:2], "replay": None}
    if len(sides) >= 4:
        out["replay"] = sides[2:4]
    return out


def final_sides(year, include_replay=True):
    """Yield (club title, lineup) for each side (and replay side) of a final."""
    m = final_match(year)
    for i in range(2):
        yield m["teams"][i], m["sides"][i]
    if include_replay and m["replay"]:
        # replay: match sides by overlap with first-leg players
        for sd in m["replay"]:
            names = {p["enwiki"] for p in sd["players"]}
            best = max(range(2), key=lambda i: len(names & {p["enwiki"] for p in m["sides"][i]["players"]}))
            yield m["teams"][best], sd


def played(p):
    return p["started"] or p["subon"]


def final_players(year, club=None, include_replay=True, pred=played):
    """Records for players who played in the final (optionally only for one club title)."""
    out = []
    for team, sd in final_sides(year, include_replay):
        if club and team not in club:
            continue
        for p in sd["players"]:
            if pred(p):
                out.append({"answer": p["answer"], "enwiki": p["enwiki"],
                            "detail": f"{team} in the {year} final", "_p": p, "_team": team})
    return out
