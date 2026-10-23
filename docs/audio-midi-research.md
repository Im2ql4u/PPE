# Audio and MIDI: capture, following, alignment, performance analysis

Digest of `research-notes/performance-capture-analysis.md` (full sources and benchmark details there). Hardware specifics: `hardware.md`. Runtime platform: **macOS + Chrome**.

## Decisions

| Topic | Decision | Basis |
|---|---|---|
| Primary channel | **MIDI** from the silent system. Audio is secondary (reference recordings, acoustic sessions without MIDI) | MIDI gives exact pitches and onsets. Piano transcription is about 97 note-F1 on MAESTRO (±50 ms) but noticeably worse on unseen pianos and rooms [reported] |
| Browser | **Chrome** (or Edge). Safari has no Web MIDI; Firefox needs a site-permission add-on. Chrome ≥ 124 prompts for all MIDI access | performance-capture §1.1 [confirmed] |
| Capture architecture | **Dual capture**. A Python daemon (python-rtmidi, CoreMIDI) writes the authoritative append-only log; Chrome Web MIDI drives the live UI only. Store `event.timeStamp`, never `performance.now()` | CoreMIDI is multi-client [reported, verify]; survives tab reloads |
| Development without the piano | **Fake piano**: a virtual CoreMIDI source replaying (n)ASAP performances with injected practice behaviour and adsilent-like message profiles; the IAC driver as fallback | performance-capture §9.4 |
| Live score following | **Not a foundation.** Later: a tolerant cursor (segment → locate → track locally) that may say "lost" | Following practice (fragments, restarts, errors) is unsolved. Matchmaker's ISMIR 2025 numbers are for complete performances, audio input |
| Analysis | **Offline per run**: segment the log into runs; localise each in the score; align with parangonar (DualDTW / TheGlueNote: about 98 note-match F clean, about 95 with synthetic repeats/skips on 5 pieces); features via partitura `encode_performance` and `make_performance_features` | performance-capture §3–4 |
| Errors vs expression | Pitch errors (missed, extra, substituted) come from alignment. **Timing and dynamics are never "errors"**: they are reported as curves relative to the user's own consistency and to reference ranges | Anti-goal; Repp/Palmer consistency findings |
| Velocity | Relative only (within-performance ranks and z-scores); never compared raw across instruments; calibration events logged | MIDI velocity → loudness is instrument-specific |
| Storage | Raw events (JSONL/Parquet) → sessions → runs → match files (partitura format) + features; SQLite index; aligner provenance on every alignment | performance-capture §9.1 |

## Datasets for development and validation

| Dataset | Use |
|---|---|
| (n)ASAP (CC BY-NC-SA) | Simulator substrate; BWV 846 references with note alignments |
| Rach3 MIDI | **Real rehearsal data, partly from an Essex EUP-116E silent piano**: validates segmentation and alignment on real practice. Terms to check |
| Batik-plays-Mozart | Aligned performances *with* harmony, cadence and phrase annotations: harmony-aware expression analysis |
| MAESTRO v3 | Reference performances (whole-cycle Chopin preludes, Suite bergamasque, WTC); needs alignment |
| ATEPP | Famous pianists, transcribed (velocity unreliable) |

## Audio (when needed)

Transcription: Kong et al. (`piano_transcription_inference`), hFT-Transformer, Transkun. Expect lower accuracy on an upright in a room. Basic Pitch is not suited to dense piano.
Beat-level tempo from audio–score sync (synctoolbox) is the robust core for reference recordings. Note-level velocity from transcription is not reliable.

## Experiments planned

- **E5 (M4):** simulator sessions from (n)ASAP with ground truth. Metrics: run-boundary F1, localisation, note-match F, and **false-error rate on clean expressive runs** (target 0).
- **Hardware day:** message inventory; CC64 resolution; release-velocity variation; mute rail off; Chrome + daemon simultaneously; jitter via IAC loopback.
