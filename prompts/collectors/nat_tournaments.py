"""nat: tournament-level prompts (goalscorers, knockout scorers, finals, hosts, venues)."""
import re

from ballion.registry import prompt
from ballion.tables import _link_title
from prompts.collectors.nat_util import dedupe, heading_text, links_in, soup, clean_name


# ------------------------------------------------------------------ goalscorer sections
def section_nodes(s, heading):
    """All elements between the first heading containing `heading` and the next heading of same or higher level."""
    for h in s.find_all(["h2", "h3", "h4"]):
        if heading_text(h).lower() == heading.lower():
            lvl = int(h.name[1])
            el = h.parent if "mw-heading" in " ".join(h.parent.get("class", [])) else h
            out = []
            for x in el.next_siblings:
                if getattr(x, "name", None) is None:
                    continue
                hh = x.find(re.compile(r"h[2-4]")) if x.name == "div" and "mw-heading" in " ".join(x.get("class", [])) else None
                if hh is not None and int(hh.name[1]) <= lvl:
                    break
                out.append(x)
            return out
    raise LookupError(f"no heading {heading!r}")


def scorers(title, heading="Goalscorers"):
    """[(name, link, goals)] from the 'N goals' bold headers + bullet lists; own goals skipped."""
    s = soup(title)
    res, n, own = [], 0, False
    for node in section_nodes(s, heading):
        for el in [node] + list(node.descendants):
            nm = getattr(el, "name", None)
            if nm in ("p", "b", "dt", "strong", "h4", "h5", "dd", "i") and not (nm in ("p", "dd") and el.find("b")):
                t = el.get_text(" ", strip=True)
                if re.search(r"own[- ]goal", t, re.I) and len(t) < 60:
                    own = True
                elif re.fullmatch(r"(\d+)\s+goals?(\s*\(.*\))?", t, re.I):
                    own, n = False, int(re.match(r"\d+", t).group())
            elif nm == "li" and not own:
                ls = links_in(el)
                if ls:
                    res.append((clean_name(ls[0][0]), ls[0][1], n))
    return res


def _scorer_fn(title, minimum=1, heading="Goalscorers"):
    def fn():
        return dedupe([{"answer": a, "enwiki": l, "detail": f"{n} goal" + ("" if n == 1 else "s")}
                       for a, l, n in scorers(title, heading) if n >= minimum])
    return fn


SCORERS = [
    ("nat048", "Name a player who scored at the 2022 World Cup", "2022 FIFA World Cup"),
    ("nat049", "Name a player who scored at the 2018 World Cup", "2018 FIFA World Cup"),
    ("nat051", "Name a player who scored at Euro 2024", "UEFA Euro 2024"),
    ("nat053", "Name a player who scored at Euro 2020", "UEFA Euro 2020"),
    ("nat054", "Name a player who scored at Euro 2016", "UEFA Euro 2016 statistics"),
    ("nat055", "Name a player who scored at the 2024 Copa América", "2024 Copa América"),
    ("nat056", "Name a player who scored at the 2021 Copa América", "2021 Copa América"),
    ("nat057", "Name a player who scored at the 2025 Africa Cup of Nations", "2025 Africa Cup of Nations"),
    ("nat058", "Name a player who scored at the 2023 Africa Cup of Nations", "2023 Africa Cup of Nations"),
    ("nat059", "Name a player who scored at the 2021 Africa Cup of Nations", "2021 Africa Cup of Nations"),
    ("nat060", "Name a player who scored at the 2019 Africa Cup of Nations", "2019 Africa Cup of Nations"),
    ("nat061", "Name a player who scored at the 2023 AFC Asian Cup", "2023 AFC Asian Cup"),
    ("nat062", "Name a player who scored at the 2025 CONCACAF Gold Cup", "2025 CONCACAF Gold Cup"),
]
for _pid, _text, _title in SCORERS:
    prompt(_pid, _text + " (own goals excluded)", f"en:{_title} — Goalscorers section",
           family="nat-scorer-at-tournament")(_scorer_fn(_title))

prompt("nat005", "Name a player who scored 2 or more goals at the 2026 World Cup (own goals excluded)",
       "en:2026 FIFA World Cup — Goalscorers section", family="nat-scorer-at-tournament")(
    _scorer_fn("2026 FIFA World Cup", 2))


# ------------------------------------------------------------------ match boxes
def name_from_title(t):
    return re.sub(r"\s*\(.*?\)$", "", t).strip()


