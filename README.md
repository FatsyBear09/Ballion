# Ballion
Ball knowledge test xD

A football take on Krillion: name a valid answer to a prompt, and the rarer the answer, the farther your 8-bit striker kicks the ball.

## Play
Open `web/index.html` in a browser. There's no build step or server; everything is in `web/`.

- 7 rounds, 30 seconds each. Wrong guesses can be retried until time runs out.
- Kick distance = points: common 10 m · uncommon 25 · rare 40 · super rare 60 · ultra rare 85 · legendary 100 (goal!)
- Daily Challenge (same 7 prompts for everyone, seeded by date, mixed themes) and Free Play (random 7 from the theme you pick: General, Premier League, La Liga, Champions League, National Teams, or all)
- Autocorrect for typos, nicknames and surnames ("Bergkmap", "Man Utd", "CR7"), only when close to a real answer

## Data pipeline
```
python prompts/build.py              # scrape answers + pageviews -> data/answers/*.csv
python prompts/build.py pl          # one theme (id prefix: gen, pl, ll, ucl, nat)
python prompts/export_web.py         # bundle prompts, tiers and aliases -> web/data/
```
- Prompts: `prompts/themes/*.md` (and the original `prompts/catalog.md`). Collectors: `prompts/collectors/*.py`
- Rarity: Wikipedia page views (last 60 days, 14 languages), rank-based tiers per prompt

## Tests
```
node web/test/matcher.test.js        # autocorrect unit cases
node web/test/typo_sweep.js          # one-typo recall over every answer
node web/test/fp_sweep.js            # false autocorrections on out-of-list names
```
Open `web/index.html?selftest=1` to play a full game automatically. The result goes in `<body data-selftest>`.
