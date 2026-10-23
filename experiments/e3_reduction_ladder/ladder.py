"""E3: a playable reduction ladder built only from expert (DCML) harmony labels.

L0 surface         every note
L1 label tones     notes whose spelled pitch (tpc) the analyst's label accounts for
                   (chord tones incl. suspensions/retardations and added tones)
L2 structural      only the structural chord (root + chord-type intervals), no changes/added tones
L3 outer voices    per harmony span: lowest and highest L2 note, sustained across the span

Usage:  uv run python experiments/e3_reduction_ladder/ladder.py [dcml_repo notes_stem]
Default: Debussy, Clair de lune.
"""

import json
import sys
from fractions import Fraction
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import ms3
import pretty_midi

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).parent / "out"

# chord types (DCML) -> intervals above the root on the line of fifths
CHORD_FIFTHS = {
    "M": (0, 4, 1), "m": (0, -3, 1), "o": (0, -3, 6), "+": (0, 4, 8),
    "Mm7": (0, 4, 1, -2), "mm7": (0, -3, 1, -2), "MM7": (0, 4, 1, 5), "mM7": (0, -3, 1, 5),
    "%7": (0, -3, 6, -2), "o7": (0, -3, 6, -9), "+7": (0, 4, 8, -2), "+M7": (0, 4, 8, 5),
    "It": (0, 4, 10), "Ger": (0, 4, 1, 10), "Fr": (0, 4, 6, 10),
}


def frac(x) -> Fraction:
    return Fraction(str(x))


def local_tonic(globalkey: str, localkey: str) -> int:
    g = ms3.name2fifths(globalkey)
    return g + ms3.roman_numeral2fifths(localkey, globalkey.islower())


def load(repo: str, stem: str):
    base = ROOT / "data/external" / repo
    notes = ms3.load_tsv(base / "notes" / f"{stem}.notes.tsv")
    harm = ms3.load_tsv(base / "harmonies" / f"{stem}.harmonies.tsv")
    harm = harm[harm.chord_tones.notna()].copy()
    spans = []
    for _, h in harm.iterrows():
        t = local_tonic(h.globalkey, h.localkey)
        label_tpcs = {t + c for c in h.chord_tones} | {t + c for c in (h.added_tones or ())}
        intervals = CHORD_FIFTHS.get(h.chord_type)
        structural = {t + h.root + i for i in intervals} if intervals else {t + c for c in h.chord_tones}
        start = frac(h.quarterbeats)
        spans.append({
            "start": start, "end": start + frac(h.duration_qb), "label": h.label,
            "mn": int(h.mn), "structural": structural, "chord_type": h.chord_type,
            # A label like ii(2) displaces the root by a suspension; DCML's chord_tones then omit
            # the root although it usually still sounds (e.g. in the bass). The analyst accounts
            # for both the displacing and the displaced tone, so L1 is the union.
            "label_tpcs": label_tpcs | structural,
        })
    return notes, spans


def span_at(spans, t: Fraction):
    for s in spans:
        if s["start"] <= t < s["end"]:
            return s
    return None


def main() -> None:
    repo, stem = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ("dcml_debussy_bergamasque", "l075-03_suite_clair")
    OUT.mkdir(exist_ok=True)
    notes, spans = load(repo, stem)
    notes = notes[notes.gracenote.isna()]

    rows = []
    for _, n in notes.iterrows():
        on = frac(n.quarterbeats)
        s = span_at(spans, on)
        rows.append({
            "on": on, "dur": frac(n.duration_qb), "midi": int(n.midi), "tpc": int(n.tpc), "staff": int(n.staff),
            "mn": int(n.mn), "tied_cont": (not ms3.utils.functions.pd.isna(n.tied)) and int(n.tied) in (-1, 0),  # continuation of a tie: not a new attack
            "span": s,
            "L1": bool(s and n.tpc in s["label_tpcs"]),
            "L2": bool(s and n.tpc in s["structural"]),
        })
    attacks = [r for r in rows if not r["tied_cont"] and r["span"]]

    # L3: outer voices per harmony span, from structural notes sounding in the span
    outer = []
    for s in spans:
        inside = [r for r in rows if r["L2"] and r["span"] is s]
        if inside:
            lo = min(inside, key=lambda r: r["midi"])
            hi = max(inside, key=lambda r: r["midi"])
            outer += [(s["start"], s["end"], lo["midi"]), (s["start"], s["end"], hi["midi"])]

    sec_per_q = 60 / 50  # slow, for listening

    def write_midi(name, events):
        pm = pretty_midi.PrettyMIDI()
        inst = pretty_midi.Instrument(program=0)
        for on, end, pitch in events:
            inst.notes.append(pretty_midi.Note(64, pitch, float(on) * sec_per_q, float(end) * sec_per_q))
        pm.instruments.append(inst)
        pm.write(str(OUT / f"{stem}_{name}.mid"))

    levels = {
        "L0_surface": [(r["on"], r["on"] + r["dur"], r["midi"]) for r in rows],
        "L1_label_tones": [(r["on"], r["on"] + r["dur"], r["midi"]) for r in rows if r["L1"]],
        "L2_structural": [(r["on"], r["on"] + r["dur"], r["midi"]) for r in rows if r["L2"]],
        "L3_outer_voices": outer,
    }
    for name, ev in levels.items():
        write_midi(name, ev)

    # piano-roll figure of the first 16 bars, one panel per level
    end_q = next((s["start"] for s in spans if s["mn"] > 16), spans[-1]["end"])
    fig, axes = plt.subplots(len(levels), 1, figsize=(16, 11), sharex=True)
    for ax, (name, ev) in zip(axes, levels.items()):
        for on, end, p in ev:
            if on < end_q:
                ax.broken_barh([(float(on), float(min(end, end_q) - on))], (p - 0.4, 0.8), color="#1a73e8")
        if name == "L0_surface":
            for r in rows:
                if r["on"] < end_q and not r["L1"]:
                    ax.broken_barh([(float(r["on"]), float(r["dur"]))], (r["midi"] - 0.4, 0.8), color="#e8710a")
        for s in spans:
            if s["start"] < end_q:
                ax.axvline(float(s["start"]), color="#ccc", lw=0.5)
        ax.set_ylabel(name, rotation=0, ha="right", fontsize=9)
    for s in spans:
        if s["start"] < end_q:
            axes[0].text(float(s["start"]), 92, s["label"], fontsize=6, rotation=60)
    axes[0].set_ylim(30, 100)
    axes[-1].set_xlabel("quarter notes (orange in L0 = notes not accounted for by the expert label)")
    fig.tight_layout()
    fig.savefig(OUT / f"{stem}_ladder.png", dpi=110)

    n_att = len(attacks)
    stats = {
        "piece": stem,
        "harmony_labels": len(spans),
        "note_attacks": n_att,
        "L1_label_tones_share": round(sum(r["L1"] for r in attacks) / n_att, 3),
        "L2_structural_share": round(sum(r["L2"] for r in attacks) / n_att, 3),
        "not_in_label_share": round(sum(not r["L1"] for r in attacks) / n_att, 3),
        "chord_types_without_interval_table": sorted({str(s["chord_type"]) for s in spans if s["chord_type"] not in CHORD_FIFTHS}),
        "measures_most_unexplained": sorted(
            {r["mn"] for r in attacks},
            key=lambda m: -sum(1 for r in attacks if r["mn"] == m and not r["L1"]) / max(1, sum(1 for r in attacks if r["mn"] == m)),
        )[:8],
    }
    (OUT / f"{stem}_stats.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
