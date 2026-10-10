"""Final-page extras: goals, shoot-out takers, man of the match."""
import re
from functools import lru_cache

from prompts.collectors.ucl_util import clean, final_title, link_title, soup_of, _team_of


def country_rec(name):
    """Country answer record: answer=country name, enwiki=national football team article."""
    return {"answer": name, "enwiki": f"{name} national football team"}


@lru_cache(maxsize=None)
def final_events(year):
    """Parse every fevent block in a final page. Returns list of
    {'teams': (home, away), 'goals': [(side, name, title, own_goal)], 'pens': [(side, name, title)]}."""
    s = soup_of(final_title(year))
    out = []
    for ev in s.select("table.fevent"):
        h, a = ev.select_one("th.fhome"), ev.select_one("th.faway")
        d = {"teams": (_team_of(h), _team_of(a)), "goals": [], "pens": []}
        in_pens = False
        for tr in ev.find_all("tr"):
            if tr.get_text(" ", strip=True) == "Penalties":
                in_pens = True
                continue
            if "fgoals" not in (tr.get("class") or []):
                continue
            for side, cls in ((0, "fhgoal"), (1, "fagoal")):
                td = tr.find("td", class_=cls)
                if td is None:
                    continue
                if in_pens:
                    for x in td.find_all("a"):
                        t = link_title(x)
                        if t:
                            d["pens"].append((side, name_of(t), t))
                else:
                    links = [x for x in td.find_all("a") if link_title(x) and not x.find_parent(class_="flagicon")
                             and not re.search(r"goal|penalty|overtime|association football", link_title(x), re.I)]
                    for x in links:
                        tail = ""
                        for sib in x.next_siblings:
                            if getattr(sib, "name", None) == "a" and link_title(sib):
                                break
                            tail += sib.get_text(" ") if hasattr(sib, "get_text") else str(sib)
                            if getattr(sib, "name", None) == "br":
                                break
                        og = bool(re.search(r"o\.g\.|own goal", tail, re.I))
                        d["goals"].append((side, name_of(link_title(x)), link_title(x), og))
        out.append(d)
    return out


def name_of(title):
    """Display name from an article title (drops a disambiguation suffix)."""
    return re.sub(r"\s*\([^)]*\)$", "", title)


@lru_cache(maxsize=None)
def final_motm(year):
    s = soup_of(final_title(year))
    box = s.select_one("table.infobox")
    for tr in box.find_all("tr") if box else []:
        th, td = tr.find("th"), tr.find("td")
        if th is None or td is None:
            continue
        lab = th.get_text(" ", strip=True)
        if re.search(r"of the match", lab, re.I) and "Fans" not in lab:
            for x in td.find_all("a"):
                if link_title(x) and not x.find_parent(class_="flagicon"):
                    return clean(x.get_text()), link_title(x)
    return None
