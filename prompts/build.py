"""Collect answers for each prompt, attach popularity, score, and write data/answers/<id>.csv.

  python prompts/build.py                  # all prompts
  python prompts/build.py p004 p005        # selected prompts
  python prompts/build.py --answers-only   # collect + validate only (no pageviews); writes data/answers_raw/
"""
import importlib
import json
import pkgutil
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from ballion.registry import PROMPTS  # noqa: E402
from ballion.scoring import TIERS, score  # noqa: E402

import prompts.collectors as _c  # noqa: E402

for m in pkgutil.iter_modules(_c.__path__):
    try:
        importlib.import_module(f"prompts.collectors.{m.name}")
    except Exception as e:  # one broken module shouldn't block building the others
        print(f"WARNING: could not import prompts.collectors.{m.name}: {e!r}", file=sys.stderr)


def collect(pid):
    ans = pd.DataFrame(PROMPTS[pid]["collect"]())
    assert {"answer", "enwiki", "detail"} <= set(ans.columns), f"{pid}: missing columns"
    assert ans["enwiki"].notna().all() and (ans["enwiki"].str.len() > 0).all(), f"{pid}: empty enwiki"
    return ans.drop_duplicates("enwiki").reset_index(drop=True)


def build(pids=None, answers_only=False):
    pids = sorted(pids or PROMPTS)
    out_dir = ROOT / "data" / ("answers_raw" if answers_only else "answers")
    out_dir.mkdir(parents=True, exist_ok=True)
    if not answers_only:
        from ballion.popularity import popularity
    for pid in pids:
        p = PROMPTS[pid]
        ans = collect(pid)
        if answers_only:
            ans.to_csv(out_dir / f"{pid}.csv", index=False)
            print(f"{pid}  {len(ans):4d} answers  {p['text']}")
            continue
        pop = popularity(ans["enwiki"].tolist())
        for col in ("qid", "views", "views_en", "n_langs"):
            ans[col] = ans["enwiki"].map(lambda t: pop[t][col])
        missing = ans[ans["qid"].isna()]
        if len(missing):
            print(f"  {pid}: {len(missing)} answers with no resolvable enwiki page: {missing['enwiki'].tolist()[:5]}")
        df = score(ans)
        df.to_csv(out_dir / f"{pid}.csv", index=False)
        counts = df["tier"].value_counts().reindex([t[0] for t in TIERS]).fillna(0).astype(int)
        print(f"{pid}  {len(df):4d} answers  " + " ".join(f"{c}" for c in counts) + f"  {p['text']}")
    index = [{k: PROMPTS[pid][k] for k in ("id", "text", "source")} for pid in sorted(PROMPTS)]
    (ROOT / "data" / "prompts.json").write_text(json.dumps(index, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    args = sys.argv[1:]
    build([a for a in args if not a.startswith("--")] or None, answers_only="--answers-only" in args)
