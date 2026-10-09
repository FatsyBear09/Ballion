# Themed prompt catalogs (draft, awaiting approval)

Five themes of about 200 new prompts each, plus the existing p001–p103 reassigned to themes (`existing.md`). The drafting rules are in `SPEC.md`. These are **catalogs only**: every source page title is verified to exist on en.wikipedia, but no collectors are written and no answer CSVs exist yet.

| theme | file | new | existing | total | modern | 2000s+ | classic |
|---|---|---|---|---|---|---|---|
| General | `general.md` | 200 | 34 | 234 | 131 | 59 | 10 |
| Premier League | `premier_league.md` | 179 | 25 | 204 | 119 | 51 | 9 |
| La Liga | `laliga.md` | 200 | 8 | 208 | 132 | 59 | 9 |
| Champions League | `champions_league.md` | 200 | 7 | 207 | 137 | 50 | 13 |
| National football | `national.md` | 200 | 29 | 229 | 151 | 43 | 6 |
| **Total** | | **979** | **103** | **1082** | 670 (68%) | 262 (27%) | 47 (5%) |

Era counts cover the new prompts only. "modern" means the answers come mostly from 2015 onward; "classic" means pre-2000-heavy. Many of the existing p001–p103 prompts are all-time ("classic") lists.

## Before building
- **Template siblings.** Many prompts are deliberate siblings that differ only by season, club or nationality, for example "<nationality> player in the PL since 2015–16" or "<season> UCL knockout scorers". Each family is capped at about 10% of its theme, but the game's prompt picker should also allow at most one per family in a 7-round game. Otherwise a game can feel repetitive, the same way the existing "≤2 per theme group" rule prevents that.
- **Live-season prompts** (2026–27 squads, current call-ups, the 2026 Ballon d'Or) change over time. Freeze them at scrape time and re-scrape each season.
- **Wikidata "played for both X and Y" prompts** (pl120–pl131, about 17 in General) need manual curation because club-membership data has gaps.
- **Possibly off-theme for younger fans:** pl009 (League One Player of the Month) and pl135 (National League clubs).
- Each file ends with a `## Summary` that lists its risky prompts (near the 12/120 answer bounds, hard scrapes, contested results).
