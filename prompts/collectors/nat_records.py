"""nat: record / list prompts (all-time leaders, goals against, awards, red cards, own goals, hat-tricks)."""
import re

from bs4 import BeautifulSoup

from ballion.registry import prompt
from ballion.tables import _link_title, rows
from prompts.collectors.nat_countries import _members
from prompts.collectors.nat_tournaments import name_from_title, scorers
from prompts.collectors.nat_util import dedupe, soup_noflags


def tables(page):
    return soup_noflags(page).find_all("table")


def hdr(t):
    r = next(rows(t), None)
    return [re.sub(r"\s+", " ", c).strip() for c in r[0]] if r else []


def find_tables(page, first, second=None, min_rows=2, max_rows=10 ** 6):
    out = []
    for t in tables(page):
        h = hdr(t)
        n = len(t.find_all("tr"))
        if h[:1] == [first] and (second is None or h[1:2] == [second]) and min_rows <= n <= max_rows:
            out.append(t)
    return out


def pl_link(ls):
    """Player article from the links of a cell (skip list / team / tournament links)."""
    for x in ls:
        if x.startswith(("List of", "Own goal")) or "national" in x or "FIFA World Cup" in x or "UEFA Euro" in x:
            continue
        return x
    return None


def rec(link, detail):
    return {"answer": name_from_title(link), "enwiki": link, "detail": detail}


# ------------------------------------------------------------------ top 10 caps / goals
TOP10 = [
    ("nat149", "France", "France national football team"),
    ("nat150", "Brazil", "Brazil national football team"),
    ("nat151", "Argentina", "Argentina national football team"),
    ("nat152", "Portugal", "Portugal national football team"),
    ("nat153", "the United States", "United States men's national soccer team"),
    ("nat154", "Nigeria", "Nigeria national football team"),
    ("nat155", "South Korea", "South Korea national football team"),
    ("nat156", "Egypt", "Egypt national football team"),
]


def _poss(n):
    return n + ("'" if n.endswith("s") else "'s")


def _top10(page):
    def fn():
        recs = []
        for t in tables(page):
            h = hdr(t)
            n = len(t.find_all("tr"))
            if h[:2] == ["Rank", "Player"] and h[2:3] in (["Caps"], ["Goals"]) and n <= 16:
                kind = "caps" if h[2] == "Caps" else "goals"
                for tx, ln in list(rows(t))[1:]:
                    l = pl_link(ln[1])
                    if l:
                        recs.append(rec(l, f"top 10 for {kind} (rank {tx[0]})"))
        return dedupe(recs)
    return fn


for _pid, _name, _page in TOP10:
    prompt(_pid, f"Name a player in {_poss(_name)} all-time top 10 for caps or for goals", f"en:{_page} — most appearances + top goalscorers tables",
           family="nat-alltime-top10")(_top10(_page))


# ------------------------------------------------------------------ top scorer of a confederation's teams
def _conf_top_scorers(heading):
    def fn():
        members = {r["enwiki"] for r in _members(heading)}
        recs = []
        for t in tables("List of top international men's football goalscorers by country"):
            h = hdr(t)
            if h[:4] == ["Rank", "Player", "Country", "Goals"]:
                for tx, ln in list(rows(t))[1:]:
                    team = next((x for x in ln[2] if "national" in x), None)
                    if team in members and ln[1]:
                        recs.append(rec(ln[1][-1], f"{tx[2]}: {tx[3]} goals"))
        return dedupe(recs)
    return fn


for _pid, _label, _head in [("nat157", "a UEFA national team", "UEFA ( Europe )"),
                            ("nat158", "an African (CAF) national team", "CAF ( Africa )"),
                            ("nat159", "an Asian (AFC) national team", "AFC ( Asia )"),
                            ("nat160", "a CONCACAF national team", "CONCACAF ( North America )")]:
    prompt(_pid, f"Name the all-time top scorer of {_label} (record holders only; ties included)",
           "en:List of top international men's football goalscorers by country — rows joined to confederation member lists",
           family="nat-top-scorer-confederation")(_conf_top_scorers(_head))


# ------------------------------------------------------------------ 100+ caps by confederation
def _caps100(conf):
    def fn():
        recs = []
        for t in tables("List of men's footballers with 100 or more international caps"):
            h = hdr(t)
            if h[:5] == ["Rank", "Player", "Nation", "Confederation", "Caps"]:
                for tx, ln in list(rows(t))[1:]:
                    if tx[3].strip() == conf and ln[1]:
                        recs.append(rec(ln[1][-1], f"{tx[4]} caps ({tx[2]})"))
        return dedupe(recs)
    return fn


for _pid, _label, _c in [("nat161", "a South American man", "CONMEBOL"), ("nat162", "an African man", "CAF"),
                         ("nat163", "a CONCACAF man", "CONCACAF")]:
    prompt(_pid, f"Name {_label} with 100 or more international caps",
           f"en:List of men's footballers with 100 or more international caps — Confederation = {_c}",
           family="nat-100-caps")(_caps100(_c))


