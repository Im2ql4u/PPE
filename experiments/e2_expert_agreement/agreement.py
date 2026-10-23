"""E2: How often do expert Roman-numeral analyses of the same piece agree?

Compares every pair (analysis.txt, analysis_X.txt) in When in Rome, time-weighted over
the span where both analyses have an active label. See README.md for the metrics.

Usage:  uv run python experiments/e2_expert_agreement/agreement.py
"""

import bisect
import csv
import sys
import warnings
from dataclasses import dataclass
from pathlib import Path

from music21 import converter, roman

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from ppe.analyses import _bracket_pitches  # noqa: E402
CORPUS = ROOT / "data" / "external" / "when_in_rome" / "Corpus"
OUT = Path(__file__).parent / "out"


@dataclass(frozen=True)
class Label:
    key: tuple[int, str]  # (tonic pitch class, mode)
    pcs: frozenset[int]
    root: int
    bass: int
    triad: frozenset[int]  # root, third, fifth only
    figure: str


def label_of(rn: roman.RomanNumeral) -> Label:
    core = {rn.root().pitchClass}
    for p in (rn.third, rn.fifth):
        if p is not None:
            core.add(p.pitchClass)
    # music21 misreads bracketed alterations ([b9] -> doubly flattened ninth, [b9b5] garbled);
    # use the corrected reading from the app's importer (see ppe/analyses.py, docs/validation.md).
    pitches, _ = _bracket_pitches(rn, rn.figure)
    return Label(
        key=(rn.key.tonic.pitchClass, rn.key.mode),
        pcs=frozenset(p.pitchClass for p in pitches),
        root=rn.root().pitchClass,
        bass=rn.bass().pitchClass,
        triad=frozenset(core),
        figure=rn.figure,
    )


def timeline(path: Path):
    """(labels as absolute-time intervals, {measure number: (absolute start, length)})."""
    s = converter.parse(str(path), format="romantext")
    rns = list(s.flatten().getElementsByClass(roman.RomanNumeral))
    out = []
    for rn in rns:
        start = float(rn.offset)
        out.append((start, start + float(rn.quarterLength), label_of(rn)))
    measures = {}
    for m in s.recurse().getElementsByClass("Measure"):
        measures.setdefault(m.number, (float(m.getOffsetInHierarchy(s)), float(m.barDuration.quarterLength)))
    return out, measures


def label_at(tl, t):
    i = bisect.bisect_right(tl, t, key=lambda x: x[0]) - 1
    if i >= 0 and tl[i][0] <= t < tl[i][1]:
        return tl[i][2]
    return None


METRICS = {
    "key": lambda a, b: a.key == b.key,
    "chord_pcs": lambda a, b: a.pcs == b.pcs,
    "root": lambda a, b: a.root == b.root,
    "triad_core": lambda a, b: a.triad == b.triad,
    "bass": lambda a, b: a.bass == b.bass,
    "chord_and_bass": lambda a, b: a.pcs == b.pcs and a.bass == b.bass,
    "strict": lambda a, b: a.key == b.key and a.pcs == b.pcs and a.bass == b.bass,
}


GRID = 0.25  # sample every sixteenth note


def compare(tl_a, tl_b, meas_a, meas_b):
    """Align by (measure number, offset within measure), not absolute time: the two files
    may encode an anacrusis or repeats differently while sharing printed measure numbers."""
    agree = dict.fromkeys(METRICS, 0.0)
    overlap = 0.0
    diffs = []
    for mn in sorted(set(meas_a) & set(meas_b)):
        (sa, la), (sb, lb) = meas_a[mn], meas_b[mn]
        steps = int(min(la, lb) / GRID)
        for k in range(steps):
            u = k * GRID
            a, b = label_at(tl_a, sa + u + 1e-6), label_at(tl_b, sb + u + 1e-6)
            if a is None or b is None:
                continue
            overlap += GRID
            for name, f in METRICS.items():
                if f(a, b):
                    agree[name] += GRID
            if not METRICS["strict"](a, b):
                diffs.append((mn, u, a.figure, b.figure, a.key, b.key))
    return overlap, agree, diffs


