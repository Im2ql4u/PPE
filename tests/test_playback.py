"""Playback equals notation; reductions and transformations keep their promises."""

from collections import Counter
from fractions import Fraction

from ppe.compare import chord_tone_status
from ppe.playback import build
from ppe.score_import import sounding_notes
from ppe.transform import candidates, minimal_voice_leading


def test_original_playback_equals_the_notation(moonlight, bach):
    for p in (moonlight, bach):
        ev, _ = build(p, start=Fraction(0), end=p.end, mode="original")
        written = Counter((first.onset, first.midi) for first, _, _ in sounding_notes(p.notes))
        played = Counter((e.onset, e.midi) for e in ev)
        assert played == written
        assert all(e.duration > 0 for e in ev)


def test_ties_are_merged_into_one_sounding_note(moonlight):
    chains = [s for s in sounding_notes(moonlight.notes) if len(s[2]) > 1]
    assert chains, "Moonlight has tied notes"
    first, dur, ids = chains[0]
    assert dur == sum(moonlight.notes_by_id()[i].duration for i in ids)


def test_playback_respects_accidentals(moonlight):
    ev, _ = build(moonlight, start=Fraction(0), end=Fraction(4), mode="original")
    top = sorted({e.midi for e in ev if e.midi > 50})
    assert top == [56, 61, 64]  # G#3, C#4, E4 (not G, C, E)


def test_transposition_shifts_every_pitch(moonlight):
    a, _ = build(moonlight, start=Fraction(0), end=Fraction(16), mode="original")
    b, _ = build(moonlight, start=Fraction(0), end=Fraction(16), mode="original", transpose=-2)
    assert [x.midi - 2 for x in a] == [y.midi for y in b]


def test_blocked_chords_keep_pitch_content_per_beat(moonlight):
    span = (Fraction(0), Fraction(16))
    orig, _ = build(moonlight, start=span[0], end=span[1], mode="blocked")
    src, _ = build(moonlight, start=span[0], end=span[1], mode="original")
    for beat in range(8):
        t0, t1 = Fraction(2 * beat), Fraction(2 * beat + 2)
        assert {e.midi for e in orig if t0 <= e.onset < t1} == {e.midi for e in src if t0 <= e.onset < t1}


def test_chord_tone_reduction_only_keeps_chord_tones(moonlight):
    ev, _ = build(moonlight, start=Fraction(0), end=moonlight.end, mode="chord_tones", analysis="DT")
    by_id = moonlight.notes_by_id()
    dt = moonlight.analysis("DT")
    for e in ev:
        n = by_id[e.ids[0]]
        assert chord_tone_status(n, dt.label_at(n.onset)) in ("chord", "accounted")


def test_outer_voices_are_extremes(bach):
    ev, _ = build(bach, start=Fraction(0), end=Fraction(4), mode="outer")
    src, _ = build(bach, start=Fraction(0), end=Fraction(4), mode="original")
    assert {e.midi for e in ev} <= {e.midi for e in src}
    assert max(e.midi for e in ev) == max(e.midi for e in src)
    assert min(e.midi for e in ev) == min(e.midi for e in src)


def test_progression_realises_each_label(moonlight):
    ev, _ = build(moonlight, start=Fraction(0), end=Fraction(16), mode="progression", analysis="BPS")
    bps = moonlight.analysis("BPS")
    for lab in bps.labels[:5]:
        sounding = {e.midi % 12 for e in ev if e.onset == lab.onset}
        assert sounding == set(lab.pcs)


def test_substitution_moves_chord_tones_by_role(moonlight):
    bps = moonlight.analysis("BPS")
    n6 = bps.label_at(moonlight.measure(3).onset + 2)  # N6 = D-F#-A in C# minor
    iv = next(c for c in candidates(n6) if c["figure"] == "iv")  # F#-A-C#
    ev, info = build(moonlight, start=n6.onset, end=n6.end, mode="original", substitution=(n6, iv["pitches"]))
    assert info["moves"], "some notes must move"
    by_id = moonlight.notes_by_id()
    for e in ev:
        n = by_id[e.ids[0]]
        if chord_tone_status(n, n6) == "chord":
            assert e.midi % 12 in {6, 9, 1}
            assert abs(e.midi - n.midi) <= 6


def test_candidates_are_ranked_by_voice_leading(moonlight):
    n6 = moonlight.analysis("BPS").label_at(moonlight.measure(3).onset + 2)
    c = candidates(n6)
    assert [x["distance"] for x in c] == sorted(x["distance"] for x in c)
    assert all(frozenset(x["pitches"]) for x in c)


def test_pedal_sustains_within_the_harmony_only(moonlight):
    dry, _ = build(moonlight, start=Fraction(0), end=Fraction(16), mode="original")
    wet, info = build(moonlight, start=Fraction(0), end=Fraction(16), mode="original", analysis="BPS", pedal=True)
    assert "pedal" in info
    bps = moonlight.analysis("BPS")
    for d, w in zip(dry, wet):
        assert (d.onset, d.midi) == (w.onset, w.midi) and w.duration >= d.duration
        lab = bps.label_at(w.onset)
        assert w.onset + w.duration <= lab.end  # never carried into the next harmony
    # the first triplet note G#3 now rings to the next G#3 attack, a triplet later
    first = next(w for w in wet if w.midi == 56)
    assert first.duration == 1


def test_minimal_voice_leading():
    total, moves = minimal_voice_leading([7, 11, 2, 5], [0, 4, 7])  # G7 -> C
    assert total == 4  # B->C (+1), D->C (-2), F->E (-1), G=G