def boxes(title):
    """[(heading, footballbox div)] in document order."""
    s = soup(title)
    root = s.find("div", class_="mw-parser-output") or s
    cur, out = "", []
    for el in root.descendants:
        nm = getattr(el, "name", None)
        if nm in ("h2", "h3", "h4"):
            cur = heading_text(el)
        elif nm == "div" and "footballbox" in (el.get("class") or []):
            out.append((cur, el))
    return out


def box_scorers(box):
    """[(link, minute-text)] open-play/penalty goals for either side; own goals and shoot-out penalties skipped."""
    out = []
    for tr in box.select("tr.fgoals"):
        prev = tr.find_previous_sibling("tr")
        if prev is not None and re.search(r"penalt", prev.get_text(" ", strip=True), re.I):
            continue  # shoot-out
        for li in tr.find_all("li"):
            txt = li.get_text(" ", strip=True)
            titles = " ".join(x.get("title", "") for x in li.find_all(attrs={"title": True}))
            if re.search(r"own goal|o\.g\.", txt + " " + titles, re.I):
                continue
            a = next((x for x in li.find_all("a") if _link_title(x) and not x.find_parent(class_="flagicon")), None)
            if a is not None:
                out.append((_link_title(a), txt))
    return out


def box_teams(box):
    out = []
    for cls in ("fhome", "faway"):
        th = box.select_one("th." + cls)
        a = next((x for x in th.find_all("a") if _link_title(x) and not x.find_parent(class_="flagicon")), None) if th else None
        if a is not None:
            out.append((a.get_text(" ", strip=True), _link_title(a)))
    return out


def _ko_scorers_fn(title, after=None):
    def fn():
        recs = []
        for head, b in boxes(title):
            if after and not re.search(after, head, re.I):
                continue
            for link, txt in box_scorers(b):
                recs.append({"answer": name_from_title(link), "enwiki": link, "detail": "knockout goal"})
        return dedupe(recs)
    return fn


KO = [
    ("nat050", "Name a player who scored in the knockout stage of the 2022 World Cup", "2022 FIFA World Cup knockout stage"),
    ("nat052", "Name a player who scored in the knockout stage of Euro 2024", "UEFA Euro 2024 knockout stage"),
    ("nat006", "Name a player who scored in the knockout stage of the 2026 World Cup", "2026 FIFA World Cup knockout stage"),
]
for _pid, _text, _title in KO:
    prompt(_pid, _text + " (own goals and shoot-out penalties excluded)", f"en:{_title} — match boxes",
           family="nat-knockout-scorer")(_ko_scorers_fn(_title))


# ------------------------------------------------------------------ finals line-ups
def final_players(title):
    """Starters plus substitutes who came on, from the line-up tables of a match article."""
    s = soup(title)
    recs, ntab = [], 0
    for t in s.find_all("table"):
        if t.find("table"):
            continue
        trs = t.find_all("tr")
        first = next((tr.find_all("td") for tr in trs if tr.find("td")), [])
        if not first or first[0].get_text(strip=True) != "GK":
            continue
        ntab += 1
        subs = False
        for tr in trs:
            tds = tr.find_all("td")
            if not tds:
                continue
            txt = tr.get_text(" ", strip=True)
            if len(tds) == 1 or (tds[0].get("colspan")):
                if re.match(r"Subst", txt):
                    subs = True
                elif re.match(r"(Manager|Head coach|Coach)", txt, re.I):
                    break
                continue
            if len(tds) < 3:
                continue
            ls = [x for x in links_in(tds[2])]
            if not ls:
                continue
            came_on = tr.find(attrs={"title": re.compile("Substituted on", re.I)}) is not None
            if subs and not came_on:
                continue
            recs.append({"answer": name_from_title(ls[0][1]) if "(" in ls[0][1] else ls[0][0],
                         "enwiki": ls[0][1], "detail": "substitute" if subs else "starter"})
    if ntab != 2:
        raise ValueError(f"{title}: expected 2 line-up tables, found {ntab}")
    return dedupe(recs)


FINALS = [
    ("nat007", "Name a player who appeared in the 2026 World Cup final", "2026 FIFA World Cup final"),
    ("nat032", "Name a player who appeared in the 2022 World Cup final", "2022 FIFA World Cup final"),
    ("nat033", "Name a player who appeared in the 2018 World Cup final", "2018 FIFA World Cup final"),
    ("nat034", "Name a player who appeared in the Euro 2024 final", "UEFA Euro 2024 final"),
    ("nat035", "Name a player who appeared in the Euro 2020 final", "UEFA Euro 2020 final"),
    ("nat036", "Name a player who appeared in the 2024 Copa América final", "2024 Copa América final"),
    ("nat047", "Name a player who appeared in the 2021 Copa América final", "2021 Copa América final"),
    ("nat046", "Name a player who appeared in the 2025 UEFA Nations League final", "2025 UEFA Nations League final"),
]
for _pid, _text, _title in FINALS:
    prompt(_pid, _text + " (starters and used substitutes)", f"en:{_title} — line-ups",
           family="nat-final-appearance")(lambda t=_title: final_players(t))


