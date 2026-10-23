# Ecosystem research

Survey of existing software, data and research relevant to the project.
Organised by the categories in the original brief (A–G). Sections are filled in over several sessions; see `research-plan.md`.

Evidence tags: **[confirmed]** checked in a primary source (repository, registry, manual, paper) on the date given · **[reported]** credible secondary source or prior knowledge, not re-checked · **[speculative]** our inference.
Reference keys like [R12] point to `references.md`.

| Section | Status |
|---|---|
| A. Interactive sheet music | Session 1 (2026-10-23) |
| B. Score ingestion and sources | Session 1 |
| C. Symbolic analysis: libraries, models, **annotated corpora** | Session 1 |
| D. Piano input and performance capture | Session 2. Hardware facts already in `hardware.md` |
| E. Score following and alignment | Session 2 |
| F. Score-aware tutor | Session 5 |
| G. Products and prior art | Session 4 |

---

## The most important finding of Session 1

**Expert harmonic analyses already exist for both pieces the user plays.** They are machine-readable and aligned to measures and beats.

| Piece | Score source | Expert analysis | Notes |
|---|---|---|---|
| Beethoven, Sonata op. 27 no. 2, mvt. 1 ("Moonlight") | DCML `beethoven_piano_sonatas`, file `14-1` (MuseScore 3.6.2, no harmony labels) [confirmed, R10] | **Two independent analyses** in *When in Rome*: Chen & Su (BPS-FH, ISMIR 2018) and "DT" (most likely Dmitri Tymoczko; to verify). RomanText format, addressed by measure and beat [confirmed, R12] | The two analyses **disagree in instructive places** (see `music-theory-engine.md` §3). |
| Debussy, *Suite bergamasque* no. 3, *Clair de lune* | DCML `debussy_suite_bergamasque`, file `l075-03_suite_clair` (MuseScore 3.6.2) [confirmed, R11] | DCML standard v2.3.0, **150 labels over 72 bars**, inside the score file, plus extracted TSV. Includes local key, chord tones, suspensions, cadences (e.g. IAC at m. 9) and phrase boundaries `{ }` [confirmed, R11] | Annotated and reviewed by DCML staff. |

Consequences:

1. The first useful version of the app does **not depend on automatic harmonic analysis**, which is still unreliable (§C.3).
   It can present expert analyses, and where experts disagree, show both.
2. The data is licensed **CC BY-NC-SA 4.0** (DCML) and **CC BY-SA 4.0 or per source** (When in Rome).
   That is fine for a personal, non-commercial tool.
   It would constrain any later public distribution of the data.
3. Larger corpora in the same formats (DCML's Distant Listening Corpus, When in Rome's roughly 2,000 analyses) cover much of the repertoire the user is likely to play next.
   Examples: Bach's *WTC I* preludes (complete in When in Rome), Chopin mazurkas, Mozart sonatas, Schumann, and Beethoven sonatas (DCML covers 28 sonatas with movements, but some have no labels yet).
   Next step: check coverage against a realistic two-year repertoire list (Session 6).

---

## A. Interactive sheet music

### Candidates (versions checked 2026-10-23 via npm and PyPI) [confirmed unless marked]

| Library | Version, date | Licence | Input | How it maps clicks and time to notes | Notes |
|---|---|---|---|---|---|
| **Verovio** (RISM Digital) | 6.3.0, 2026-08-19 (npm + PyPI) | LGPL-3.0-or-later | MEI (native), MusicXML (incl. compressed), Humdrum `**kern`, ABC, PAE | Every SVG element carries an ID from the MEI tree. `getElementsAtTime(ms)`, `getTimesForElement(id)` (score onset/offset *and* ms), `getMIDIValuesForElement`, `renderToTimemap`, `getPageWithElement`, `renderToExpansionMap` + `getExpansionIdsForElement` / `getNotatedIdForElement` for repeats. `select({measureRange})` renders excerpts. `ResetXmlIdSeed` makes generated IDs reproducible. [R1, R2] | C++ compiled to WebAssembly, the same engine in browser and Python. Used by the 2026 interactive-analysis research interface [R16]. Has an experimental editor API, which we shouldn't rely on. |
| **OpenSheetMusicDisplay (OSMD)** | 2.2.1, 2026-10-12 | BSD-3-Clause | MusicXML only (incl. `.mxl`) | Geometric: `GraphicSheet.GetNearestNote(point)`, `GetNearestVoiceEntry`, `tryGetTimestampFromPosition`, `domToSvg`. `GraphicalNote.setColor()`, `setVisible()`. Built-in `Cursor` steps through the score. [R3] | Renders through VexFlow. MusicXML-native, so less conversion. Polished default look. Audio playback is a separate sponsor-only product [reported]. |
| VexFlow | 5.0.0, 2025-03-05 | MIT | Programmatic API, no file import | Manual | A low-level engraving toolkit. Only relevant for drawing small custom snippets, e.g. a chord in a tooltip. |
| abcjs | 6.7.2, 2026-10-16 | MIT | ABC notation | Click callbacks built in | Excellent for **small generated exercises** (scales, voicings, reductions). Not suited to full piano scores. |
| MuseScore 4 | desktop app | GPL-3.0 | everything | n/a | The **editor** of choice. Opens the DCML `.mscx` files. Command-line conversion to MusicXML. Not embeddable. |
| LilyPond | desktop | GPL-3.0 | `.ly` | n/a | Best typographic quality, batch only. Not interactive. Not needed. |

