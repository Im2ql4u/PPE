# App architecture (milestone 1)

How the implemented system is put together, and where to extend it.

## Data flow

```
score file ─► Verovio (pinned) ─► MEI ─► core notes ◄── cross-check ── music21 parse
(kern/MusicXML)                    │      (addresses)  ◄── edition check ── DCML note table
                                   │
analysis files ─► RomanText / DCML importers ─► labelled layers (aligned by measure+offset)
                                   │
                                   ▼
                     Piece (ppe/model.py) ─► pack (data/packs/<id>/piece.pkl + validation.json)
                                   │
                         FastAPI (ppe/api.py)
   ┌────────────┬──────────────┬───┴──────────┬───────────────┬────────────────┐
 /score       /inspect       /playback     /alternatives    /pieces/{id}
 SVG pages    selection →    events for    rule-based       notes, labels,
 (transpose)  facts, readings the sampler  substitutes      comparisons, statuses
   └────────────┴──────────────┴──────────────┴───────────────┴────────────────┘
                                   │
          Browser: actions.js (selection → inspect → state) → score.js · keyboard.js · panel.js
                                   audio.js (Web Audio sampler, sync highlighting)
```

## Shared representation

- **Note**: one notehead, addressed by `(measure, offset, staff, voice, MIDI)`. ID is built from that address (`m16.s2.v1.o0.p35`). `render_id` links to the SVG element; `track` is a curated listening track.
- **Label**: one analyst's reading of a span: key, figure, spelled chord tones, root, bass, inversion, family (for explanations), analyst variants.
- **Analysis**: a layer with provenance (analyst, source, licence, kind = expert/automatic/user), its labels, analyst notes and data issues.
- **Score time**: exact fractions of a quarter note from the start. Seconds exist only in the browser's player.
- **Selection**: either explicit note IDs (a note, a chord) or a span `[start, end)` (a harmony, a measure, a passage).

Domain logic lives in Python. The browser renders and coordinates; its only logic is geometry, layout and scheduling (in `util.js`, unit-tested).

## Adding a piece

1. Get a MusicXML or `**kern` score (or a MuseScore file plus a conversion step) and any analyses (RomanText or DCML TSV).
2. Add a `PieceSpec` in `ppe/pieces.py`: paths, attribution, licence, default tempo, track rules, and (if available) a reference note table.
3. `uv run python -m ppe build <id>`. Read the output: cross-check agreement, alignment fit per analysis, data notes. Investigate anything unexplained before relying on the piece. The build fails on unexplained notation discrepancies.

A piece without expert analyses works too: selection, keyboard, intervals, chord naming, reductions that don't need an analysis, and transposition. The analysis-dependent parts simply don't appear.

## Extension points for later milestones

| Future capability | Where it plugs in |
|---|---|
| MIDI recording (the silent piano) | New `ppe/capture` module and endpoint; the browser's `audio.js` already exposes sounding-note callbacks, and selections and notes have stable addresses for alignment results to point at. |
| Performance alignment / mirrors | New layer kind on `Piece` (runs with alignments) keyed by note IDs; the score already colours notes by class, so a "timing" colouring is a new class. |
| Ear training / probes | Uses `/playback` (any mode, any transposition) plus a backend grader over `Label`s, so answers are accepted from *any* analyst where they disagree. |
| User's own analysis | An `Analysis` with `kind="user"`; lanes, comparisons and explanations work unchanged. |
| AI tutor | Tool calls over `/inspect`, `/alternatives`, `/pieces/{id}`: the same facts the panel shows, with IDs for citation. |
| Improvisation | `/playback` with `mode="progression"` and a loop already plays an analyst's harmony as an accompaniment skeleton. |