# ------------------------------------------------------------------ venues
from ballion.tables import rows  # noqa: E402

_STADIUM_RE = re.compile(r"stadium|ar[eé]na|stade|stadion|stadio|estadio|estádio|olympi|park|field|dome|parc|"
                         r"azteca|wembley|camp nou|bernabéu|luzhniki|hampden|ibrox|bowl|place|sports city|"
                         r"allianz|westfalen|volksparks|bbva|akron", re.I)
_NOT_STADIUM = re.compile(r"national football team|association|federation|capacity|metropolitan|county", re.I)


DISPLAY = {"Central Stadium (Yekaterinburg)": "Ekaterinburg Arena (Central Stadium)"}


def venues(title, section="Venues"):
    """[(display, link)] of stadium articles in a tournament's Venues section."""
    s = soup(title)
    seen, out = set(), []
    for n in section_nodes(s, section):
        for t in ([n] if n.name == "table" else n.find_all("table")):
            rs = list(rows(t))
            if not rs:
                continue
            hdr = rs[0][0]
            if any(re.search(r"team|camp|training|group", c, re.I) for c in hdr):
                continue  # base-camp / training-site tables
            col = next((i for i, c in enumerate(hdr) if c.strip().lower() == "stadium"), None)
            for tx, ln in rs[1:] if col is not None else rs:
                cells = [ln[col]] if col is not None else ln
                for ls in cells:
                    for link in ls:
                        if link in seen or _NOT_STADIUM.search(link):
                            continue
                        if col is None and not _STADIUM_RE.search(link):
                            continue
                        seen.add(link)
                        out.append((DISPLAY.get(link) or name_from_title(link), link))
    return out


def _venue_fn(parts):
    def fn():
        recs = []
        for title, sec in parts:
            recs += [{"answer": a, "enwiki": l, "detail": title} for a, l in venues(title, sec)]
        return dedupe(recs)
    return fn


VENUES = [
    ("nat003", "Name a stadium that hosted a match at the 2026 World Cup", [("2026 FIFA World Cup", "Venues")]),
    ("nat131", "Name a stadium that hosted a match at the 2018 or 2022 World Cup",
     [("2018 FIFA World Cup", "Venues"), ("2022 FIFA World Cup", "Venues")]),
    ("nat132", "Name a stadium that hosted a match at Euro 2020 or Euro 2024",
     [("UEFA Euro 2020", "Venues"), ("UEFA Euro 2024", "Venues")]),
    ("nat134", "Name a stadium that hosted a match at the 2024 Copa América", [("2024 Copa América", "Venues")]),
    ("nat135", "Name a stadium that hosted a match at the 2023 or 2025 Africa Cup of Nations",
     [("2023 Africa Cup of Nations", "Venues"), ("2025 Africa Cup of Nations", "Venues")]),
    ("nat136", "Name a stadium that hosted a match at the 2019 or 2023 AFC Asian Cup",
     [("2019 AFC Asian Cup", "Venues"), ("2023 AFC Asian Cup", "Venues")]),
    ("nat137", "Name a stadium that hosted a match at the 2025 CONCACAF Gold Cup", [("2025 CONCACAF Gold Cup", "Venues")]),
]
for _pid, _text, _parts in VENUES:
    prompt(_pid, _text, "en:" + ", ".join(f"{t}#{s}" for t, s in _parts), family="nat-stadium")(_venue_fn(_parts))


@prompt("nat004", "Name a host city of the 2026 World Cup", "en:2026 FIFA World Cup#Venues — City column",
        family="nat-host-city")
def _nat004():
    s = soup("2026 FIFA World Cup")
    t = next(x for n in section_nodes(s, "Venues") for x in ([n] if n.name == "table" else n.find_all("table")))
    alias = {"New York/New Jersey": "New York City", "San Francisco Bay Area": "San Francisco Bay Area"}
    recs = []
    for tx, ln in list(rows(t))[1:]:
        fifa = re.sub(r"\s*\(.*", "", tx[0]).strip()
        city = alias.get(fifa, fifa)
        recs.append({"answer": fifa.replace("/", " / "), "enwiki": city, "detail": tx[0]})
    return dedupe(recs)
