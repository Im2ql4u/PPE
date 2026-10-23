# Synthesis: answers to the brief's eight questions

Status: end of research sessions 1–2 (2026-10-23). This page answers the brief's closing questions in order and links to the evidence.
For the full argument, read `product-concepts.md`.

---

## 1. The strongest product vision

**A Passage Laboratory** (`vision.md`, `product-concepts.md` §3). Every passage you learn becomes a lab with four verbs:

- **lenses**: expert analyses, automatic drafts, your own analysis, models and reference pianists, side by side, *including their disagreements*;
- **transforms**: reduce, transpose, alter a chord, isolate a voice, re-rhythm, exaggerate your rubato;
- **probes**: predict-then-hear, minimal pairs, transposition probes, cold next-day probes, improvising onto the skeleton;
- **mirrors**: what you actually did, from a MIDI flight recorder.

A grounded tutor narrates, but only from lens data.
The organising idea: **relationships are what stays invariant under transformation**, and you learn them by perturbing the music and listening.

## 2. The most valuable features

Ranked by evidence × originality × feasibility (`feature-ideas.md`):

1. **Two analysts, one passage**, with note-level disagreement highlighting (A1). Built offline in E1.
2. **Reduction ladder**, playable, from expert labels (A3). Built offline in E3.
3. **Predict-then-reveal** as an enforced flow for every lens and the tutor (C1).
4. **Counterfactual chord + minimal-pair ABX**, one rule-based engine (B2, C2).
5. **Transposition probe**: does your knowledge survive a key change? (C3)
6. **Keyboard geometry** with degree labels per local key (A5).
7. **Flight recorder → restart map, practice timeline, consistency map, cold probes** (D1–D4, C6).
8. **Grounded tutor** with verified, cited claims (E-series).

## 3. Existing technology worth reusing

| Layer | Reuse |
|---|---|
| Expert data | DCML corpora (CC BY-NC-SA), When in Rome (RomanText), (n)ASAP aligned performances, Batik-plays-Mozart, BPS-Motif, Jazz Harmony Treebank, Rach3 practice MIDI |
| Symbolic core | music21 10.5 (BSD), partitura 1.9 (Apache-2.0), ms3 2.6 (GPL), tonal.js (MIT, browser) |
| Rendering | Verovio (LGPL; **pinned 6.2.x** after the 6.3.0 regression found in E1); OSMD as fallback |
| Performance | python-rtmidi, Web MIDI (Chrome), parangonar (alignment), partitura features; Matchmaker later |
| Models (optional) | IDyOM-family (expectation), incon-style consonance models, AnalysisGNN/RNHybrid (automatic draft + interactive completion), Aria / Anticipatory Music Transformer (local generation) |
| Tools | MuseScore 4 (editing, corrections), Audiveris (OMR fallback) |

## 4. The most promising original ideas

None of these was found in products or prior art (sources in the research notes):

- **Lenses that argue**: interpretive disagreement (between experts, models, and you) as the core interaction. Grounded in a measured fact: experts agree only 0.5–0.9 strictly (E2), and 7% of Moonlight's notes change chord-tone status depending on the analyst (E1).
- **Transposition probe** as a diagnostic of motor-only vs. relational knowledge (it also catches LLM memorisation in evaluation).
- **Repertoire-derived minimal pairs and counterfactuals** realised with minimal voice-leading in the original texture.
- **The app as an n-of-1 lab**: testing untested piano-pedagogy staples (rhythmic variants, slow practice) on the user with cold probes.
- **Corpus-switchable expectation** ("surprising to a listener raised on Bach vs Chopin") and a **piano-aware consonance and voicing landscape**.
- **Improvising onto the reduction ladder** and **partimento with feedback** as the bridge from classical repertoire to improvisation.

## 5. The major technical obstacles

(`technical-risks.md`)

1. **Silent factual errors in dependencies.** Already happened (Verovio 6.3.0). Mitigated by golden tests.
2. **Aligning analyses to scores** (anacrusis, repeats, conversion artefacts). Already caused false disagreement in E2 before the fix.
3. **Following and aligning real practice** (fragments, restarts, errors): unsolved online. Offline segment-then-align is the plan.
4. **Coverage**: expert lenses exist for 3 of the 9 reference pieces; aligned references for 1.
5. **LLM reliability** for musical facts: about 49% on score QA. Contained by tools-only facts and a claim checker.
6. **Transfer**: whether understanding improves playing. The app measures this on its user rather than assuming it.

## 6. The proposed system architecture

**Option B** (`architecture-options.md`): a local Python service (FastAPI) holding the symbolic core, lenses, transforms, probe grading, MIDI capture daemon and tutor tool server, with SQLite + files.
A Chrome UI (TypeScript, Verovio WASM, Web MIDI, Web Audio, tonal.js) handles everything real-time.
Data model centred on **musical addresses** `(score_version, mc, onset, staff, voice, pitch)`, **layers with provenance**, **variants**, and **runs with alignments**, with three clocks kept separate.
Runs on macOS; developed cross-platform with `uv`.

## 7. The appropriate development sequence

(`roadmap.md`)

1. M1 piece packs (symbolic core, golden tests).
2. M2 passage lab: lenses + transforms in the browser.
3. M3 probes.
4. M4 mirror (simulator first, then hardware).
5. M5 tutor.
6. M6 improvisation.
7. M7+ model lenses and research features.

Nothing before M4 needs the piano.

## 8. The first concrete experiment or prototype worth implementing

**Pack Moonlight mvt. 1 and Clair de lune, and serve one page**:

- the Verovio score with notes coloured by analyst agreement;
- click a note to see its address, both expert labels and chord-tone status per analyst;
- play buttons for the four reduction levels.

It turns E1 + E3 (both working offline) into the backbone with stable addresses and tests. The next experiments that most reduce uncertainty:

- **E4:** score an automatic analyser against *both* Moonlight analyses and the BWV 846 analysis ("agrees with at least one expert").
- **E5:** a simulated practice session from (n)ASAP BWV 846, to test segmentation and alignment before the piano arrives.

---

## What is proven, plausible and speculative

| Proven (measured or confirmed here) | Plausible (good evidence, untested here) | Speculative (ideas to test) |
|---|---|---|
| Expert analyses exist for 3 reference pieces; addresses map across parsers (E1); experts disagree 10–50% (E2); label-based reductions explain 94% of Clair de lune's notes (E3); the Verovio 6.3.0 regression; LLM score-QA limits (published benchmarks) | Cold probes, practice-behaviour analysis, terminal feedback, predict-before-reveal, functional ear training help learning (pedagogy evidence); offline alignment of runs works (published on clean data) | That seeing disagreement improves hearing; that transforms and probes transfer to playing; that model lenses (expectation, consonance) aid learning; that the app as an n-of-1 lab yields usable conclusions |
