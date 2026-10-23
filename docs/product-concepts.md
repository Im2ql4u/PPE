# What should this project become? Competing product concepts

This is the central synthesis of the research (sessions 1–2, 2026-10-23).
It compares six coherent concepts, each something the project *could* become, then recommends one integrated direction.
Supporting evidence lives in `research-notes/` and `experiments/`. Evidence tags as elsewhere: [confirmed] / [reported] / [speculative].

---

## 1. What the research established (the constraints any concept must respect)

| # | Finding | Evidence |
|---|---|---|
| F1 | The beginner-app loop (falling notes or score, wait-for-key, right/wrong) is **solved and commoditised**. The 2025–26 "AI tutors" put an LLM voice on top of the same core. | products-landscape §1, §8 |
| F2 | **No product links what is played to harmonic and structural analysis of real classical repertoire, or uses the existing expert corpora.** | products-landscape G3, G9 |
| F3 | **Expert annotations exist at scale.** DCML (about 1,000+ pieces, cadences and phrases), When in Rome (about 2,000 analyses, 339 pieces with 2+ analyses), BPS-Motif (motifs in 32 Beethoven first movements), GTTM database (300 pieces, second analyst on 33), Jazz Harmony Treebank (about 150 standards, parse trees), schema-annotated Mozart. | ecosystem C.2; cognition §3, §5, §6 |
| F4 | **Experts disagree, measurably and where it matters.** Strict agreement on Roman numerals: 0.89–0.90 for chorales and designed double annotations, 0.78 Mozart (DCML vs 16 theorists), about 0.5–0.7 Romantic piano. Moonlight mvt. 1: 0.66. **7% of Moonlight's notes change chord-tone status depending on the analyst**, concentrated at the musically ambiguous moments. | E1, E2 [confirmed, own measurement] |
| F5 | Automatic analysis is a **draft**: about 0.58 strict accuracy for the best 2026 model against a single reference. It improves to about 0.80 when 95% of labels are given (interactive completion). It is not obviously far below inter-expert agreement on Romantic repertoire (not like-for-like). | ecosystem C.3; E2 |
| F6 | Expert labels support **deterministic, playable reductions** with no ML: 94% of *Clair de lune*'s note attacks are explained by the DCML labels. | E3 [confirmed] |
| F7 | LLMs **cannot be the source of musical facts**: about 49% on score QA from text and 24% from images (2025 frontier); persistent failures at locating, counting and structure; famous pieces risk recalled commentary. Tool grounding helps (+16 points). Unguarded AI tutors can *harm* learning (−17% on exams); guardrailed ones help when they enforce pre-written expert content and sequencing. | llm-symbolic-ai §1, §5 |
| F8 | Learning science: **measure with cold probes**, not end-of-session accuracy. **Analyse practice behaviour**, not hours. **Terminal, faded, bandwidth feedback**, not concurrent visual displays. **Predict before reveal.** Ear training is **functional and in-context**. **Structural maps and cue-starts** for memory. Several piano staples (rhythmic variants, slow practice, hands-separate practice) **have no controlled evidence**, so they are open to n-of-1 testing. | pedagogy-evidence §10 |
| F9 | Geometric harmony views (Tonnetz, orbifolds, spiral array) have **almost no learning evidence**. Learner-*constructed* representations beat watched ones. Falling-note augmentation improves short-term reproduction, not reading or understanding. | visualization-hci §1, §3, §8 |
| F10 | Performance capture via MIDI is easy. **Following *practice* (fragments, restarts, errors) is unsolved**; segment-then-align offline is the feasible path. Validated tooling exists: partitura, parangonar, Matchmaker. Real practice data from a silent Essex upright exists (Rach3). | performance-capture §2–5 |
| F11 | Validated cognition models usable as lenses: IDyOM (expectation), consonance models (incon), exact voice-leading geometry, corpus statistics. Weakly validated: tension models, automatic Schenker, pattern discovery (F1 about 0.5). | cognition §10 |
| F12 | The renderer is not a source of truth: Verovio 6.3.0 silently plays wrong pitches from `**kern` input (regression). | E1 [confirmed] |
| F13 | Reference repertoire: 9 pieces in 4 harmonic languages. Expert data exists for 3, aligned performances for 1, 3 are private arrangements. | repertoire.md |

---

## 2. Six concepts

Each is described as if it were the whole product, so the trade-offs are sharp.

