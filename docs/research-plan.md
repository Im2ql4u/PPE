# Research plan

This is a research-first project: a personal environment for learning piano (see `vision.md` once written).
No application code is written until the research is done and the user explicitly asks for implementation.

This file is the **entry point for every working session**. Read the "Resume here" section first.

---

## Resume here

**Status:** Session 1 complete (2026-10-23).
**Next session:** Session 2 — performance capture & score following (see plan below).
**Before Session 2:** the user should run hardware experiment H1 in `hardware.md` (≈10 minutes, needs only a USB-C cable and Chrome/Edge).

---

## Who this is for (calibration)

The research prompt was written for an ambitious intermediate pianist interested in Beethoven, Chopin, Liszt, Rachmaninoff, Debussy and Bach.
The actual user is **an early-stage adult learner** who plays Beethoven's "Moonlight" Sonata, 1st movement, and part of the opening of Debussy's *Clair de lune*.
Their technical background (physics, ML, scientific computing) is strong.

This changes priorities and runs through every document:

- The repertoire that matters for the next 1–2 years is roughly grade 3–6 (Bach's *Anna Magdalena Notebook* and *Little Preludes*, easier Chopin preludes and waltzes, Schumann's *Album for the Young*, Satie, Grieg's *Lyric Pieces*), plus deepening the two pieces already known.
  Liszt and Rachmaninoff are long-term aspirations. They are not design targets.
- Features must be useful **this month** at the current level.
  A feature that only pays off for someone who can sight-read a Chopin étude is postponed.
- The user can absorb mathematical explanations easily, but cannot yet *hear* or *play* much of what such explanations describe.
  The gap between understanding and doing is the main pedagogical risk (see `pedagogy.md`).

## Hardware facts that shape the research

Essex EUP-111 upright with an **adsilent 2** silent system (see `hardware.md`).
The adsilent 2 has optical key sensors and sends **USB MIDI** (note on/off with velocity, release velocity, damper, soft pedal and sostenuto CCs).
Consequence: the primary performance-capture channel is **MIDI, not microphone transcription**.
Audio transcription is demoted from a core subsystem to an optional research topic.
Expected to hold, but unverified until experiment H1.

## Principles for the research

1. Primary sources over summaries: manuals, repositories, papers, licence files.
2. Every claim is tagged with one of:
   - **[confirmed]**: checked in a primary source or by experiment.
   - **[reported]**: stated by a credible source but not checked.
   - **[speculative]**: our inference or hypothesis.
3. Prefer reusing expert-made data (e.g. human harmonic annotations) over automatic analysis, where it exists.
4. Each document ends with "Open questions" that feed `open-questions.md`.
5. No session tries to do everything. Each session has a scope, writes its findings, and updates "Resume here".

## Session plan

| # | Scope | Main outputs | Status |
|---|-------|--------------|--------|
| 1 | Plan, hardware, and the "score + analysis core": notation renderers, symbolic-analysis libraries, **existing expert-annotated corpora**, score sources for the user's pieces | `research-plan.md`, `hardware.md`, `ecosystem-research.md` (sections A–C), `music-theory-engine.md` (first draft), `references.md` | done |
| 2 | Performance capture (Web MIDI, timing, velocity calibration), MIDI-to-score alignment, score following (Matchmaker, Parangonar, partitura), performance-analysis methods; audio transcription as a secondary topic | `audio-midi-research.md`, ecosystem section D–E | — |
| 3 | Learning science and piano pedagogy, with the evidence and its limits | `pedagogy.md` | — |
| 4 | Products and prior art: commercial apps, research prototypes, what to reuse or learn from | ecosystem section G | — |
| 5 | Score-aware tutor design: LLM + symbolic tools, grounding, provenance | ecosystem section F, tutor section of `architecture-options.md` | — |
| 6 | Feature ideation: at least 20 original ideas, critically evaluated against pedagogy and feasibility | `feature-ideas.md` | — |
| 7 | Architecture options and the shared musical data model (identities, time coordinates, uncertainty) | `architecture-options.md`, `data-model.md` | — |
| 8 | Feasibility experiments (isolated, in `experiments/`): MIDI capture, render-and-select, load expert annotations, alignment | `experiments/*/README.md` | — |
| 9 | Risks, open questions, synthesis, roadmap | `technical-risks.md`, `open-questions.md`, `roadmap.md`, `synthesis.md` | — |

Sessions 3–6 can be reordered. Session 8 depends on the user installing Python (not currently installed; Node 24 and Git are).

## Environment notes (2026-10-23)

- Windows 11, VS Code, Node v24.19.0, Git 2.55.
- **Python is not installed** (only the Microsoft Store alias). Needed for music21, partitura and the DCML tools.
  Recommendation: install Python 3.12 or 3.13 via `winget install Python.Python.3.12` or use `uv`. Decide in Session 8.
- Not yet a git repository.

## Session log

### Session 1 — 2026-10-23

- Read the adsilent 2 user guide v1.00 in full, including the MIDI implementation chart. Findings are in `hardware.md`.
- Surveyed notation renderers, symbolic-analysis libraries, annotated corpora and score sources. Findings are in `ecosystem-research.md` and `music-theory-engine.md`.
