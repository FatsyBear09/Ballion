"""Rarity tiers from per-prompt popularity ranks (fewer views = rarer).

The rarest 1-2 answers are legendary; the rest are split into equal-sized
groups from common to ultra rare, so every tier is roughly equally populated.
"""
import numpy as np

TIERS = [
    ("common", 10),
    ("uncommon", 25),
    ("rare", 40),
    ("super rare", 60),
    ("ultra rare", 85),
    ("legendary", 100),
]
LEGENDARY_2_FROM = 50  # prompts with at least this many answers get 2 legendaries, else 1


def score(df, views_col="views"):
    logv = np.log10(df[views_col].clip(lower=0) + 1)
    df = df.assign(rarity_z=-(logv - logv.mean()) / logv.std(ddof=0))
    df = df.sort_values(views_col, ascending=False, kind="stable").reset_index(drop=True)
    n = len(df)
    n_leg = 0 if n < 2 else (1 if n < LEGENDARY_2_FROM else 2)
    tier_idx = np.empty(n, dtype=int)
    for i, chunk in enumerate(np.array_split(np.arange(n - n_leg), len(TIERS) - 1)):
        tier_idx[chunk] = i
    tier_idx[n - n_leg:] = len(TIERS) - 1
    df["tier"] = [TIERS[i][0] for i in tier_idx]
    df["points"] = [TIERS[i][1] for i in tier_idx]
    return df
