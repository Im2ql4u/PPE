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


def figures_above_bass(bass: str, others: list[str]) -> list[dict]:
    """Distinct simple intervals above the bass, smallest first: the figured-bass reading of a
    sonority (a Neapolitan sixth over its bass is 'minor 3rd, minor 6th', i.e. 6/3)."""
    from music21 import interval as m21interval

    seen, out = set(), []
    b = m21pitch.Pitch(bass)
    for name in others:
        p = m21pitch.Pitch(name)
        if p.name == b.name:
            continue
        i = m21interval.Interval(b, p)
        simple = m21interval.Interval(i.simpleName)
        if simple.simpleName in seen:
            continue
        seen.add(simple.simpleName)
        out.append({"name": simple.niceName, "short": simple.simpleName, "semitones": simple.semitones,
                    "number": simple.generic.simpleUndirected, "low": pretty(b.name), "high": pretty(p.name)})
    return sorted(out, key=lambda x: (x["number"], x["semitones"]))


def is_stacked_thirds(c: m21chord.Chord) -> bool:
    """True if the chord's pitch classes are root, third, fifth (seventh, ninth) with every step a
    major or minor third above the previous one. music21's isTriad/isSeventh/isNinth count generic
    steps only and accept e.g. B♯–D (a diminished third) as a third."""
    try:
        steps = [c.getChordStep(k) for k in (1, 3, 5, 7, 9)]
    except Exception:  # noqa: BLE001
        return False
    present = [p for p in steps if p is not None]
    if steps[0] is None or steps[1] is None or steps[2] is None:
        return False
    if any(steps[i] is None and steps[i + 1] is not None for i in range(len(steps) - 1)):
        return False  # gaps (e.g. a ninth without a seventh) are not a plain stack
    if len({p.pitchClass for p in present}) != len({p.pitchClass for p in c.pitches}):
        return False
    return all((b.pitchClass - a.pitchClass) % 12 in (3, 4) for a, b in zip(present, present[1:]))


def chord_identity(names: list[str]) -> dict | None:
    """Name the sonority of distinct pitches (lowest first). Needs at least three pitch classes:
    two notes are an interval, not a chord."""
    distinct = {}
    for nm in names:
        distinct.setdefault(m21pitch.Pitch(nm).name, nm)
    if len(distinct) < 3:
        return None
    c = m21chord.Chord(list(distinct.values()))
    if not is_stacked_thirds(c):
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


def inspect(piece: Piece, ids: list[str] | None = None, start: Fraction | None = None, end: Fraction | None = None,
            transpose: int = 0) -> dict:
    """Describe a selection. With `transpose`, all spelled names, keys and explanations are given in the
    transposed key; Roman numerals, roles and scale degrees are unchanged (they are relations)."""
    from ppe.render import transposition_interval
    from ppe.serialize import label_json
    from ppe.transform import transpose_label, transpose_name

    interval, _ = transposition_interval(transpose, piece.measures[0].key_fifths)

    def tl(lab):
        return transpose_label(lab, interval, transpose) if lab is not None else None

    def tn(name):
        return transpose_name(name, interval) if transpose else name

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
    names = [tn(n.name) for n in sorted(attacks, key=lambda n: n.midi)]
    bass = min(attacks, key=lambda n: n.midi)

    # intervals: two distinct pitches -> one interval; otherwise each distinct pitch above the bass
    distinct = []
    for n in sorted(attacks, key=lambda n: n.midi):
        if n.midi not in [d.midi for d in distinct]:
            distinct.append(n)
    if len(distinct) == 2:
        lo, hi = tn(distinct[0].name), tn(distinct[1].name)
        intervals = [describe_interval(lo, hi) | {"low": pretty(lo), "high": pretty(hi)}]
    else:
        intervals = figures_above_bass(tn(bass.name), [tn(d.name) for d in distinct[1:]])

    lenses = []
    for an in piece.analyses:
        labs = [l for l in an.labels if l.onset < s1 and l.end > s0]
        primary = an.label_at(s0) or (labs[0] if labs else None)
        statuses = []
        for n in attacks:
            lab = an.label_at(n.onset)
            st = chord_tone_status(n, lab)
            # roles and degrees are relations: computed in the original key, valid in any transposition
            statuses.append({"id": n.id, "status": st, "role": chord_role(n, lab) if lab and st == "chord" else None,
                             "degree": scale_degree(n.name, lab) if lab else None})
        nxt = None
        if primary is not None:
            i = an.labels.index(primary)
            nxt = an.labels[i + 1] if i + 1 < len(an.labels) else None
        readings = []
        for lab in labs:
            j = an.labels.index(lab)
            after = an.labels[j + 1] if j + 1 < len(an.labels) else None
            readings.append(label_json(tl(lab), an, tl(after)))
        lenses.append({
            "analysis": an.id,
            "labels": [l.id for l in labs],
            "readings": readings,
            "primary": primary.id if primary else None,
            "notes": [{"m": x.measure, "text": x.text} for x in an.notes
                      if piece.measure_at(s0).number <= x.measure <= piece.measure_at(s1 - Fraction(1, 960)).number],
            "statuses": statuses,
            "voice_leading": voice_leading(tl(primary), tl(nxt)) if primary and nxt else None,
        })

    comparisons = []
    for a, b in combinations(piece.analyses, 2):
        la, lb = a.label_at(s0), b.label_at(s0)
        if la is None or lb is None:
            continue
        cls = classify(la, lb)
        comparisons.append({"a": a.id, "b": b.id, "cls": cls,
                            "text": explain_comparison(cls, tl(la), tl(lb), a.id, b.id),
                            "disputed_notes": [n.id for n in attacks
                                               if (chord_tone_status(n, a.label_at(n.onset)) == "non-chord")
                                               != (chord_tone_status(n, b.label_at(n.onset)) == "non-chord")]})

    return {
        "span": {"on": float(s0), "end": float(s1), "text": describe_span(piece, s0, s1)},
        "transpose": {"semitones": transpose, "interval": interval},
        "notes": [{"id": n.id, "name": pretty(tn(n.name)), "midi": n.midi, "track": n.track} for n in attacks],
        "pitch_classes": sorted({pretty(m21pitch.Pitch(tn(n.name)).name) for n in attacks}),
        "bass": pretty(tn(bass.name)),
        "chord": chord_identity(names),
        "intervals": intervals,
        "lenses": lenses,
        "comparisons": comparisons,
    }
