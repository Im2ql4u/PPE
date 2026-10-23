# Music theory engine

How the project represents, interprets and analyses musical structure.
**First draft, Session 1.** The data model is developed further in Session 7 (`data-model.md`).

Evidence tags as in `ecosystem-research.md`.

---

## 1. Principle: analysis is layered knowledge with provenance

The brief asks that the LLM not be "responsible for all musical reasoning".
Session 1 sharpens that: **most of the musical knowledge the app shows should not be computed at all.**
It should come from the score itself or from experts, with the source always visible.

| Layer | What | Example | Trust | Where it comes from |
|---|---|---|---|---|
| L0 Score facts | Notes, durations, voices, staves, markings | "m. 32, RH, beat 2: A4" | As good as the score transcription | MusicXML / MEI |
| L1 Derived facts | Deterministic functions of L0 | Pitch-class set, intervals above the bass, sonority type, register, voice-leading distances, dissonant intervals | Certain, given L0 | Our code + music21/partitura |
| L2 Expert analyses | Human annotations, possibly several per passage | "Chen & Su: V7. Tymoczko (?): V9♭9" | High, but interpretive | DCML, When in Rome |
| L3 Algorithmic hypotheses | Model or rule output, with alternatives | "Top-3: V7 (0.61), viio7/V (0.22), …" | A draft. Must be labelled as such | AnalysisGNN-family models, key-finding, tension models |
| L4 The user's analyses | The user's own labels and notes | "I hear this as a pivot" | The user's | Annotation UI |
| L5 Explanations | Natural-language accounts that *cite* L0–L4 | "The A in the right hand is a ♭9 over the dominant…" | Only as good as its citations | LLM, grounded via tool calls |

Rules:

- Nothing in L5 is stored as a musical fact. Explanations reference L0–L4 objects by address.
- L2 and L3 are never merged into a single "the analysis". Disagreement is displayed, not resolved.
- L4 is first-class. The user analysing a passage and then comparing with experts is one of the strongest learning activities available (Session 3 to evidence this).

## 2. Why disagreement is a feature, not noise

Experts genuinely disagree about harmonic analysis.
The disagreements cluster at exactly the points that are musically interesting: ambiguity, chromaticism, transitions.
A tool that hides this teaches false certainty.
A tool that shows *where and why* readings differ teaches how harmony actually works.

## 3. Case study: two expert analyses of Moonlight, mvt. 1

Source: When in Rome, `Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op027_No2(Moonlight)/1/` [confirmed, R12]:

- `analysis.txt`: Chen & Su, BPS-FH dataset (ISMIR 2018). Converted and proof-read by M. Gotham.
- `analysis_DT.txt`: "DT", most likely D. Tymoczko (to confirm). Includes notes and explicit variants.

Both use 2/2 time and the same measure numbering. They agree on most of the movement: the opening progression i – i4/2 – VI – N6 – V7 – i, the move to E major around m. 7–9, and the coda.
Where they differ, each difference is a different *kind* of analytical question.

