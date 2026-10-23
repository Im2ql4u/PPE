"""Playback events: the original texture, honest reductions, voice filters, and transformations.

Every mode states what it is (see MODES). Reductions that depend on an analysis say so; none of them
claims to be "the essence" of the passage.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction

from ppe.compare import chord_role, chord_tone_status
from ppe.model import Label, Note, Piece
from ppe.score_import import sounding_notes

MODES = {
    "original": {
        "name": "As written",
        "about": "Every note, as notated.",
        "needs_analysis": False,
    },
    "blocked": {
        "name": "Blocked chords",
        "about": "The same notes, sounded together on each beat and held. A texture reduction: it doesn't depend on any analysis.",
        "needs_analysis": False,
    },
    "outer": {
        "name": "Outer voices",
        "about": "Only the highest and the lowest note at each moment: the soprano–bass frame that carries much of the harmony's motion.",
        "needs_analysis": False,
    },
    "melody": {
        "name": "Top line",
        "about": "Only the highest note at each moment.",
        "needs_analysis": False,
    },
    "bass": {
        "name": "Bass line",
        "about": "Only the lowest note at each moment.",
        "needs_analysis": False,
    },
    "chord_tones": {
        "name": "Chord tones only",
        "about": "Notes that the chosen analyst's chord labels account for; passing and neighbour notes removed. It shows what a reading claims, not how the passage must be heard.",
        "needs_analysis": True,
    },
    "progression": {
        "name": "The analyst's chords",
        "about": "Each label played as a plain block chord with smooth voice leading. A realisation of the analysis, not a reduction of the score.",
        "needs_analysis": True,
    },
}


@dataclass
class PlayNote:
    onset: Fraction
    duration: Fraction
    midi: int
    ids: list[str] = field(default_factory=list)  # notehead ids to highlight
    velocity: float = 0.62
    changed: bool = False  # altered by a transformation

    def to_json(self) -> dict:
        return {"onset": float(self.onset), "duration": float(self.duration), "midi": self.midi,
                "ids": self.ids, "velocity": round(self.velocity, 3), "changed": self.changed}


def _in_span(n: Note, start: Fraction, end: Fraction) -> bool:
    return start <= n.onset < end


def original(piece: Piece, start: Fraction, end: Fraction, tracks: set[str] | None) -> list[PlayNote]:
    out = []
    for first, dur, ids in sounding_notes(piece.notes):
        if not _in_span(first, start, end):
            continue
        if tracks and first.track not in tracks:
            continue
        out.append(PlayNote(first.onset, min(dur, end - first.onset), first.midi, ids))
    _shape_velocity(out)
    return out


def _shape_velocity(notes: list[PlayNote]) -> None:
    """A light voicing: the highest note at each onset slightly louder, the rest softer."""
    by_onset: dict[Fraction, list[PlayNote]] = {}
    for p in notes:
        by_onset.setdefault(p.onset, []).append(p)
    for group in by_onset.values():
        top = max(group, key=lambda p: p.midi)
        for p in group:
            p.velocity = 0.72 if p is top and len(group) > 0 else 0.55


def blocked(piece: Piece, start: Fraction, end: Fraction, tracks: set[str] | None) -> list[PlayNote]:
    src = original(piece, start, end, tracks)
    out: list[PlayNote] = []
    for m in piece.measures:
        if m.end <= start or m.onset >= end:
            continue
        t = m.onset
        while t < m.end:
            w_end = min(t + m.beat, m.end)
            if w_end > start and t < end:
                group = [p for p in src if t <= p.onset < w_end]
                seen = {}
                for p in group:
                    if p.midi not in seen:
                        seen[p.midi] = PlayNote(max(t, start), max(w_end, p.onset + p.duration) - max(t, start), p.midi, list(p.ids))
                    else:
                        seen[p.midi].ids += p.ids
                out.extend(seen.values())
            t = w_end
    _shape_velocity(out)
    return sorted(out, key=lambda p: (p.onset, p.midi))


def _sounding_at(src: list[PlayNote], t: Fraction) -> list[PlayNote]:
    return [p for p in src if p.onset <= t < p.onset + p.duration]


def outer(piece: Piece, start: Fraction, end: Fraction, tracks: set[str] | None, which: str = "both") -> list[PlayNote]:
    src = original(piece, start, end, tracks)
    keep = []
    for p in src:
        sounding = _sounding_at(src, p.onset)
        hi = max(q.midi for q in sounding)
        lo = min(q.midi for q in sounding)
        if (which in ("both", "top") and p.midi == hi) or (which in ("both", "bass") and p.midi == lo):
            keep.append(p)
    for p in keep:
        p.velocity = 0.66
    return keep


def chord_tones(piece: Piece, start: Fraction, end: Fraction, tracks: set[str] | None, analysis_id: str) -> list[PlayNote]:
    an = piece.analysis(analysis_id)
    by_id = piece.notes_by_id()
    out = []
    for p in original(piece, start, end, tracks):
        n = by_id[p.ids[0]]
        if chord_tone_status(n, an.label_at(n.onset)) in ("chord", "accounted"):
            out.append(p)
    return out


def progression(piece: Piece, start: Fraction, end: Fraction, analysis_id: str) -> list[PlayNote]:
    """Each label as a block chord: bass in the bass register, upper voices with minimal motion."""
    from music21 import pitch as m21pitch

    an = piece.analysis(analysis_id)
    out = []
    prev_upper: list[int] | None = None
    for lab in an.labels:
        if lab.end <= start or lab.onset >= end:
            continue
        on, off = max(lab.onset, start), min(lab.end, end)
        bass_pc = m21pitch.Pitch(lab.bass).pitchClass
        bass = 36 + ((bass_pc - 36) % 12)  # C2..B2
        pcs = sorted({m21pitch.Pitch(n).pitchClass for n in lab.pitches})
        upper = _voice_upper(pcs, prev_upper)
        prev_upper = upper
        out.append(PlayNote(on, off - on, bass, [], 0.6))
        out += [PlayNote(on, off - on, m, [], 0.5) for m in upper]
    return out


def _voice_upper(pcs: list[int], prev: list[int] | None) -> list[int]:
    """Close-position upper voices around middle C; if a previous chord exists, pick the voicing
    (among the rotations) with the smallest total motion."""
    def rotations():
        for r in range(len(pcs)):
            order = pcs[r:] + pcs[:r]
            base = 55  # G3
            voicing, cur = [], base
            for pc in order:
                m = cur + ((pc - cur) % 12)
                voicing.append(m)
                cur = m + 1
            yield voicing
            yield [v + 12 for v in voicing]
    cands = list(rotations())
    if prev is None:
        return min(cands, key=lambda v: abs(sum(v) / len(v) - 64))
    def cost(v):
        return sum(min(abs(a - b) for b in prev) for a in v) + sum(min(abs(a - b) for b in v) for a in prev)
    return min(cands, key=cost)


def substitute(piece: Piece, events: list[PlayNote], label: Label, target_pitches: list[str]) -> tuple[list[PlayNote], list[dict]]:
    """Replace the chord of `label` by `target_pitches` inside the label's span, keeping the texture:
    every chord tone moves to the nearest note of the same role in the new chord (root to root, third
    to third, ...), or to the nearest new chord tone if that role doesn't exist. Non-chord tones are
    kept. Returns new events and the list of moves."""
    from music21 import interval as m21interval
    from music21 import pitch as m21pitch

    root = m21pitch.Pitch(target_pitches[0])
    role_pc = {}
    for name in target_pitches:
        p = m21pitch.Pitch(name)
        gen = 1 if p.name == root.name else m21interval.Interval(root, p).generic.mod7
        role = {1: "root", 3: "third", 5: "fifth", 7: "seventh", 2: "ninth"}.get(gen, "other")
        role_pc.setdefault(role, p.pitchClass)
    target_pcs = {m21pitch.Pitch(n).pitchClass for n in target_pitches}
    by_id = piece.notes_by_id()
    moves, out = [], []
    for e in events:
        n = by_id.get(e.ids[0]) if e.ids else None
        if n is None or not (label.onset <= e.onset < label.end):
            out.append(e)
            continue
        role = chord_role(n, label)
        if role is None:
            out.append(e)
            continue
        pc = role_pc.get(role)
        if pc is None:
            pc = min(target_pcs, key=lambda q: min((q - e.midi) % 12, (e.midi - q) % 12))
        up, down = (pc - e.midi) % 12, (e.midi - pc) % 12
        new = e.midi + (up if up <= down else -down)
        if new != e.midi:
            moves.append({"from": e.midi, "to": new, "ids": e.ids, "role": role})
        out.append(PlayNote(e.onset, e.duration, new, e.ids, e.velocity, changed=new != e.midi))
    return out, moves


def pedal_by_harmony(events: list[PlayNote], piece: Piece, analysis_id: str, end: Fraction) -> None:
    """Simulate a sustain pedal changed at every harmony boundary of an analysis: each note sounds on
    to the end of its harmony, or until the same key is struck again."""
    an = piece.analysis(analysis_id)
    by_midi: dict[int, list[PlayNote]] = {}
    for e in sorted(events, key=lambda e: e.onset):
        by_midi.setdefault(e.midi, []).append(e)
    for same in by_midi.values():
        for i, e in enumerate(same):
            lab = an.label_at(e.onset)
            if lab is None:
                continue
            stop = min(lab.end, end)
            if i + 1 < len(same):
                stop = min(stop, same[i + 1].onset)
            if stop - e.onset > e.duration:
                e.duration = stop - e.onset


def build(piece: Piece, *, start: Fraction, end: Fraction, mode: str = "original", analysis: str | None = None,
          tracks: set[str] | None = None, transpose: int = 0,
          substitution: tuple[Label, list[str]] | None = None, pedal: bool = False) -> tuple[list[PlayNote], dict]:
    if mode not in MODES:
        raise ValueError(f"unknown mode {mode}")
    if MODES[mode]["needs_analysis"] and not analysis:
        raise ValueError(f"mode {mode} needs an analysis")
    if mode == "original":
        ev = original(piece, start, end, tracks)
    elif mode == "blocked":
        ev = blocked(piece, start, end, tracks)
    elif mode == "outer":
        ev = outer(piece, start, end, tracks, "both")
    elif mode == "melody":
        ev = outer(piece, start, end, tracks, "top")
    elif mode == "bass":
        ev = outer(piece, start, end, tracks, "bass")
    elif mode == "chord_tones":
        ev = chord_tones(piece, start, end, tracks, analysis)
    else:
        ev = progression(piece, start, end, analysis)
    info: dict = {"mode": mode, **MODES[mode]}
    if substitution is not None:
        label, target = substitution
        ev, moves = substitute(piece, ev, label, target)
        info["moves"] = moves
    if pedal and analysis and mode not in ("progression",):
        pedal_by_harmony(ev, piece, analysis, end)
        info["pedal"] = f"Sustain pedal changed at each harmony of {analysis}."
    if transpose:
        for e in ev:
            e.midi += transpose
    return ev, info
