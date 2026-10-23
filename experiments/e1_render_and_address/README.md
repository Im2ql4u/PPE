# E1 (lite): render, address, and colour by expert agreement

**Question.** Can we render a real piano score in Verovio, map every rendered note to a renderer-independent *musical address* (measure, onset, pitch), and attach expert analyses to the notes, reliably?

**Input.** Beethoven op. 27/2 mvt. 1, Craig Sapp's Humdrum edition (`sonata14-1.krn`). Two Roman-numeral analyses from When in Rome: BPS (Chen & Su) and DT (Tymoczko).

**Run.** `uv run python experiments/fetch_data.py && uv run python experiments/e1_render_and_address/render_address.py`. Writes `out/report.json` and `out/moonlight_agreement.html`, the score with noteheads coloured by analyst agreement.

## Results (2026-10-23)

| Check | Result |
|---|---|
| Verovio notes vs. music21 notes (independent parsers, same file) | 1,141 of 1,143 music21 notes get identical (measure, onset, MIDI pitch) addresses. Differences: Verovio lists tie continuations as onsets (41 extra), plus 2 notes in mm. 60–61. **Address mapping works; tie handling must be explicit.** |
| Same input, same ID seed → identical IDs | yes |
| IDs after changing one note's pitch | 1,181/1,182 IDs still point to the same address |
| ID scheme for `**kern` input | IDs encode the **source line and field** (`note-L23F2`). Stable under in-place edits, but **every later ID shifts if a line is inserted**. Confirms that renderer IDs can't be the project's primary key (see `docs/music-theory-engine.md` §4). |
| Chord-tone status of each note under each expert analysis | 1,017 chord tone for both · 54 non-chord tone for both · **85 (7.2%) analysts disagree** · 26 unlabelled. Disputed notes fall in mm. 4, 13, 16, 18, 25, 35–37, 39–40, 47–52, 54, 58. |

> **Correction (implementation, 2026-10-23).** The chord-tone counts above used music21's reading of DT's
> `V9[b9]`, which spells the ninth as A♭ (enharmonically the root) instead of A♮. With correct spelling,
> **77** notes (not 85) change status between the analysts. See `docs/validation.md` §2 and §4.

## Finding: Verovio 6.3.0 regression (silent wrong pitches)

With Verovio **6.3.0** (latest on PyPI and npm, 2026-08-19), `**kern` input loses accidentals implied by the key signature.
Moonlight's opening G♯–C♯–E comes out as **G–C–E** in Verovio's own MIDI output, `getMIDIValuesForElement`, and the exported MEI.
The engraving still looks right. The playback is wrong.

Minimal reproduction (`*k[f#]`, notes `f# f fn c#`):

| Verovio | MIDI pitches | Correct? |
|---|---|---|
| 4.5.1, 5.6.0, 6.0.0, 6.2.0 | 66 65 65 61 | yes |
| **6.3.0** | **65** 65 65 61 | no |

MusicXML input to 6.3.0 is correct. We pin `verovio>=6.2,<6.3` in `pyproject.toml`.
Worth reporting upstream (rism-digital/verovio); not done, since that would be an outward action.

**Lessons for the architecture:**

1. Pitch and time facts must come from the project's own symbolic model (music21/partitura), **not from the renderer**. The renderer only draws, and maps addresses to SVG elements.
2. Golden tests: for every score the app imports, compare renderer-derived pitches against the symbolic model's. A mismatch blocks the import. That test would have caught this in seconds.
3. Pin and test dependency upgrades, even for mature libraries.

## Limits

- One piece, one source format (`**kern`). MusicXML from MuseScore (the DCML scores) is not yet tested in this harness.
- Aligning RomanText to the score assumed 2/2 throughout and no anacrusis (true for this movement). The general case needs the `mc`/`mn` handling in `docs/music-theory-engine.md` §4.
- "Chord tone" here means pitch class ∈ the Roman numeral's pitch classes at that onset. Suspensions, and notes sustained across a chord change, are judged at their onset only.
