# Roadmap

Direction: the Passage Laboratory (`product-concepts.md`). Architecture: option B (`architecture-options.md`).
Principle: **vertical slices on real pieces**, each ending in something used at the piano. No milestone depends on the physical piano before M4, and M4 is developed against a simulator.

Status legend: ✅ done · ▶ next · ○ planned.

---

## M0. Research and feasibility ✅ (2026-10-23)

Research notes (6), experiments E1–E3, repertoire audit, synthesis documents.
Key de-risking results: musical addresses work (E1); expert disagreement is measurable (E1, E2); deterministic reductions from labels work (E3); Verovio regression found and pinned (E1).

## M1. Piece packs: the symbolic core ▶

**Goal:** a CLI and Python package that turns a score plus any available analyses into a versioned, tested "piece pack".

- Importers:
  - MusicXML/MXL, `**kern`, MuseScore 3 (DCML, via ms3);
  - RomanText (When in Rome) and DCML harmonies/cadences/phrases as layers with provenance.
- Normalised events with musical addresses (`architecture-options.md` data model); content-hash `ScoreVersion`.
- Golden tests: renderer-derived pitch and onset vs core for every event (catches E1's Verovio-6.3-class bugs).
- Lens alignment: RomanText (mn, beat) → (mc, onset) with explicit anacrusis and repeat handling. Verified on Moonlight (2 analyses), Clair de lune (DCML) and BWV 846 (WiR + ASAP score).
- Transforms v1: transpose, reduction ladder (E3 generalised), voice isolation. All produce `Variant`s with provenance.

**Acceptance:**

- (a) Three reference pieces packed.
- (b) 100% address agreement core vs renderer, excluding documented tie handling.
- (c) Every analysis label lands on the correct beat in 3 hand-checked bars per piece.
- (d) Property tests pass: transposition invertible; reductions only remove notes.

## M2. Passage Lab v0: lenses + transforms in the browser ○

**Goal:** a single-page app where the user selects any passage and sees, hears and plays it through lenses and transforms.

- Verovio score (pinned 6.2.x, or fixed upstream), selection by note, beat, bar or span.
- Keyboard panel with degree labels in the local key (A5). Sampler playback (Web Audio) with < 20 ms latency target.
- Lenses: expert analyses side by side with disagreement highlighting (A1); reduction ladder playback (A3).
- Transforms: transpose (B1), solo or mute a voice (B3).
- Web MIDI input shown on the keyboard (no analysis yet). Works with the on-screen keyboard if no MIDI is present.

**Acceptance:** on Moonlight mm. 1–23 and Clair de lune mm. 1–26, the user can click any note and see its address, both analyses (where present) and its chord-tone status per analyst; hear L0–L3; transpose and play along.
**Use test:** one week of the user's own practice with the tool. Log which lenses are opened.

## M3. Probes v0 ○

- Predict-then-reveal state machine (C1) over the lens panel: hear → commit a prediction (label, function or "which analyst") → reveal → log.
- Counterfactual-chord engine (B2), rule-based with minimal voice-leading realisation. The same engine powers minimal-pair ABX (C2).
- Transposition probe (C3) with MIDI input: play a passage in a new key; note-level comparison against the transposed score (simple symbolic diff; no full alignment needed for short excerpts).
- Learner model v0: items, responses, spacing state, all in SQLite.

**Acceptance:** backend grading accepts *any* expert's label where analysts disagree. ABX trials are generated for all three reference pieces. Every probe response is stored with timestamp and cold/warm flag.

## M4. Mirror v0: capture, segmentation, offline alignment ○

Developed against a simulator; validated on the real piano when it arrives.

- **Fake piano**: a virtual CoreMIDI port replaying (n)ASAP performances (BWV 846 first) with injected practice behaviour (restarts, loops, slow passes, hands separately, piano-synmist mistakes). Ground-truth JSON. Configurable adsilent-like message profile (release velocity, CC64 continuous or switch).
- Capture daemon (python-rtmidi; raw append-only log, host-time stamps), plus browser fallback.
- Segmentation into runs → localisation → offline alignment (parangonar DualDTW / TheGlueNote) → partitura features.
- First mirrors: restart map (D2), practice timeline (D3), cold probes (C6).

**Acceptance (on simulator):**

- run-boundary F1 ≥ 0.9 (±0.5 s);
- ≥ 90% of runs localised within 1 bar;
- note-match F ≥ 0.9 on clean runs;
- **zero "errors" reported on clean expressive performances** (anti-goal guard).

**Hardware day** (when the piano arrives): run the characterisation script (`hardware.md` H1–H4; performance-capture §9.4 step 5).

## M5. Tutor v0 ○

- Tool server over the core (llm-symbolic-ai §8.1). Structured claims with citations; claim checking; reveal policy from the M3 state machine.
- Gold question set (start from the 17 seed items; grow to about 150, with transposed twins).
- Model choice by evaluation: one local model (via Ollama or llama.cpp on the Mac) and one API model.

**Acceptance:** contradiction rate < 2 per 100 claims on the gold set; zero location chips produced from LLM text; no labels revealed outside the policy.

## M6. Improvisation track v0 ○

- Skeleton loop and improvise (F1) on *Comptine*, BWV 846 and op. 28/4: app plays the skeleton; user improvises; post-take view of chord-tone and non-chord-tone use.
- Upward ladder (B7): elaborate a reduction level back into a texture.

## M7+. Lens plug-ins and research features ○

Ordered by evidence × value:

1. RN concordance (A9);
2. reference-pianist curves for BWV 846 (A14);
3. expectation lens (A11, after an IDyOM-family spike);
4. consonance landscape (A12);
5. n-of-1 experiment designer (D7);
6. schema finder (A8);
7. partimento studio (F3);
8. generative partners (B9/F5).

---

## Dependencies

```
M1 ──► M2 ──► M3 ──► M5
 │             │
 └──────► M4 ──┘ (cold probes need runs)
 M2 ──► M6
```

## The first concrete prototype (recommended next step)

**M1 + the thinnest M2**: pack Moonlight mvt. 1 (Sapp kern + BPS + DT) and Clair de lune (DCML), and serve one page that shows:

- the score with notes coloured by analyst agreement (E1, now interactive);
- a click-a-note panel with address, both labels and chord-tone status;
- a play button for each reduction level.

That is roughly what E1 and E3 already compute offline, turned into the app's backbone with stable addresses and tests.
