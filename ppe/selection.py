"""What is in a selection? Pitch content, intervals, chord identity, each analyst's reading."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations

from music21 import chord as m21chord
from music21 import key as m21key
from music21 import pitch as m21pitch

from ppe.compare import chord_role, chord_tone_status, classify
from ppe.explain import describe_interval, explain_comparison
from ppe.model import Label, Note, Piece
from ppe.spelling import pretty
from ppe.transform import voice_leading

ACC = {-2: "𝄫", -1: "♭", 0: "", 1: "♯", 2: "𝄪"}


def _m21(n: Note) -> m21pitch.Pitch:
    return m21pitch.Pitch(n.name)


def span_of(notes: list[Note]) -> tuple[Fraction, Fraction]:
    return min(n.onset for n in notes), max(n.end for n in notes)


def describe_span(piece: Piece, start: Fraction, end: Fraction) -> str:
    m1, m2 = piece.measure_at(start), piece.measure_at(end - Fraction(1, 960))
    b1 = 1 + (start - m1.onset) / m1.beat
    b2 = 1 + (end - m2.onset) / m2.beat

    def beat(b: Fraction) -> str:
        return str(int(b)) if b.denominator == 1 else f"{float(b):.3g}"
    if m1.number == m2.number:
        whole = start == m1.onset and end == m1.end
        return f"m. {m1.number}" if whole else f"m. {m1.number}, beat {beat(b1)}" + ("" if end - start <= m1.beat else f"–{beat(b2)}")
    return f"mm. {m1.number}–{m2.number}"


def scale_degree(name: str, label: Label) -> str:
    k = m21key.Key(label.key.tonic, label.key.mode)
    deg, acc = k.getScaleDegreeAndAccidentalFromPitch(m21pitch.Pitch(name))
    a = int(acc.alter) if acc is not None else 0
    return f"{ACC.get(a, '')}{deg}"


def chord_identity(names: list[str]) -> dict | None:
    """Name the sonority of distinct pitches (lowest first). Needs at least three pitch classes:
    two notes are an interval, not a chord."""
    distinct = {}
    for nm in names:
        distinct.setdefault(m21pitch.Pitch(nm).name, nm)
    if len(distinct) < 3:
        return None
    c = m21chord.Chord(list(distinct.values()))
    tertian = c.isTriad() or c.isSeventh() or c.isNinth()
    if not tertian:
        # A passage with passing and neighbour notes is not one chord; naming the whole pitch set
        # ("diminished pentacluster") would mislead. The analysts' readings speak instead.
        return None
    try:
        root = c.root().name
        inv = c.inversion() if c.isTriad() or c.isSeventh() else None
    except Exception:  # noqa: BLE001
        root, inv = None, None
    return {"name": c.commonName, "root": pretty(root) if root else None, "bass": pretty(c.bass().name),
            "inversion": inv, "is_tertian": True}


def inspect(piece: Piece, ids: list[str] | None = None, start: Fraction | None = None, end: Fraction | None = None) -> dict:
    by_id = piece.notes_by_id()
    if ids:
        notes = [by_id[i] for i in ids if i in by_id]
    else:
        notes = [n for n in piece.notes if start <= n.onset < end]
    if not notes:
        return {"empty": True}
    s0, s1 = (start, end) if start is not None else span_of(notes)
    if ids and len({n.onset for n in notes}) == 1:
        # a single vertical: the span is the attack itself; use its shortest duration for labels
        s1 = s0 + min(n.duration for n in notes)
    attacks = [n for n in notes if n.is_attack] or notes
    names = [n.name for n in sorted(attacks, key=lambda n: n.midi)]
    bass = min(attacks, key=lambda n: n.midi)

    # intervals: two distinct pitches -> one interval; otherwise each distinct pitch above the bass
    distinct = []
    for n in sorted(attacks, key=lambda n: n.midi):
        if n.midi not in [d.midi for d in distinct]:
            distinct.append(n)
    if len(distinct) == 2:
        intervals = [describe_interval(distinct[0].name, distinct[1].name) | {"low": pretty(distinct[0].name), "high": pretty(distinct[1].name)}]
    elif len(distinct) <= 5:
        intervals = [describe_interval(bass.name, d.name) | {"low": pretty(bass.name), "high": pretty(d.name)}
                     for d in distinct[1:]]
    else:
        intervals = []  # too many notes for a meaningful interval list

    lenses = []
    for an in piece.analyses:
        labs = [l for l in an.labels if l.onset < s1 and l.end > s0]
        primary = an.label_at(s0) or (labs[0] if labs else None)
        statuses = []
        for n in attacks:
            lab = an.label_at(n.onset)
            st = chord_tone_status(n, lab)
            statuses.append({"id": n.id, "status": st, "role": chord_role(n, lab) if lab and st == "chord" else None,
                             "degree": scale_degree(n.name, lab) if lab else None})
        nxt = None
        if primary is not None:
            i = an.labels.index(primary)
            nxt = an.labels[i + 1] if i + 1 < len(an.labels) else None
        lenses.append({
            "analysis": an.id,
            "labels": [l.id for l in labs],
            "primary": primary.id if primary else None,
            "notes": [{"m": x.measure, "text": x.text} for x in an.notes
                      if piece.measure_at(s0).number <= x.measure <= piece.measure_at(s1 - Fraction(1, 960)).number],
            "statuses": statuses,
            "voice_leading": voice_leading(primary, nxt) if primary and nxt else None,
        })

    comparisons = []
    for a, b in combinations(piece.analyses, 2):
        la, lb = a.label_at(s0), b.label_at(s0)
        if la is None or lb is None:
            continue
        cls = classify(la, lb)
        comparisons.append({"a": a.id, "b": b.id, "cls": cls,
                            "text": explain_comparison(cls, la, lb, a.id, b.id),
                            "disputed_notes": [n.id for n in attacks
                                               if (chord_tone_status(n, a.label_at(n.onset)) == "non-chord")
                                               != (chord_tone_status(n, b.label_at(n.onset)) == "non-chord")]})

    return {
        "span": {"on": float(s0), "end": float(s1), "text": describe_span(piece, s0, s1)},
        "notes": [{"id": n.id, "name": pretty(n.name), "midi": n.midi, "track": n.track} for n in attacks],
        "pitch_classes": sorted({pretty(m21pitch.Pitch(n.name).name) for n in attacks}),
        "bass": pretty(bass.name),
        "chord": chord_identity(names),
        "intervals": intervals,
        "lenses": lenses,
        "comparisons": comparisons,
    }
