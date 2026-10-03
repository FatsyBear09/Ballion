# Ballion

A football (soccer) take on krillion.io. Players get a prompt ("Name a player who scored 100+ La Liga goals") and must give a valid answer. Rarer answers score more, and in the game an 8-bit striker kicks the ball farther. Live at https://fatsybear09.github.io/Ballion/ (repo is public).

## Layout
- `prompts/catalog.md`: all 103 prompts by theme (p001–p003 written by the user, p004–p103 drafted by Claude and approved by the user)
- `prompts/collectors/*.py`: one scraper per prompt, registered with `@prompt(pid, text, source)` from `ballion/registry.py`. Each returns `[{answer, enwiki, detail}]`; `enwiki` is the answer's English Wikipedia title.
- `ballion/`: shared helpers. `wiki.py` handles the cached Wikipedia API (cache in `data/raw/cache/`, gitignored) and a global rate limiter. The rest: `tables.py` (wikitable parser), `wikidata.py` (SPARQL), `popularity.py` (page views), `scoring.py` (tiers).
- `prompts/build.py`: collect, fetch page views and score, writing `data/answers/<pid>.csv`. `--answers-only` writes `data/answers_raw/` without page views.
- `prompts/export_web.py`: bundles prompts, tiers and answer aliases into `web/data.js`
- `web/`: the game, plain HTML/JS/Canvas with no build step. `js/scene.js` is the pixel-art stadium and animation, `js/game.js` the game flow, `js/matcher.js` the autocorrect, `js/audio.js` the WebAudio sound effects.

## Commands
```
python prompts/build.py [p004 p005 ...]   # re-scrape + rescore (all prompts if none given)
python prompts/export_web.py              # rebuild web/data.js after any data change
node web/test/matcher.test.js             # autocorrect unit cases (must all pass)
node web/test/typo_sweep.js               # one-typo recall over every answer (~99.97%)
node web/test/fp_sweep.js                 # false autocorrections on out-of-list names (~0.5%)
cd web && python -m http.server 8765      # play locally at http://localhost:8765
```
Useful URL params: `?selftest=1` plays a full game automatically and writes the result to `<body data-selftest>`. `?shot=kick&m=60&tier=3&t=1.2` freezes an animation frame. Also `?shot=final` and `?help=1`.

Pushing to `main` with changes under `web/` redeploys GitHub Pages via `.github/workflows/pages.yml`.

## Game rules (decided with the user)
- 7 rounds, one prompt each, with a 30 s timer. Wrong guesses can be retried until time runs out. A timeout is a whiff animation and 0 points.
- Tiers, points and kick distance (points = meters on a 100 m pitch; legendary goes into the net):
  common 10 (grey), uncommon 25 (green), rare 40 (blue), super rare 60 (dark blue), ultra rare 85 (purple), legendary 100 (gold). The final score is the sum, out of a max of 700.
- Daily Challenge: the same 7 prompts for everyone, seeded by the local date; Daily #1 = 2026-10-03. Free Play draws 7 random prompts. A game has at most 2 prompts from the same theme group.
- Autocorrect should be lenient on spelling but must not accept a *different* real entity. Typed names count when they're an alias or surname, or a first name that's unique within the prompt; typos are tolerated by edit distance scaled to length. A correctly spelled name of another entity is a miss (e.g. "Yaya Toure" must not match Kolo Touré).

## Rarity method
- Popularity proxy: Wikipedia user page views over the **last 60 days**, summed across 14 language editions, via the batched action API (`prop=pageviews`, 50 titles per request). You **must follow `continue`**, or most titles silently get 0 views. The 12-month REST endpoint is too slow under Wikimedia rate limits; on p002/p003 the 60-day ranking matched it at Spearman 0.98–0.99.
- Tiers are **rank-based within each prompt**: the rarest 1 (fewer than 50 answers) or 2 (50 or more) are legendary, and the rest split evenly from common to ultra rare. The user rejected the earlier z-score cutoffs because hard answers landed in common.
- Known bias: current fame inflates views (e.g. Haaland is common for old awards, newly promoted Como outranks Juventus). Accepted for now; the plan is to blend in real player answers later.

## Data decisions
- "Played for both X and Y" (p095–p103): needs at least 1 league appearance for each senior team per the Wikipedia infobox. Loans count, wartime guest spells don't. This excludes e.g. Clive Allen and Peter Beardsley (Man Utd/City).
- Country prompts link to national-team articles. West Germany is merged into Germany; the Soviet Union, Yugoslavia, Czechoslovakia, Serbia and Montenegro, and CIS are separate answers.
- Some prompts were widened because the strict version was too small: p012 (Golden/Silver/Bronze Ball), p076 and p078 (cup finalists). p043 is "winning final matchday squad for 2 clubs".

## Open questions for the user
- p002 says "over 100" goals (strict), which excludes Makaay and Oyarzabal on exactly 100; the newer prompts use "100 or more".
- p003 includes French amateur-era (pre-1932) champions, tagged `amateur-only` in the CSV. Keep them or drop them?
- The ballion.io domain isn't bought yet. To use it: add `web/CNAME` and point DNS at GitHub Pages.

## Rules
- Never commit the user's email address. The scraper User-Agent uses the repo URL as contact. The email was scrubbed from git history before the repo went public.
- The user works from two clones (a lab server and a laptop). Pull before editing and push when done.
- Wikimedia rate-limits aggressively. Keep requests going through `ballion.wiki._get` (cache + shared throttle at `MAX_RPS = 5`) rather than adding raw `requests` calls.
