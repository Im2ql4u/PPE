# Validation record

What the app checks, how, and what was found while building milestone 1.
Each check is either run on every build (and shown under *Sources, licences and checks* in the app) or encoded as a test (`tests/`).

Principle: **no single library is trusted as the source of truth.** Facts are derived one way and checked another. Where they disagree, the disagreement is investigated, explained, and either fixed or documented with evidence. A build with an unexplained disagreement fails.

---

## 1. Notes: pitch, time, identity

**Pipeline.** Score file → Verovio (pinned 6.2.x) → MEI with stable IDs → core notes, using onsets and ends from Verovio's timemap and pitch, spelling, voice and ties from the MEI. Each note is addressed by `(measure, offset, staff, voice, MIDI pitch)`. Renderer IDs are attached, never used as identity.

**Cross-check against an independent parser (music21), every build:**

| Piece | Agreement | Discrepancies | Explanation |
|---|---|---|---|
| Moonlight (Sapp `**kern`) | 1,155 of 1,182 (97.7%) | 29, all in mm. 60, 61, 63, 65, 66 | **music21 bug.** Each region starts at a left-hand spine split (`*^`, source lines 862–863, 909, 940, 956). music21's Humdrum importer drops sub-spines there (m. 65: *no* left-hand notes; the source has G♯2, G♯1, B♯3, G♯2, G♯2) and shifts the whole-note bass of mm. 60–61 by a measure. Checked against the source text: the core is right. |
| Bach BWV 846 (ASAP MusicXML) | 619 of 619 (100%) | 8 notes differ in *staff* only (m. 33) | Cross-staff writing: the parsers assign the notes to different staves. Pitch and time agree. |

**Second edition (informational for Moonlight, required for Clair de lune):**
Moonlight's core (Sapp, after Durand/Dukas) vs DCML's independent encoding: **1,181 of 1,182 noteheads agree.** The single difference is m. 48 beat 1, B3 (Sapp) vs A3 (DCML). Both analyses read I in E major there, which favours B, but this is **open** until checked against an urtext scan.
For *Clair de lune*, the converted MusicXML must match DCML's note table (≥ 99%), or the build fails. This guarantees the labels sit on the notes the analysts annotated.

**Verovio's own MIDI vs the MEI pitches:** 0 mismatches (checked every build).

## 2. Library defects found (and what we do about them)

| Defect | Effect | Evidence | Handling |
|---|---|---|---|
| **Verovio 6.3.0**: key-signature-implied accidentals dropped on `**kern` import | Moonlight's G♯–C♯–E plays as G–C–E; the engraving still looks right | Minimal case `*k[f#] f#` → MIDI 65 in 6.3.0, 66 in 4.5.1–6.2.0 (experiment E1) | Pinned `verovio>=6.2,<6.3`; `test_verovio_pinned_below_regression`, `test_kern_key_signature_accidentals_survive_import` |
| **Verovio in worker threads** cannot find its fonts unless the resource path is set | Renders nothing (silently) in the web server | Reproduced through FastAPI's thread pool | Resource path set explicitly for every toolkit (`ppe/render.py`) |
| **music21 Humdrum importer**: spine splits | Notes dropped and shifted (see §1) | Source lines quoted above | Core built from Verovio's MEI; music21 used only as the cross-check |
| **music21 RomanText**: bracketed alterations applied to the *diatonic* step | `V9[b9]` in C♯ minor gets A♭ (enharmonically the root) instead of A♮; `V9[b9b5]` becomes a garbled four-note chord | `roman.RomanNumeral("V9[b9]", "c#").pitches` | Figures re-parsed: base figure via music21, alterations applied as intervals above the root; every reinterpretation is logged as a data note (`test_bracketed_ninths_are_intervals_above_the_root`) |
| **music21 `isSeventh`/`isNinth`** accept diminished thirds as thirds | A bar of passing notes was named "A♯ diminished pentacluster" | `Chord(["A3","B#3","C#4","D4","F#4"]).isNinth()` is True | Own stacked-thirds test (`is_stacked_thirds`); chords named only when every step is a major or minor third |
| **DCML `chord_tones`** omit a root displaced by a suspension (`ii(2)`) although it sounds | The sustained bass would count as "not in the chord" | *Clair de lune* m. 15 (experiment E3) | Structural chord computed from root + chord type; named suspensions and added notes are kept separately |
| **Source typo** in When in Rome's BWV 846 analysis: `viio64b3` (missing space) | music21 reads an unintended chord | — | Flagged as a data note on the lens; not silently corrected |

## 3. Analyses: alignment