def analyst(path: Path) -> str:
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("Analyst:"):
            return line.split(":", 1)[1].strip()
    return ""


def group_of(rel: Path, other: str, analyst_b: str) -> str:
    cat = "/".join(rel.parts[:2])
    if other == "analysis_B.txt":
        return "TAVERN encoder a vs b (Beethoven+Mozart variations)"
    if other == "analysis_BCMH.txt":
        return "Bach chorales: individual analyst vs BCMH"
    if "Mozart" in cat and "Piano_Sonatas" in cat:
        return "Mozart sonatas: DCML vs named theorist"
    if "computer" in analyst_b.lower():
        return f"{cat}: vs DT ('Tymoczko and his computer')"
    return f"{cat}: analysis.txt vs {other}"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    rows, all_diffs, failures = [], [], []
    only = sys.argv[1] if len(sys.argv) > 1 else ""  # optional substring filter for quick checks
    dirs = sorted({p.parent for p in CORPUS.rglob("analysis*.txt") if only in str(p)})
    for d in dirs:
        files = sorted(d.glob("analysis*.txt"))
        main_f = d / "analysis.txt"
        if len(files) < 2 or not main_f.exists():
            continue
        rel = d.relative_to(CORPUS)
        try:
            tl_a, meas_a = timeline(main_f)
        except Exception as ex:  # noqa: BLE001 - record and continue
            failures.append((str(rel), "analysis.txt", repr(ex)[:120]))
            continue
        for other in files:
            if other.name == "analysis.txt":
                continue
            try:
                tl_b, meas_b = timeline(other)
            except Exception as ex:  # noqa: BLE001
                failures.append((str(rel), other.name, repr(ex)[:120]))
                continue
            if not tl_a or not tl_b:
                continue
            len_a, len_b = tl_a[-1][1], tl_b[-1][1]
            # Files sometimes number measures differently (anacrusis as m0 vs m1). Try a
            # measure-number shift of -1/0/+1 and keep the best by chord agreement; the shift
            # is recorded. Picking the max of 3 biases agreement up slightly (documented).
            best = None
            for shift in (0, -1, 1):
                mb = {k + shift: v for k, v in meas_b.items()}
                res = compare(tl_a, tl_b, meas_a, mb)
                score = res[1]["chord_pcs"] / res[0] if res[0] else 0
                if best is None or score > best[0] + 1e-9:
                    best = (score, shift, res)
            _, shift, (overlap, agree, diffs) = best
            an_a, an_b = analyst(main_f), analyst(other)
            rows.append({
                "piece": str(rel).replace("\\", "/"),
                "other": other.name,
                "group": group_of(rel, other.name, an_b),
                "analyst_a": an_a[:60],
                "analyst_b": an_b[:60],
                "len_a": len_a,
                "len_b": len_b,
                "length_ratio": min(len_a, len_b) / max(len_a, len_b),
                "measure_shift": shift,
                "overlap": overlap,
                **{k: (v / overlap if overlap else 0.0) for k, v in agree.items()},
            })
            for mn, u, fa, fb, ka, kb in diffs:
                all_diffs.append((str(rel).replace("\\", "/"), other.name, mn, u, fa, fb, ka, kb))
        print(".", end="", flush=True)
    print()

    with open(OUT / "pairs.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with open(OUT / "diffs.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["piece", "other", "measure", "offset_in_measure", "figure_a", "figure_b", "key_a", "key_b"])
        w.writerows(all_diffs)
    with open(OUT / "failures.csv", "w", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerows(failures)
    print(f"pairs={len(rows)} failures={len(failures)}", file=sys.stderr)


if __name__ == "__main__":
    main()
