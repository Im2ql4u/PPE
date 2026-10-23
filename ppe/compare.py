"""Comparing analyses: segment-level disagreement classes and note-level chord-tone status.

Definitions (also in docs/validation.md):

- A *segment* is a maximal time span over which neither analysis changes label.
- For each segment, the two active labels are compared on key (tonic pitch class + mode),
  chord pitch-class set, and bass pitch class:
    same          key, chord and bass all equal                      ("strict agreement", as in E2)
    key_frame     chord equal, key differs (bass may also differ)    (tonicisation vs modulation)
    inversion     chord and key equal, bass differs
  Key takes precedence over bass: a figure's implied bass is often a notational convention (e.g.
  Moonlight m. 16: N6 vs VI over an actual B pedal that neither figure describes).
    extension     one chord's pitch classes are a strict subset of the other's (V7 vs V9♭9)
    other_quality same root, otherwise different chord
    other_chord   different root and none of the above
- *Boundaries* where one analysis changes label and the other does not are counted separately
  (granularity), because they are not visible in the segment classes.
- Agreement fractions are weighted by duration in quarter notes.
- *Chord-tone status* of a note under an analysis: its pitch class is in the active label's chord
  pitch classes (or in the label's extra tones: suspensions/added tones). Judged at the note's onset.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from music21 import pitch as m21pitch

from ppe.model import Analysis, Label, Note, Piece

CLASSES = ("same", "key_frame", "inversion", "extension", "other_quality", "other_chord")
CLASS_TEXT = {
    "same": "Both analysts read this the same way.",
    "key_frame": "Same chord, heard in a different key.",
    "inversion": "Same chord and key, but a different note is taken as the bass.",
    "extension": "One reading includes an extra chord tone.",
    "other_quality": "Same root, different chord quality.",
    "other_chord": "Different chords.",
}


def _pc(name: str) -> int:
    return m21pitch.Pitch(name).pitchClass


def key_pc(label: Label) -> tuple[int, str]:
    return _pc(label.key.tonic), label.key.mode


def classify(a: Label, b: Label) -> str:
    same_chord = a.pcs == b.pcs
    same_bass = _pc(a.bass) == _pc(b.bass)
    same_key = key_pc(a) == key_pc(b)
    if same_chord:
        if not same_key:
            return "key_frame"
        return "same" if same_bass else "inversion"
    if a.pcs < b.pcs or b.pcs < a.pcs:
        return "extension"
    if _pc(a.root) == _pc(b.root):
        return "other_quality"
    return "other_chord"


@dataclass(frozen=True)
class Segment:
    onset: Fraction
    end: Fraction
    a: str  # label id
    b: str
    cls: str


def segments(piece: Piece, a: Analysis, b: Analysis) -> list[Segment]:
    cuts = sorted({lab.onset for lab in a.labels} | {lab.onset for lab in b.labels} | {piece.end})
    out = []
    for s, e in zip(cuts, cuts[1:]):
        la, lb = a.label_at(s), b.label_at(s)
        if la is None or lb is None:
            continue
        cls = classify(la, lb)
        if out and out[-1].a == la.id and out[-1].b == lb.id:
            prev = out[-1]
            out[-1] = Segment(prev.onset, e, la.id, lb.id, cls)
        else:
            out.append(Segment(s, e, la.id, lb.id, cls))
    return out


def summary(piece: Piece, a: Analysis, b: Analysis) -> dict:
    segs = segments(piece, a, b)
    total = sum((s.end - s.onset for s in segs), Fraction(0))
    by_cls = {c: sum((s.end - s.onset for s in segs if s.cls == c), Fraction(0)) for c in CLASSES}
    a_cuts = {lab.onset for lab in a.labels}
    b_cuts = {lab.onset for lab in b.labels}
    return {
        "a": a.id, "b": b.id,
        "duration_quarters": float(total),
        "fractions": {c: round(float(v / total), 4) if total else 0.0 for c, v in by_cls.items()},
        "strict_agreement": round(float(by_cls["same"] / total), 4) if total else 0.0,
        "boundaries_only_in_a": len(a_cuts - b_cuts),
        "boundaries_only_in_b": len(b_cuts - a_cuts),
        "boundaries_shared": len(a_cuts & b_cuts),
    }


def chord_tone_status(note: Note, label: Label | None) -> str | None:
    if label is None:
        return None
    if note.pc in label.pcs:
        return "chord"
    if note.pc in label.extra_pcs:
        return "accounted"  # suspension / added tone the label names
    return "non-chord"


def chord_role(note: Note, label: Label) -> str | None:
    """Role of a chord tone relative to the label's root: root, third, fifth, seventh, ninth."""
    if note.pc not in label.pcs:
        return None
    rp = _pc(label.root)
    for name in label.pitches:
        if _pc(name) == note.pc:
            semis = (note.pc - rp) % 12
            if name == label.root or semis == 0:
                return "root"
            from music21 import interval

            generic = interval.Interval(m21pitch.Pitch(label.root), m21pitch.Pitch(name)).generic.mod7
            return {3: "third", 5: "fifth", 7: "seventh", 2: "ninth", 4: "eleventh", 6: "thirteenth"}.get(generic, "other")
    return None


def note_statuses(piece: Piece) -> dict[str, dict[str, str | None]]:
    """note id -> {analysis id -> status} for every note attack."""
    out = {}
    for n in piece.notes:
        out[n.id] = {an.id: chord_tone_status(n, an.label_at(n.onset)) for an in piece.analyses}
    return out


def disputed_notes(piece: Piece, a: Analysis, b: Analysis) -> list[str]:
    """Notes whose chord-tone status differs between two analyses (both labelled)."""
    out = []
    for n in piece.notes:
        sa, sb = chord_tone_status(n, a.label_at(n.onset)), chord_tone_status(n, b.label_at(n.onset))
        if sa is not None and sb is not None and (sa == "non-chord") != (sb == "non-chord"):
            out.append(n.id)
    return out