| Bars | Chen & Su (BPS) | DT | Kind of disagreement | What the user can learn |
|---|---|---|---|---|
| 4 | `V7` | `V7 b1.5 i64 b2 V b2.5 V7` | **Granularity**: one dominant, or a cadential 6/4 decorating it? | The same bar can be heard at different "zoom levels". |
| 7 | `i b2 E: ii` | `i b2 iv E: ii` | **Pivot chord**: where does the old key end? | How modulation uses chords common to two keys. |
| 12 | `… b: viio7 b2.5 V65` | `… viio7/V b2.5 V7/V b: V7` | **Tonicization vs. modulation**: are we *in* B minor, or in E minor pointing at B? | Hierarchy of keys. A "key" can be local. |
| 15–16 | `V/iv` → `N6` (in B minor) | `e: V` → `VI` *or* `VImaj7` *or* `Ger4/3` (three variants recorded). Note: "chords here are pretty hard to identify" | **Function of a chromatic chord**, and key frame | One sound, several functional explanations. Each predicts a different continuation. |
| 25 | `i b2 c#: viio65 b2.5 iv64` | `i c#: iv b2 viio6/5`. Note: "the point of key shift here is very elusive" | **Modulation boundary** | Key changes are often gradual, not instantaneous. |
| 32, 35, 39 | `V7`, `viio7` | `V9[b9]`, `V9[b9]`, `V9[b9b5]` | **Chord tone or not?** Is the A a ♭9 belonging to the dominant, or a neighbour note? Is a diminished seventh over the dominant pedal a rootless V9? | viio7 ≅ V9♭9 without its root. One of the most useful equivalences in tonal (and jazz) harmony. |
| 47 | `V65` | `V6` | Seventh present or not (texture-dependent) | Reading chord content from arpeggiated texture. |
| 55–57 | Tonicization of III within C♯ minor (`V65/III … III`) | Brief modulation to E major (`E: ii … I`) | Same phenomenon at different hierarchical levels | |

[Analysis of bars confirmed from the two files. The musical glosses in the last column are ours, i.e. standard tonal theory.]

This table is close to a feature specification in itself:
**"Analysis disagreement view"**: click a bar, see each expert's reading, see the notes that support each one highlighted on the score and keyboard, hear the passage with each reading's chord tones emphasised.
Listed for evaluation in `feature-ideas.md` (Session 6).

## 4. Addressing musical objects (the identity problem)

Every layer above must point at the same musical objects.
That needs an addressing scheme that survives re-import, re-rendering and editing.

### Problems found in the actual data

- **Measure count vs. measure number.** DCML uses both: `mc` (physical, 1..N in the file) and `mn` (printed number).
  They differ for anacruses, split measures, voltas and numbering exceptions.
  RomanText uses printed numbers. MusicXML has both an implicit index and a `number` attribute.
- **Onset units differ.** DCML uses fractions of a whole note (`mc_onset = 3/8`) and quarter-beats (`quarterbeats = 21/2`).
  RomanText uses beats in the notated metre (`b2.5` in 2/2 means halfway through the 2nd half-note beat).
  Floating point can't be trusted for any of these. **Use exact rationals.**
- **Repeats.** Written position ≠ performed position. Verovio's expansion map and DCML's `quarterbeats_all_endings` both address this, differently.
- **Renderer IDs** (Verovio `xml:id`, OSMD object references) are generated at import and change when the source is re-exported.

### Proposed scheme [speculative, validate in Session 7–8]

```
ScoreAddress  = (score_id, mc, onset_in_measure: Fraction, staff, voice?, pitch?)
TimeSpan      = (score_id, start: ScoreAddress, end: ScoreAddress)
score_id      = content hash of the normalised note list (not the file), so cosmetic edits don't break links
```

- `mn` and `beat` are **derived views** for display and for importing RomanText.
- Renderer IDs are a **per-render lookup table** `ScoreAddress ↔ svg element id`, rebuilt on every load.
- Annotations made against an earlier version of the score are re-attached by matching on (mc, onset, pitch).
  Unmatched ones are flagged, not silently dropped.
- Three time coordinates are kept separate and connected only by explicit alignments:
  - **score time**: rational, in whole notes from the start, written or expanded.
  - **performance time**: seconds in a MIDI recording.
  - **audio time**: seconds in an audio file.
  An alignment is itself data with provenance (automatic or corrected).

## 5. Representations that make relationships first-class

The project's philosophy, "a landscape of relationships, not 88 keys", is partly a representation choice.
Candidate representations, each suiting a different view:

