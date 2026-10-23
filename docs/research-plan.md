# Research plan

This is a research-first project: a personal environment for learning piano.
No application code is written until the user explicitly asks for implementation. Isolated experiments live in `experiments/`.

This file is the **entry point for every working session**. Read "Resume here" first.

---

## Resume here

**Status (2026-10-23):** research sessions 1–2 complete. Synthesis written.

- Start with `synthesis.md`, then `product-concepts.md`.
- Recommended direction: the **Passage Laboratory** (lenses, transforms, probes, mirrors).
- Recommended next step: **roadmap M1** (piece packs) plus the thinnest **M2** page, once the user approves moving from research to building.

**If continuing research instead of building**, the highest-value open items are:

1. **E4:** score an automatic analyser (AnalysisGNN/RNHybrid, `manoskary/analysisgnn`; check licence) against *both* Moonlight analyses and BWV 846, using "agrees with at least one expert".
2. **E5:** fake-piano simulator from (n)ASAP BWV 846 with injected practice behaviour, plus segmentation and parangonar alignment.
3. **E1-full:** Verovio vs OSMD bake-off on MusicXML for the reference pieces.
4. **Licence checks** listed in `open-questions.md`.
5. **Questions for the user** in `open-questions.md` (anthology source files, exact silent-system version, Mac model, priorities, tutor model policy).

## Context (corrected in session 2)

- **Platform:** developed on Windows in VS Code; **runs on macOS** (Chrome). Runtime decisions (MIDI, browser, local models) are made for macOS.
- **Hardware:** the piano (Essex upright with an adsilent silent system) has **not arrived**. The model and silent-system version are unverified. Nothing depends on it before roadmap M4; a simulator stands in.
- **Scope:** the user's current pieces and level shape the educational design but **do not bound the project**. Classical repertoire, advanced harmony, jazz improvisation, ear training and musical exploration are all in scope.
- **Reference repertoire:** the user's *Piano Anthology Vol. I* (nine works; `repertoire.md`).

## Principles for the research

1. Primary sources over summaries: manuals, repositories, papers, licence files.
2. Every claim is tagged **[confirmed]**, **[reported]** or **[speculative]**.
3. Benchmark numbers come with dataset, metric and limits.
4. Prefer expert-made data over automatic analysis where it exists. Measure disagreement rather than hide it.
5. Small isolated experiments to test feasibility; no main-application code yet.

## Document map

| Document | Content |
|---|---|
| `synthesis.md` | Answers to the brief's eight final questions. **Start here** |
| `product-concepts.md` | Six competing concepts, comparison, recommendation (central document) |
| `vision.md` | Philosophy and experience of the recommended direction |
| `feature-ideas.md` | About 60 consolidated, evaluated ideas with verdicts |
| `architecture-options.md` | Four architectures, recommendation, data model, testing strategy |
| `roadmap.md` | Milestones M1–M7 with acceptance criteria |
| `technical-risks.md` | Risks with mitigations and retiring experiments |
| `open-questions.md` | Questions for the user, planned experiments, unverified claims |
| `repertoire.md` | Coverage audit of the nine reference pieces |
| `ecosystem-research.md` | Notation, sources, OMR, symbolic analysis, benchmark interpretation (sections A–C; pointers for D–G) |
| `music-theory-engine.md` | Layered analysis with provenance, Moonlight disagreement case study, addressing |
| `pedagogy.md` | Evidence-graded design principles (digest) |
| `audio-midi-research.md` | Capture, following, alignment, analysis decisions (digest) |
| `hardware.md` | adsilent 2 as documented (unverified for the actual instrument) |
| `references.md` | Source index (sessions 1–2; the research notes carry their own source lists) |
| `research-notes/*.md` | Six agent-produced research notes, reviewed: products, pedagogy, cognition and models, visualisation/HCI/improvisation, performance capture, LLMs and symbolic AI |

## Experiments

| ID | Question | Result | Folder |
|---|---|---|---|
| E1 | Render, address and attach expert analyses note by note | Works (1,141/1,143 addresses agree). Found the Verovio 6.3.0 regression. 7.2% of Moonlight notes are disputed chord tones | `experiments/e1_render_and_address` |
| E2 | How often do expert Roman-numeral analyses agree? | Strict 0.53–0.90 by corpus; 0.79 overall; Moonlight 0.66 | `experiments/e2_expert_agreement` |
| E3 | Deterministic reduction ladder from expert labels | 94.3% of Clair de lune's note attacks explained; DCML `chord_tones` quirk found | `experiments/e3_reduction_ladder` |
| H1–H4 | adsilent capture characterisation | Pending hardware | `hardware.md`, `experiments/h1-midi-capture` |

Reproduce: `uv sync`, `uv run python experiments/fetch_data.py`, then each experiment's script (see its README).

## Environment

- `uv` project, Python 3.12 (`pyproject.toml`, `uv.lock`), project-local `.venv`. `verovio` pinned `<6.3`.
- Corpora are fetched to `data/external/` (gitignored) by `experiments/fetch_data.py`.
- The user's anthology PDF is gitignored (copyrighted arrangements).
- Git: local repository, `main` branch, no remote.

## Session log

### Session 1 (2026-10-23)

- Read the adsilent 2 user guide in full (`hardware.md`).
- Surveyed notation renderers, symbolic-analysis libraries, annotated corpora and score sources.
- Found expert analyses for Moonlight (two) and Clair de lune.

### Session 2 (2026-10-23)

- Corrections from the user: macOS runtime; piano not yet available and its version unverified; broader scope; anthology as reference repertoire.
- Set up git, uv, Python 3.12, corpus fetching.
- Six parallel research investigations (notes in `research-notes/`), reviewed and integrated.
- Experiments E1–E3. Repertoire coverage audit.
- Re-examined the "58%" benchmark (datasets, metric, caveats) and set it against measured human agreement (E2).
- Synthesis: product concepts, vision, features, architecture, roadmap, risks, open questions.
