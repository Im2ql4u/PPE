# Feature ideas: consolidated and critically evaluated

Sources: the original brief; six research notes (`research-notes/*.md`, about 90 raw ideas); experiments E1–E3.
Duplicates are merged. Each idea is evaluated on:

- **Mechanism:** why it should help someone learn.
- **Evidence:** S strong / M moderate / W weak / – none (speculative). Grades refer to the *mechanism*; the feature itself is untested.
- **Feasibility:** H high (deterministic, data exists) / M medium / L low (research-grade or needs new data).
- **Originality** relative to the surveyed landscape: H / M / L.
- **Main risk.**
- **Verdict:**
  - **Core**: in the first vertical slices (roadmap M2–M3).
  - **Next**: M4–M6.
  - **Later**: after the core proves useful.
  - **Research**: needs an experiment first.
  - **Reject**: with reasons.

Organised by the Passage Laboratory's four verbs (`product-concepts.md` §3).

---

## A. Lenses: seeing a passage through interpretations

| # | Idea | Mechanism | Ev. | Feas. | Orig. | Main risk | Verdict |
|---|---|---|---|---|---|---|---|
| A1 | **Two analysts, one passage**: expert analyses side by side, disagreement classified (granularity / key frame / chord-tone status / genuine) and highlighted note by note | Contrasting cases; shows that analysis is interpretation | M (contrasting cases), – (feature) | **H** (E1 built it offline) | **H** | Confusing for a beginner; frame as "two ways to hear it" | **Core** |
| A2 | **Disagreement map**: score overlay of where lenses diverge (experts, auto draft, models), as "places worth studying" | Directs attention to ambiguity | – | H once lenses exist | **H** (no prior art found) | Incommensurable divergences; use ranks | Next |
| A3 | **Reduction ladder**: surface → label tones → structure → outer voices; each rung playable | Chunking; hierarchy; outer voices carry perceived tension (Lehne 2013) | M | **H** (E3) | M | Implies the analysis is the hearing; show provenance | **Core** |
| A4 | **Voice-leading strings**: each voice drawn as a string across chords, thickness = distance moved | Makes linear motion visible; links chords to counterpoint | – | H for notated voices | M | Clutter beyond 4 voices; selection-scoped | Next |
| A5 | **Keyboard geometry view**: degree labels on the actual key shapes; same function in different keys side by side | Abstract ↔ physical mapping, the project's core philosophy | – | H | M–H | Pretty but passive; pair with transposition probe (C4) | **Core** |
| A6 | **Structure map** (sections, cadences, phrases from DCML or user) with performance cues | Retrieval structure for memory (Chaffin & Imreh) | M | H where labels exist | M | Data only for 3 of 9 reference pieces; user-built otherwise | Next |
| A7 | **Motif tracker** with transformation labels (transposed, inverted, augmented, sequenced) | Pattern recognition, chunking | W | M (expert BPS-Motif for Beethoven; algorithms F1 ≈ 0.5) | M | Over-generation; expert-labelled first | Later |
| A8 | **Schema finder** (Prinner, Romanesca, Fonte, …) across the user's repertoire | Expert chunks; links to partimento | W | M (research code) | H | False positives outside galant style | Later |
| A9 | **"Where else does this happen?"** RN n-gram concordance across repertoire and corpora, playable | Variability across contexts → abstraction | M (category learning) | **H** | M–H | Label-convention mismatches between corpora | Next |
| A10 | **How typical is this progression?** Composer-conditional counts with intervals | Style as evidence | – | H (DCML stats) | H | Small-n; show counts not just probabilities | Later |
| A11 | **Expectation lens** (IDyOM-family): note and chord surprise and uncertainty; corpus-switchable "listener" | Validated expectation model (behaviour, EEG, MEG) | M (model), – (learning) | M (monophonic; melody extraction) | **H** | Model surprise ≠ user's surprise; make the disagreement data | Research → Later |
| A12 | **Consonance and voicing landscape** (roughness, harmonicity, familiarity; piano inharmonicity; register) | Psychoacoustic reasons for voicing rules | M (models validated) | M (reimplement incon models) | H | Pedal and inharmonicity extensions unvalidated | Later |
| A13 | **Tension curves**: user draws their own, then compares with several models | Metacognition; learner-built > watched | W (models), M (construction) | M | M–H | Tension models weakly validated; never "the" tension | Research |
| A14 | **Reference pianists**: tempo and dynamics curves of (n)ASAP/MAESTRO performances on the same score | Contrastive listening of interpretation | M | H for BWV 846 only (repertoire.md) | H | Normativity; show range, not mean | Next (BWV 846) |
| A15 | **Analysis-language translator** (DCML ↔ RomanText ↔ figured bass ↔ plain English), deterministic parse | Vocabulary acquisition | – | H | M | — | Later |
| A16 | Wavescape / keyscape linked to the score | Multi-scale tonal overview | – | M | M | Hard to read without guidance | Later |
| A17 | Tonnetz, orbifold or spiral views; Tonnetz-to-hand morph | Geometric intuition | **W/none** (viz §1) | M | M–H (morph) | Pretty, unproven; instrument usage | Research (morph only) |
| A18 | Jazz parse-tree explorer (Jazz Harmony Treebank) | Hierarchy of preparation and prolongation | – | M | H | Repertoire not yet relevant | Later (jazz track) |

