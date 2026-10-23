"""Analyses: import, alignment, the bracket fix, comparison definitions, explanations."""

from fractions import Fraction
from pathlib import Path

import pytest
from music21 import key, roman

from ppe.analyses import import_dcml, label_from_rn
from ppe.compare import classify, disputed_notes, segments, summary
from ppe.explain import explain_label
from ppe.model import Key, Label, Measure, Piece
from ppe.pieces import EXT


def _lab(figure, k, measure=1):
    return label_from_rn(roman.RomanNumeral(figure, key.Key(k)), lid="x", analysis_id="a",
                         onset=Fraction(0), end=Fraction(1), measure=measure, beat=Fraction(1))


def test_bracketed_ninths_are_intervals_above_the_root():
    # music21 alone gives A-flat (= the root, enharmonically) for V9[b9] in C# minor
    assert set(_lab("V9[b9]", "c#").pitches) == {"G#", "B#", "D#", "F#", "A"}
    assert set(_lab("V9[b9b5]", "c#").pitches) == {"G#", "B#", "D", "F#", "A"}  # DT: "D7/G#"


def test_alignment_is_best_at_zero_shift(moonlight, bach):
    for p in (moonlight, bach):
        for aid, al in p.validation["alignment"].items():
            assert al["best_is_zero"], (p.id, aid, al)
            assert al["0"] > 0.9


def test_moonlight_analyses_at_hand_checked_places(moonlight):
    bps, dt = moonlight.analysis("BPS"), moonlight.analysis("DT")
    t16 = moonlight.measure(16).onset
    a, b = bps.label_at(t16), dt.label_at(t16)
    assert (a.figure, a.key.tonic, a.key.mode) == ("N6", "B", "minor")
    assert (b.figure, b.key.tonic, b.key.mode) == ("VI", "E", "minor")
    assert set(a.pitches) == set(b.pitches) == {"C", "E", "G"}
    assert any("Ger4/3" in alt for alt in b.alternatives)
    assert {n.measure for n in dt.notes} >= {16, 25, 34, 39}


def test_comparison_classes_on_synthetic_labels():
    assert classify(_lab("V7", "C"), _lab("V7", "C")) == "same"
    assert classify(_lab("V", "C"), _lab("I", "G")) == "key_frame"
    assert classify(_lab("I", "C"), _lab("I6", "C")) == "inversion"
    assert classify(_lab("V7", "c#"), _lab("V9[b9]", "c#")) == "extension"
    assert classify(_lab("I", "C"), _lab("i", "C")) == "other_quality"
    assert classify(_lab("I", "C"), _lab("V", "C")) == "other_chord"


def test_moonlight_comparison_at_hand_checked_bars(moonlight):
    bps, dt = moonlight.analysis("BPS"), moonlight.analysis("DT")
    labs = {l.id: l for l in bps.labels + dt.labels}
    by_start = {s.onset: s for s in segments(moonlight, bps, dt)}
    m = lambda n, beat_q=0: moonlight.measure(n).onset + beat_q  # noqa: E731
    assert by_start[m(16)].cls == "key_frame"  # N6 in b vs VI in e: same C-E-G
    assert by_start[m(32)].cls == "extension"  # V7 vs V9[b9]
    assert by_start[m(4, 1)].cls == "other_chord"  # V7 vs cadential i64
    assert labs[by_start[m(1)].a].figure == "i"


def test_moonlight_agreement_summary_is_consistent(moonlight):
    s = summary(moonlight, moonlight.analysis("BPS"), moonlight.analysis("DT"))
    assert sum(s["fractions"].values()) == pytest.approx(1.0, abs=1e-3)
    # Corrected value (the E1/E2 0.663 was inflated by music21's [b9] reading; see docs/validation.md)
    assert s["strict_agreement"] == pytest.approx(0.6413, abs=2e-3)


def test_disputed_notes_are_where_the_readings_differ(moonlight):
    d = disputed_notes(moonlight, moonlight.analysis("BPS"), moonlight.analysis("DT"))
    measures = {int(x.split(".")[0][1:]) for x in d}
    assert 60 < len(d) < 100
    assert {4, 16, 35, 39} <= measures
    assert not measures & {1, 2, 5}  # the opening is read identically


def test_explanation_names_the_lowered_degree(moonlight):
    n6 = moonlight.analysis("BPS").label_at(moonlight.measure(3).onset + 2)
    assert n6.figure == "N6"
    text = explain_label(n6)["instance"]
    assert "lowered second degree" in text and "D–F♯–A" in text


def test_second_inversion_tonic_is_not_explained_as_home(moonlight):
    lab = moonlight.analysis("BPS").label_at(moonlight.measure(33).onset)
    assert lab.figure == "i64" and lab.family == "tonic six-four"
    assert "not a resting point" in explain_label(lab)["gist"]


def test_dcml_import_keeps_suspended_roots_structural():
    tsv = EXT / "dcml_debussy_bergamasque" / "harmonies" / "l075-03_suite_clair.harmonies.tsv"
    mtsv = EXT / "dcml_debussy_bergamasque" / "measures" / "l075-03_suite_clair.measures.tsv"
    if not tsv.exists():
        pytest.skip("DCML Debussy corpus not fetched")
    import ms3

    mt = ms3.load_tsv(mtsv)
    measures = [Measure(int(r.mn), i, Fraction(str(r.quarterbeats)), Fraction(str(r.duration_qb)), r.timesig,
                        Fraction(3, 2), int(r.keysig)) for i, r in mt.iterrows()]
    piece = Piece("clair", "", "", "", 63, measures, [], [], [], "", "")
    an = import_dcml(tsv, piece, aid="DCML", analyst="", source="", licence="", colour="")
    assert len(an.labels) == 150
    first = an.labels[0]
    assert (first.figure, first.key.tonic, first.key.mode) == ("I6", "D-", "major")
    assert set(first.pitches) == {"D-", "F", "A-"}
    # m15 'ii(2)': the root E-flat is displaced by F, but it is still part of the structural chord
    lab = next(l for l in an.labels if l.measure == 15 and l.raw.startswith("ii(2)"))
    assert "E-" in lab.pitches and lab.pcs == frozenset({3, 6, 10})
