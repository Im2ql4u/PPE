"""Transformations: chord substitution candidates, voice leading, transposition naming."""

from __future__ import annotations

import itertools

from music21 import key as m21key
from music21 import pitch as m21pitch
from music21 import roman

from ppe.analyses import _bracket_pitches, _family
from ppe.explain import FAMILY
from ppe.model import Label
from ppe.spelling import figure_display, pretty

MAJOR_CANDIDATES = ["I", "ii", "iii", "IV", "V", "vi", "viio", "V7", "ii7", "IV7", "viio7",
                    "iv", "bVI", "bIII", "bVII", "N6", "V7/V", "V7/vi", "V7/IV", "V7/ii", "It6", "Ger65"]
MINOR_CANDIDATES = ["i", "iio", "III", "iv", "v", "V", "VI", "VII", "viio", "V7", "viio7", "iio7",
                    "N6", "It6", "Ger65", "Fr43", "V7/iv", "V7/VI", "V7/III", "IV", "I"]


def transpose_name(name: str, interval: str) -> str:
    """Transpose a spelled pitch name (with or without octave) by a named interval ('M2', '-A1')."""
    from music21 import interval as m21interval

    if interval in ("P1", ""):
        return name
    return m21pitch.Pitch(name).transpose(m21interval.Interval(interval)).nameWithOctave \
        if any(ch.isdigit() for ch in name) else m21pitch.Pitch(name).transpose(m21interval.Interval(interval)).name


def transpose_label(label: Label, interval: str, semitones: int) -> Label:
    """The same Roman numeral in the transposed key: keys and spellings move, figure and roles don't."""
    from dataclasses import replace

    from ppe.model import Key

    if not semitones:
        return label
    return replace(
        label,
        key=Key(transpose_name(label.key.tonic, interval), label.key.mode),
        pitches=tuple(transpose_name(p, interval) for p in label.pitches),
        root=transpose_name(label.root, interval), bass=transpose_name(label.bass, interval),
        pcs=frozenset((pc + semitones) % 12 for pc in label.pcs),
        extra_pcs=frozenset((pc + semitones) % 12 for pc in label.extra_pcs),
    )


def pc_distance(a: int, b: int) -> int:
    d = (b - a) % 12
    return d if d <= 6 else d - 12


def minimal_voice_leading(src: list[int], dst: list[int]) -> tuple[int, list[tuple[int, int, int]]]:
    """Smallest total semitone motion mapping every source pitch class to a destination pitch class
    such that every destination is reached (Tymoczko-style, allowing doublings). Brute force; chords
    have at most ~5 distinct pitch classes. Returns (total, [(src, dst, signed motion)])."""
    src, dst = sorted(set(src)), sorted(set(dst))
    best = None
    if len(src) >= len(dst):
        for assign in itertools.product(dst, repeat=len(src)):
            if set(assign) != set(dst):
                continue
            moves = [(s, d, pc_distance(s, d)) for s, d in zip(src, assign)]
            total = sum(abs(m[2]) for m in moves)
            if best is None or total < best[0]:
                best = (total, moves)
    else:
        for assign in itertools.product(src, repeat=len(dst)):
            if set(assign) != set(src):
                continue
            moves = [(s, d, pc_distance(s, d)) for s, d in zip(assign, dst)]
            total = sum(abs(m[2]) for m in moves)
            if best is None or total < best[0]:
                best = (total, moves)
    return best if best else (0, [])


def voice_leading(a: Label, b: Label) -> dict:
    def spelled(lab: Label) -> dict[int, str]:
        return {m21pitch.Pitch(n).pitchClass: pretty(n) for n in lab.pitches}
    sa, sb = spelled(a), spelled(b)
    total, moves = minimal_voice_leading(list(sa), list(sb))
    return {
        "from": a.display, "to": b.display, "total": total,
        "moves": [{"from": sa[s], "to": sb[d], "semitones": m, "from_pc": s, "to_pc": d} for s, d, m in moves],
        "common_tones": sorted(pretty(sa[pc]) for pc in set(sa) & set(sb)),
    }


def candidates(label: Label, limit: int = 8) -> list[dict]:
    """Rule-based substitutes for a chord, in the label's key, ranked by voice-leading distance."""
    k = m21key.Key(label.key.tonic, label.key.mode)
    pool = MAJOR_CANDIDATES if label.key.mode == "major" else MINOR_CANDIDATES
    out = []
    seen = {label.pcs}
    for fig in pool:
        try:
            rn = roman.RomanNumeral(fig, k)
        except Exception:  # noqa: BLE001 - skip figures music21 can't build in this key
            continue
        pitches, _ = _bracket_pitches(rn, fig)
        pcs = frozenset(p.pitchClass for p in pitches)
        if pcs in seen:
            continue
        seen.add(pcs)
        total, _ = minimal_voice_leading(list(label.pcs), list(pcs))
        fam = _family(rn, fig)
        names = []
        for p in sorted(pitches, key=lambda p: 0 if p.name == rn.root().name else (p.pitchClass - rn.root().pitchClass) % 12):
            if p.name not in names:
                names.append(p.name)
        out.append({
            "figure": fig, "display": figure_display(fig), "pitches": names,
            "pitches_text": "–".join(pretty(n) for n in names),
            "distance": total, "common_tones": len(label.pcs & pcs),
            "family": fam, "gist": FAMILY.get(fam, ("", ""))[0],
        })
    out.sort(key=lambda c: (c["distance"], -c["common_tones"]))
    return out[:limit]