Analyses are aligned by **(printed measure number, offset within the measure)**, never by absolute time: files encode upbeats differently (experiment E2's first run produced false disagreement this way).
Labels persist until the next label (RomanText convention).

**Self-check on every build.** The fraction of note attacks that are chord tones of the active label is computed at the actual alignment and with the labels shifted by ±1 beat and ±1 measure. A correct alignment must score highest at zero shift:

| Analysis | At alignment | ±1 beat | ±1 measure |
|---|---|---|---|
| Moonlight, BPS (Chen & Su) | **94.9%** | 58.7% / 52.6% | 44.9% / 42.4% |
| Moonlight, DT (Tymoczko) | **92.2%** | 58.7% / 51.7% | 44.8% / 42.9% |
| BWV 846, WiR (Gotham et al.) | **96.9%** | 85.1% / 84.6% | 47.4% / 44.8% |
| BWV 846, AugmentedNet (automatic) | **92.2%** | 81.4% / 80.4% | 46.0% / 42.0% |

(BWV 846 changes harmony once per bar, so a one-beat shift still lands mostly in the same chord; zero shift is still clearly best.)

Hand-checked placements (tests): Moonlight m. 16, BPS = N⁶ in B minor, DT = VI in E minor, both C–E–G; DT's variants (VImaj7, Ger⁴₃) and notes (mm. 16, 25, 34, 39) attached to the right measures.

## 4. Comparing analyses: definitions

For each maximal span where neither analysis changes label (time-weighted, in quarter notes):

| Class | Definition |
|---|---|
| `same` | same key (tonic pitch class and mode), same chord pitch classes, same bass |
| `key_frame` | same chord pitch classes, **different key** (bass may differ) |
| `inversion` | same chord and key, different bass |
| `extension` | one chord's pitch classes are a strict subset of the other's |
| `other_quality` | same root, otherwise different |
| `other_chord` | anything else |

Key takes precedence over bass because a figure's implied bass is often notational convention. At Moonlight m. 16 the actual bass is a B pedal that neither N⁶ nor VI describes; what differs is the key frame.
Boundaries where only one analysis changes label are counted separately (granularity).

**A note's chord-tone status** under an analysis: its pitch class is in the active label's chord (or in its named suspensions or added notes), judged at the note's onset.

### Corrected figures

The bracket defect above inflated two numbers reported during research. With `V9[b9]` read as A♭, BPS's `V7` and DT's `V9[b9]` had identical pitch-class sets, so they counted as agreement.

| Quantity | Reported in research (E1/E2) | Corrected |
|---|---|---|
| Moonlight strict agreement BPS vs DT | 0.663 (E2, first run) | **0.641** (app definition); 0.625 in E2's re-run |
| Moonlight notes whose chord-tone status depends on the analyst | 85 | **77** |
| Corpus-wide strict agreement (E2, 329 pairs) | 0.79 | 0.79 (Corelli 0.64 → 0.67, Chopin 0.53 → 0.54) |

The remaining 0.641 vs 0.625 difference is definitional: E2 used music21's label durations, which leave bars without a label line (BPS has none for mm. 29 and 31) unlabelled. The app applies the RomanText convention that a label persists until the next one.

Moonlight, BPS vs DT, time fractions: same 64.1% · key frame 14.9% · extension 11.6% · other chord 6.9% · other quality 1.5% · inversion 1.1%. Ten label boundaries exist only in DT, two only in BPS.

## 5. Playback

- **Playback equals notation**: for both pieces, the multiset of (onset, MIDI pitch) played in "As written" mode equals the notated sounding notes with ties merged (`test_original_playback_equals_the_notation`). Accidentals are checked explicitly (Moonlight's opening plays G♯3–C♯4–E4).
- **Transposition**: playback shifts every pitch by exactly n; the *rendered* score's pitches (Verovio's transposition) equal core pitch + n for every note (tested for +1, −3, +5). The interval spelling is chosen for the simplest key signature (C♯ minor −1 → C minor via an augmented unison down, not B♯ minor).
- **Pedal** (optional): notes sustain to the end of their harmony in the chosen analysis, or until the same key is struck again; never into the next harmony (`test_pedal_sustains_within_the_harmony_only`). This is a simulation, labelled as such. The score's own pedal marks are not used.

## 6. Reductions: what each one claims

| Mode | Depends on an analysis? | Claim | Tested invariant |
|---|---|---|---|
| Blocked chords | no | the notes of each beat, sounded together | same pitch set per beat as the original |
| Outer voices / top line / bass line | no | highest and lowest note at each moment | subset of the original; extremes preserved |
| Chord tones only | **yes** | notes the analyst's labels account for | every kept note is a chord tone of its label |
| The analyst's chords | **yes** | a realisation of the labels, not of the score | each block chord has exactly the label's pitch classes |

The UI states for each mode whether it depends on an analysis. None is presented as "the essence" of the passage.

## 7. Explanations

Generated deterministically from label data (no language model). Every sentence's facts come from the label: key, figure, chord tones, root, bass, inversion, next label. The general paragraphs are fixed texts per chord family. Fixes from review: degrees now name alterations ("on the *lowered* second degree" for N⁶), and a tonic in second inversion is no longer explained as "Home" (`tonic six-four` family).

## 8. Known limitations (honest list)

- One edition per piece. Fingerings, pedal marks and dynamics are displayed (engraved) but not analysed.
- Grace notes are not part of the core (none in the current pieces; Clair de lune to be checked on the Mac).
- Repeats are not expanded (none in the current pieces).
- Track definitions (Melody/Triplets/Bass) are curated rules per piece, shown on hover.
- Substitution alternatives are rule-based candidates in the label's key, ranked by voice-leading distance; they are not stylistic judgements.
- The m. 48 edition variant (B3 vs A3) is unresolved.
