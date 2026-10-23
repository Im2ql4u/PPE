"""Piece registry and builder.

A piece is built from a score file plus analysis files, all fetched into data/external by
`python -m ppe fetch`. Nothing derived from these sources is committed (licences differ, see
DATA_LICENSES.md); packs are built locally into data/packs by `python -m ppe build`.
"""

from __future__ import annotations

import json
import pickle
from dataclasses import dataclass, field, replace
from fractions import Fraction
from pathlib import Path
from typing import Callable

from ppe.analyses import import_dcml, import_romantext
from ppe.mei_import import load_mei, mei_to_core
from ppe.model import Note, Piece, Track
from ppe.validate import crosscheck_music21, crosscheck_reference_notes

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "data" / "external"
PACKS = ROOT / "data" / "packs"
WIR = EXT / "when_in_rome" / "Corpus"

# Lens colours: distinct, muted, readable on paper.
COLOURS = {"BPS": "#2f6f8f", "DT": "#b4532a", "WiR": "#2f6f8f", "AugNet": "#7a6a2e", "DCML": "#6b4c8a"}


@dataclass
class AnalysisSpec:
    id: str
    path: Path
    analyst: str
    kind: str  # expert | automatic
    source: str
    licence: str
    format: str = "romantext"  # or "dcml"


@dataclass
class TrackSpec:
    id: str
    name: str
    rule: str
    test: Callable[[Note], bool]


@dataclass
class PieceSpec:
    id: str
    title: str
    subtitle: str
    composer: str
    tempo_qpm: float
    score: Path
    score_source: str
    score_licence: str
    analyses: list[AnalysisSpec]
    tracks: list[TrackSpec]
    # Parser disagreements that have been investigated and explained (see docs/validation.md).
    known_discrepancy_measures: set[int] = field(default_factory=set)
    known_discrepancy_note: str = ""
    requires: str = ""  # human hint if the score file is missing
    # A second encoding to compare note by note: for converted scores, the analysts' own note table
    # (must agree); for other pieces, an independent edition (informational).
    reference_notes: Path | None = None
    reference_required: bool = False
    reference_note: str = ""


MOONLIGHT_WIR = WIR / "Piano_Sonatas" / "Beethoven,_Ludwig_van" / "Op027_No2(Moonlight)" / "1"
BWV846_WIR = WIR / "Keyboard_Other" / "Bach,_Johann_Sebastian" / "The_Well-Tempered_Clavier_I" / "01"

