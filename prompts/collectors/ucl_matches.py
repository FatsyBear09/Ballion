"""Match-box parser for UEFA Champions League season pages (knockout, group and league phase)."""
import re
from functools import lru_cache

from prompts.collectors.ucl_finals_parse import name_of
from prompts.collectors.ucl_util import link_title, soup_of

STAGES = [("po", r"play-?offs?"), ("r16", r"Round of 16"), ("r32", r"Round of 32"), ("qf", r"Quarter"),
          ("sf", r"Semi"), ("f", r"^Final$"), ("grp", r"^Group [A-Z]$|^Group stage$"), ("lp", r"League phase")]
SKIP_LINK = re.compile(r"goal|penalty|overtime|association football|^Own", re.I)


def stage_of(text):
    t = re.sub(r"\[.*?\]", "", text).strip()
    for k, rx in STAGES:
        if re.search(rx, t, re.I if k != "f" and k != "grp" else 0):
            return k
    return None


FED = {"The Football Association": "England", "Royal Spanish Football Federation": "Spain",
       "Italian Football Federation": "Italy", "German Football Association": "Germany",
       "French Football Federation": "France", "Royal Dutch Football Association": "Netherlands",
       "Portuguese Football Federation": "Portugal", "Royal Belgian Football Association": "Belgium",
       "Scottish Football Association": "Scotland", "Hellenic Football Federation": "Greece",
       "Turkish Football Federation": "Turkey", "Austrian Football Association": "Austria",
       "Swiss Football Association": "Switzerland", "Danish Football Association": "Denmark",
       "Norwegian Football Federation": "Norway", "Football Association of Wales": "Wales",
       "Kazakhstan Football Federation": "Kazakhstan", "Cyprus Football Association": "Cyprus",
       "Football Association of the Czech Republic": "Czech Republic",
       "Croatian Football Federation": "Croatia", "Football Association of Serbia": "Serbia",
       "Slovak Football Association": "Slovakia", "Ukrainian Association of Football": "Ukraine",
       "Association of Football Federations of Azerbaijan": "Azerbaijan"}


def _team(th, known=None):
    link = None
    for a in th.find_all("a"):
        if a.find_parent(class_="flagicon"):
            continue
        t = link_title(a)
        if t:
            link = (a.get_text(strip=True), t)
            break
    txt = th.get_text(" ", strip=True)
    if link is None and known and txt in known:
        link = (txt, known[txt])
    img = th.select_one(".flagicon img")
    alt = img.get("alt", "").strip() if img else ""
    return link, FED.get(alt, alt)


def _goals(td):
    out = []
    if td is None:
        return out
    for x in td.find_all("a"):
        t = link_title(x)
        if not t or x.find_parent(class_="flagicon") or SKIP_LINK.search(t):
            continue
        tail = ""
        for sib in x.next_siblings:
            if getattr(sib, "name", None) == "a" and link_title(sib):
                break
            tail += sib.get_text(" ") if hasattr(sib, "get_text") else str(sib)
            if getattr(sib, "name", None) == "br":
                break
        if "fb-goal" not in str(x.parent) and not re.search(r"\d+'", tail):
            continue
        out.append((t, bool(re.search(r"o\.g\.|own goal", tail, re.I))))
    return out


@lru_cache(maxsize=None)
def matches(page):
    """Parse every football box on a page. Each match:
    {stage, home, away (article titles), hc, ac (flag alt = country), hg, ag [(title, own_goal)],
     score, venue (stadium title), city}."""
    s = soup_of(page)
    out, stage = [], None
    known = {}
    for th in s.select("div.footballbox th.fhome, div.footballbox th.faway"):
        lk, _ = _team(th)
        if lk:
            known[th.get_text(" ", strip=True)] = lk[1]
    for el in s.select("h2, h3, h4, div.footballbox"):
        if el.name in ("h2", "h3", "h4"):
            st = stage_of(el.get_text(" ", strip=True))
            if st:
                stage = st
            continue
        ev = el.select_one("table.fevent")
        if ev is None:
            continue
        h, a = ev.select_one("th.fhome"), ev.select_one("th.faway")
        (hl, hc), (al, ac) = _team(h, known), _team(a, known)
        if not hl or not al:
            continue
        gtr = ev.find("tr", class_="fgoals")
        hg = _goals(gtr.find("td", class_="fhgoal")) if gtr else []
        ag = _goals(gtr.find("td", class_="fagoal")) if gtr else []
        pens = []
        trs = ev.find_all("tr")
        for i, tr in enumerate(trs):
            if tr.get_text(" ", strip=True) == "Penalties" and i + 1 < len(trs):
                for side, cls in ((0, "fhgoal"), (1, "fagoal")):
                    td = trs[i + 1].find("td", class_=cls)
                    for x in td.find_all("a") if td else []:
                        t = link_title(x)
                        if t and not x.find_parent(class_="flagicon"):
                            pens.append((side, t))
        fr = el.select_one(".fright")
        venue = city = None
        if fr:
            ls = [link_title(x) for x in fr.select('[itemprop="location"] a') if link_title(x)]
            venue = ls[0] if ls else None
            city = ls[1] if len(ls) > 1 else None
        score = ev.select_one("th.fscore").get_text(" ", strip=True) if ev.select_one("th.fscore") else ""
        out.append({"stage": stage, "home": hl[1], "away": al[1], "hn": hl[0], "an": al[0], "hc": hc, "ac": ac,
                    "hg": hg, "ag": ag, "pens": pens, "score": score, "venue": venue, "city": city})
    return out


def scorer_recs(ms, side_filter=None, detail=""):
    """Scorer records from matches. side_filter(match, side) -> bool selects which side's goals count."""
    recs = []
    for m in ms:
        for side, key, team in ((0, "hg", m["home"]), (1, "ag", m["away"])):
            if side_filter and not side_filter(m, side):
                continue
            for t, og in m[key]:
                if og:
                    continue
                recs.append({"answer": name_of(t), "enwiki": t, "detail": f"{detail} ({team})".strip()})
    return recs
