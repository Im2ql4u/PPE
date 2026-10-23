"""The core's notes are correct: pitches (incl. accidentals), timing, render mapping, transposition."""

from collections import Counter
from fractions import Fraction

import verovio

from ppe.mei_import import mei_to_core
from ppe.render import transposed_mei_pitches, transposition_interval


def test_verovio_pinned_below_regression():
    # 6.3.0 drops key-signature accidentals from **kern input (experiments/e1); 6.2.x is correct.
    assert verovio.toolkit().getVersion().startswith("6.2"), verovio.toolkit().getVersion()


def test_kern_key_signature_accidentals_survive_import():
    kern = "**kern\n*k[f#]\n*M4/4\n=1\n4f#\n4f\n4fn\n4c#\n=\n*-\n"
    tk = verovio.toolkit()
    tk.loadData(kern)
    _, notes, report = mei_to_core(tk.getMEI())
    assert [n.midi for n in sorted(notes, key=lambda n: n.onset)] == [66, 65, 65, 61]
    assert report["verovio_midi_vs_mei_pitch_mismatches"] == []


def test_moonlight_opening_is_spelled_and_timed_correctly(moonlight):
    m1 = [n for n in moonlight.notes if n.measure == 1]
    upper = sorted((n for n in m1 if n.staff == 1), key=lambda n: n.onset)[:3]
    assert [n.name for n in upper] == ["G#3", "C#4", "E4"]
    assert [n.offset for n in upper] == [0, Fraction(1, 3), Fraction(2, 3)]
    bass = sorted(n.name for n in m1 if n.staff == 2)
    assert bass == ["C#2", "C#3"]
    assert all(n.duration == 4 for n in m1 if n.staff == 2)


def test_moonlight_core_agrees_with_independent_parser(moonlight):
    x = moonlight.validation["crosscheck"]
    assert x["agreement_rate"] > 0.97
    assert moonlight.validation["unexplained_discrepancies"] == []
    # every disagreement is inside the documented spine-split measures
    measures = {int(d.split()[0][1:]) for d in x["only_in_core"] + x["only_in_music21"]}
    assert measures <= {60, 61, 63, 65, 66}


def test_moonlight_matches_an_independent_edition(moonlight):
    ref = moonlight.validation["reference"]
    assert ref["agreeing"] == ref["reference_notes"] - 1  # one known variant
    assert ref["only_in_core"] == ["m48 +0 midi 59"] and ref["only_in_reference"] == ["m48 +0 midi 57"]


def test_bach_core_agrees_completely(bach):
    assert bach.validation["crosscheck"]["agreement_rate"] == 1.0


def test_every_note_has_a_unique_render_id(moonlight, bach):
    for p in (moonlight, bach):
        rids = [n.render_id for n in p.notes]
        assert all(rids)
        assert len(set(rids)) == len(rids)
        assert len({n.id for n in p.notes}) == len(p.notes)


def test_measures_are_contiguous(moonlight, bach):
    for p in (moonlight, bach):
        for a, b in zip(p.measures, p.measures[1:]):
            assert a.end == b.onset
        assert all(n.onset >= 0 and n.duration > 0 for n in p.notes)


def test_transposition_interval_prefers_simple_key_signatures():
    assert transposition_interval(1, 4) == ("m2", -5)  # C# minor -> D minor, not C## minor
    # C# minor down a semitone is C minor (3 flats) via an augmented unison down, not B# minor (9 sharps)
    assert transposition_interval(-1, 4) == ("-A1", -7)
    assert transposition_interval(0, 4) == ("P1", 0)


def test_rendered_transposition_matches_core_pitches(moonlight):
    for semis in (1, -3, 5):
        interval, _ = transposition_interval(semis, moonlight.measures[0].key_fifths)
        rendered = transposed_mei_pitches(moonlight.mei, interval)
        diffs = Counter(rendered[n.render_id] - n.midi for n in moonlight.notes)
        assert diffs == Counter({semis: len(moonlight.notes)}), (semis, diffs.most_common(3))
