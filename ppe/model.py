"""The shared musical representation.

All times are exact `Fraction`s in quarter notes from the start of the piece ("score time").
A note is identified by its musical address (measure, offset, staff, voice, pitch), never by a
renderer ID; renderer IDs are attached separately (`Note.render_id`) and rebuilt on every import.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Literal

TieKind = Literal["start", "continue", "stop"] | None


@dataclass(frozen=True)
class Measure:
    number: int  # printed measure number
    index: int  # 0-based physical index
    onset: Fraction  # quarters from the start
    duration: Fraction  # actual duration in quarters
    time_signature: str  # "2/2"
    beat: Fraction  # length of one notated beat in quarters (2/2 -> 2, 9/8 -> 3/2, 4/4 -> 1)
    key_fifths: int  # key signature, sharps positive
    render_id: str = ""

    @property
    def end(self) -> Fraction:
        return self.onset + self.duration


@dataclass(frozen=True)
class Note:
    """One notehead. Tied continuations are separate noteheads with `tie` set."""

    id: str
    measure: int
    offset: Fraction  # quarters from the start of its measure
    onset: Fraction  # quarters from the start of the piece
    duration: Fraction  # notated duration of this notehead
    staff: int  # 1 = top
    voice: int
    midi: int
    name: str  # spelled, e.g. "G#3"
    step: str  # "G"
    alter: int  # -2..2
    octave: int
    tie: TieKind = None
    render_id: str | None = None
    track: str = ""  # curated listening track (see ppe.pieces)

    @property
    def end(self) -> Fraction:
        return self.onset + self.duration

    @property
    def pc(self) -> int:
        return self.midi % 12

    @property
    def is_attack(self) -> bool:
        """False for the tied continuation of an earlier notehead."""
        return self.tie not in ("continue", "stop")


@dataclass(frozen=True)
class Key:
    tonic: str  # spelled, e.g. "C#"
    mode: Literal["major", "minor"]

    @property
    def label(self) -> str:
        from ppe.spelling import pretty

        return f"{pretty(self.tonic)} {self.mode}"


@dataclass(frozen=True)
class Label:
    """One harmonic label from one analysis, positioned in score time."""

    id: str
    analysis: str  # analysis id
    onset: Fraction
    end: Fraction
    measure: int
    beat: Fraction  # 1-based beat in the notated metre
    key: Key
    figure: str  # as written by the analyst, e.g. "V65", "N6", "viio7/V"
    display: str  # typographic form, e.g. "V⁶₅"
    pitches: tuple[str, ...]  # spelled chord pitches, root position order
    pcs: frozenset[int]
    root: str
    bass: str
    quality: str  # "major", "minor", "diminished", "half-diminished", "dominant seventh", ...
    inversion: int  # 0 = root position
    family: str  # explanation family, see ppe.explain
    applied_to: str | None = None  # "V" for V/V
    raw: str = ""  # source line or label
    alternatives: tuple[str, ...] = ()  # analyst-recorded variant readings (figures)
    extra_pcs: frozenset[int] = frozenset()  # tones the label accounts for beyond the chord (suspensions, added tones)
    cadence: str | None = None


@dataclass
class AnalystNote:
    measure: int
    text: str


@dataclass
class Analysis:
    id: str  # short id, e.g. "BPS"
    analyst: str  # human-readable attribution
    kind: Literal["expert", "automatic", "user"]
    source: str  # URL or path
    licence: str
    colour: str
    labels: list[Label] = field(default_factory=list)
    notes: list[AnalystNote] = field(default_factory=list)
    issues: list[str] = field(default_factory=list)  # parse/alignment problems found while importing

    def label_at(self, t: Fraction) -> Label | None:
        for lab in self.labels:
            if lab.onset <= t < lab.end:
                return lab
        return None


@dataclass
class Track:
    """A listening track ("Melody", "Triplets", "Bass"), defined per piece by a documented rule."""

    id: str
    name: str
    rule: str  # human-readable definition
    count: int = 0


@dataclass
class Piece:
    id: str
    title: str
    subtitle: str
    composer: str
    tempo_qpm: float  # default playback tempo in quarter notes per minute
    measures: list[Measure]
    notes: list[Note]
    analyses: list[Analysis]
    tracks: list[Track]
    score_source: str
    score_licence: str
    mei: str = ""  # renderer input with IDs; kept out of JSON responses
    validation: dict = field(default_factory=dict)

    def measure(self, number: int) -> Measure:
        for m in self.measures:
            if m.number == number:
                return m
        raise KeyError(number)

    def measure_at(self, t: Fraction) -> Measure:
        for m in self.measures:
            if m.onset <= t < m.end:
                return m
        return self.measures[-1]

    def analysis(self, aid: str) -> Analysis:
        for a in self.analyses:
            if a.id == aid:
                return a
        raise KeyError(aid)

    @property
    def end(self) -> Fraction:
        return self.measures[-1].end

    def notes_by_id(self) -> dict[str, Note]:
        return {n.id: n for n in self.notes}