### C1. Score Atlas: an explorable, multi-lens score

*The passage you are learning, seen through every available lens.* Click any note or span; see what each analyst says, where they disagree, the reduction ladder, voice-leading strings, motifs, schemata, the keyboard shape of each chord, and how typical the progression is for this composer. Hear every level.

- **Fluencies served:** harmonic ★★★, musical ★★, physical ★.
- **Evidence:** analysis-based memory (Chaffin; moderate); learner-built representations > watched (F9). The value of *watching* analyses is weakly evidenced.
- **Originality:** high (F2, F4). Lenses-that-argue has no prior art found.
- **Difficulty:** medium. Mostly deterministic; data pipelines are the work.
- **Failure mode:** a beautiful museum. Understanding without hearing or playing it (illusion of competence, Kardas & O'Brien).

### C2. Practice Mirror: a practice laboratory with a flight recorder

*Every minute at the piano is recorded and becomes inspectable.* An always-on MIDI logger segments practice into runs, aligns them to the score offline, and shows a restart heat-map, practice-strategy timeline, tempo and voicing curves, a consistency map (intention vs accident), and comparison with reference pianists. A cold-probe scheduler and n-of-1 experiment designer test practice methods on *you*.

- **Fluencies served:** physical ★★★, musical ★★, harmonic ★.
- **Evidence:** strongest pedagogical grounding (F8). The practice-behaviour and cold-probe principles are among the best-supported.
- **Originality:** high in products (gaps G1, G5, G6). The research prior art (Rach3, Piano Precision) is not productised.
- **Difficulty:** medium-high. Practice segmentation and alignment are research-grade (F10). Needs the piano; simulation covers development.
- **Failure mode:** a dashboard. Metrics without musical meaning, or a gradebook in disguise.

### C3. Ear–Hand Gym: perception and production probes from your own repertoire

*Turn every passage into exercises that train hearing and doing together.* Predict-then-hear, minimal-pair ABX (one chord changed), sing the bass, transposition probes ("play bars 1–4 in D minor": does fluency survive?), voicing gym with voice-leading feedback, cue-start memory drills, spaced repetition of harmonic vocabulary across keys.

- **Fluencies served:** musical (audiation) ★★★, harmonic ★★★, physical ★★.
- **Evidence:** moderate. Inner hearing predicts sight-reading; functional ear training; retrieval and spacing; audio-motor coupling forms fast (F8). Repertoire-embedded ear training is untested but well motivated.
- **Originality:** medium-high (G4, G7). Generic ear trainers exist; repertoire-derived ones don't.
- **Difficulty:** low-medium, mostly deterministic.
- **Failure mode:** a drill app. Gamification creep; isolated from the music's meaning.

### C4. Improvisation Bridge: from pieces to playing freely

*Inhabit a piece's harmony and make your own music in it.* Loop the harmonic skeleton of *Comptine* or a Chopin prelude and improvise over it; galant schemata and partimento with gentle feedback; guide-tone lines; jazz parse trees (Jazz Harmony Treebank) to collapse and expand; call-and-response; optional generative partners (Aria, Anticipatory Music Transformer, running locally).

- **Fluencies served:** musical ★★★, harmonic ★★, physical ★★.
- **Evidence:** improvisation descriptively grounded (Berliner, Norgaard, Pressing); pedagogy outcomes weakly evidenced. Improvisation correlates with sight-reading (Mishra).
- **Originality:** high for partimento-with-feedback and improvise-inside-a-piece (no prior art found).
- **Difficulty:** medium (rule-based), high (generative, real-time).
- **Failure mode:** too early. The user is an early-stage player; free improvisation can feel aimless without vocabulary.

### C5. Conversational Tutor: an AI teacher that knows the score

*Ask anything about what's on the stand.* An LLM with tools over the symbolic core: grounded answers with clickable citations, predict-before-reveal enforced by a state machine, analyst-debate mode, misconception-typed feedback.

- **Fluencies served:** harmonic ★★, musical ★, physical ★ (indirect).
- **Evidence:** mixed: large gains when guardrailed and built on pre-written expert content (Kestin); harm when unguarded (Bastani).
- **Originality:** medium (many AI tutors). Grounded, auditable claims with music-specific verification are new.
- **Difficulty:** medium (tools) to high (verification and evaluation).
- **Failure mode:** a chatbot. Fluent, plausible, partly wrong, and it does the learner's thinking for them.

### C6. Musicology Bench: a personal laboratory for musical questions

*Ask the music questions and get computed answers.* Where else does this progression occur? How surprising is this note for a listener raised on Bach vs Chopin? Which voice-leading is minimal? Where do models and experts disagree? Corpus statistics, expectation and tension models, consonance landscapes, all queryable and comparable.

- **Fluencies served:** harmonic ★★, musical ★, physical –.
- **Evidence:** the models are validated to varying degrees (F11); the learning value of exploring them is unknown.
- **Originality:** high (lenses that argue; corpus-swap expectation; model-disagreement dashboard).
- **Difficulty:** medium.
- **Failure mode:** an intellectual toy. Fascinating for a physicist and irrelevant to playing the piano better.

### Comparison

| | Educational value | Evidence base | Originality | Difficulty | Hardware needed | Main failure mode |
|---|---|---|---|---|---|---|
| C1 Score Atlas | high (harmonic) | moderate | high | medium | no | museum |
| C2 Practice Mirror | high (physical) | **strongest** | high | med–high | yes (simulable) | dashboard |
| C3 Ear–Hand Gym | **high (all three)** | moderate | med–high | **low–med** | helpful | drill |
| C4 Improvisation Bridge | high (musical) | weak–moderate | high | med–high | yes | too early |
| C5 Conversational Tutor | medium | mixed | medium | med–high | no | chatbot |
| C6 Musicology Bench | low–medium | low | high | medium | no | toy |

No single concept covers all three fluencies without its failure mode. Each failure mode is prevented by *another* concept:

- C1's museum is cured by C3's probes: every lens ends in hearing or playing.
- C3's drill is cured by C1's meaning: exercises come from the music's structure.
- C2's dashboard is cured by C1's score anchoring and the cold-probe principle.
- C5's chatbot is cured by C1's lenses as its only source of facts and C3's predict-first state machine.
- C6's toy is cured by subordinating models to passages the user is actually learning.

---

## 3. Recommendation: a **Passage Laboratory**

**What the project should become:** an environment in which *every passage you are learning becomes a small laboratory.*
It is not a piano app with analysis features bolted on.
Four verbs organise everything, and the shared data model is built around them:

| Verb | What it means | Examples | Source concepts |
|---|---|---|---|
| **Look through lenses** | See the passage through every available interpretation, each with provenance, side by side, *including where they disagree* | Expert analyses (BPS vs DT), automatic draft, your own analysis; reduction ladder; voice-leading strings; motifs and schemata; expectation and consonance models; reference pianists' tempo curves | C1, C6 |
| **Transform** | Perturb the passage and observe what changes and what stays invariant | Transpose; reduce; remove a voice; alter one chord (counterfactual); re-voice; re-rhythm; re-pedal; exaggerate or neutralise your own rubato | C1, C3, C4 |
| **Probe** | Test yourself at the keyboard and by ear, before being told | Predict-then-hear; minimal-pair ABX; sing the bass; transposition probe; cue-start; cold next-day probe; improvise over the skeleton | C3, C4 |
| **Mirror** | See what you actually did, over time | Runs, restarts, consistency, tempo and voicing curves, comparison with pianists, n-of-1 practice experiments | C2 |

And one voice across all of them:

- **Tutor** (C5) as narrator and Socratic partner. It may only state facts the lenses provide, must cite them, and is held to predict-before-reveal by the application state machine.

### Why this is the right shape

1. **It matches the philosophy literally.** "Relationships rather than 88 keys" means understanding structure as what is **invariant under transformation**: a progression survives transposition, a skeleton survives elaboration, a function survives re-voicing.
   This is how a physicist learns a system: perturb it and watch. Transform + probe makes relationships *experienced*, not just displayed.
2. **It turns the project's most distinctive asset into its core.** Expert annotations, their measured disagreement (F3, F4) and deterministic reductions (F6) are what no product has (F2). Lenses-that-argue is genuinely new and honest about uncertainty.
3. **It respects the evidence about learning.** Probes implement predict-before-reveal, retrieval and cold measurement (F8). Mirrors implement practice-behaviour analysis and terminal feedback. Lenses alone would be the weakly evidenced part, so they always lead into probes.
4. **It degrades gracefully across data regimes** (F13). Rich pieces get expert lenses. Partial pieces get an automatic draft plus the user's own analysis as a lens. Private arrangements get the same transforms and probes.
5. **It keeps the hard research problems off the critical path.** Lenses, transforms and probes need no live score following and no ML. The mirror needs practice alignment but can run offline (F10). Generative partners and model lenses are optional plug-ins.

### What it is *not* (deliberate exclusions)

| Not building | Reason |
|---|---|
| Falling-notes or wait-mode note trainer | Commoditised (F1). Improves reproduction, not reading or understanding (F9). |
| Accuracy scores, streaks, badges | Anti-goal. Practice-performance metrics mislead (F8). |
| A score editor | MuseScore exists. The app imports. |
| Built-in OMR | Every OMR path ends in human correction. External tools (Audiveris, MuseScore) plus import suffice (ecosystem B). |
| Microphone transcription as a core channel | MIDI is available. Audio is a secondary, later lens (F10). |
| An LLM that analyses | It explains analyses (F7). |
| Automatic Schenkerian or deep hierarchical analysis as fact | Trained on fugue subjects. Show only hand-made or flagged hypotheses (F11). |
| Absolute-pitch training, isomorphic-layout evangelism | Low yield for adults; evidence for *viewing* layouts is absent (pedagogy §5.3; viz §1.7). |
| Live "follow me through the piece" as a foundation | Unsolved for practice. Built later as a tolerant cursor that may say "lost" (F10). |

### The honest risks of this recommendation

- **Understanding may not transfer to playing.** Causal evidence that theory knowledge improves performance is thin (pedagogy §6).
  Mitigation: every lens leads into a probe at the keyboard. The mirror and cold probes measure whether *this user's* playing changes. The app is instrumented to falsify its own premise.
- **Scope.** Four verbs times many lenses is a lot.
  Mitigation: the roadmap builds one vertical slice (one passage, two lenses, two transforms, two probes) before broadening.
- **Data coverage.** Only 3 of 9 reference pieces have expert lenses.
  Mitigation: the user's own analysis is a first-class lens. The automatic draft is clearly marked. Correcting the draft is itself a C3-style exercise.
- **Over-intellectualisation.** The user is an early-stage player with an analytical mind. A lab can become a way of *not* practising.
  Mitigation: the mirror tracks time at the keyboard versus time in lenses. The default flow ends at the piano.

---

## 4. Signature interactions (the first ones worth building)

Chosen for originality × evidence × feasibility, all deterministic, all working on the reference pieces. Details and evaluations are in `feature-ideas.md`.

1. **Two analysts, one passage** (Moonlight mm. 12–18). BPS and DT side by side. Disputed notes highlighted (E1). Hear each reading's chord tones emphasised. *Then* the probe: "which do you hear?", logged as the user's own lens.
2. **Reduction ladder with play-back-and-play** (Clair de lune, BWV 846). Surface → label tones → structure → outer voices (E3). Each rung is heard, then played by the user. The ladder runs upward too: improvise elaborations back onto the skeleton.
3. **Counterfactual chord** (Moonlight m. 3/m. 16 N6; Chopin op. 28/4). Click a chord to get a fan of rule-based alternatives realised with minimal voice-leading. Hear in context. Minimal-pair ABX: "which is Beethoven?"
4. **Transposition probe** (any learned passage). Play it in another key. Where fluency collapses shows what is stored as finger sequence vs. as harmonic shape. The same probe defeats LLM memorisation in tutor evaluation.
5. **Flight recorder → restart map** (once the piano arrives; simulated before). Where you always stop, set against the phrase and cadence annotations.

---

## 5. Decision summary

- **Build:** the Passage Laboratory core (lenses, transforms, probes) on a symbolic core with stable musical addresses. Then the mirror. Then the tutor voice. Then improvisation and model lenses.
- **Reuse:** Verovio (pinned, golden-tested), music21, partitura, parangonar, ms3, DCML / When in Rome / (n)ASAP data, tonal.js, Web MIDI, python-rtmidi. MuseScore as editor. Optional local models (IDyOM-family, Aria, AMT) as plug-ins.
- **Postpone:** live score following, audio transcription, generative partners, schema detection and motif discovery beyond expert labels, embedding maps.
- **Don't build:** see the exclusions table.
- **First concrete prototype:** see `roadmap.md` M1–M2. A Moonlight + Clair de lune "piece pack" pipeline, then a single-page passage lab with the two-analyst lens, the reduction ladder and one probe.