### Assessment

- Both Verovio and OSMD can support "click any note, chord or measure and inspect it".
  They differ in *how* the link between graphics and music is kept:
  - Verovio keeps a **document model with IDs** (MEI) and exposes time and ID queries.
    This suits a system where analysis, performance data and annotations all point at musical objects.
  - OSMD keeps a **graphical model** that you query by position.
    Linking it back to external data (e.g. a DCML note row) needs our own mapping by measure, onset, staff and pitch.
- **Leaning: Verovio** [speculative, to test in experiment E1].
  Reasons: native MEI with stable IDs, time maps, repeat expansion, Humdrum import (for Craig Sapp's Beethoven edition), the same toolkit in Python for server-side work, and adoption by current MIR research tools.
  Risks: LGPL (fine for local use), and engraving quality on dense piano textures is unverified.
- **Whatever the renderer, renderer IDs must not be the primary key of musical objects.**
  IDs generated at import change when the source file is re-exported from MuseScore.
  The project needs its own **musical address** (measure count, onset as a rational number, staff, voice, pitch) with renderer IDs as a derived, per-render mapping.
  See `music-theory-engine.md` §4. This is the central data-model decision.
- **Don't build an editor.** Corrections to scores happen in MuseScore 4. The app re-imports.

### Experiment E1 (Session 8): renderer bake-off

Render Moonlight mvt. 1 (from DCML `14-1.mscx` → MusicXML via MuseScore 4 CLI) and *Clair de lune* in both Verovio and OSMD.
Evaluate:

1. Visual fidelity: triplets against dotted rhythms, three voices in the right hand of Moonlight, 9/8 cross-staff writing in *Clair de lune*.
2. Click → (measure, onset, staff, pitch) correctness for 20 hand-picked notes.
3. Highlighting from a time position.
4. Load and render time.
5. Effort to colour noteheads by an analysis layer (chord tone vs. non-chord tone).

Acceptance: one renderer passes all five on both pieces.

---

## B. Score ingestion and sources

### Formats

| Format | Role in this project |
|---|---|
| MusicXML 4.0 (`.musicxml`, `.mxl`) | Main interchange format. Every editor exports it. |
| MEI 5 | Candidate internal score format if Verovio is chosen. Richest model for IDs and editorial markup. |
| MuseScore `.mscx` / `.mscz` | Format of the DCML corpora. Convert with the MuseScore CLI (`MuseScore4.exe -o out.mxl in.mscx`) [reported] or read with `ms3`. Note: DCML files are MuseScore **3.6.2**. MuseScore 4 renders them but can't save back in that format [confirmed, R10]. |
| Humdrum `**kern` | Craig Sapp's Beethoven sonatas edition (Durand 1915, ed. Dukas) [confirmed, R14]. **No licence file**, so private use only. Verovio reads it. |
| MIDI | Performance data, and scores where nothing better exists. Lacks spelling, voices and notation, so it is a poor score format. |
| PDF / scans | Human reference only, unless converted by OMR. |

### Where scores come from

| Source | What | Licence | Use |
|---|---|---|---|
| DCML corpora (GitHub, Zenodo) [R10, R11, R13] | MuseScore scores with harmony annotations: Beethoven sonatas, Mozart sonatas, Chopin, Debussy, Schumann, Liszt, Grieg, Dvořák, Tchaikovsky and more (the "Distant Listening Corpus") | CC BY-NC-SA 4.0 | **Primary source** where coverage exists. |
| When in Rome [R12] | About 2,000 Roman-numeral analyses of about 1,500 works. Scores included for some, linked for others. | CC BY-SA 4.0 for new material, original licence otherwise | **Primary analysis source** (RomanText). |
| (n)ASAP [R15] | 222 MusicXML scores aligned to 1,067 MIDI performances (from MAESTRO), with beat and note alignments. v2.1, May 2025. | CC BY-NC-SA 4.0 | Performance comparison and alignment testing. **Includes Moonlight mvt. 3 (`14-3`) but not mvt. 1** [confirmed]. |
| OpenScore (MuseScore + IMSLP) [R17] | Volunteer transcriptions of public-domain scores | CC0 | Clean scores where available. Coverage of piano repertoire is uneven [reported]. |
| MuseScore.com community scores | Very large, variable quality | Per uploader and site terms | Personal use. Quality varies, so check against an urtext PDF. |
| IMSLP | PDFs of public-domain editions | Public domain in most jurisdictions | Reference images, and OMR input. |

### Optical music recognition (OMR)

- **Audiveris** 5.10.2 (2026-03-27) [reported, R18]: classical, rule-based plus neural recognition, with a correction editor.
  The project itself says "a 100% recognition ratio is simply out of reach in many cases".
  We found no piano-specific benchmark. Licence AGPL-3.0 [reported].
- **Sheet Music Transformer++** (Ríos-Vila et al., v4 June 2025) [R19]: end-to-end full-page *pianoform* OMR, a research model.
  **Legato** (ICLR 2026, reported) [R20]: a large pretrained full-page OMR model producing ABC. Not verified.
- **Assessment:** OMR is a **postponed, low-priority** capability for this project.
  For a single user learning a few pieces a year, the realistic path is: find an existing MusicXML (DCML, OpenScore, MuseScore.com) → proofread against an urtext PDF in MuseScore.
  Fallback: run Audiveris → correct in MuseScore.
  Every pathway ends in human correction. Building OMR into the app adds little.
- **The PDF should stay visible.** A side-by-side "engraved original" view is cheap to add and helps the user trust the transcription.

---

## C. Symbolic analysis

### C.1 Libraries (versions checked 2026-10-23)

| Library | Version | Licence | Language | What it is good for |
|---|---|---|---|---|
| **music21** | 10.5.1 (2026-10-22), Python ≥ 3.11 | BSD-3 [confirmed via source header] | Python | Broadest toolkit: parsing MusicXML, MEI, kern, ABC, RomanText. `RomanNumeral` objects, `romanNumeralFromChord(chord, key)`, key-finding (Krumhansl and variants), chordify, voice-leading utilities, transposition. **The RomanText parser is what reads When in Rome.** |
| **partitura** | 1.9.0 (2026-05-25), Python ≥ 3.10 | Apache-2.0 | Python | Score and **performance** representation (note arrays with score and performed time). Alignment I/O (match files). `estimate_key` (Krumhansl), `estimate_spelling` (ps13), `estimate_voices` (Chew & Wu), **`estimate_tonaltension` (Herremans & Chew tension ribbons)**, `encode_performance` (tempo, timing, articulation, velocity from an alignment), `make_performance_features` (asynchrony, articulation, dynamics, pedal) [confirmed, R6]. |
| ms3 | 2.6.5 (2026-09-17) | GPL-3.0 | Python | Reads and writes DCML MuseScore files. Extracts notes, measures and harmonies tables [confirmed, R10]. |
| dimcat | 3.4.1 (2026-07-28) | GPL-3.0 | Python | Corpus-level analysis of DCML data. Probably unnecessary for us. |
| parangonar | 3.4.0 (2026-10-09) | Apache-2.0 [reported] | Python | Note-level score-to-performance alignment (Session 2). |
| pymatchmaker | 0.3.0 (2026-05-25), **Python < 3.13** | Apache-2.0 | Python | Real-time score following (Session 2). |
| tonal (tonal.js) | 6.5.1 (2026-10-14) | MIT | TypeScript | Lightweight theory in the browser: intervals, scales, chords, chord symbols, Roman numerals, voicings. Good for the **keyboard and harmony-explorer UI**, where a Python round-trip would be sluggish. |

**Python version constraint:** pymatchmaker needs < 3.13, librosa 1.0 needs ≥ 3.12, and music21 needs ≥ 3.11. **So Python 3.12.**

### C.2 Annotated corpora and formats

- **DCML harmony annotation standard** (v2.3.0) [R10, R11, R13].
  A label such as `#viio2(64)/vi` is parsed into columns: `globalkey`, `localkey`, `numeral`, `form`, `figbass`, `changes` (suspensions and retardations), `relativeroot`, `cadence` (PAC, IAC, HC, EC, DC, PC), `phraseend` (`{`, `}`, `}{`), `chord_type`, `chord_tones`, `added_tones`, `root` and `bass_note`.
  `chord_tones`, `root` and `bass_note` are expressed **on the line of fifths relative to the local tonic**.
  That is a representation that directly supports "relationships rather than keys" (see `music-theory-engine.md`).
  Positions are given as `mc` (measure count, physical) *and* `mn` (measure number, as printed), plus onset as a fraction of a whole note.
- **RomanText** (Tymoczko, Gotham, Cuthbert, Ariza, ISMIR 2019) [R12]: plain text, `m12 VI b1.5 i64 b2 b: viio7`.
  It has **first-class variants** (`m16var1`, `m16var2`) and notes, so ambiguity can be recorded at the source.
  Parsed by music21.
- **Dilemmadata** (Hentschel, Karystinaios, Widmer, Neuwirth, MEC 2026) [R21]: a merged corpus of 1,621 pieces and about 2.8M note-wise labels (AugmentedNet dataset + DLC) in one homogeneous format, CC BY 4.0.
  It lists the hazards of mixing standards: vocabulary, syntax, what a "row" is, and incompatible toolchains (music21 vs ms3/dimcat).
  These are exactly the hazards we face when combining DCML and When in Rome.
  84 pieces exist in both corpora with different original analyses, a ready-made set for studying disagreement.

### C.3 Automatic harmonic analysis: how good is it?

| System | Year | Strict Roman-numeral accuracy (key + degree + quality + inversion all correct) | Source |
|---|---|---|---|
| AugmentedNet | 2021 | about 45% (full test set). Higher on When in Rome subsets | [R22] |
| ChordGNN | 2023 | up to +11.6 points over AugmentedNet on conventional RN | [R23] |
| AnalysisGNN | 2025 | Comparable. Adds non-chord-tone detection, cadences, phrases | [R24] |
| RNHybrid (MusicBERT + GNN) | 2026 | **≈ 0.58** blind on both benchmarks | [R16] |
| RNHybrid with known labels given | 2026 | 0.58 → **0.80–0.83** on masked positions when 95% of labels are given | [R16] |

Assessment [speculative but well-grounded]:

- Fully automatic Roman-numeral analysis gets roughly **4 in 10 chords wrong** under the strict metric.
  Component accuracies (e.g. local key ≈ 0.85, degree ≈ 0.73 for RNHybrid) are much better than the full label.
- The strict metric also *overstates* error, because the reference is a single analysis, and experts disagree.
  The authors acknowledge this [R16]. Moonlight shows it directly (see `music-theory-engine.md` §3).
- **Design implication:** automatic analysis is a **draft to be confirmed**, shown with alternatives (the 2026 interface shows top-3 candidates with likelihoods) and corrected by the user.
  The "interactive completion" result (accuracy rises as labels are fixed) supports a workflow where the user's corrections propagate.
  Code: `manoskary/analysisgnn`; demo interface at analysisgnn.com, Verovio-based [R16]. Licence not yet checked.
- **For pieces with expert annotations, use those.** For other pieces: run the model, label it "automatic draft", and let the user correct it.
  That is itself a strong exercise for learning harmony (see `pedagogy.md`, Session 3).

### C.4 What is robust, what is interpretive, what is ambiguous

| Task | Status | Basis |
|---|---|---|
| Pitch content, intervals, sonority type of a vertical slice, bass note | **Deterministic** given the score | Set theory. Trivial. |
| Pitch spelling from MIDI | Robust (ps13 ≈ 99%+ on tonal music) [reported] | partitura |
| Global key | Robust for most tonal pieces | Key-profile methods |
| Local key / modulation boundaries | **Interpretive**. Experts disagree about where a modulation begins | Moonlight m. 7, m. 25 |
| Chord segmentation (which notes form one harmony) | Interpretive in arpeggiated or contrapuntal textures | Every piano piece the user plays |
| Chord-tone vs. non-chord-tone | Interpretive. Depends on segmentation | AnalysisGNN NCT module |
| Roman numeral of a clear chord in a known key | Deterministic | music21 |
| Function of chromatic chords (N6 vs. VI vs. Ger+6 vs. viio7/V) | **Ambiguous**. Several readings can be legitimate | Moonlight m. 16 |
| Cadences | Mostly robust at phrase level. Types are sometimes debated | DCML labels |
| Phrase and formal segmentation | Interpretive. Multiple hierarchical levels | |
| Motif recognition | Algorithms exist (e.g. SIA/COSIATEC family) [reported], but what counts as *meaningful* is interpretive | Session 6 |
| Tonal tension | Model output, not ground truth. Several incompatible models | Herremans & Chew (in partitura), Lerdahl TPS |

---

## Open questions arising from Session 1

1. Verovio vs. OSMD: decided by experiment E1.
2. Does the DCML score of `14-1` (Moonlight) match the measure numbering of the When in Rome analyses (BPS uses 2/2 with 69 measures)? Alignment by measure and beat must be verified note-by-note for the first 10 bars.
3. Who is "DT" in When in Rome's `analysis_DT.txt`? Most likely Dmitri Tymoczko (TAOM corpus); confirm.
4. Licence of `manoskary/analysisgnn`, and whether it runs on CPU in reasonable time for one movement.
5. Which pieces in a realistic two-year repertoire have expert annotations? Coverage audit.
6. Is MuseScore 4's CLI conversion of DCML 3.6.2 files faithful (voices, cross-staff, ties)? Part of E1.