| Representation | What it makes visible | Use |
|---|---|---|
| **Scale degree relative to local tonic** | The same pattern in any key looks the same | Default label on keyboard and score overlays. DCML provides chord tones relative to local tonic directly. |
| **Line of fifths** (… F C G D A E B F♯ …) | Key relationships, spelling, diatonic vs. chromatic distance | DCML's native encoding. Key-distance visualisation. |
| **Pitch-class circle / chromatic clock** | Interval classes, symmetry (diminished, augmented, whole-tone) | Debussy (whole-tone, pentatonic), symmetrical chords. |
| **Tonnetz** | Triads as triangles, parsimonious (smooth) chord changes | Neo-Riemannian motion. Chromatic third-relations. |
| **Voice-leading space** (Tymoczko) | Chords as points, progressions as paths, smoothness as distance | "Why does this progression feel smooth?" |
| **Physical keyboard geometry** | Key positions, black/white topology, hand span, finger patterns | Fingering, reach, "the shape of a chord under the hand in this key". |

The interesting part is the **mapping between abstract and physical**.
A V7–I in C and in D♭ is the same object in degree space but a very different *shape* under the hand.
Much of physical fluency is learning these key-specific shapes; much of harmonic fluency is learning to see them as the same thing.
A view that shows both at once, degree labels on the actual keyboard shapes, is the core of the "intelligent keyboard" idea and is cheap to build.

## 6. Where computation happens [speculative, decided in Session 7]

- **Browser (TypeScript, tonal.js):** anything interactive and instant.
  Chord naming of a selected slice, interval display, transposition preview, scale and degree overlays on the keyboard, voicing generation for exercises.
- **Python service (music21, partitura, ms3):** import and normalisation of scores, reading corpora (DCML TSV, RomanText), tonal tension, key-finding, model inference (AnalysisGNN family), alignment, and batch analysis cached to disk.
- Analysis results are computed once per score version and cached as data addressed by `ScoreAddress`.
  The browser never recomputes what the server has stored.

## 7. Representing uncertainty

- **Expert alternatives** (L2): kept as separate analyses with analyst attribution.
  RomanText variants (`m16var1`) are imported as alternatives within one analysis.
- **Model hypotheses** (L3): top-k with scores.
  Scores are presented as the model's ranking, **not as probabilities of being right**.
  Model confidence is not calibrated against expert agreement unless we measure it.
- **User verdicts** (L4): accept, reject, or "I hear it differently".
  Stored, never overwritten by re-analysis.
- **Measuring disagreement** (an experiment for Session 8): compute agreement between BPS and DT for Moonlight.
  Use the Dilemmadata pieces with two analyses to get a corpus-level baseline for how often experts disagree, and on what.
  That baseline is the honest ceiling for any automatic analysis.

## 8. Tension, expectation, and "why is this beautiful?"

Candidate computational models (to research properly in Session 6):

- **Tonal tension ribbons** (Herremans & Chew 2016): cloud diameter, cloud momentum and tensile strain in the spiral array.
  Implemented in partitura (`estimate_tonaltension`) [confirmed, R6].
- **Tonal Pitch Space** (Lerdahl 2001): hierarchical tension and attraction [reported].
- **IDyOM** (Pearce): information-theoretic expectation (melodic surprise as information content) [reported].
  Python availability to check.

Position for now [speculative]: these are **lenses, not explanations**.
A model's curve is worth showing when it is (a) clearly labelled as a model, (b) comparable against the user's own judgement ("mark where you feel tension peak, then compare"), and (c) decomposable into musical causes the user can hear (dissonance, distance from tonic, register, rhythm).
Otherwise it is an impressive-looking graph that teaches little. This is the brief's own warning.

## Open questions

1. Is a content hash of the normalised note list stable enough to identify a score across MuseScore re-exports?
2. Can RomanText (`mn`, beat) be mapped unambiguously to `(mc, onset)` for the user's pieces? (Moonlight: yes, probably, since there's no anacrusis and 2/2 throughout.)
3. Which voice-leading and tension models have usable, maintained implementations?
4. How should a chord "slice" be defined in arpeggiated piano textures, where vertical sonorities don't coincide with harmonies? This affects every L1 computation on Moonlight and *Clair de lune*.
