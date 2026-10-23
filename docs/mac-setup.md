# Setting up Passage Laboratory on your Mac

Step by step. Everything that needs downloading or installing is here; nothing else is required.
Expected time: about 15 minutes, most of it downloads.

Commands go in **Terminal** (Applications → Utilities → Terminal). Copy one block at a time.

---

## 1. Tools (one time)

**Homebrew** (the macOS package manager). Skip if `brew --version` already works:

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then follow the two "Next steps" lines it prints (they add `brew` to your PATH).

**git, uv (Python manager), Node, Chrome:**

```sh
brew install git uv node
brew install --cask google-chrome   # skip if Chrome is installed
```

- `uv` installs the right Python (3.12) by itself in step 2. You don't need to install Python.
- `node` is only used for the JavaScript tests.
- Chrome is the supported browser: Safari has no Web MIDI, which the next milestone (recording from the piano) needs.

## 2. Get the project

```sh
cd ~
git clone https://github.com/Im2ql4u/PPE.git
cd PPE
uv sync
```

`uv sync` downloads Python 3.12 and the libraries (music21, Verovio, FastAPI, …) into `PPE/.venv`. About 300 MB, a minute or two.

## 3. Fetch the music data and build the pieces

```sh
uv run python -m ppe fetch
uv run python -m ppe build
```

- `fetch` downloads the scores and expert analyses (When in Rome, DCML, the Sapp edition, ASAP) into `data/external/`, about 30 MB using sparse checkouts.
- `build` turns them into "piece packs" and **checks them**: every note is cross-checked between two parsers, every analysis' alignment is tested, and the build stops if anything unexplained turns up. You should see:

  ```
  building moonlight …
    1182 notes; cross-check with music21: 97.7% agreement; unexplained discrepancies: 0
    BPS: chord-tone fit 94.9% at its alignment; best at zero shift: True
    …
  skip clair-de-lune: sources missing. Needs MuseScore …
  ```

  The 97.7% is expected and explained in `docs/validation.md` (a music21 bug, not a data problem).

## 4. Clair de lune (needs MuseScore)

*Clair de lune* comes from the DCML corpus as a MuseScore file, which must be converted to MusicXML once.

```sh
brew install --cask musescore
uv run python -m ppe convert
uv run python -m ppe build clair-de-lune
```

The build compares the converted score note by note with DCML's own note table (the score the analysts annotated) and **refuses to build if they differ by more than 1%**.
If that happens with MuseScore 4, try the version DCML used (3.6.2):

1. Download *MuseScore 3.6.2* for macOS from <https://github.com/musescore/MuseScore/releases/tag/v3.6.2> and drag it to Applications.
2. Point the converter at it and convert again:

   ```sh
   export MUSESCORE="/Applications/MuseScore 3.app/Contents/MacOS/mscore"
   uv run python -m ppe convert
   uv run python -m ppe build clair-de-lune
   ```

Please tell me what the build printed either way (agreement percentage, any discrepancies); it's the first real test of this pipeline.

## 5. Run it

```sh
uv run python -m ppe serve
```

Open **<http://127.0.0.1:8765>** in Chrome. Stop the server with `Ctrl-C`.

Later, after `git pull`, re-run `uv sync` and `uv run python -m ppe build` (packs are rebuilt from the data; nothing to re-download).

## 6. Tests (optional)

```sh
uv run pytest                                  # musical and technical assumptions (about 46 tests)
node --test web/tests/*.test.mjs               # frontend logic
uv run python -m ppe serve &                   # then, with the server running:
node tests/e2e/smoke.mjs                       # drives Chrome: clicks, keys, playback (12 checks)
kill %1                                        # stop the background server
```

## Troubleshooting

| Symptom | Fix |
|---|---|
| No sound | Click anywhere in the page once (browsers only start audio after an interaction); check the Mac's output device. The first play loads the piano samples (~2 MB). |
| "Address already in use" | Another server is running: `uv run python -m ppe serve --port 8766` and open that port. |
| A piece shows "(not built)" | Run `uv run python -m ppe build`; for Clair de lune see step 4. |
| `ppe doctor` | `uv run python -m ppe doctor` prints the Verovio version, MuseScore location and which pieces are built. |
| Verovio version | Pinned to 6.2.x on purpose: 6.3.0 plays wrong notes for some scores (docs/validation.md). Don't upgrade it. |
