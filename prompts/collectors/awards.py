"""p004-p023: individual honours (awards and top-scorer titles)."""
import re

from ballion.registry import prompt
from ballion.tables import _link_title, wikitables

NAT_TEAM = re.compile(r"national (football|soccer) team|national under-")


# ---------------------------------------------------------------- helpers
def _int(v):
    return int(re.sub(r"\D", "", str(v)) or 1)


def _rows(table):
    """Like ballion.tables.rows, but flag icons are dropped, links are (title, anchor text) pairs,
    and malformed rowspan/colspan attributes (e.g. '2"') are tolerated."""
    for f in table.select("span.flagicon"):
        f.decompose()
    pending = {}
    for tr in table.find_all("tr"):
        cells = tr.find_all(["td", "th"], recursive=False)
        texts, links, col = [], [], 0
        it = iter(cells)
        while True:
            if col in pending:
                p = pending[col]
                texts.append(p[1]); links.append(p[2])
                p[0] -= 1
                if p[0] == 0:
                    del pending[col]
                col += 1
                continue
            c = next(it, None)
            if c is None:
                break
            t = c.get_text(" ", strip=True)
            ls = [(x, a.get_text(" ", strip=True)) for a in c.find_all("a") if (x := _link_title(a))]
            span, rs = _int(c.get("colspan", 1)), _int(c.get("rowspan", 1))
            for _ in range(span):
                if rs > 1:
                    pending[col] = [rs - 1, t, ls]
                texts.append(t); links.append(ls)
                col += 1
        yield texts, links


def _heading(t):
    h = t.find_previous(["h2", "h3", "h4"])
    return h.get_text(" ", strip=True) if h else ""


def _table(page, header, heading=None):
    """The first wikitable whose header row starts with `header` (and, optionally, whose
    preceding section heading contains `heading`)."""
    for t in wikitables(page):
        first = next(_rows(t))[0]
        if first[:len(header)] == header and (heading is None or heading in _heading(t)):
            return t
    raise LookupError(f"{page}: no table with header {header} / heading {heading}")


def _people(cell_links):
    """Person links in a cell (flags already removed; national-team links dropped)."""
    return [(t, txt) for t, txt in cell_links if not NAT_TEAM.search(t)]


class Acc:
    """Accumulate answers keyed by enwiki title, preserving first-seen order."""

    def __init__(self):
        self.d = {}

    def add(self, title, name, ev):
        name = re.sub(r"\s*[†‡§*#^]+$", "", re.sub(r"\s*\(\d+\)$", "", name)).strip()
        r = self.d.setdefault(title, {"answer": name, "enwiki": title, "ev": []})
        if ev not in r["ev"]:
            r["ev"].append(ev)

    def out(self, joiner=", "):
        return [{"answer": r["answer"], "enwiki": r["enwiki"], "detail": joiner.join(r["ev"])}
                for r in self.d.values()]


def _season_winners(table, season_col, player_col, acc=None, label="", season_ok=None, club_col=None):
    """Add every person linked in `player_col` for rows whose season looks like a year."""
    acc = acc or Acc()
    for tx, ln in _rows(table):
        if len(tx) <= player_col:
            continue
        season = tx[season_col].strip()
        if not re.match(r"^\d{4}", season) or (season_ok and not season_ok(season, ln[season_col])):
            continue
        season = re.match(r"^[\d–/\-]+", season).group(0).strip("–-")
        club = ""
        if club_col is not None and len(_people(ln[club_col])) == 1:
            club = f" ({_people(ln[club_col])[0][1]})"
        for title, name in _people(ln[player_col]):
            acc.add(title, name, f"{label}{season}{club}")
    return acc


RANK = {"1st": 1, "2nd": 2, "3rd": 3}


def _ranked(table, max_rank, acc=None, label="", year_ok=None, rank_label=False):
    """Year | Rank | Player ... tables (Ballon d'Or, continental awards)."""
    acc = acc or Acc()
    for tx, ln in _rows(table):
        if len(tx) < 3 or not re.match(r"^\d{4}$", tx[0]) or RANK.get(tx[1], 99) > max_rank:
            continue
        if year_ok and not year_ok(int(tx[0])):
            continue
        for title, name in _people(ln[2]):
            acc.add(title, name, f"{label}{tx[0]}" + (f" {tx[1]}" if rank_label else ""))
    return acc


YRP = ["Year", "Rank", "Player"]


