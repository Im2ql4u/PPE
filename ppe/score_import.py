"""Import a score file (MusicXML or Humdrum **kern) into the core model via music21.

music21 is the source of truth for pitch and time; the renderer (Verovio) is mapped onto it and
checked against it (see ppe.render).
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from pathlib import Path

from music21 import chord as m21chord
from music21 import converter, meter, stream
from music21 import note as m21note

from ppe.model import Measure, Note
from ppe.spelling import m21_name


def _frac(x) -> Fraction:
    return Fraction(x).limit_denominator(960)


def _beat_length(ts: meter.TimeSignature) -> Fraction:
    # 2/2 -> 2 quarters, 9/8 -> 3/2 (dotted quarter), 4/4 -> 1, 3/4 -> 1, 6/8 -> 3/2
    return _frac(ts.beatDuration.quarterLength)


def _offset_id(x: Fraction) -> str:
    return f"{x.numerator}" if x.denominator == 1 else f"{x.numerator}_{x.denominator}"


def load_score(path: Path) -> stream.Score:
    s = converter.parse(str(path))
    if not isinstance(s, stream.Score):
        raise ValueError(f"{path} did not parse as a Score")
    return s


def staff_parts(score: stream.Score) -> list[stream.Part]:
    """Parts ordered top staff first. Humdrum spines are often listed bottom-up; sort by pitch."""
    parts = [p for p in score.parts if p.recurse().notes]

    def mean_pitch(p: stream.Part) -> float:
        ps = [pp.midi for n in p.recurse().notes for pp in n.pitches]
        return sum(ps) / len(ps)

    return sorted(parts, key=mean_pitch, reverse=True)


def import_measures(score: stream.Score) -> list[Measure]:
    top = staff_parts(score)[0]
    out = []
    for idx, m in enumerate(top.getElementsByClass(stream.Measure)):
        ts = m.timeSignature or m.getContextByClass(meter.TimeSignature)
        ks = m.keySignature or m.getContextByClass("KeySignature")
        out.append(
            Measure(
                number=int(m.number),
                index=idx,
                onset=_frac(m.getOffsetInHierarchy(score)),
                duration=_frac(m.duration.quarterLength) or _frac(ts.barDuration.quarterLength),
                time_signature=ts.ratioString,
                beat=_beat_length(ts),
                key_fifths=int(ks.sharps) if ks is not None else 0,
            )
        )
    return out


def import_notes(score: stream.Score, measures: list[Measure]) -> tuple[list[Note], dict]:
    onset_of = {m.number: m.onset for m in measures}
    notes: list[Note] = []
    skipped = Counter()
    seen: Counter = Counter()
    for staff_idx, part in enumerate(staff_parts(score), start=1):
        for m in part.getElementsByClass(stream.Measure):
            # Voice numbers: order of voices within the staff and measure (1 = first listed).
            # Source voice ids are unreliable (Humdrum sub-spines get object ids; MusicXML
            # numbers voices 5/6 on the second staff), so we renumber per staff.
            # Some Humdrum measures hold notes directly *and* in Voice objects; keep both.
            voices = list(m.voices)
            if not voices or len(m.notes):
                voices.insert(0, m)  # m.notes is non-recursive: only direct children
            for vnum, v in enumerate(voices, start=1):
                for el in v.notes:
                    if el.duration.isGrace or el.quarterLength == 0:
                        skipped["grace"] += 1
                        continue
                    offset = _frac(el.getOffsetInHierarchy(m))
                    pieces = (
                        [(n.pitch, n.tie) for n in el.notes]
                        if isinstance(el, m21chord.Chord)
                        else [(el.pitch, el.tie)]
                    )
                    for p, tie in pieces:
                        alter = int(p.accidental.alter) if p.accidental is not None else 0
                        key = (int(m.number), staff_idx, vnum, offset, p.midi)
                        seen[key] += 1
                        suffix = "" if seen[key] == 1 else f".{seen[key]}"
                        nid = f"m{m.number}.s{staff_idx}.v{vnum}.o{_offset_id(offset)}.p{p.midi}{suffix}"
                        notes.append(
                            Note(
                                id=nid,
                                measure=int(m.number),
                                offset=offset,
                                onset=onset_of[int(m.number)] + offset,
                                duration=_frac(el.quarterLength),
                                staff=staff_idx,
                                voice=vnum,
                                midi=int(p.midi),
                                name=m21_name(p.step, alter) + str(p.octave),
                                step=p.step,
                                alter=alter,
                                octave=int(p.octave),
                                tie=tie.type if tie is not None and tie.type in ("start", "continue", "stop") else None,
                            )
                        )
    notes.sort(key=lambda n: (n.onset, -n.midi, n.staff, n.voice))
    return notes, {"skipped": dict(skipped)}


def sounding_notes(notes: list[Note]) -> list[tuple[Note, Fraction, list[str]]]:
    """Merge tie chains into sounding notes: (first notehead, total duration, all notehead ids)."""
    out = []
    open_chains: dict[tuple[int, int, int], int] = {}  # (staff, voice, midi) -> index in out
    for n in sorted(notes, key=lambda n: (n.onset, n.staff, n.voice, n.midi)):
        k = (n.staff, n.voice, n.midi)
        if n.tie in ("continue", "stop") and k in open_chains:
            i = open_chains[k]
            first, dur, ids = out[i]
            out[i] = (first, dur + n.duration, ids + [n.id])
            if n.tie == "stop":
                del open_chains[k]
            continue
        out.append((n, n.duration, [n.id]))
        if n.tie == "start":
            open_chains[k] = len(out) - 1
    return out