# ------------------------------------------------------------------ countries a striker has scored against
def _against(page):
    def fn():
        recs = []
        for t in tables(page):
            h = hdr(t)
            if "Opponent" in h and "Date" in h and len(t.find_all("tr")) > 20:
                oi = h.index("Opponent")
                for tx, ln in list(rows(t))[1:]:
                    team = next((x for x in ln[oi] if "national" in x and ("football team" in x or "soccer team" in x)), None)
                    if team:
                        name = re.sub(r" (men's )?national (football|soccer) team$", "", team)
                        recs.append({"answer": name, "enwiki": team, "detail": f"scored against ({tx[h.index('Date')]})"})
                break
        return dedupe(recs)
    return fn


AGAINST = [("nat164", "Lionel Messi"), ("nat165", "Cristiano Ronaldo"), ("nat166", "Harry Kane"),
           ("nat167", "Robert Lewandowski"), ("nat168", "Kylian Mbappé"), ("nat169", "Neymar"),
           ("nat170", "Romelu Lukaku"), ("nat171", "Erling Haaland"), ("nat172", "Edin Džeko"),
           ("nat173", "Sunil Chhetri"), ("nat174", "Ali Daei")]
for _pid, _p in AGAINST:
    prompt(_pid, f"Name a country {_p} has scored against for his national team",
           f"en:List of international goals scored by {_p} — Opponent column", family="nat-scored-against")(
        _against(f"List of international goals scored by {_p}"))


# ------------------------------------------------------------------ scorers for one nation at a tournament
def _own_goal_after(a):
    nxt = ""
    for sib in a.next_siblings:
        if getattr(sib, "name", None) == "a":
            break
        nxt += sib.get_text() if hasattr(sib, "get_text") else str(sib)
        if "," in nxt:
            break
    return re.search(r"o\.?g\.?|own goal", nxt.split(",")[0], re.I) is not None


def _nation_scorers(page, kind):
    def fn():
        recs = []
        for t in tables(page):
            h = hdr(t)
            if kind == "by-tournament" and len(h) == 2 and h[1].lower().startswith("goalscorer"):
                for tr in t.find_all("tr")[1:]:
                    cells = tr.find_all(["td", "th"])
                    for a in cells[-1].find_all("a"):
                        l = _link_title(a)
                        if l and not _own_goal_after(a):
                            recs.append(rec(l, f"scored in {cells[0].get_text(' ', strip=True)}"))
            elif kind == "player-table" and h[:2] == ["Player", "Goals"] and len(t.find_all("tr")) > 8:
                for tx, ln in list(rows(t))[1:]:
                    l = pl_link(ln[0])
                    if l and tx[1].strip().isdigit() and int(tx[1]) > 0:
                        recs.append(rec(l, f"{tx[1]} goals"))
        return dedupe(recs)
    return fn


NATION = [
    ("nat175", "England", "a men's World Cup", "England at the FIFA World Cup", "by-tournament"),
    ("nat176", "England", "a men's European Championship", "England at the UEFA European Championship", "by-tournament"),
    ("nat179", "Portugal", "a men's World Cup", "Portugal at the FIFA World Cup", "player-table"),
    ("nat181", "the United States", "a men's World Cup", "United States at the FIFA World Cup", "player-table"),
    ("nat182", "Japan", "a men's World Cup", "Japan at the FIFA World Cup", "player-table"),
    ("nat183", "Morocco", "a men's World Cup", "Morocco at the FIFA World Cup", "player-table"),
]
for _pid, _team, _tour, _page, _kind in NATION:
    prompt(_pid, f"Name a player who has scored for {_team} at {_tour}", f"en:{_page} — goalscorers table",
           family="nat-nation-scorer")(_nation_scorers(_page, _kind))


# ------------------------------------------------------------------ World Cup records
@prompt("nat184", "Name a player who has scored 5 or more goals at men's World Cups (career total)",
        "en:List of FIFA World Cup top goalscorers — all-time table (5+ goals)", family="nat-wc-record")
def _nat184():
    t = find_tables("List of FIFA World Cup top goalscorers", "Rank", "Player", min_rows=50)[0]
    recs = []
    for tx, ln in list(rows(t))[1:]:
        if tx[3].isdigit() and int(tx[3]) >= 5 and ln[1]:
            recs.append(rec(ln[1][0], f"{tx[3]} goals ({tx[2]})"))
    return dedupe(recs)


@prompt("nat185", "Name a player who has scored an own goal at a men's World Cup",
        "en:List of FIFA World Cup own goals — own goals table", family="nat-wc-record")
def _nat185():
    t = find_tables("List of FIFA World Cup own goals", "No.", "Player", min_rows=30)[0]
    recs = []
    for tx, ln in list(rows(t))[1:]:
        if ln[1]:
            recs.append(rec(ln[1][0], f"own goal for {tx[3]}"))
    return dedupe(recs)


@prompt("nat186", "Name a player who has been sent off at a men's World Cup since 2010",
        "en:List of FIFA World Cup red cards — players table, 2010–2026", family="nat-wc-record")