# ---------------------------------------------------------------- Ballon d'Or / FIFA
@prompt("p004", "Name a winner of the men's Ballon d'Or (1956–2025, including the 2010–15 FIFA Ballon d'Or)",
        "en:Ballon d'Or — Winners table (1st place)")
def ballon_dor():
    return _ranked(_table("Ballon d'Or", YRP + ["Team"]), 1).out()


@prompt("p005", "Name a player who has finished in the top 3 of the men's Ballon d'Or voting (1956–2025)",
        "en:Ballon d'Or — Winners table (1st–3rd place)")
def ballon_dor_podium():
    return _ranked(_table("Ballon d'Or", YRP + ["Team"]), 3, rank_label=True).out()


@prompt("p006", "Name a winner of FIFA's men's player of the year award (FIFA World Player of the Year 1991–2009, "
        "FIFA Ballon d'Or 2010–15, or The Best FIFA Men's Player 2016–)",
        "en:FIFA World Player of the Year, en:Ballon d'Or (2010–15 rows), en:The Best FIFA Men's Player — 1st place")
def fifa_player():
    acc = _ranked(_table("FIFA World Player of the Year", YRP, heading="FIFA World Player of the Year"), 1)
    _ranked(_table("Ballon d'Or", YRP + ["Team"]), 1, acc, year_ok=lambda y: 2010 <= y <= 2015)
    _ranked(_table("The Best FIFA Men's Player", YRP), 1, acc)
    return acc.out()


# ---------------------------------------------------------------- golden shoes / English awards
@prompt("p007", "Name a winner of the European Golden Shoe (top scorer across Europe's leagues)",
        "en:European Golden Shoe — winners table (L'Équipe 1968–91, ESM 1997–)")
def golden_shoe():
    t = _table("European Golden Shoe", ["Season", "Player", "Club"])
    return _season_winners(t, 0, 1, club_col=2).out()


@prompt("p008", "Name a player who has won (or shared) the Premier League Golden Boot",
        "en:Premier League Golden Boot — winners table")
def pl_golden_boot():
    t = _table("Premier League Golden Boot", ["Season", "Player", "Nationality", "Club"])
    return _season_winners(t, 0, 1, club_col=3).out()


@prompt("p009", "Name a winner of the Premier League Player of the Season award",
        "en:Premier League Player of the Season — winners table")
def pl_pots():
    t = _table("Premier League Player of the Season", ["Season", "Player", "Position"])
    return _season_winners(t, 0, 1, club_col=4).out()


@prompt("p010", "Name a winner of the PFA Players' Player of the Year award (England)",
        "en:PFA Players' Player of the Year — winners table")
def pfa_poty():
    t = _table("PFA Players' Player of the Year", ["Year", "", "Player", "Club"])
    return _season_winners(t, 0, 2, club_col=3).out()


@prompt("p011", "Name a winner of the FWA Footballer of the Year award (England, men's)",
        "en:FWA Footballer of the Year — winners table")
def fwa_foty():
    t = _table("FWA Footballer of the Year", ["Year", "Nat.", "Player", "Club"])
    return _season_winners(t, 0, 2, club_col=3).out()


# ---------------------------------------------------------------- World Cup
@prompt("p012", "Name a player who won the Golden, Silver or Bronze Ball at a men's FIFA World Cup (1982–2026)",
        "en:FIFA World Cup awards — Golden Ball table (official winners 1982–present)")
def wc_golden_ball():
    acc = Acc()
    for tx, ln in _rows(_table("FIFA World Cup awards", ["World Cup", "Golden Ball", "Silver Ball"])):
        if not re.match(r"^\d{4}", tx[0]):
            continue
        for col, award in ((1, "Golden"), (2, "Silver"), (3, "Bronze")):
            for title, name in _people(ln[col]):
                acc.add(title, name, f"{tx[0][:4]} {award}")
    return acc.out()


@prompt("p013", "Name a player who was the top scorer (Golden Boot/Shoe winner, incl. joint and retrospective "
        "pre-1982 top scorers) at a men's FIFA World Cup",
        "en:FIFA World Cup awards — Golden Boot table, 'Top goalscorer'/'Golden Shoe'/'Golden Boot' column")
def wc_golden_boot():
    t = _table("FIFA World Cup awards", ["Top goalscorer"], heading="Golden Boot")
    acc = Acc()
    for tx, ln in _rows(t):
        if len(tx) < 3 or not re.match(r"^\d{4}", tx[0]):
            continue
        for title, name in _people(ln[1]):
            acc.add(title, name, f"{tx[0][:4]} ({tx[2]} goals)")
    return acc.out()


