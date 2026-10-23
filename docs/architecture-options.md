# Architecture options

Target: a local-first application **running on macOS** (Apple Silicon, Chrome), developed on Windows. Everything must be cross-platform at the code level. Runtime decisions (MIDI, browser, local models) are made for macOS.
Product direction: the Passage Laboratory (`product-concepts.md` §3).

## Requirements that discriminate between architectures

| # | Requirement | Source |
|---|---|---|
| R1 | Symbolic core in Python: music21, partitura, parangonar, ms3 have no browser equivalents | ecosystem C.1 |
| R2 | Sub-20 ms audio and visual response to key presses; low-latency sampler playback | pedagogy P13 (audio-motor coupling) |
| R3 | MIDI capture that survives tab reloads and runs without the UI open (the flight recorder) | performance-capture §1.5 |
| R4 | Stable musical addresses, independent of renderer IDs; golden tests renderer vs core | E1, F12 |
| R5 | Lenses (analyses, models, recordings, user annotations) stored as layers with provenance and alternatives | music-theory-engine §1, §7 |
| R6 | Optional heavy components (local LLM, IDyOM, Aria/AMT, alignment) must not be required to run the app | product-concepts §3 |
| R7 | One developer; maintainability over sophistication | — |
| R8 | Personal data (recordings, learning history) stays local | llm-symbolic-ai §7 |

## Option A: browser-only app, offline-precomputed data

A static TypeScript single-page app (Vite + React or Svelte; Verovio WASM; tonal.js; Web MIDI; Web Audio sampler; IndexedDB).
Python runs only offline, as a build step producing "piece packs" (JSON/MEI) that the app loads.

