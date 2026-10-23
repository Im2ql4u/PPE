"""Selections: chord naming only for genuine chords; transposed descriptions keep relations."""

import pytest

from ppe.selection import chord_identity, inspect


@pytest.mark.parametrize("names,expected", [
    (["C4", "E4", "G4"], ("C", "C")),
    (["E3", "G3", "C4"], ("C", "E")),  # first inversion: root C, bass E
    (["G3", "B3", "D4", "F4"], ("G", "G")),
    (["F##3", "A#3", "C#4", "E4"], ("F𝄪", "F𝄪")),
    (["G2", "B3", "D4", "F4", "A-4"], ("G", "G")),
])
def test_chords_are_named(names, expected):
    c = chord_identity(names)
    assert c is not None and (c["root"], c["bass"]) == expected


@pytest.mark.parametrize("names", [
    ["A3", "B#3", "C#4", "D4", "F#4"],  # a passage's pitch collection, not a chord (music21 calls it a "pentacluster")
    ["C4", "D4", "E4"],
    ["C4", "E4"],  # two notes: an interval
])
def test_non_chords_are_not_named(names):
    assert chord_identity(names) is None


def test_transposed_description_changes_names_not_relations(moonlight):
    m16 = moonlight.measure(16)
    a = inspect(moonlight, start=m16.onset, end=m16.end)
    b = inspect(moonlight, start=m16.onset, end=m16.end, transpose=2)
    ra = {l["analysis"]: l for l in a["lenses"]}
    rb = {l["analysis"]: l for l in b["lenses"]}
    bps_a, bps_b = ra["BPS"]["readings"][0], rb["BPS"]["readings"][0]
    assert bps_a["figure"] == bps_b["figure"] == "N6"
    assert bps_a["key"]["label"] == "B minor" and bps_b["key"]["label"] == "C♯ minor"
    assert bps_b["pitches"] == ["D", "F♯", "A"]
    assert [s["degree"] for s in ra["BPS"]["statuses"]] == [s["degree"] for s in rb["BPS"]["statuses"]]
    assert [s["role"] for s in ra["DT"]["statuses"]] == [s["role"] for s in rb["DT"]["statuses"]]
