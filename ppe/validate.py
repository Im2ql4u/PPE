"""Cross-validation of the core against an independent parser, and other build-time checks."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from ppe.model import Note
from ppe.score_import import import_measures, import_notes, load_score


def crosscheck_reference_notes(core: list[Note], notes_tsv: Path) -> dict:
    """Compare the core with a DCML note table (the score the analysts annotated), by
    (measure number, offset within the measure in quarters, MIDI pitch), including tied continuations."""
    import ms3
    from fractions import Fraction

    t = ms3.load_tsv(notes_tsv)
    if "gracenote" in t.columns:
        t = t[t.gracenote.isna()]
    ref = Counter((int(r.mn), Fraction(str(r.mn_onset)) * 4, int(r.midi)) for _, r in t.iterrows())
    mine = Counter((n.measure, n.offset, n.midi) for n in core)
    both = ref & mine

    def fmt(c: Counter) -> list[str]:
        return [f"m{m} +{off} midi {p}" + (f" ×{k}" if k > 1 else "") for (m, off, p), k in sorted(c.items())]

    return {
        "reference": str(notes_tsv.name),
        "core_notes": sum(mine.values()), "reference_notes": sum(ref.values()),
        "agreeing": sum(both.values()),
        "agreement_rate": round(sum(both.values()) / max(1, sum(ref.values())), 4),
        "only_in_core": fmt(mine - ref), "only_in_reference": fmt(ref - mine),
    }


def crosscheck_music21(core: list[Note], source: Path) -> dict:
    """Compare (measure, offset, MIDI) multisets between the core and music21's own parse.

    Staff is compared separately: cross-staff notation legitimately differs between parsers.
    """
    s = load_score(source)
    m21_notes, _ = import_notes(s, import_measures(s))
    core_c = Counter((n.measure, n.offset, n.midi) for n in core)
    m21_c = Counter((n.measure, n.offset, n.midi) for n in m21_notes)
    both = core_c & m21_c
    only_core = core_c - m21_c
    only_m21 = m21_c - core_c

    core_staff = Counter((n.measure, n.offset, n.midi, n.staff) for n in core)
    m21_staff = Counter((n.measure, n.offset, n.midi, n.staff) for n in m21_notes)
    staff_diff = sorted({k[:3] for k in (core_staff - m21_staff)} & set(both))

    def fmt(c: Counter) -> list[str]:
        return [f"m{m} +{off} midi {p}" + (f" ×{k}" if k > 1 else "") for (m, off, p), k in sorted(c.items())]

    return {
        "independent_parser": "music21",
        "core_notes": sum(core_c.values()),
        "music21_notes": sum(m21_c.values()),
        "agreeing": sum(both.values()),
        "agreement_rate": round(sum(both.values()) / max(1, sum(core_c.values())), 4),
        "only_in_core": fmt(only_core),
        "only_in_music21": fmt(only_m21),
        "staff_assignment_differs": [f"m{m} +{off} midi {p}" for m, off, p in staff_diff],
    }
