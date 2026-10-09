# Themed prompt catalogs: drafting spec

Ballion is splitting its prompts into five themes, each targeting ~200 prompts:

| theme | file | id prefix | scope |
|---|---|---|---|
| General | `general.md` | `gen` | Everything not owned by another theme: Ballon d'Or and other individual awards, Bundesliga, Serie A, Ligue 1, Eredivisie, Primeira Liga, MLS, Saudi Pro League, other leagues, transfers, Club World Cup, Europa/Conference League, cross-league careers, video game/cover-athlete style pop-culture lists with Wikipedia articles |
| Premier League | `premier_league.md` | `pl` | English football in the Premier League era (1992+): PL clubs, players, managers, records, seasons, awards, FA Cup, League Cup, Community Shield, Championship-promotion |
| La Liga | `laliga.md` | `ll` | Spanish football: La Liga, Copa del Rey, Supercopa, Spanish clubs, players and managers in Spain, El Clásico, Pichichi/Zamora |
| Champions League | `champions_league.md` | `ucl` | UEFA Champions League (and some European Cup history): winners, finals, squads, scorers, records, group-stage/knockout participants, managers |
| National football | `national.md` | `nat` | National teams: World Cups, Euros, Copa América, AFCON, Asian Cup, Gold Cup, Nations League, caps/goals, squads, captains, managers, qualifiers |

## Hard rules for every prompt
1. **Answers are Wikipedia entities.** Every answer must have its own English Wikipedia article (player, manager, club, national team, stadium, city, company). No numbers, years, scores or free text as answers. Rarity is computed from page views of these articles.
2. **Answer count 12–120** (hard ceiling 130). Prompts below 12 answers are too small for tiers; above 130 is a slog. Prefer 20–80.
3. **Scrapable source.** Each prompt names a concrete English Wikipedia page (and section/table if needed) from which the full answer list can be scraped by a script. The page title **must be verified to exist** via the Wikipedia API (see below). A Wikidata SPARQL source is acceptable if you state the property logic, but prefer page tables.
4. **Unambiguous rule.** The inclusion rule must be decidable from the source (e.g. "at least 1 Premier League appearance in 2015–16 per the season squad table"). Note edge cases in the notes column.
5. **Recency for younger players.** Weight toward football a 15–25 year old would know:
   - **≥ 60%** of prompts `modern` (answers mostly from 2015 onward, or current/recent seasons)
   - **≤ 30%** `2000s+` (answers span roughly 2000 onward)
   - **≤ 10%** `classic` (all-time / pre-2000 heavy), and only iconic ones
6. **Variety.** No single template family (e.g. "Name a player in <club>'s <season> squad") may exceed ~10% of a theme. Mix players, clubs, managers, countries, stadiums, transfers, records, awards, firsts, career paths ("played for both X and Y"), nationality filters ("Name a Brazilian who has played in the Premier League"), etc.
7. **No duplicates** of the existing 103 prompts in `prompts/catalog.md` (they get reassigned to themes separately), nor of prompts obviously belonging to another theme.
8. **Fun > trivia.** Prompts should feel like a pub quiz a young fan would enjoy: recognisable stars should be valid common answers, with deep cuts as legendary answers. Avoid prompts where every answer is obscure.

## Verifying source titles
Batch up to 50 titles per request (follow redirects; a title in `missing` does not exist):
```
curl -s -A "Ballion/0.1 (https://github.com/FatsyBear09/Ballion)" \
  "https://en.wikipedia.org/w/api.php?action=query&format=json&redirects=1&titles=TITLE1|TITLE2"
```
URL-encode titles (en dash `–` is `%E2%80%93`). Keep it to ≤ 2 requests/second. To sanity-check answer counts, fetch a page's wikitext or HTML (`action=parse&page=...&prop=wikitext`) for a sample of prompts, especially ones whose estimate you are unsure of.

## Output format
One markdown file per theme. Group prompts under `##` sub-headings (e.g. "Records", "Clubs", "Squads"), each a table:

```
| id | prompt | source | est. | era | sample answers (common → rare) | notes |
|---|---|---|---|---|---|---|
| pl001 | Name a player who has scored a Premier League hat-trick since 2015 | en:List of Premier League hat-tricks | 90 | modern | Haaland, Salah, Son, Wood, Mitrović | count hat-tricks dated 2015-08-01 onward |
```
End the file with a `## Summary` section: total prompts, count per era, count per sub-heading, and any prompts you'd flag as risky.
