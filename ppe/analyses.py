"""Import harmonic analyses (RomanText, DCML) as labelled layers aligned to the core's measures.

Alignment is by (printed measure number, offset within measure), never by absolute time: files may
encode an anacrusis differently (experiment E2). Labels persist until the next label (RomanText
convention); repeat lines like "m42-46 = m5-9" are expanded by music21.
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

from music21 import converter, roman
from music21 import interval as m21interval

from ppe.model import Analysis, AnalystNote, Key, Label, Piece
from ppe.spelling import figure_display

_MEASURE_LINE = re.compile(r"^m(\d+)(var\d+)?\b")


def _q(x) -> Fraction:
    return Fraction(x).limit_denominator(960)


def _quality(rn: roman.RomanNumeral) -> str:
    if rn.isDominantSeventh():
        return "dominant seventh"
    if rn.isDiminishedSeventh():
        return "diminished seventh"
    if rn.isHalfDiminishedSeventh():
        return "half-diminished seventh"
    if rn.isMajorTriad():
        return "major"
    if rn.isMinorTriad():
        return "minor"
    if rn.isDiminishedTriad():
        return "diminished"
    if rn.isAugmentedTriad():
        return "augmented"
    if rn.seventh is not None:
        return {"major": "major seventh", "minor": "minor seventh"}.get(rn.quality, "seventh chord")
    return rn.commonName or rn.quality


def _family(rn: roman.RomanNumeral, figure: str) -> str:
    f = figure
    if f.startswith(("Ger", "It", "Fr")):
        return "augmented sixth"
    if f.startswith("N"):
        return "neapolitan"
    if f.startswith("Cad"):
        return "cadential six-four"
    if "/" in f:
        return "applied"
    alone = rn.romanNumeralAlone.upper()
    if rn.frontAlterationAccidental is not None or (rn.key.mode == "major" and alone in ("III", "VI", "VII") and rn.isMajorTriad()):
        if not ("/" in f):
            return "mixture" if rn.frontAlterationAccidental is not None else _degree_family(alone, rn)
    return _degree_family(alone, rn)


def _degree_family(alone: str, rn: roman.RomanNumeral) -> str:
    if alone == "VII" and (rn.isDiminishedTriad() or rn.isDiminishedSeventh() or rn.isHalfDiminishedSeventh()):
        return "leading-tone"
    if alone == "V" and rn.inversion() == 2 and rn.seventh is None:
        return "dominant"
    return {"I": "tonic", "II": "predominant", "IV": "predominant", "V": "dominant",
            "VI": "submediant", "III": "mediant", "VII": "subtonic"}.get(alone, "other")


def chord_tones_ordered(rn: roman.RomanNumeral) -> list[str]:
    root = rn.root()
    def step(p):
        return m21interval.Interval(root, p).generic.mod7 if p.name != root.name else 1
    uniq = {}
    for p in rn.pitches:
        uniq.setdefault(p.name, p)
    return [p.name for p in sorted(uniq.values(), key=step)]


_BRACKET_INTERVALS = {"b9": "m9", "#9": "A9", "9": "M9", "b5": "d5", "#5": "A5", "b13": "m13", "#11": "A11"}


def _bracket_pitches(rn: roman.RomanNumeral, figure: str) -> tuple[list, list[str]]:
    """Resolve bracketed alterations ourselves.

    music21 applies bracketed alterations ([b9], [b5]) to the *diatonic* chord step, so in a minor key
    V9[b9] becomes a doubly-flattened ninth (A♭ over G♯ in C♯ minor) instead of A♮, and two
    alterations in one bracket ([b9b5]) yield a garbled chord. Analysts (Tymoczko) mean intervals
    above the root. So: parse the figure without brackets, then apply each alteration as an interval
    above the root; [noN] removes a step."""
    issues: list[str] = []
    alts = re.findall(r"\[([^\]]*)\]", figure)
    if not alts:
        return list(rn.pitches), issues
    base_fig = re.sub(r"\[[^\]]*\]", "", figure)
    base = roman.RomanNumeral(base_fig, rn.key)
    root = base.root()
    pitches = list(base.pitches)
    m21_names = sorted({p.name for p in rn.pitches})
    for group in alts:
        for kind, tok in re.findall(r"(no|add)?([b#]?\d+)", group):
            step = int(re.sub(r"\D", "", tok)) % 7 or 7
            same_step = [i for i, p in enumerate(pitches)
                         if (0 if p.name == root.name else m21interval.Interval(root, p).generic.mod7) == step]
            if kind == "no":
                pitches = [p for i, p in enumerate(pitches) if i not in same_step]
                continue
            if tok not in _BRACKET_INTERVALS:
                if kind != "add":
                    issues.append(f"{figure}: alteration '{tok}' not interpreted")
                continue
            target = m21interval.Interval(_BRACKET_INTERVALS[tok]).transposePitch(root)
            if same_step:
                for i in same_step:
                    pitches[i] = target
            else:
                pitches.append(target)
    ours = sorted({p.name for p in pitches})
    if ours != m21_names:
        issues.append(f"{figure}: music21 reads {m21_names}; interpreted as intervals above the root: {ours}")
    return pitches, issues


def label_from_rn(rn: roman.RomanNumeral, *, lid: str, analysis_id: str, onset: Fraction, end: Fraction,
                  measure: int, beat: Fraction, raw: str = "", issues: list[str] | None = None) -> Label:
    figure = rn.figure
    pitches, fix_issues = _bracket_pitches(rn, figure)
    if issues is not None:
        issues.extend(f"m{measure}: {msg}" for msg in fix_issues)
    names = {}
    for p in pitches:
        names.setdefault(p.name, p)
    pcs = [p.pitchClass for p in names.values()]
    if len(set(pcs)) < len(pcs) and issues is not None:
        issues.append(f"m{measure}: {figure} contains two spellings of one pitch class: {sorted(names)}")
    root = rn.root()

    def order(p):
        return 0 if p.name == root.name else m21interval.Interval(root, p).generic.mod7

    quality = _quality(rn)
    if re.search(r"9", figure):
        quality = "dominant minor ninth" if "b9" in figure else ("dominant ninth" if rn.romanNumeralAlone.upper() == "V" else "ninth chord")
    return Label(
        id=lid, analysis=analysis_id, onset=onset, end=end, measure=measure, beat=beat,
        key=Key(rn.key.tonic.name, rn.key.mode),
        figure=figure, display=figure_display(figure),
        pitches=tuple(p.name for p in sorted(names.values(), key=order)),
        pcs=frozenset(pcs),
        root=root.name, bass=rn.bass().name,
        quality=quality, inversion=int(rn.inversion()),
        family=_family(rn, figure),
        applied_to=rn.secondaryRomanNumeral.figure if rn.secondaryRomanNumeral is not None else None,
        raw=raw,
    )


def import_romantext(path: Path, piece: Piece, *, aid: str, analyst: str, kind: str, source: str,
                     licence: str, colour: str) -> Analysis:
    text = path.read_text(encoding="utf-8")
    s = converter.parse(text, format="romantext")
    an = Analysis(id=aid, analyst=analyst, kind=kind, source=source, licence=licence, colour=colour)

    # time signature consistency: the analysis must use the score's metre
    ts_line = re.search(r"^Time [Ss]ignature:\s*(\S+)", text, re.M)
    if ts_line and ts_line.group(1) != piece.measures[0].time_signature:
        an.issues.append(f"analysis metre {ts_line.group(1)} differs from score {piece.measures[0].time_signature}")

    raw_by_measure: dict[int, str] = {}
    for line in text.splitlines():
        m = _MEASURE_LINE.match(line.strip())
        if m and not m.group(2):
            raw_by_measure[int(m.group(1))] = line.strip()

    measure_numbers = {m.number for m in piece.measures}
    items = []
    for rn in s.flatten().getElementsByClass(roman.RomanNumeral):
        meas = rn.getContextByClass("Measure")
        number = int(meas.number) if meas is not None else None
        if number is None or number not in measure_numbers:
            an.issues.append(f"label {rn.figure} in measure {number} has no matching score measure")
            continue
        local = _q(rn.getOffsetInHierarchy(meas))
        m = piece.measure(number)
        if local >= m.duration:
            an.issues.append(f"label {rn.figure} at m{number} offset {local} lies beyond the measure")
            continue
        items.append((m.onset + local, number, local, rn))
    items.sort(key=lambda x: x[0])

    for i, (onset, number, local, rn) in enumerate(items):
        end = items[i + 1][0] if i + 1 < len(items) else piece.end
        m = piece.measure(number)
        an.labels.append(label_from_rn(
            rn, lid=f"{aid}-{i}", analysis_id=aid, onset=onset, end=end, measure=number,
            beat=1 + local / m.beat, raw=raw_by_measure.get(number, ""), issues=an.issues,
        ))

    _attach_variants_and_notes(text, an, piece)
    _check_unparsed_tokens(text, an)
    return an


def _attach_variants_and_notes(text: str, an: Analysis, piece: Piece) -> None:
    lines = [l.strip() for l in text.splitlines()]
    for i, line in enumerate(lines):
        mv = re.match(r"^m(\d+)var\d+\s+(.*)$", line)
        if mv:
            number = int(mv.group(1))
            tokens = [t for t in re.split(r"\s+", mv.group(2)) if t and not re.fullmatch(r"b[\d.]+", t)]
            figures = [t for t in tokens if not t.endswith(":")]
            for idx, lab in enumerate(an.labels):
                if lab.measure == number:
                    an.labels[idx] = _replace(lab, alternatives=lab.alternatives + (" ".join(figures),))
                    break
        mp = re.match(r"^Pedal:\s*(\S+)\s+m\s*(\d+)", line)
        if mp:
            from ppe.spelling import pretty

            an.notes.append(AnalystNote(measure=int(mp.group(2)), text=f"Pedal point on {pretty(mp.group(1))}"))
        if line.startswith("Note:"):
            # attach to the nearest following measure line, else the previous one
            target = None
            for j in list(range(i + 1, min(i + 4, len(lines)))) + list(range(i - 1, max(i - 4, -1), -1)):
                mm = _MEASURE_LINE.match(lines[j])
                if mm:
                    target = int(mm.group(1))
                    break
            an.notes.append(AnalystNote(measure=target or 0, text=line[len("Note:"):].strip()))


def _check_unparsed_tokens(text: str, an: Analysis) -> None:
    """Flag tokens like 'viio64b3' (a missing space) that music21 may silently misread."""
    for line in text.splitlines():
        if not _MEASURE_LINE.match(line.strip()):
            continue
        for tok in line.split()[1:]:
            if re.search(r"[A-Za-z].*b\d", tok) and not tok.startswith("b") and "[" not in tok:
                an.issues.append(f"suspicious token '{tok}' in line '{line.strip()}' (missing space before a beat?)")


_DCML_QUALITY = {"M": "major", "m": "minor", "o": "diminished", "+": "augmented",
                 "Mm7": "dominant seventh", "mm7": "minor seventh", "MM7": "major seventh",
                 "mM7": "minor-major seventh", "%7": "half-diminished seventh", "o7": "diminished seventh",
                 "+7": "augmented seventh", "+M7": "augmented major seventh",
                 "It": "Italian sixth", "Ger": "German sixth", "Fr": "French sixth"}
_DCML_INTERVALS = {"M": (0, 4, 1), "m": (0, -3, 1), "o": (0, -3, 6), "+": (0, 4, 8),
                   "Mm7": (0, 4, 1, -2), "mm7": (0, -3, 1, -2), "MM7": (0, 4, 1, 5), "mM7": (0, -3, 1, 5),
                   "%7": (0, -3, 6, -2), "o7": (0, -3, 6, -9), "+7": (0, 4, 8, -2), "+M7": (0, 4, 8, 5),
                   "It": (0, 4, 10), "Ger": (0, 4, 1, 10), "Fr": (0, 4, 6, 10)}
_FIGBASS_INV = {None: 0, "": 0, "7": 0, "6": 1, "65": 1, "64": 2, "43": 2, "2": 3, "42": 3}


def import_dcml(harmonies_tsv: Path, piece: Piece, *, aid: str, analyst: str, source: str, licence: str,
                colour: str) -> Analysis:
    """DCML harmony labels (ms3 TSV) aligned by (mn, mn_onset).

    Structural chord = root + chord-type intervals; tones the label names beyond that (suspensions,
    retardations, added notes) go to `extra_pcs`. DCML's derived `chord_tones` omit a root displaced
    by a suspension (e.g. ii(2)) although it usually still sounds (experiment E3), so the structural
    chord is computed from root + type rather than taken from `chord_tones`.
    """
    import ms3

    h = ms3.load_tsv(harmonies_tsv)
    h = h[h.chord_tones.notna()]
    an = Analysis(id=aid, analyst=analyst, kind="expert", source=source, licence=licence, colour=colour)
    rows = []
    for _, r in h.iterrows():
        number = int(r.mn)
        try:
            m = piece.measure(number)
        except KeyError:
            an.issues.append(f"label {r.label} in m{number} has no matching score measure")
            continue
        local = Fraction(str(r.mn_onset)) * 4
        rows.append((m.onset + local, number, local, r))
    rows.sort(key=lambda x: x[0])
    for i, (onset, number, local, r) in enumerate(rows):
        end = rows[i + 1][0] if i + 1 < len(rows) else piece.end
        global_minor = str(r.globalkey).islower()
        tonic = ms3.name2fifths(r.globalkey) + ms3.roman_numeral2fifths(r.localkey, global_minor)
        local_minor = bool(r.localkey_is_minor)
        intervals = _DCML_INTERVALS.get(r.chord_type)
        structural = [tonic + int(r.root) + iv for iv in intervals] if intervals else [tonic + c for c in r.chord_tones]
        named = [tonic + c for c in r.chord_tones] + [tonic + c for c in (r.added_tones or ())]
        def name(tpc: int) -> str:
            return str(ms3.fifths2name(tpc)).replace("b", "-")
        struct_names = [name(t) for t in structural]
        pcs = frozenset(m21_pc(n) for n in struct_names)
        extra = frozenset(m21_pc(name(t)) for t in named) - pcs
        figure = str(r.chord)
        meas = piece.measure(number)
        an.labels.append(Label(
            id=f"{aid}-{i}", analysis=aid, onset=onset, end=end, measure=number, beat=1 + local / meas.beat,
            key=Key(name(tonic), "minor" if local_minor else "major"),
            figure=figure, display=figure_display(re.sub(r"\(.*?\)", "", figure)),
            pitches=tuple(struct_names), pcs=pcs, root=name(tonic + int(r.root)),
            bass=name(tonic + int(r.bass_note)), quality=_DCML_QUALITY.get(r.chord_type, str(r.chord_type)),
            inversion=_FIGBASS_INV.get(None if r.figbass is None or str(r.figbass) == "<NA>" else str(r.figbass), 0),
            family=_dcml_family(r), applied_to=None if _na(r.relativeroot) else str(r.relativeroot),
            raw=str(r.label), extra_pcs=extra, cadence=None if _na(r.cadence) else str(r.cadence),
        ))
    return an


def _na(x) -> bool:
    return x is None or str(x) in ("<NA>", "nan", "")


def m21_pc(name: str) -> int:
    from music21 import pitch as m21pitch

    return m21pitch.Pitch(name).pitchClass


def _dcml_family(r) -> str:
    num = str(r.numeral)
    if not _na(r.relativeroot):
        return "applied"
    if num in ("Ger", "It", "Fr"):
        return "augmented sixth"
    if num.lstrip("b#").upper() == "II" and num.startswith("b"):
        return "neapolitan"
    if num.startswith(("b", "#")):
        return "mixture"
    if str(r.chord_type) in ("o", "o7", "%7") and num.upper() == "VII":
        return "leading-tone"
    return {"I": "tonic", "II": "predominant", "IV": "predominant", "V": "dominant", "VI": "submediant",
            "III": "mediant", "VII": "subtonic"}.get(num.upper(), "other")


def _replace(lab: Label, **kw) -> Label:
    from dataclasses import replace

    return replace(lab, **kw)