# ---------------------------------------------------------------- continental awards
@prompt("p014", "Name a winner of the African Footballer of the Year award (France Football 1970–94 or CAF 1992–)",
        "en:African Footballer of the Year — France Football award + CAF award tables (1st place)")
def african_foty():
    p = "African Footballer of the Year"
    acc = _ranked(_table(p, YRP, heading="France Football"), 1, label="FF ")
    _ranked(_table(p, YRP, heading="CAF award"), 1, acc, label="CAF ")
    return acc.out()


@prompt("p015", "Name a winner of the (men's) South American Footballer of the Year award "
        "(El Mundo 1971–85 or El País 1986–)",
        "en:South American Footballer of the Year — El Mundo (1971–85) + El País (1986–) tables (1st place)")
def south_american_foty():
    p = "South American Footballer of the Year"
    acc = _ranked(_table(p, YRP, heading="El Mundo award (1971"), 1)
    _ranked(_table(p, YRP, heading="El País award (1986"), 1, acc)
    return acc.out()


@prompt("p016", "Name a winner of the Asian Footballer of the Year award (AFC award incl. AFC International "
        "Player of the Year, or the IFFHS award)",
        "en:Asian Footballer of the Year — IFFHS, AFC and AFC International tables (1st place)")
def asian_foty():
    p = "Asian Footballer of the Year"
    acc = _ranked(_table(p, YRP, heading="IFFHS"), 1, label="IFFHS ")
    _ranked(_table(p, YRP, heading="AFC award (international)"), 1, acc, label="AFC Intl ")
    _ranked([t for t in wikitables(p) if _heading(t) == "AFC award"][0], 1, acc, label="AFC ")
    return acc.out()


@prompt("p017", "Name a winner of Tuttosport's Golden Boy award (best under-21 player in Europe)",
        "en:Golden Boy (award) — winners table")
def golden_boy():
    t = _table("Golden Boy (award)", ["Year", "Winner", "Club(s)"])
    return _season_winners(t, 0, 1, club_col=2).out()


# ---------------------------------------------------------------- league / competition top scorers
@prompt("p018", "Name a player who has finished a season as La Liga's top scorer (Pichichi Trophy, men's)",
        "en:Pichichi Trophy — Men winners table")
def pichichi():
    t = _table("Pichichi Trophy", ["Season", "Player(s)"], heading="Men")
    return _season_winners(t, 0, 1).out()


@prompt("p019", "Name a player who has finished a Serie A season as top scorer (Capocannoniere, 1929–30 onwards)",
        "en:Capocannoniere — Winners table, Serie A seasons only")
def capocannoniere():
    t = _table("Capocannoniere", ["Season", "Player(s)"])
    return _season_winners(t, 0, 1, season_ok=lambda s, l: any("Serie A" in x for x, _ in l)).out()


@prompt("p020", "Name a player who has finished a season as the Bundesliga's top scorer",
        "en:List of Bundesliga top scorers by season — Winners table")
def bundesliga_top():
    t = _table("List of Bundesliga top scorers by season", ["Season", "Player(s)"])
    return _season_winners(t, 0, 1).out()


@prompt("p021", "Name a player who has finished a season as top scorer of France's top flight (Ligue 1 / Division 1)",
        "en:List of Ligue 1 top scorers — Top scorers by season table")
def ligue1_top():
    t = _table("List of Ligue 1 top scorers", ["Season", "Player(s)"])
    return _season_winners(t, 0, 1).out()


@prompt("p022", "Name a player who has been (joint) top scorer of a European Cup / UEFA Champions League season",
        "en:List of UEFA Champions League top scorers — Top scorers by season table")
def ucl_top():
    t = _table("List of UEFA Champions League top scorers", ["Season", "Player(s)"])
    return _season_winners(t, 0, 1).out()


@prompt("p023", "Name a player who was (joint) top scorer at a UEFA European Championship finals tournament",
        "en:UEFA European Championship top goalscorers — Top goalscorers for each tournament table")
def euro_top():
    t = _table("UEFA European Championship top goalscorers", ["Edition", "Player", "Team"])
    acc = Acc()
    for tx, ln in _rows(t):
        if len(tx) < 4 or not re.match(r"^\d{4}", tx[0]):
            continue
        for title, name in _people(ln[1]):
            acc.add(title, name, f"{tx[0][:4]} ({re.sub(r'[^0-9]', '', tx[3])} goals)")
    return acc.out()