def _nat186():
    t = find_tables("List of FIFA World Cup red cards", "Tournament", "#", min_rows=100)[0]
    recs = []
    for tx, ln in list(rows(t))[1:]:
        m = re.match(r"(\d{4})", tx[0])
        if m and int(m.group(1)) >= 2010 and ln[3]:
            recs.append(rec(ln[3][0], f"sent off in {tx[0]}"))
    return dedupe(recs)


@prompt("nat187", "Name a man who switched to a second senior national team in 2021 or later",
        "en:List of association football players capped by two senior national teams — 2021–present (women filtered out)",
        family="nat-switch")
def _nat187():
    from prompts.collectors.nat_tournaments import section_nodes
    s = soup_noflags("List of association football players capped by two senior national teams")
    recs = []
    for n in section_nodes(s, "2021–present"):
        for t in ([n] if n.name == "table" else n.find_all("table")):
            for tx, ln in list(rows(t))[1:]:
                if "female" in tx[0].lower() or not ln[0]:
                    continue
                recs.append(rec(ln[0][0], f"{tx[1]} to {tx[2]} ({tx[3]})"))
    return dedupe(recs)


@prompt("nat188", "Name a player named in the UEFA Team of the Tournament at Euro 2016, 2020 or 2024",
        "en:UEFA European Championship awards — Team of the Tournament table", family="nat-award")
def _nat188():
    t = find_tables("UEFA European Championship awards", "Edition", "Goalkeepers")[0]
    recs = []
    for tx, ln in list(rows(t))[1:]:
        m = re.search(r"(2016|2020|2024)", tx[0])
        if m:
            for cell in ln[1:5]:
                for l in cell:
                    recs.append(rec(l, f"Team of the Tournament {m.group(1)}"))
    return dedupe(recs)


@prompt("nat189", "Name a winner of the World Cup Golden Ball, Golden Boot, Golden Glove or Young Player award since 2006",
        "en:FIFA World Cup awards — Golden Ball, Golden Boot, Golden Glove, Young Player tables (2006–2026)",
        family="nat-award")
def _nat189():
    page = "FIFA World Cup awards"
    recs = []
    specs = [("World Cup", "Golden Ball", "Golden Ball", 1), ("Top goalscorer", "Top goalscorer", "Golden Boot", 1),
             ("World Cup", "Lev Yashin Award", "Golden Glove", 1), ("World Cup", "FIFA Young Player", "Young Player", 1)]
    for t in tables(page):
        h = hdr(t)
        rs = list(rows(t))
        if h[:2] == ["World Cup", "Golden Ball"]:
            kind, start = "Golden Ball", 1
        elif h[:1] == ["Top goalscorer"] and len(rs) > 2 and rs[1][0][:2] == ["World Cup", "Top goalscorer"]:
            kind, start = "Golden Boot", 2
        elif h[:2] == ["World Cup", "Lev Yashin Award"] or (h[:1] == ["Lev Yashin Award"] and rs[1][0][:2] == ["World Cup", "Lev Yashin Award"]):
            kind, start = "Golden Glove", 2 if h[:1] == ["Lev Yashin Award"] else 1
        elif h[:2] == ["World Cup", "FIFA Young Player"]:
            kind, start = "Young Player", 1
        else:
            continue
        for tx, ln in rs[start:]:
            m = re.search(r"(\d{4})", tx[0]) if len(tx[0]) < 40 else None
            if m and int(m.group(1)) >= 2006 and len(ln) > 1:
                l = pl_link(ln[1])
                if l:
                    recs.append(rec(l, f"{kind} {m.group(1)}"))
    return dedupe(recs)


@prompt("nat190", "Name a player who has scored a hat-trick for England (men's team)",
        "en:List of England national football team hat-tricks — full table", family="nat-hat-trick")
def _nat190():
    t = find_tables("List of England national football team hat-tricks", "No.", "Date", min_rows=50)[0]
    recs = []
    for tx, ln in list(rows(t))[1:]:
        l = pl_link(ln[3])
        if l:
            recs.append(rec(l, f"{tx[2]} goals v {tx[4]} ({tx[1]})"))
    return dedupe(recs)


@prompt("nat191", "Name a player who has scored a hat-trick at the Copa América",
        "en:List of Copa América hat-tricks — full table", family="nat-hat-trick")
def _nat191():
    t = find_tables("List of Copa América hat-tricks", "Sequence", "Player", min_rows=50)[0]
    recs = []
    for tx, ln in list(rows(t))[1:]:
        l = pl_link(ln[1])
        if l:
            recs.append(rec(l, f"{tx[2]} goals for {tx[4]} ({tx[7]})"))
    return dedupe(recs)


@prompt("nat063", "Name a player who scored 5 or more goals in UEFA qualifying for the 2026 World Cup",
        "en:2026 FIFA World Cup qualification (UEFA) — Top goalscorers section", family="nat-qualifying-scorer")
def _nat063():
    return dedupe([rec(l, f"{n} goals") for a, l, n in scorers("2026 FIFA World Cup qualification (UEFA)", "Top goalscorers")
                   if n >= 5 and "qualification" not in l and not re.match(r"\d{4}", l)])