## B. Transforms: perturbing a passage to reveal what is invariant

| # | Idea | Mechanism | Ev. | Feas. | Orig. | Main risk | Verdict |
|---|---|---|---|---|---|---|---|
| B1 | **Transpose** a passage (any key, with sensible spelling) and play it | Invariance under transposition = relational knowledge | M (transfer) | **H** | L (as transform) | — | **Core** |
| B2 | **Counterfactual chord**: fan of alternatives (P/L/R, secondary dominant, tritone sub, mixture, model infill) realised with minimal voice-leading, auditioned in context | Contrast: the composer's choice gains meaning from what it isn't | M (contrast), – (feature) | M–H (rule-based) | **H** on real repertoire | Mechanical-sounding realisations; keep the original texture | **Core** (rule-based) |
| B3 | Remove, isolate or solo a voice; hear inner voices | Auditory stream segregation; attention | – | H | L | — | **Core** |
| B4 | **Re-rhythm**: Moonlight triplets → block chords; rhythmic variants | Classic practice method; chunking | –/W (rhythmic variants untested) | H | L | Rhythmic-variant efficacy unknown, so it's an n-of-1 candidate | Next |
| B5 | **Exaggerate or neutralise your own rubato** (partitura decode) | Hear your own shaping as an object | – | M | H | Sampler quality | Next (needs mirror) |
| B6 | Re-pedal: same passage, alternative pedalling, A/B | Links an invisible action to its sound | – | M (needs CC64 data) | H | Pedal resynthesis realism | Later |
| B7 | **Improvise onto the skeleton**: ladder upward from L3/L2 | Generation; partimento logic | M (descriptive) | H (rule-based checking) | H | Aimless without vocabulary; offer schemata | Next |
| B8 | Natural-language edits ("make the LH an Alberti bass") via LLM driving music21 tools | Lowers the cost of exploration | – | M | M | Hallucinated theory; tools only | Later |
| B9 | Generative continuations or infills (Aria, AMT) as contrast fans | Widens imaginable possibilities | – | M (local models; licences partly unverified) | M | Labelled "generated", never "the composer" | Research |

## C. Probes: hearing and playing before being told

| # | Idea | Mechanism | Ev. | Feas. | Orig. | Main risk | Verdict |
|---|---|---|---|---|---|---|---|
| C1 | **Predict-then-reveal state machine** for every lens: hear/predict → commit → compare with analysts → name | Pretesting effect; prevents the AI-crutch effect | **S** (pretesting), M (Kestin/Bastani) | **H** | M | Feels slower; make skip cheap but logged | **Core** |
| C2 | **Minimal-pair ABX** from the user's repertoire (one chord, inversion or suspension changed) | Discrimination with contrast; interleaving of confusables | M | **H** (shares B2 engine) | M–H | Drill creep; short, quiet, optional | **Core** |
| C3 | **Transposition probe**: play a learned passage in another key; where fluency collapses = motor-only storage | Diagnostic transfer task | – | **H** | **H** | Frustrating; make it diagnostic, not graded | **Core** |
| C4 | **Audiation probe**: imagine or sing before playback; "does this version match the score?" (altered-note check) | Notational audiation (Brodsky); inner hearing predicts reading | M | H | M | Hard to verify singing without a mic; use self-report + ABX | Next |
| C5 | **Functional ear training from the repertoire**: scale degree of the melody at bar n, bass line playback, "which voice moved?" | Functional, in-context hearing | M | H | M–H | — | Next |
| C6 | **Cold probes**: first unassisted play of a passage next session, the canonical learning measure | Learning ≠ performance | **S** | H (needs mirror) | M | Noisy single takes; aggregate | Next (with mirror) |
| C7 | **Cue-start drills**: start from any structural landmark from memory | Retrieval cues for memory (Chaffin) | M | H | M | — | Later |
| C8 | **Harmonic vocabulary SRS**: produce a voicing or progression in a new key or context, not replay it | Retrieval and spacing | M (verbal), – (music) | H | M | Motor SRS intervals unknown | Later |
| C9 | **Voicing gym**: play successive voicings; feedback on motion, parallels, common tones; minimal alternative shown | Links function, geometry and hearing | – | H | M–H | Rule feedback feels like grading; listen-back framing | Next |
| C10 | Learner-built listening map (mark form while listening, then compare with annotations) | Construction > reading (Gromko & Poorman) | M | M | M | Form data scarce | Later |
| C11 | Sight-reading staircase scored for continuity | Sight-reading as a separate skill | M | M | M | Item calibration | Later |
| C12 | Teach-the-agent: explain a passage to a naive agent; backend checks claims | Self-explanation | W | M | M | Agent accepting wrong claims | Research |

