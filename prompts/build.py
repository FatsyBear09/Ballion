"""Collect answers for each prompt, attach popularity, score, and write data/answers/<id>.csv.

  python prompts/build.py                  # all prompts
  python prompts/build.py p004 p005        # selected prompts
  python prompts/build.py pl ucl           # every prompt with these id prefixes (a theme)
  python prompts/build.py --answers-only   # collect + validate only (no pageviews); writes data/answers_raw/
  python prompts/build.py --from-raw pl    # score the answers already in data/answers_raw/ (no re-scraping)

A prompt whose collector fails, or whose answer count is outside MIN_ANSWERS..MAX_ANSWERS, is
reported and skipped, so one broken scraper never sinks a long build. Page views are fetched
once for the union of all answers, since many answers recur across prompts.
"""
import importlib
import json
import pkgutil
import re
import sys
import traceback
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from ballion.registry import PROMPTS  # noqa: E402
from ballion.scoring import TIERS, score  # noqa: E402
from ballion.themes import theme_of  # noqa: E402

import prompts.collectors as _c  # noqa: E402

MIN_ANSWERS, MAX_ANSWERS = 12, 130
# Windows consoles default to cp1252, which can't print prompt text like "≥" or "–".
for stream in (sys.stdout, sys.stderr):
    stream.reconfigure(encoding="utf-8", errors="replace")

for m in pkgutil.iter_modules(_c.__path__):
    try:
        importlib.import_module(f"prompts.collectors.{m.name}")
    except Exception as e:  # one broken module shouldn't block building the others
        print(f"WARNING: could not import prompts.collectors.{m.name}: {e!r}", file=sys.stderr)


def collect(pid):
    ans = pd.DataFrame(PROMPTS[pid]["collect"]())
    assert {"answer", "enwiki", "detail"} <= set(ans.columns), f"{pid}: missing columns"
    assert ans["enwiki"].notna().all() and (ans["enwiki"].str.len() > 0).all(), f"{pid}: empty enwiki"
    # A player without an article sometimes links to a "List of ..." page; that's not the answer's own page.
    ans = ans[~ans["enwiki"].str.startswith("List of ")]
    return ans.drop_duplicates("enwiki").reset_index(drop=True)


def select(args):
    if not args:
        return sorted(PROMPTS)
    out = []
    for a in args:
        if re.fullmatch(r"[a-z]+", a):
            out += [pid for pid in PROMPTS if re.fullmatch(a + r"\d+", pid)]
        elif a in PROMPTS:
            out.append(a)
        else:
            print(f"WARNING: unknown prompt {a}", file=sys.stderr)
    return sorted(set(out))


def from_raw(pid):
    """Reuse the answers saved by an earlier --answers-only run instead of re-scraping."""
    ans = pd.read_csv(ROOT / "data" / "answers_raw" / f"{pid}.csv")
    ans = ans[~ans["enwiki"].str.startswith("List of ")]
    return ans.drop_duplicates("enwiki").reset_index(drop=True)


def build(pids=None, answers_only=False, raw=False):
    pids = pids or sorted(PROMPTS)
    out_dir = ROOT / "data" / ("answers_raw" if answers_only else "answers")
    out_dir.mkdir(parents=True, exist_ok=True)

    collected, failed = {}, {}
    for pid in pids:
        try:
            ans = from_raw(pid) if raw else collect(pid)
        except Exception as e:
            failed[pid] = f"{type(e).__name__}: {e}"
            traceback.print_exc(limit=2, file=sys.stderr)
            continue
        if not MIN_ANSWERS <= len(ans) <= MAX_ANSWERS:
            failed[pid] = f"{len(ans)} answers (allowed {MIN_ANSWERS}-{MAX_ANSWERS})"
            continue
        collected[pid] = ans
        if answers_only:
            ans.to_csv(out_dir / f"{pid}.csv", index=False)
            print(f"{pid}  {len(ans):4d} answers  {PROMPTS[pid]['text']}", flush=True)

    if not answers_only and collected:
        from ballion.popularity import popularity
        titles = sorted({t for ans in collected.values() for t in ans["enwiki"]})
        print(f"fetching page views for {len(titles)} distinct answers across {len(collected)} prompts", flush=True)
        pop = popularity(titles)
        for pid, ans in collected.items():
            for col in ("qid", "views", "views_en", "n_langs"):
                ans[col] = ans["enwiki"].map(lambda t: pop[t][col])
            missing = ans[ans["qid"].isna()]
            if len(missing):
                print(f"  {pid}: {len(missing)} answers with no resolvable enwiki page: {missing['enwiki'].tolist()[:5]}")
            df = score(ans)
            df.to_csv(out_dir / f"{pid}.csv", index=False)
            counts = df["tier"].value_counts().reindex([t[0] for t in TIERS]).fillna(0).astype(int)
            print(f"{pid}  {len(df):4d} answers  " + " ".join(f"{c}" for c in counts) + f"  {PROMPTS[pid]['text']}")

    if failed:
        print(f"\n{len(failed)} prompt(s) skipped:")
        for pid, why in failed.items():
            print(f"  {pid}: {why}")
    index = [{"id": pid, "text": PROMPTS[pid]["text"], "source": PROMPTS[pid]["source"],
              "theme": theme_of(pid), "family": PROMPTS[pid]["family"]} for pid in sorted(PROMPTS)]
    (ROOT / "data" / "prompts.json").write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf8")
    return collected, failed


if __name__ == "__main__":
    args = sys.argv[1:]
    build(select([a for a in args if not a.startswith("--")]), answers_only="--answers-only" in args,
          raw="--from-raw" in args)