SPECS: dict[str, PieceSpec] = {
    "moonlight": PieceSpec(
        id="moonlight",
        title="Sonata quasi una fantasia",
        subtitle="Op. 27 No. 2 · I. Adagio sostenuto",
        composer="Ludwig van Beethoven",
        tempo_qpm=56,
        score=EXT / "sapp_beethoven" / "kern" / "sonata14-1.krn",
        score_source="Craig Stuart Sapp, Humdrum edition of the Beethoven piano sonatas (after Durand, 1915, ed. Dukas). github.com/craigsapp/beethoven-piano-sonatas",
        score_licence="No licence file in the source repository: used locally only, never redistributed.",
        analyses=[
            AnalysisSpec("BPS", MOONLIGHT_WIR / "analysis.txt",
                         "Tsung-Ping Chen & Li Su (BPS-FH, 2018)", "expert",
                         "When in Rome (Gotham et al.): converted and proof-read by Mark Gotham",
                         "CC BY-SA 4.0 (When in Rome); original BPS-FH data per its authors"),
            AnalysisSpec("DT", MOONLIGHT_WIR / "analysis_DT.txt",
                         "Dmitri Tymoczko", "expert",
                         "When in Rome (Gotham et al.)", "CC BY-SA 4.0 (When in Rome)"),
        ],
        tracks=[
            TrackSpec("melody", "Melody", "Upper staff, notes longer than a triplet eighth",
                      lambda n: n.staff == 1 and n.duration != Fraction(1, 3)),
            TrackSpec("triplets", "Triplets", "Upper staff, triplet eighths",
                      lambda n: n.staff == 1 and n.duration == Fraction(1, 3)),
            TrackSpec("bass", "Bass", "Lower staff", lambda n: n.staff == 2),
        ],
        known_discrepancy_measures={60, 61, 63, 65, 66},
        known_discrepancy_note=(
            "Every discrepancy starts at a left-hand spine split (`*^`, source lines 862–863, 909, 940, 956). "
            "There music21's Humdrum importer drops sub-spines (m. 65: no left-hand notes at all; the source "
            "has G♯2, G♯1, B♯3, G♯2, G♯2) and shifts the whole-note bass of mm. 60–61 by a measure (B♯1/C♯2 "
            "swapped). Verovio (humlib) matches the source in every checked case; the core follows Verovio."
        ),
        reference_notes=EXT / "dcml_beethoven" / "notes" / "14-1.notes.tsv",
        reference_note=(
            "Compared with DCML's independent edition: 1,181 of 1,182 noteheads agree. The one difference is "
            "m. 48, beat 1: B3 here, A3 in DCML. Both analyses read I (E major) there, which favours B, but "
            "only an urtext scan can settle it."
        ),
    ),
    "bach-prelude-c": PieceSpec(
        id="bach-prelude-c",
        title="Prelude in C major",
        subtitle="The Well-Tempered Clavier I · BWV 846",
        composer="Johann Sebastian Bach",
        tempo_qpm=66,
        score=EXT / "asap_bwv846" / "xml_score.musicxml",
        score_source="(n)ASAP dataset (Foscarin et al. 2020; Peter et al. 2023), Bach/Prelude/bwv_846. github.com/CPJKU/asap-dataset",
        score_licence="CC BY-NC-SA 4.0",
        analyses=[
            AnalysisSpec("WiR", BWV846_WIR / "analysis.txt", "Mark Gotham et al.", "expert",
                         "When in Rome: \"manually, through judicious automation, and in collaboration with colleagues and students\"",
                         "CC BY-SA 4.0"),
            AnalysisSpec("AugNet", BWV846_WIR / "analysis_automatic.rntxt", "AugmentedNet v1.9.1 (automatic)",
                         "automatic", "When in Rome; model by Nápoles López et al. (ISMIR 2021)", "CC BY-SA 4.0"),
        ],
        tracks=[
            TrackSpec("figuration", "Figuration", "Upper staff", lambda n: n.staff == 1),
            TrackSpec("inner", "Inner voice", "Lower staff, notes shorter than a half note",
                      lambda n: n.staff == 2 and n.duration < 2),
            TrackSpec("bass", "Bass", "Lower staff, half notes and longer", lambda n: n.staff == 2 and n.duration >= 2),
        ],
    ),
    "clair-de-lune": PieceSpec(
        id="clair-de-lune",
        title="Clair de lune",
        subtitle="Suite bergamasque, L. 75 · III",
        composer="Claude Debussy",
        tempo_qpm=63,
        score=EXT / "converted" / "l075-03_suite_clair.musicxml",
        score_source="DCML Debussy Suite bergamasque corpus (MuseScore 3), converted to MusicXML with MuseScore. github.com/DCMLab/debussy_suite_bergamasque",
        score_licence="CC BY-NC-SA 4.0",
        analyses=[
            AnalysisSpec("DCML", EXT / "dcml_debussy_bergamasque" / "harmonies" / "l075-03_suite_clair.harmonies.tsv",
                         "DCML annotators (Hentschel, Rammos, Neuwirth, Rohrmeier et al.)", "expert",
                         "DCML Distant Listening Corpus", "CC BY-NC-SA 4.0", format="dcml"),
        ],
        tracks=[
            TrackSpec("upper", "Right hand", "Upper staff", lambda n: n.staff == 1),
            TrackSpec("lower", "Left hand", "Lower staff", lambda n: n.staff == 2),
        ],
        requires="Needs MuseScore to convert the DCML file: see docs/mac-setup.md (`python -m ppe convert`).",
        reference_notes=EXT / "dcml_debussy_bergamasque" / "notes" / "l075-03_suite_clair.notes.tsv",
        reference_required=True,
        reference_note="The converted MusicXML must match DCML's note table (the score the labels were written on).",
    ),
}


def available() -> list[str]:
    return [pid for pid, s in SPECS.items() if s.score.exists() and all(a.path.exists() for a in s.analyses)]


