"""Summarise out/pairs.csv into out/summary.md (group-level agreement)."""

from pathlib import Path

import pandas as pd

OUT = Path(__file__).parent / "out"
METRICS = ["key", "chord_pcs", "root", "triad_core", "bass", "chord_and_bass", "strict"]

pairs = pd.read_csv(OUT / "pairs.csv")
failures = pd.read_csv(OUT / "failures.csv", header=None, names=["piece", "file", "error"])
ok = pairs[pairs.length_ratio >= 0.95]


def weighted(g: pd.DataFrame) -> pd.Series:
    w = g.overlap
    row = {m: (g[m] * w).sum() / w.sum() for m in METRICS}
    row["pairs"] = len(g)
    row["median_strict"] = g.strict.median()
    row["p10_strict"] = g.strict.quantile(0.1)
    return pd.Series(row)


table = ok.groupby("group").apply(weighted).sort_values("strict", ascending=False)
overall = weighted(ok)

lines = [
    "# E2 summary (generated)",
    "",
    f"Pairs parsed: {len(pairs)}; kept (length ratio >= 0.95): {len(ok)}; parse failures: {len(failures)}; "
    f"pairs aligned with a measure-number shift: {(ok.measure_shift != 0).sum()}.",
    "",
    "Time-weighted agreement (fraction of the overlapping duration where the two analyses agree):",
    "",
    "| Group | pairs | key | chord pcs | root | triad core | bass | chord+bass | strict | median strict (per piece) | 10th pct |",
    "|---|---|---|---|---|---|---|---|---|---|---|",
]
for g, r in table.iterrows():
    lines.append(
        f"| {g} | {int(r.pairs)} | " + " | ".join(f"{r[m]:.2f}" for m in METRICS)
        + f" | {r.median_strict:.2f} | {r.p10_strict:.2f} |"
    )
lines.append(
    f"| **All kept pairs** | {int(overall.pairs)} | " + " | ".join(f"{overall[m]:.2f}" for m in METRICS)
    + f" | {overall.median_strict:.2f} | {overall.p10_strict:.2f} |"
)
lines += ["", "Moonlight mvt. 1 (BPS vs DT):", ""]
moon = pairs[pairs.piece.str.contains("Moonlight") & pairs.piece.str.endswith("/1")]
lines.append(moon[["other", "length_ratio"] + METRICS].to_markdown(index=False))
lines += ["", "Excluded for length mismatch:", ""]
lines.append(pairs[pairs.length_ratio < 0.95][["piece", "other", "length_ratio"]].to_markdown(index=False))
lines += ["", "Parse failures by file:", "", failures.groupby("file").size().to_markdown()]
(OUT / "summary.md").write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