- **For:** simplest runtime (open a page), fast UI, trivially portable.
- **Against:** fails R3 (capture dies with the tab); weak on R1 (no alignment or analysis on the user's new material at runtime); every new score or recording needs a CLI round-trip. IndexedDB is a poor long-term home for practice data.
- **Verdict:** fine for the first lens/transform prototype. Not a destination.

## Option B: local Python service + browser UI (recommended)

```
┌──────────────────────── Chrome (localhost) ────────────────────────┐
│ UI: score (Verovio WASM) · keyboard · lens panels · probes · tutor │
│ Real-time: Web MIDI in → visual + Web Audio sampler (<20 ms)       │
│ Light theory in TS (tonal.js): chord naming, transposition preview │
└──────────────▲───────────────────── HTTP + WebSocket ──────────────┘
               │
┌──────────────┴──────────────── Python service (FastAPI) ──────────────────────┐
│ core/      piece packs: import → normalise → addresses → golden tests          │
│ lenses/    expert analyses (DCML, RomanText) · auto draft · user · models      │
│ transforms/ reduce · transpose · counterfactual · revoice (provenance)         │
│ probes/    state machine · backend grading · cold-probe scheduler              │
│ mirror/    capture daemon (python-rtmidi) · segmentation · alignment · feats   │
│ tutor/     tool server for LLM (local or API) · claim checking                 │
│ storage:   SQLite (index, layers, sessions) + files (MEI/MusicXML, MIDI, match)│
└────────────────────────────────────────────────────────────────────────────────┘
        optional sidecars: IDyOM(py), Aria/AMT (MLX/MPS), local LLM (llama.cpp/Ollama)
```

- **For:** meets R1–R8. Real-time stays in the browser (R2). The authoritative record and all analysis live in Python (R1, R3). Sidecars are optional (R6). One process to start.
  The same `core` package is importable from notebooks, so research and app share code.
- **Against:** two languages and a protocol between them. The user starts a service (one command, or a launchd agent on macOS).
- **macOS specifics:**
  - CoreMIDI is multi-client, so Chrome and the Python daemon can both read the piano [reported; verify on arrival].
  - Virtual CoreMIDI ports (python-rtmidi) enable a "fake piano" simulator that Chrome cannot tell from the real thing.
  - Safari has no Web MIDI; target Chrome.
  - Chrome ≥ 124 prompts for MIDI permission.

## Option C: desktop app (Tauri or Electron) with a Python sidecar

Option B packaged into a native window, with the Python service bundled (PyInstaller or similar) and started by the shell.

- **For:** one-click launch, native menus, file associations. Could use native CoreMIDI from Rust (Tauri) for capture.
- **Against:** packaging Python scientific stacks for macOS (codesigning, notarisation, arm64 wheels) is a known time sink. No capability that B lacks matters for a single user.
- **Verdict:** a packaging step to consider *after* B is stable, if ever.

## Option D: notebook-first research workbench

Jupyter + ipywidgets / anywidget, Verovio in notebook outputs, all logic in Python.

- **For:** fastest for experiments; already how E1–E3 were done.
- **Against:** fails R2 for practice at the piano; poor UI for probes and mirrors.
- **Verdict:** keep as the **research bench** beside B, sharing `core`. Not the product.

## Recommendation

**B, starting with A's front-end discipline**: the first prototype consumes precomputed piece packs (A-style), served by the Python service. Live analysis endpoints, capture and the tutor are added behind the same API.
D remains the lab bench. C is deferred indefinitely.

## Shared data model (first cut)

```
Piece(id, title, composer, licence, sources[])
 └─ ScoreVersion(id = hash(normalised events), source_file, importer, created)
     ├─ Event(address, pitch{midi, spelling}, duration, staff, voice, tie, ...)   # address below
     ├─ RenderMap(score_version, renderer, renderer_version, event_address ↔ svg_id)
     └─ Layer(id, kind ∈ {harmony, cadence, phrase, motif, schema, fingering, pedal,
               tension, expectation, reduction, user_note, ...},
              provenance{analyst | model+version | user, source_uri, licence},
              items[ Span(start_address, end_address), value, alternatives[], confidence? ])

Variant(id, base: ScoreVersion, span, transform{name, params, version}, result: ScoreVersion)

Recording(id, device, device_settings, calibration_id, clock)
 └─ Session └─ Run(t0, t1, localisation{score_version, span, hands, confidence})
                 └─ Alignment(provenance{aligner+version}, pairs[score_event ↔ perf_note | ins | del])
                 └─ Features(per-note, per-beat: tempo, timing, articulation, velocity, pedal)

Probe(id, kind, target{span|concept}, prompt, expected{from layer ids}, policy)
 └─ Response(t, answer, grading{by backend}, confidence_self, cold: bool)

LearnerModel: items{concept|passage} → history of probes, spacing state; experiments[] (n-of-1)
```

**Musical address** (validated in E1):
`(score_version, mc, onset_in_measure: Fraction, staff, voice?, pitch?)`.
`mn` (printed measure number) and beat are derived views. Renderer IDs only appear in `RenderMap`.
Annotations made on an older `ScoreVersion` are re-attached by matching (mc, onset, pitch); unmatched ones are flagged.

**Three clocks, never mixed implicitly:** score time (rational whole notes, written or expanded), performance time (CoreMIDI host-time nanoseconds), audio time (samples). They are connected only by `Alignment` objects with provenance.

## Testing strategy

| Subsystem | Test | Ground truth |
|---|---|---|
| Import and addresses | Golden test: core pitch and onset vs renderer-derived values for every event | E1 harness; fails on the Verovio 6.3.0 regression |
| Expert-lens import | Round-trip DCML/RomanText → layer → back; known labels at known addresses | Corpus files |
| Reductions and transforms | Property tests: transposition is invertible; L2 ⊆ L1 ⊆ L0; reductions never add pitches outside the label | Definitions |
| Probes | Backend grading against layers, including multiple acceptable answers when analysts disagree | Layers |
| Capture | Fake-piano replay with known timing; jitter measurement on macOS | Simulator |
| Segmentation and alignment | Synthetic practice sessions from (n)ASAP with injected restarts and errors; Rach3 for realism | Simulator ground truth |
| Tutor | Claim checking against the core; gold question set with transposed twins | llm-symbolic-ai §8.5 |
| Pedagogy | n-of-1 designs with cold probes | pedagogy §11 |