## D. Mirrors: seeing what you actually did

All depend on capture, segmentation and offline alignment (roadmap M4). Development uses the fake-piano simulator.

| # | Idea | Mechanism | Ev. | Feas. | Orig. | Main risk | Verdict |
|---|---|---|---|---|---|---|---|
| D1 | **Flight recorder**: every MIDI event logged, sessions → runs | Learner-owned data; prerequisite | — | H (capture), M (segmentation) | H in products | Capture gaps; daemon reliability | Next (first mirror) |
| D2 | **Restart / attention map** set against phrase and cadence annotations | Restart points reveal mental representation (Chaffin; Rach3) | M | M | H | Segmentation errors; show confidence | Next |
| D3 | **Practice-strategy timeline** (loops, lengthening segments, run-throughs, slow practice) | Practice behaviour > hours (Duke 2009) | M | M | H | Over-interpretation | Next |
| D4 | **Consistency map**: across passes, which deviations are stable (intention) vs variable (accident) | Operational "rubato is not error" | M (Repp, Palmer) | M | H | Beginners are inconsistent by nature; trends only | Next |
| D5 | Tempo and voicing curves vs reference range | Interpretation awareness | M | M (BWV 846 references now) | M–H | Normativity | Later |
| D6 | Hesitation detector (delays before errors or hand shifts, not phrase-aligned) | Trouble-spot diagnosis | W | M | M | False positives on agogic accents | Later |
| D7 | **n-of-1 experiment designer**: randomise passages to practice methods; cold-probe outcomes | Tests untested staples (rhythmic variants, slow practice) on *you* | M (method) | M | **H** | Carry-over, regression to the mean; pre-register | Later |
| D8 | Metacognitive calibration: predict your cold-probe result, compare | Counters illusions of competence | M | H | M | — | Later |
| D9 | Pedal–harmony check: CC64 changes against harmony changes; blur index | Hear and see pedal decisions | – | M (needs continuous CC64) | H | Intentional blur (Debussy) is not an error; phrase it as a question | Later |
| D10 | Post-take audio A/B: your take vs one dimension corrected (e.g. melody velocities evened) | Feedback in the auditory modality; less dependence | W–M | M | H | Sampler quality | Later |

## E. Tutor (voice across all verbs)

| # | Idea | Verdict |
|---|---|---|
| E1 | Grounded Q&A over the selection: tool calls into the core; every factual claim cites addresses; location chips generated from IDs, never from LLM text | Next (after M3) |
| E2 | Claim badges with live verification (verified / contradicted / interpretive) | Next |
| E3 | Analyst-debate mode on disagreements (A1), with "reconstructed rationale" labelled as such | Next |
| E4 | Misconception typing: deterministic comparator classifies the error (key frame, quality, inversion, root vs bass); LLM only phrases it | Next |
| E5 | Levels of explanation: perceptual → notational → functional → contextual → aesthetic (labelled opinion) | Next |

## F. Improvisation track (later, but planned)

| # | Idea | Verdict |
|---|---|---|
| F1 | Loop the harmonic skeleton of *Comptine* / op. 28/4 / a Bach prelude; improvise a new melody; plan shown a bar ahead | Next (after core; needs only the sampler) |
| F2 | Guide-tone lines and shell voicings over any RN or chord sequence | Later |
| F3 | Partimento studio (Rule of the Octave, schemata, gentle voice-leading feedback after the take) | Later (no prior art with feedback) |
| F4 | Call-and-response inside a piece's harmony (rule-based transforms of the user's answer) | Later |
| F5 | Generative co-improviser (Aria/Somax-style), local | Research |

## G. Rejected (and why)

| Idea | Reason |
|---|---|
| Falling-note display as a main view | Improves short-term reproduction, not reading or understanding (P.I.A.N.O.; Deja survey). Commoditised. |
| Accuracy percentages, streaks, levels, badges | Anti-goal. Misleading metrics (learning ≠ performance). |
| Real-time visual timing feedback during play | Did not reduce errors and may add load (Brandmeyer 2011). Guidance dependence. |
| Absolute-pitch trainer as a core feature | 14% success after 12–40 h in adults (Wong 2020). Low yield. |
| Isomorphic "shadow keyboard" | Evidence concerns *playing* isomorphic instruments, not viewing them. |
| Automatic Schenkerian background as fact | Model trained on fugue subjects (0.75 per-note). Contested theory. |
| Embedding "style maps" of the user's playing | Opaque dimensions; no validated meaning. |
| Webcam hand and technique tracking | Unreliable consumer precedent; large effort; revisit later. |
| LLM-generated harmonic analysis | Unreliable (llm-symbolic-ai §1). LLMs explain lens data only. |