def build_piece(pid: str) -> Piece:
    spec = SPECS[pid]
    mei = load_mei(spec.score)
    measures, notes, mei_report = mei_to_core(mei)
    notes = [replace(n, track=next((t.id for t in spec.tracks if t.test(n)), "other")) for n in notes]
    tracks = [Track(t.id, t.name, t.rule, sum(1 for n in notes if n.track == t.id)) for t in spec.tracks]
    piece = Piece(
        id=pid, title=spec.title, subtitle=spec.subtitle, composer=spec.composer, tempo_qpm=spec.tempo_qpm,
        measures=measures, notes=notes, analyses=[], tracks=tracks,
        score_source=spec.score_source, score_licence=spec.score_licence, mei=mei,
    )
    for a in spec.analyses:
        colour = COLOURS.get(a.id, "#444")
        if a.format == "dcml":
            an = import_dcml(a.path, piece, aid=a.id, analyst=a.analyst, source=a.source, licence=a.licence, colour=colour)
        else:
            an = import_romantext(a.path, piece, aid=a.id, analyst=a.analyst, kind=a.kind, source=a.source,
                                  licence=a.licence, colour=colour)
        piece.analyses.append(an)

    xcheck = crosscheck_music21(notes, spec.score)
    unexplained = [d for d in xcheck["only_in_core"] + xcheck["only_in_music21"]
                   if int(d.split()[0][1:]) not in spec.known_discrepancy_measures]
    reference = None
    if spec.reference_notes is not None and spec.reference_notes.exists():
        reference = crosscheck_reference_notes(notes, spec.reference_notes)
        reference["note"] = spec.reference_note
        reference["required"] = spec.reference_required
    piece.validation = {
        "mei": mei_report,
        "crosscheck": xcheck,
        "unexplained_discrepancies": unexplained,
        "known_discrepancy_note": spec.known_discrepancy_note,
        "reference": reference,
        "analysis_issues": {an.id: an.issues for an in piece.analyses},
        "alignment": {an.id: alignment_check(piece, an.id) for an in piece.analyses},
    }
    if reference and spec.reference_required and reference["agreement_rate"] < 0.99:
        raise RuntimeError(f"{pid}: score differs from the annotated reference: {reference['only_in_core'][:5]} / {reference['only_in_reference'][:5]}")
    if unexplained:
        raise RuntimeError(f"{pid}: core and music21 disagree outside documented measures: {unexplained[:10]}")
    if mei_report["verovio_midi_vs_mei_pitch_mismatches"]:
        raise RuntimeError(f"{pid}: Verovio MIDI and MEI pitches disagree: {mei_report['verovio_midi_vs_mei_pitch_mismatches'][:5]}")
    return piece


def alignment_check(piece: Piece, aid: str) -> dict:
    """Is the analysis aligned to the right place? Fraction of note attacks that are chord tones of
    the active label, at the actual alignment and with the labels shifted by ±1 beat and ±1 measure.
    A correct alignment should score clearly highest at shift 0."""
    from ppe.compare import chord_tone_status

    an = piece.analysis(aid)
    beat = piece.measures[0].beat
    bar = piece.measures[0].duration
    out = {}
    for name, shift in [("-1 measure", -bar), ("-1 beat", -beat), ("0", Fraction(0)), ("+1 beat", beat), ("+1 measure", bar)]:
        hits = total = 0
        for n in piece.notes:
            if not n.is_attack:
                continue
            lab = an.label_at(n.onset - shift)
            st = chord_tone_status(n, lab)
            if st is None:
                continue
            total += 1
            hits += st in ("chord", "accounted")
        out[name] = round(hits / total, 4) if total else None
    out["best_is_zero"] = out["0"] == max(v for k, v in out.items() if v is not None and k != "best_is_zero")
    return out


def pack_dir(pid: str) -> Path:
    return PACKS / pid


def save(piece: Piece) -> None:
    d = pack_dir(piece.id)
    d.mkdir(parents=True, exist_ok=True)
    with open(d / "piece.pkl", "wb") as fh:
        pickle.dump(piece, fh)
    (d / "validation.json").write_text(json.dumps(piece.validation, indent=2, default=str), encoding="utf-8")


def load(pid: str) -> Piece:
    with open(pack_dir(pid) / "piece.pkl", "rb") as fh:
        return pickle.load(fh)


def built() -> list[str]:
    return [pid for pid in SPECS if (pack_dir(pid) / "piece.pkl").exists()]
