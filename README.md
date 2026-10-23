# Passage Laboratory

A local environment for exploring piano music as a system of relationships: select any passage of a real score and see what is sounding, how expert analysts read it (and where they disagree), what it looks like on the keyboard, how it sounds stripped to its harmony, transposed, or with a different chord, and why.

> Milestone 1: the Passage Lab vertical slice. Pieces: Beethoven, *Moonlight* Sonata i; Bach, Prelude in C (WTC I); Debussy, *Clair de lune* (built on the Mac once MuseScore is installed).

**Setting up on a Mac: [docs/mac-setup.md](docs/mac-setup.md)** (step-by-step handout).

## Quick start

```sh
uv sync                              # Python 3.12 + dependencies into .venv
uv run python -m ppe fetch           # scores and expert analyses → data/external (≈30 MB)
uv run python -m ppe build           # build and validate piece packs → data/packs
uv run python -m ppe serve           # → http://127.0.0.1:8765 (use Chrome)
```

## What you can do

- **Select**: click a note; double-click for its chord; click empty space for a measure; click a label under the staff for a harmony; shift-click to extend. `←` `→` step through the harmonies, playing each.
- **See**: the selected notes on an 88-key keyboard, coloured by role in the chord (R, 3, 5, 7) with scale degrees underneath; the chord's name and its figures above the bass; each analyst's reading with a plain-language explanation; where and *how* the readings differ (same chord in another key, an extra chord tone, …); the voice leading into the next chord.
- **Compare**: two expert analyses of *Moonlight* (Chen & Su; Tymoczko) run as lanes under the score; notes the analysts disagree about are marked in red. For Bach, an expert analysis against an automatic one (AugmentedNet).
- **Listen**: as written, blocked chords, outer voices, top line, bass line, chord tones only (per analyst), or the analyst's chords plainly voiced; mute melody, triplets or bass; loop, slow down, simulated pedal.
- **Transform**: transpose (score, sound and keyboard move; numerals and degrees don't); replace a chord with an alternative, voice-led into the original texture, and compare by ear.
- **Check**: *Sources, licences and checks* in the panel shows where every score and analysis comes from and the validation results.

Deep links: `http://127.0.0.1:8765/#piece=moonlight&s=60&e=64&t=2` opens m. 16, transposed up a tone.

## Tests

```sh
uv run pytest                        # 46 tests: notation, alignment, comparisons, playback, API
node --test web/tests/*.test.mjs     # frontend logic
node tests/e2e/smoke.mjs             # real-browser interaction test (server must be running)
```

## Layout

| Path | What |
|---|---|
| `ppe/` | Python: symbolic core and service. `model` (shared representation) · `mei_import` (core from Verovio's MEI) · `validate` (cross-checks) · `analyses` (RomanText, DCML) · `compare` (disagreement classes) · `selection` (what's in a selection) · `explain` · `playback` (reductions, pedal) · `transform` (substitution, voice leading, transposition) · `render` (SVG) · `pieces` (registry, build) · `api` (FastAPI) |
| `web/` | Browser app (Preact + htm, no build step): `score.js`, `keyboard.js`, `panel.js`, `audio.js` (sampled piano), `actions.js` (coordination), `util.js` (pure, tested) |
| `tests/` | pytest suite; `tests/e2e/smoke.mjs` (Chrome DevTools Protocol) |
| `docs/` | Research, synthesis, roadmap, **[validation record](docs/validation.md)**, [app architecture](docs/app-architecture.md) |
| `experiments/` | Research experiments E1–E3 |

Licences of data, samples and libraries: [DATA_LICENSES.md](DATA_LICENSES.md).
