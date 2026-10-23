# Performance capture, score following, alignment and performance analysis

> **Agent-produced research note, dated 2026-10-23. To be reviewed before decisions are based on it.**
> Scope: research topic "performance capture, score following/alignment, performance analysis and relevant ML" for the computational piano learning laboratory (local web app; React/TS front end, Python back end with partitura/music21; macOS + Chrome; MIDI from an Essex upright with an adsilent silent system as primary channel; audio secondary).
>
> **Evidence tags.** **[confirmed]** = checked against a primary source (paper, spec, repository, PyPI metadata) during this research session. **[reported]** = claimed by authors or a secondary source; not independently checked (or checked only via abstract). **[speculative]** = this note's own inference, design proposal or estimate.
>
> **Benchmark caveat.** Every number below is given with its dataset, metric and tolerance where known. None of these benchmarks measures *practice* (fragmentary, error-laden playing) except Rach3 (§2.5), and Rach3 shows that methods tuned on polished performances degrade sharply there.

---

## 0. Executive summary

1. **Capture**: Chrome (or Edge) Web MIDI on macOS is viable for live UI. Firefox works but needs a site-permission add-on, and Safari has no native support [confirmed]. The robust architecture is **dual capture**. A small Python daemon (python-rtmidi on CoreMIDI) writes an append-only raw event log, which is the source of truth. Chrome Web MIDI drives low-latency visual feedback. CoreMIDI is multi-client, so both can open the piano's port at the same time [reported]. Development needs no piano. A Python "fake piano" publishes a **virtual CoreMIDI source** that replays (n)ASAP/MAESTRO/Rach3 MIDI with injected practice behaviour, and Chrome sees it as a real device [speculative design; virtual ports reported supported on macOS].
2. **Score following of practice is not solved.** Online followers are benchmarked on complete, mostly correct performances. Matchmaker's ISMIR 2025 evaluation (audio input) reaches only ~33–44% of notes within 50 ms piece-wise on (n)ASAP/Batik/Vienna4x22 [confirmed]. Repeat- and skip-robust MIDI HMMs exist: Nakamura's outer-product HMM (2014) and Arzt's "any-time" tracking (2010) [confirmed existence]. The JKU Rach3 study (ISMIR 2025) found that even a state-of-the-art *offline* aligner (TheGlueNote) matched only roughly 40–60% of notes on real rehearsal MIDI, against >90% on (n)ASAP/Batik [confirmed from figure; values read off a bar chart]. **Recommendation**: use online following only for a tolerant "where am I" cursor. Do all analysis offline, per *pass*, after segmenting the practice log [speculative].
3. **Offline alignment of whole performances is solved enough to use.** parangonar's DualDTWNoteMatcher and TheGlueNote reach ~98% note-match F on clean performances. TheGlueNote keeps ~94–95% with ~20% injected repeats/skips, where Nakamura's HMM tool falls to 44% (5 Chopin/Beethoven pieces, TheGlueNote paper Table 4) [confirmed]. Both parangonar (Apache-2.0, v3.4.0, 2026-10-09) and Nakamura's AlignmentTool (MIT, v240109) are available [confirmed].
4. **Analysis stack**: partitura (Apache-2.0, v1.9.0, 2026-05-25) provides `encode_performance` (beat_period, timing, articulation_log, velocity) and performance features (asynchrony, articulation, dynamics, pedal) from score + performance + alignment [confirmed]. Use this rather than re-implementing it.
5. **Error vs expression**: symbolic alignment gives you *pitch* errors (missed, extra, substituted notes) robustly. *Timing* "errors" must never be inferred from deviation alone. Report timing as a curve relative to the learner's own history and to reference pianists, not as right or wrong [speculative/design principle, consistent with the anti-goal].
6. **Simulation**: Morsi et al.'s `piano-synmist` toolkit (SMC 2024) injects realistic-ish mistakes into MIDI performances [confirmed exists; its probabilities "are not based on actual analysis" per README]. Combine it with a practice-behaviour generator (restarts, loops, tempo drops) over (n)ASAP. Then validate on Rach3 real rehearsal MIDI, part of which comes from an **Essex EUP-116E silent piano**, very close to the user's instrument [confirmed from paper].

---

## 1. Performance capture on macOS

### 1.1 Browser support (status October 2026)
- **Chrome / Edge**: Web MIDI has shipped since Chrome 43 / Edge 79. Since Chrome 124 (rolled out in 2024), *all* Web MIDI access, not only SysEx, sits behind a permission prompt. A denied request rejects `requestMIDIAccess()` [confirmed: <https://developer.chrome.com/blog/web-midi-permission-prompt>].
- **Firefox ≥ 108**: supported, but the first call prompts the user to install an auto-generated **site permission add-on**. It needs a secure context and Permissions-Policy `midi`. `midi` and `midi-sysex` are separate permissions, and both get the "heightened consent" dialog [confirmed: Bugzilla 1796191, 1795025; MDN compat note]. This is workable, but the UX is clunky for a local app.
- **Safari (macOS/iOS)**: **no native Web MIDI**. WebKit bug 107250 is still open, and caniuse lists Safari up to Technology Preview as unsupported. A third-party macOS Safari extension ("Web MIDI for Safari") injects a CoreMIDI-backed `navigator.requestMIDIAccess` from Safari 18.4 [confirmed status via <https://caniuse.com/webmidi>, <https://bugs.webkit.org/show_bug.cgi?id=107250>; extension reported]. Do not target Safari.
- **Spec status**: the W3C Web MIDI API is still a Working Draft (version dated 20 Oct 2026, Audio WG) [confirmed: <https://www.w3.org/TR/webmidi/>]. Requirements: secure context (`localhost` counts as secure), optional `sysex: true`, and `software: true` to expose software synths.
- **SysEx**: not needed for performance capture (note on/off, CC64/67 are channel messages). Request `sysex: false` to keep the prompt light. SysEx would only matter for configuring the silent system, if it supports that [speculative].

### 1.2 Timestamps and latency
- **Spec semantics**: `MIDIMessageEvent.timeStamp` is a `DOMHighResTimeStamp` giving "the time the message was received by the system". It is relative to the document's time origin (`performance.timeOrigin`). `MIDIOutput.send(data, timestamp)` schedules output in the same clock [confirmed: W3C WD §5.4–5.5].
- **Chromium on macOS**: Chromium's CoreMIDI backend converts each packet's `MIDITimeStamp` (mach host time) to seconds via `AudioConvertHostTimeToNanos` and passes it to the renderer. The event timestamp is therefore the **CoreMIDI driver timestamp**, not the moment JS ran the handler [confirmed in Chromium 61 source `media/midi/midi_manager_mac.cc`; current code may differ, re-check]. Practical rules [speculative but standard]:
  - Always store `event.timeStamp`, never `performance.now()` inside the handler. Main-thread jank (React renders, GC) delays the handler but not the stamp.
  - Persist absolute time as `performance.timeOrigin + event.timeStamp`, and also log a monotonic session-relative time. Wall clock alone drifts and jumps.
  - Process MIDI in a **dedicated module** outside React state. Batch UI updates per animation frame.
- **USB MIDI transport**: USB-MIDI 1.0 class devices are usually full-speed USB with 1 ms frame polling, so transport quantisation is ~1 ms. That is negligible next to the silent system's own sensing pipeline. The dominant unknowns are internal to the adsilent: optical key sensing, velocity computation, and whether note-on is emitted at estimated hammer-strike time [speculative; no adsilent latency spec found]. The adsilent user guides mention USB-MIDI (USB-Mini on v1, USB-C on AdSilent 2) and a "proportional pedal" setting, but publish no velocity resolution, release-velocity or CC64 resolution [confirmed absence in what was found: <https://www.maene.be/media/akeneo_connector/media_files/A/d/AdSilent_2_user_guide_ENG_4654.pdf>]. **Action when the piano arrives**: run a capture-characterisation script (§9.4) and do not assume release velocity or continuous CC64 until measured.
- **Jitter**: no recent primary measurement of Chrome Web MIDI input jitter on macOS was found. Measure it locally. A loopback through the IAC Driver bus, sending with scheduled timestamps and receiving in Chrome and Python, gives software-path jitter. A Python vs Chrome comparison on the same physical events gives relative offset [speculative test design].

### 1.3 CoreMIDI multi-client behaviour
CoreMIDI lets several client processes connect to the same source endpoint at once. Chrome, a Python daemon and a DAW can all receive the piano's events, unlike WinMM on Windows, where ports are typically exclusive [reported; widely documented in CoreMIDI programming guides, not re-verified this session]. This is what makes the dual-capture architecture cheap.

### 1.4 Libraries
- **WebMIDI.js v3** (djipco/webmidi; Apache-2.0; browser and Node.js; TypeScript typings shipped) [confirmed licence/repo; API details reported]. `WebMidi.enable({sysex:false})`, `input.addListener("noteon"|"noteoff"|"controlchange", cb)`. Events expose `timestamp` plus `note.attack`/`note.release`, which are normalised velocities, with raw 7-bit values also available. It is a convenience layer only; the raw API is ~40 lines. For an app that must preserve every byte, use the raw API or keep WebMIDI.js's `e.message.rawData`.
- **python-rtmidi** (MIT; v1.5.8; Python ≥ 3.8; wraps RtMidi's CoreMIDI backend) [confirmed via PyPI]. The input callback receives `(message, delta_time)`; on macOS the deltas derive from CoreMIDI timestamps [reported]. It supports **virtual ports** on macOS (CoreMIDI virtual sources and destinations) [reported].
- **mido**: higher-level messages, MIDI files, a callback thread [confirmed docs]. For capture, take timestamps from python-rtmidi directly rather than relying on mido's `msg.time` semantics on input [speculative caution].
- **Web Serial / WebUSB**: not applicable. The OS class driver claims a USB-MIDI device [speculative, standard].

### 1.5 Recommended capture architecture [speculative design]
```
 adsilent USB-MIDI ──► CoreMIDI ──┬──► Python capture daemon (python-rtmidi)
                                  │      • append-only raw log (JSONL/Parquet), host-time stamps
                                  │      • session/pass segmentation, alignment jobs
                                  │      • WebSocket → browser (position, analyses)
                                  └──► Chrome Web MIDI (UI feedback only, <10 ms visual path)
 dev: Python "fake piano" ──► CoreMIDI virtual source "PPE-Sim" ──► (same two consumers)
```
- **Source of truth = Python log.** It survives browser reloads and tab sleeps, avoids per-origin permission resets, and lets analysis run without the UI open. The browser keeps only an ephemeral ring buffer.
- **Fallback**: if the daemon is not running, the browser posts its own captured events to the backend, with `source: "webmidi"`. Each event keeps its own clock domain. Never mix clocks without an explicit offset estimate.
- **Simulation**: a Python process opens a virtual output port (rtmidi `open_virtual_port("PPE-Sim")`) and replays MIDI files in real time with realistic timing. To Chrome and to the capture daemon it is indistinguishable from the piano. The **IAC Driver** (Audio MIDI Setup) is the alternative if virtual ports misbehave. loopMIDI is Windows-only and irrelevant on macOS.

---

## 2. Score following (online)

### 2.1 Matchmaker (CPJKU / KAIST): `pymatchmaker`
- **What**: Python library for real-time alignment. Algorithms per `methods.yaml`:
  - **Audio**: OLTW-Arzt (after Brazier & Widmer 2020), OLTW-Dixon (Dixon 2005), outer-product HMM (Nakamura 2014), switching Kalman filter (Jiang & Raphael 2020), Arzt + tempo model, multi-fold OLTW over unfolded score variants.
  - **MIDI**: `arzt`, `dixon`, `outerhmm`, `hmm` (Cancino-Chacón et al. 2023, i.e. the ACCompanion follower), and `pthmm` (pitch-based HMM, the **default**).
  - **Inputs**: files (simulation mode), live devices (`[devices]` extra: PyAudio + python-rtmidi), or a custom stream, e.g. a WebSocket [confirmed: <https://github.com/pymatchmaker/matchmaker>].
- **Licence & maintenance**: Apache-2.0. PyPI versions 0.1.x (Dec 2024–Jan 2025), 0.2.1 (2025-10-13), **0.3.0 (2026-05-25)**. Python ≥3.10, <3.13. Requires FluidSynth for simulation [confirmed via PyPI JSON]. Actively maintained research code, still 0.x.
- **Reported accuracy** (Park, Cancino-Chacón, Chiruthapudi, Nam, *ISMIR 2025*, arXiv:2510.10087) [confirmed from the arXiv HTML]:
  - Datasets: (n)ASAP subset (59 performances, 2.65 h), Batik (30 perf., 2.85 h), Vienna4x22 (88 perf., 2.24 h).
  - Metric: alignment rate (AR) at ≤50/100/500/1000/2000 ms, plus median absolute error. Errors >2 s are excluded from the AE statistics.
  - Chroma features, **audio input**:
    - OLTW-Arzt: MAE 91 ms (n)ASAP, 107 ms Batik, 153 ms Vienna. Piece-wise AR≤50 ms 44%, 36% and 33%. Total AR≤2 s 93%, 90% and 87%.
    - HMM baseline (no tempo model): far worse, MAE 346–642 ms.
  - Algorithmic latency: 0.07 ms (OLTW-Arzt) to 3.6 ms (HMM) per frame, plus 1–43 ms feature extraction. Measured **in simulation**, not live.
  - The tables extracted report audio configurations. A MIDI-input benchmark was not found in the paper; verify before quoting.
  - **Limitations**: complete performances of solo classical piano; no evaluation on stops, restarts, repeated fragments or error-dense playing; no live testing.
- **Take-away**: Matchmaker is the best open *framework* for MIDI score following, with HMM/OLTW MIDI followers and streaming plumbing. Its published numbers do not speak to practice conditions.

### 2.2 Other followers
- **Nakamura et al., outer-product HMM** (JNMR 43(2), 2014; arXiv:1404.2313). Polyphonic MIDI score following that explicitly models **arbitrary repeats and skips** and admits performance mistakes, with reduced complexity for practical-length scores [confirmed from abstract]. Related work:
  - *AR-HSMM* (ISMIR 2015) for trills, tremolos and arpeggios [confirmed exists].
  - "A stochastic temporal model of polyphonic MIDI performance with ornaments" (arXiv:1404.2314).
  - Audio-to-score following with errors and arbitrary repeats/skips, monophonic (arXiv:1512.07748) [confirmed existence].
  - This family is the most directly relevant prior art for **MIDI practice following**. Matchmaker includes `outerhmm`.
- **Arzt & Widmer, "any-time" music tracking** (STAIRS 2010): handles "omissions, forward and backward jumps, unexpected repetitions, or (re-)starts in the middle of the piece". It does this by continuously re-evaluating position hypotheses across the score, combined with OLTW for local precision [confirmed from abstract: <https://www.cp.jku.at/research/papers/Arzt_Widmer_STAIRS_2010.pdf>]. Related work:
  - "Flexible score following" (Arzt, Goebl & Widmer, Vienna Talk 2015) [confirmed existence].
  - Symbolic fingerprinting for piece and position identification (Arzt, Böck & Widmer, ISMIR 2012). Rach3 reused it for piece identification: weighted F1 0.989, macro F1 0.929 over 71 scores, with failures on short or highly fragmentary takes [confirmed: Rach3 paper Table 2].
- **Peter, Hu & Widmer, SMC 2025**: real-time piano transcription followed by **symbol-level tracking** (TOLTW/OLTW matchers in parangonar). It outperforms audio-only OLTW in precision and robustness [reported from abstract; numbers not extracted]. This supports the view that the *symbolic* domain is the right place to track, and MIDI input gets that for free.
- **ACCompanion** (Cancino-Chacón et al., IJCAI 2023): MIDI-input expressive accompanist with a real-time follower + tempo/expressive prediction [confirmed paper; follower details reported]. Its HMM is in Matchmaker as `hmm`.
- **parangonar online matchers**: `OnlineTransformerMatcher` (learned, offline-RL-trained; Peter, ISMIR 2023) and TOLTW/OLTW [confirmed in repo].
- **Antescofo**: IRCAM-originated real-time score following and synchronous language for mixed music; now commercialised (Metronaut accompaniment app). Closed source [reported]. Not usable as a component.
- **"Piano Precision"** (Yucong Jiang, ISMIR 2021 late-breaking demo): a prototype that records multiple takes and visualises tempo, loudness and articulation rather than colouring wrong notes. It targets students who already hear their wrong notes [confirmed: <https://archives.ismir.net/ismir2021/latebreaking/000036.pdf>]. Philosophically closest to this project; no public release found.
- **Commercial apps** (Wolfie, Hanon Pro, Simply Piano, etc.) advertise mistake-tolerant tracking and accuracy scores [reported marketing]. They conflict with the anti-goal and are not studied further.

### 2.3 Is online following of *practice* solved?
**No** [confirmed by Rach3 authors' own framing; the conclusion is mine]. Evidence:
- Benchmarks (Matchmaker 2025, Peter 2025) use complete performances.
- The Rach3 paper (Morsi, Chiruthapudi, Peter, Pilkov, Bishop, Maezawa, Serra, Cancino-Chacón, ISMIR 2025) states that rehearsal data poses challenges "not present in polished performance". Its examples are mistakes, jumps, and "non-compositional repetitions (i.e., playing the same passage repeatedly)". The paper shows that state-of-the-art alignment yields far more insertions and deletions on rehearsals (§2.5).
- Repeat- and skip-aware MIDI HMMs exist (Nakamura 2014). However, no public evaluation was found of them on *real practice logs* with 2-bar loops, hand-separate practice, slow-practice tempo (e.g. 40% of target) and long pauses.

**Recommended approach for MIDI** [speculative design]:
1. **Segment first**. Pauses (e.g. >1.5–4 s; Rach3 used >4 s to separate pieces), long-held sustain-pedal silences and backward jumps cut the stream into *runs*.
2. **Locate each run globally**. Symbolic fingerprinting (Arzt 2012) or a cheap subsequence DTW over pitch/chord sequences finds candidate score positions after a few notes. For hand-separate practice, match against left- or right-hand-only score projections as extra candidates.
3. **Track locally**. Within a run, a forward HMM/OLTW, e.g. Matchmaker `pthmm`/`outerhmm` initialised at the located position, drives the cursor. Allow a "lost" state: show nothing rather than a wrong position.
4. **Re-align offline** once the run ends (seconds later): DualDTW/TheGlueNote on the score window ± margin. All stored analysis uses this offline alignment.
5. **Learn the user's habits**. Restart points within a piece recur, as in Rach3 Figure 5's "progressively longer" segments. A per-piece prior over likely restart positions improves step 2.

---

## 3. Offline alignment

### 3.1 parangonar (CPJKU; Silvan Peter et al.)
- **Licence/maintenance**: Apache-2.0. Frequent releases: 2.0.0 (2024-10), 3.0.0 (2025-06), 3.2.0 (2026-01), 3.3.x (2026-05/08), **3.4.0 (2026-10-09)** [confirmed: PyPI JSON].
- **Matchers** [confirmed: repo README and refs.md]:
  - `AutomaticNoteMatcher` (hierarchical DTW + combinatorial optimisation; Peter et al., TISMIR 6(1) 2023).
  - `AnchorPointNoteMatcher`, used with annotations to build **(n)ASAP**.
  - `DualDTWNoteMatcher` ("default and SOTA"; Peter, ISMIR 2023).
  - `TheGlueNoteMatcher` (transformer note-similarity + DTW; Peter & Widmer, ISMIR 2024).
  - Online: `OnlineTransformerMatcher`, `TOLTWMatcher`, `OLTWMatcher`.
  - `RepeatIdentifier` (MEC 2025, infers which score repeats were taken).
  - `SubPartMatcher`.
  - Audio-to-score matchers (MEC 2026).
- **Accuracy** (TheGlueNote paper, Table 4; 5 pieces: Beethoven Op. 53/iii, Chopin Op. 9/1, 9/2, 10/11, 60; metric = note-match F-score; "Mismatch" = synthetic skips/repeats covering ~20% of notes) [confirmed: <https://arxiv.org/html/2408.04309v1>]:

| Method | Clean F | Mismatch F | Runtime clean / mismatch (s) |
|---|---|---|---|
| Nakamura HMM (AlignmentTool) | 98 | 44 | 152 / 6458 |
| AutomaticNoteMatcher | 92 | 78 | 588 / 808 |
| DualDTWNoteMatcher | 98 | 88 | 96 / 208 |
| TheGlueNote-small + DTW | 98 | 95 | 21 / 31 |

Limitations: only 5 pieces; synthetic mismatch rather than real practice; professional performances.

- **(n)ASAP**: note alignments for ASAP (Foscarin et al., ISMIR 2020), described as >7 M annotated notes and ~100 h of music, the largest fully note-aligned corpus. Created with segment-constrained (anchor-point) matching [confirmed: TISMIR 2023, DOI 10.5334/tismir.149].

### 3.2 Nakamura's Symbolic Music Alignment Tool ("AlignmentTool")
- C++ tool, **MIT licence**, current `AlignmentTool_v240109`. It also offers an older Qt UI and a **web-based visualiser/editor** for correcting alignments [confirmed: <https://midialignment.github.io/demo.html>].
- Pipeline: preliminary HMM alignment → **performance-error detection** (missing, extra and pitch-error notes) → realignment of suspect regions with merged-output HMMs (Nakamura, Yoshii & Katayose, ISMIR 2017) [confirmed].
- partitura can import its outputs (`partitura.io.importnakamura`, "corresp"/match formats) [confirmed: partitura docs]. Used by trompa-align [confirmed].
- Weakness: it degrades badly under large structural mismatch (44% F above) and is slow there. Strength: explicit error labelling and a mature manual-correction UI.

### 3.3 DTW variants and audio
- **synctoolbox** (Müller et al., JOSS 2021; **MIT** code): multiscale / memory-restricted multiscale DTW with chroma and onset features, for high-resolution audio–audio and audio–score sync [confirmed repo/licence].
- **RUMAA** (Chang, Dixon, Benetos, WASPAA 2025): transformer aligning MusicXML *with repeat signs* directly to audio, plus score-informed transcription and mistake detection.
  - Vienna4x22 alignment F: 98.4 without repeats and **98.4 with repeats**. On the repeat condition Nakamura HMM scores 36.4, hDTW 28.2 and GlueNote 12.7. The baselines were given scores *without* unfolded repeats, which explains the collapse.
  - No code release found [confirmed from arXiv HTML].

### 3.4 Aligning fragmented practice (many partial passes) [speculative design]
1. Segment the session log into runs (§2.3).
2. For each run, locate candidate score windows: fingerprint, or chroma/pitch subsequence DTW against the unfolded score; for hand-separate playing, also against per-staff projections.
3. Align the run to the window ± 2 bars with DualDTW or TheGlueNote via `SubPartMatcher`, or AlignmentTool restricted to the window.
4. Accept an alignment only if the match ratio clears a threshold (e.g. ≥60% of performed notes matched) and the time map is monotone. Otherwise mark the run "unaligned/exploratory" and keep it, because noodling is also practice.
5. Output one match file per run plus a run index: score start/end beat, hands, tempo ratio and error counts.

This turns an unsolved online problem into many small, well-posed offline ones. Ground truth for testing comes from the simulator (§9), and real-data validation from Rach3.

---

## 4. Performance analysis

### 4.1 partitura (CPJKU)
- **Apache-2.0**, v1.9.0 (2026-05-25), Python ≥3.10 [confirmed: PyPI].
- Reads and writes MusicXML, MEI, Kern, MIDI and **match** files. The match format is documented in Foscarin, Karystinaios, Peter, Cancino-Chacón, Grachten & Widmer, arXiv:2206.01104 [confirmed].
- `partitura.musicanalysis.encode_performance(score, performance, alignment)` returns per-note-onset `beat_period` (local tempo), `timing` (onset deviation from the tempo curve), `articulation_log` (log ratio of performed to notated duration, tempo-normalised) and `velocity`. The `tempo_smooth` option can be `'average'`, `'derivative'` or a callable. `decode_performance` inverts this to render a performance from parameters [confirmed: API docs].
- `make_performance_features` implements `asynchrony_feature`, `articulation_feature`, `dynamics_feature` and `pedal_feature` [confirmed: API docs].
- Also: `estimate_voices`, `estimate_key`, `estimate_spelling`, `estimate_tonaltension`, note-feature extraction (the Basis Mixer basis functions).
- This is the core of the Python analysis back end.

### 4.2 Expressive performance modelling (Basis Mixer lineage)
- Basis Mixer: Grachten & Widmer (2012), Cancino-Chacón & Grachten (2016), Cancino-Chacón et al. "Computational models of expressive music performance: a comprehensive and critical review", *Frontiers in Digital Humanities* 2018 [reported; standard references].
- Score features are basis functions (dynamics markings, metrical position, pitch, slurs, etc.) predicting tempo, timing, velocity and articulation. The features are mostly in partitura. Key use here: **explain** a learner's deviations in terms of score features. Example: "you slow down at phrase ends roughly like the reference pianists do" [speculative application].

### 4.3 Datasets (score-aligned unless noted)

| Dataset | Content | Licence / access | Use here |
|---|---|---|---|
| MAESTRO v3 | ~199 h of competition performances (Yamaha Disklavier), audio+MIDI, ~7 M notes | CC BY-NC-SA 4.0 [reported] | Reference pianists; transcription training |
| ASAP / (n)ASAP | 222 scores, ~1 000 perfs (MAESTRO subset) with beat/downbeat and note alignments | CC BY-NC-SA (inherits MAESTRO) [reported] | Main simulation substrate; "N pianists" comparisons |
| Batik-plays-Mozart | 12 Mozart sonatas (36 mvts), Roland Batik on computer-monitored Bösendorfer, 102 421 notes, match files + harmony/cadence/phrase annotations | Repo with LICENSE.md (terms not extracted) [confirmed contents] | Links to DCML-style annotations: harmony-aware expression analysis |
| Vienna 4x22 | 4 excerpts × 22 pianists (Bösendorfer SE), revised version with match files | Research use [reported] | Inter-pianist variability, melody lead |
| Magaloff Chopin corpus | Nikita Magaloff, almost all Chopin solo works, Bösendorfer, >300 k notes, error-annotated | Not public [reported] | Literature only. Notable: shows that even a master makes many "errors" (Flossmann et al. 2010) |
| ATEPP | ~1 000 h, 11 677 perfs, 49 famous pianists, 1 580 movements; **transcribed from commercial audio**; MusicXML for ~43% | CC BY 4.0 + disclaimer [confirmed] | "Your rubato vs famous pianists" (caveat: transcription noise in velocity/offsets) |
| Rach3 MIDI | >750 h rehearsal MIDI, 4 pianists (3 advanced, 1 beginner), >4 years, 3 000+ files, MusicXML; silent pianos incl. **Essex EUP-116E** and Yamaha GB1K silent | CC BY 4.0 paper; dataset at r3midi.rach3project.com [confirmed paper] | Real practice: validation of segmentation/alignment |
| PianoVAM | Disklavier amateur practice sessions with audio, MIDI, video, fingering | arXiv 2509.08800 [reported]; fingering labels reportedly not public | Practice behaviour; fingering |
| STPD (Benetos et al. 2012) | 7 Disklavier perfs with annotated missed/extra notes | Research [reported] | Mistake-detection benchmark |

### 4.4 Specific measures and their pitfalls
- **Tempo and timing**: `beat_period` per score onset. Smooth with care, because over-smoothing hides rubato. Present tempo as a ratio to the user's own median tempo for that passage, not to a metronome mark [speculative].
- **Asynchrony / melody lead**: melody notes typically sound ~30 ms early in chords. Goebl (JASA 110, 2001; 22 pianists, Bösendorfer) showed the lead nearly vanishes at finger–key level, so it is largely a **velocity artefact** [confirmed from abstract]. A silent-system's note-on time depends on where the sensor estimates the "strike". So melody lead measured on the adsilent mixes playing technique with sensor model, and comparisons to Bösendorfer/Disklavier data must be relative [speculative].
- **Articulation**: `articulation_log` = log(performed duration / notated duration) after tempo normalisation. On piano, *sounding* duration under sustain pedal differs from *key* duration. Compute both "key articulation" and "sounding articulation" (pedal-extended) [speculative, standard practice].
- **Pedalling**: CC64 is continuous on many digital and hybrid instruments (half-pedal). Whether the adsilent sends continuous values must be verified. Typical analyses:
  - pedal-change timing relative to harmony changes (legato "syncopated" pedalling: release shortly after the new chord's onset);
  - pedal depth;
  - "blurring" index: the number of distinct harmonies sounding under one pedal.
  - partitura's `pedal_feature` is a starting point [confirmed exists].
- **Dynamics from velocity**: MIDI velocity → loudness mapping is instrument-specific and undefined by the MIDI standard. Dannenberg (ICMC 2006) found wide variation across synthesizers and suggested modelling velocity as roughly a square-law amplitude mapping over a ~60 dB range [reported via secondary sources]. Consequences [speculative]:
  - Never compare raw velocities across instruments (adsilent vs Disklavier vs Bösendorfer vs ATEPP transcriptions). Use **within-performance z-scores or ranks** (e.g. voice balance as velocity difference within a chord) and calibrate the adsilent once against a recorded acoustic level if absolute dynamics matter.
  - ATEPP velocities are *estimated* by a transcription model, so they are less reliable.
- **Release velocity**: rarely analysed in the literature. If present, it could inform "how the key was released" for articulation teaching [speculative].

### 4.5 Errors vs expressive deviation
- **Pitch-level errors are well defined given a score**:
  - *missed* = score note unmatched;
  - *extra* = performed note unmatched;
  - *substitution* = a pitch near an unmatched score note in the same onset cluster.
  - Alignment tools already output these: AlignmentTool explicitly labels missing, extra and pitch errors; parangonar marks deletions and insertions [confirmed].
  - Caveats: ornament realisations (trills, grace notes), score editions and repeats generate false "errors". TheGlueNote and RUMAA show that repeat-awareness matters.
- **Timing and dynamics have no ground truth.** A deviation is only "error-like" when it is an outlier with respect to:
  - the learner's own consistent intention across passes;
  - the reference distribution of pianists;
  - local context (a hesitation preceding a missed note).
  - This framing (consistency and outlierness, not deviation from deadpan) is the operational form of "rubato is not error" [speculative design principle].
- **Mistake detection literature**:
  - Benetos, Klapuri & Dixon, "Score-informed transcription for automatic piano tutoring" (EUSIPCO 2012, introduced STPD) [reported].
  - Ewert, Wang, Müller & Sandler, "Score-informed identification of missing and extra notes in piano recordings" (ISMIR 2016) [confirmed exists].
  - Wang, Ewert & Dixon (IEEE/ACM TASLP 2017, score-informed dictionary learning) [reported].
  - On STPD, RUMAA reports F_extra 89.2 / F_missed 95.3, vs Wang 84.9 / 92.6 and Ewert 77.0 / 94.5 [confirmed from RUMAA Table 4]. Audio domain, tiny dataset.
  - **Polytune** (Chou et al., AAAI 2025; code at github.com/ben2002chou/Polytune): end-to-end audio+score error detection. 64.1% average error-detection F1 across 14 instruments on *synthetic* error datasets [confirmed from abstract].
  - Morsi et al., "Sounds out of Pläce? Score-independent detection of conspicuous mistakes in piano performances" (ISMIR 2023). A TCN that detects mistakes without a score. In the Rach3 replication with synthetic mistakes: F1 0.445 (P 0.400, R 0.528) [confirmed: Rach3 §7]. **Score-free mistake detection is weak**. With MIDI and a score, symbolic alignment is far more reliable.

---

## 5. Practice-behaviour analysis

- **Classic studies** (manual, small-N):
  - Miklaszewski (1989), case study of a pianist preparing a Debussy prelude from video.
  - Chaffin & Imreh, "Practicing perfection" (2002 book; *Psych. Science* 2005; "Pulling teeth and torture", 1997). Over 58 sessions of a concert pianist learning Bach's Italian Concerto Presto, they found that **where practice segments start and stop** tracks formal structure and "performance cues".
  - Gruson (1988/2001): beginners repeat single notes, experts repeat musically coherent units.
  - Miksza (2011 review) and How, Tan & Miksza (2022 PRISMA review) note that no study used >40 h of rehearsal recordings [confirmed via Rach3 references and text].
  - **Implication**: restart and stop locations are a *validated* window into a learner's mental representation of the piece. This is exactly what MIDI logs can measure automatically.
- **Computational work**:
  - Winters, Gururani & Lerch, "Automatic practice logging" (ISMIR 2016): 34 h of annotated piano practice audio; chroma + DTW to identify the piece being practised [confirmed].
  - Sokolovskis, Herremans & Chew (Frontiers in Psychology 2018): interface for graphical analysis of practice behaviours [confirmed exists].
  - **Rach3** (ISMIR 2025) is the state of the art for MIDI. It does piece identification by symbolic fingerprinting (F1 0.989 weighted), cuts multi-piece files at >4 s silences, and does **rehearsal structure analysis** with cross-similarity (score vs rehearsal) and self-similarity matrices over 100 ms "chord bins" with a Bernoulli pitch-profile likelihood. Diagonals are grouped into equivalent segments.
    - Figure 5 shows recognisable strategies: progressively longer repetitions of a segment, practising an ending repeatedly, full run-throughs.
    - There is **no quantitative evaluation yet** (annotation planned), and hyper-parameters such as the chord-bin Δt are "hard to tune" [confirmed].
  - Cancino-Chacón & Pilkov, "The Rach3 dataset: towards data-driven analysis of piano performance rehearsal" (MMM 2024) [confirmed exists].
- **Conclusion**: automatic segmentation of MIDI practice into runs and repetitions is **feasible but immature**. Reuse Rach3's pipeline ideas. Own the evaluation by simulating with known ground truth, and hand-annotate a few hours of the user's own practice later [speculative].

---

## 6. Fingering, difficulty, physical modelling

- **PIG dataset** (Nakamura, Saito & Yoshii, "Statistical learning and estimation of piano fingering", *Information Sciences* 517, 2020; arXiv:1904.10237): 150 pieces with fingerings by multiple pianists. Licence: research, non-commercial [reported; the project page at beam.kisarazu.ac.jp returned 404 during this check].
  - High-order HMMs were found best at the time. Match rates against human fingerings are modest (on the order of 60–70% "general match rate"), partly because humans disagree [reported from memory of paper; verify].
- **Later models**:
  - Ramoneda, Jeong, Nakamura, Serra & Miron, "Automatic piano fingering from partially annotated scores using autoregressive neural networks" (ACM MM 2022). ArLSTM and ArGNN (GNN for polyphony) with beam search, plus **ThumbSet** (2 523 pieces, crowdsourced, partial and noisy fingering). They outperform HMM and RNN baselines [confirmed from abstract; numbers not extracted].
  - Pitch-difference fingering matching (EURASIP JASMP 2022) [confirmed exists].
  - RL fingering (2021) [confirmed exists].
  - Joint hand-and-finger detection from MIDI (arXiv:2609.28787, 2026, PIG 130/10 splits) [reported].
- **Difficulty** (Ramoneda et al.):
  - *Mikrokosmos-difficulty* and fingering-based difficulty (ICASSP 2022) [reported].
  - **CIPI** ("Can I play it?"): 652 MusicXML scores with Henle difficulty levels 1–9, used for multi-dimensional difficulty (pitch, fingering, expressiveness embeddings) (*Expert Systems with Applications* 238, 2024). CC BY-NC-SA 4.0, on request via Zenodo [confirmed].
  - **PSyllabus**: 7 901 pieces, 11 levels, audio-based difficulty (IEEE/ACM TASLP 33, 2025). Research use [confirmed].
  - Ramoneda's PhD (UPF, defended April 2026) consolidates this line [reported].
  - Use here: **passage-level** difficulty to explain *why* the user always restarts at bar 23 (a fingering jump), not grading [speculative].
- **Physical / ergonomic modelling**:
  - Parncutt, Sloboda, Clarke, Raekallio & Desain (1997, *Music Perception* 14) proposed a rule-based fingering cost model: stretch, span and weak-finger rules over hand-span tables [reported; standard reference]. Simple to implement and explainable. It can be **parameterised by the user's measured hand span** (comfortable/maximal spans per finger pair).
  - Combined with PIG-trained HMMs, this gives "fingering suggestions that fit your hand" [speculative].
  - Fingering cannot be observed from MIDI. It needs video (PianoVAM-style) or user annotation. Any fingering feature is advisory.

---

## 7. Audio (secondary channel)

- **Transcription SOTA** (MAESTRO v3 test set; mir_eval note metrics; onset tolerance ±50 ms; offset tolerance max(50 ms, 20% of duration); clean Disklavier recordings in a concert-hall setting):

| System | Note F1 (onset) | +offset | +velocity |
|---|---|---|---|
| Onsets & Frames (Hawthorne et al., ICLR 2019) | ~94.8 | — | — |
| Kong et al. (TASLP 2021; PyPI `piano_transcription_inference`; also sustain-pedal detection) | ~96.7 | — | — |
| hFT-Transformer (Toyama et al., ISMIR 2023; Sony) | 97.43 | 90.32 | 89.25 |
| Transkun (Yan & Duan; semi-CRF, NeurIPS 2021; non-hierarchical transformer, ISMIR 2024; `pip install transkun`) | among the best on MAPS | — | — |

  Sources: Onsets & Frames, Kong and hFT [reported; hFT numbers from paper table]; Transkun [reported].
- **Streaming and real-time**:
  - Streaming encoder–decoder with sustain-pedal-consistent offsets (Wei, Zhao, Wu & Yoshii, ISMIR 2024 / arXiv:2503.01362), "comparable to offline SOTA" [reported].
  - "Onsets and Velocities" CNN (Fernandez 2023) aims at affordable real-time [reported].
  - On Apple-silicon CPUs, offline Kong/hFT runs faster than real time for practice-length files. True low-latency streaming (<100 ms) is plausible with the CNN models but **unverified** [speculative].
- **Robustness**: models trained on MAESTRO overfit its acoustics.
  - Edwards, Dixon, Benetos, Maezawa & Kusaka (IEEE SPL 2024) found onset F1 on MAPS (unseen pianos) of 88.4 for their augmented Kong-architecture model, vs Hawthorne 86.4, Kong 82.4, Maman & Bermano 87.3, Toyama 85.1 [confirmed from search extract of paper table].
  - An upright in a domestic room with a microphone will be noticeably worse than MAESTRO numbers. Expect several F1 points lower, and worse for velocity/offsets [speculative].
  - **Basic Pitch** (Spotify, ICASSP 2022, Apache-2.0) is lightweight and instrument-agnostic, but weaker on dense piano textures than piano-specific models [reported]. Not recommended for piano.
  - **Conclusion**: audio is for (a) recordings without MIDI, e.g. a teacher's acoustic piano, and (b) reference recordings. Never for primary analysis when MIDI exists.
- **Reference recordings of famous pianists**:
  - Option A: MAESTRO/ASAP MIDI (competition pianists, real Disklavier MIDI). Best data quality.
  - Option B: ATEPP transcriptions (famous pianists, transcription noise).
  - Option C: the user's own audio files of commercial recordings → transcribe (Kong/hFT/Transkun) → symbolic alignment (DualDTW/TheGlueNote). Alternatively audio-to-score sync with synctoolbox (chroma + onset features, MrMsDTW) when only beat-level tempo curves are needed.
  - Beat-level tempo curves from audio-score sync are the robust core. Note-level velocity from transcribed audio is unreliable for cross-performer comparison [speculative, consistent with §4.4].

---

## 8. Expressive performance rendering (reference interpretations)

- **VirtuosoNet** (Jeong, Kwon, Kim & Nam; ISMIR 2019 / ICML 2019): hierarchical attention RNN from MusicXML to expressive MIDI. Pretrained checkpoint `dasaem/virtuosonet` (HAN+GRU), which the author says **placed 1st in RenCon 2025**. Repo shows no LICENSE file → licence unclear; ask before redistribution [confirmed repo state].
- **ScorePerformer** (Borovik & Viro, ISMIR 2023; github.com/ilya16/ScorePerformer): controllable rendering with fine-grained style controls. Alignment/preprocessing code not released [reported]. PERiScoPe dataset (>35 000 note-aligned pairs, 2025) [reported].
- **Pianist Transformer** (You et al., arXiv:2512.02652, Dec 2025): self-supervised pretraining on 10B MIDI tokens, 135M params, editable workflow. Code and checkpoints on the project page; code licence not stated [confirmed from abstract].
- Others:
  - Peransformer (arXiv:2510.10175).
  - Joint rendering and transcription (arXiv:2509.23878).
  - S2A score-to-audio (ICASSP 2025).
  - DExter (diffusion; Zhang et al. 2024) [reported, not verified this session].
- **RenCon 2025** (ISMIR 2025, Daejeon): 9 entries, online preliminary evaluation plus live rendering. Organisers conclude "significant advances" but not human-level expression (arXiv:2605.02059) [confirmed from abstract].
- **Use in the app** [speculative]:
  - "Deadpan vs rendered vs real pianists" listening comparisons.
  - Rendered performances as **probes** ("here is one plausible shaping"), always shown next to real-pianist distributions, so the model's taste is not presented as the norm.
  - partitura `decode_performance` can render a performance from *user-edited* parameter curves: "hear your own performance with the rubato of bar 12 exaggerated".

---

## 9. Architecture notes

### 9.1 Data pipeline [speculative design]
```
raw_events  (append-only, never edited)
  └─ sessions   (contiguous capture periods; device info, adsilent firmware/settings, calibration id)
       └─ runs/passes   (segmentation: pauses, jumps, restarts → [t_start, t_end])
            ├─ localisation   (piece id, score window, hands, confidence)
            ├─ alignment      (match file per run; aligner name+version+params)
            ├─ features       (partitura encode_performance + perf features, per note & per beat)
            └─ annotations    (user notes/tags, "this was intentional", corrected alignments)
```
- **Raw event record** (JSONL or Parquet):
  - `{seq, t_host_ns (CoreMIDI host time → ns), t_session_s, src ("rtmidi"|"webmidi"|"sim"), port, bytes:[...], decoded:{type, ch, note, vel, cc, val}}`
  - Keep bytes *and* decoded fields. Running-status and 0-velocity note-offs are normalised in `decoded` only.
- **Reconstructed performance**: standard MIDI file per run, with ticks at 1 ms resolution and tempo 500 000 µs/quarter at 480 PPQ ≈ 1.04 ms. This allows exact round-tripping with partitura and AlignmentTool.
- **Alignment**: the **match file format** (partitura reads and writes it; documented in arXiv:2206.01104) is the canonical storage. Also store a JSON projection for the front end: `{score_note_id, perf_note_id|null, label: match|deletion|insertion|ornament}`. Always store **aligner provenance**, so that re-running with a better aligner is a migration, not data loss.
- **Score identity**: score notes carry stable IDs (partitura `note.id`, preserved from MusicXML/MEI `xml:id`). DCML / When-in-Rome / (n)ASAP annotations attach by measure/beat → note IDs.
- **Storage**: SQLite (sessions, runs, metadata) plus files (raw logs, MIDI, match, Parquet features). Local-first; no server database needed.

### 9.2 Browser vs Python split [speculative]

| In browser (TS) | In Python |
|---|---|
| Web MIDI live input (UI only), falling-notes/keyboard view, live "where am I" cursor fed by backend or a light JS follower | Authoritative capture (python-rtmidi), log writing |
| Score rendering (Verovio/OSMD), overlays of analyses | Segmentation, localisation, alignment (parangonar, AlignmentTool), partitura features |
| Interactive charts (tempo ribbons, velocity balance) | Reference corpora indexing ((n)ASAP, ATEPP, Batik), stats |
| Playback via Web Audio / sampler; MIDI out | Transcription of audio (Kong/hFT/Transkun), synctoolbox |
| | Simulator (fake piano), test harness |

The communication link is a WebSocket. The backend pushes `position` (score beat, confidence) at ~20–50 Hz and `run_completed` events with analysis IDs.

### 9.3 Latency budget [speculative]
- Visual note feedback comes straight from Web MIDI: under 10–20 ms after OS delivery.
- The score-position cursor goes via the backend follower: under 100 ms is acceptable because it is not musical feedback.
- Post-run analysis: under 2 s for a 30 s run. DualDTW/TheGlueNote on short windows should be fast. TheGlueNote-small took 21 s for 5 *whole* pieces in its paper.

### 9.4 Simulation and test plan (no physical piano needed) [speculative design]
1. **Fake-piano device**. A Python process creates a CoreMIDI virtual source `PPE-Sim` and replays a MIDI performance in real time, with optional jitter (Gaussian ±1–3 ms) and the adsilent's expected message profile:
   - running status;
   - note-on velocity 0 vs explicit note-off;
   - release velocity on/off;
   - CC64 continuous vs switch-like (0/127);
   - CC67.
   - Both Chrome and the capture daemon consume it. A "speed" factor allows accelerated tests (offline mode bypasses real time).
2. **Practice-behaviour generator**. From an aligned (n)ASAP or Batik performance (ground-truth score↔perf map), synthesise a session:
   - **Fragment selection**: choose passages (2–8 bars) with a bias to "hard" bars (by difficulty proxy or high error rate).
   - **Loops**: repeat a fragment k times, often extending the end ("progressively longer", as observed in Rach3), sometimes restarting mid-bar after an error.
   - **Restarts**: on injected error, stop with probability p, pause 0.5–5 s, restart at the previous phrase start, bar line or same beat.
   - **Tempo**: global slow-practice factor (0.4–1.0) plus within-run drift and rubato copied from the original performance (time-warp, not regenerated).
   - **Hands separate**: drop the LH or RH staff.
   - **Mistakes**: via `piano-synmist` (forward/backward insertion, mistouch, pitch change, drag; per-texture probabilities) [confirmed toolkit], plus own operators: wrong-octave, held-too-long, pedal-late, missing note in chord.
   - **Noise**: noodling between runs (unrelated notes), page-turn pauses, metronome-free count-ins.
   - **Output**: MIDI stream plus a ground-truth JSON giving run boundaries, the score window for each run, the injected mistakes with IDs, and the true alignment.
3. **Metrics**:
   - **Segmentation**: run-boundary F1 with ±0.5 s tolerance.
   - **Localisation**: score-window IoU (in beats); % runs located within 1 bar; time-to-lock (notes needed).
   - **Online follower**: % of time the cursor is within 1 beat; *false-confidence rate* (confident but wrong, the most harmful failure); recovery time after a jump.
   - **Alignment**: note-match F (as in parangonar papers); separate F for injected-error regions.
   - **Mistake detection**: P/R/F per class (missed, extra, substitution); false-error rate on *clean* runs of expressive performances. This is a key anti-goal guard: expressive timing must produce zero "errors".
   - **Expression stability**: features (tempo curve, velocity balance) of a clean run vs the same run with injected pitch mistakes should differ little. This tests that alignment errors do not leak into expressive analysis.
4. **Corpora for testing**:
   - Synthetic sessions from (n)ASAP/Batik/Vienna4x22: ground truth by construction.
   - **Rach3 MIDI**: real practice, including an Essex EUP-116E silent piano. Qualitative validation and hand-annotated subsets.
   - Later, the user's own sessions, with a 1–2 h hand-annotated gold set.
5. **Capture characterisation on arrival** (one evening):
   - (a) Log every message type the adsilent emits.
   - (b) Check whether CC64 is continuous: depress slowly and count distinct values.
   - (c) Check whether release velocity varies.
   - (d) Velocity range per key at fixed playing intent (velocity-curve settings).
   - (e) Run Chrome and Python simultaneously and compare timestamps on the same events.
   - (f) Long-run stability (USB sleep, reconnects). Hot-plug handling: Web MIDI `statechange`, rtmidi port polling.

---

## 10. Ideas: performance-analysis features that respect expression
Each item lists feasibility (F), evidence (E) and risk (R). All [speculative] as product ideas.

1. **"Your rubato vs N pianists" ribbon.** Plot the beat-level tempo curve of the user's best recent pass over the inter-quartile band of (n)ASAP/MAESTRO/ATEPP performers of the same piece. Tempo is normalised to each performance's median, so only *shape* is compared.
   - F: high for (n)ASAP pieces (alignments exist); medium for ATEPP (needs alignment).
   - E: inter-pianist variability studies (Vienna 4x22; Repp's analyses).
   - R: implying the band is "correct". Mitigate by also showing outliers by famous pianists and wording it as "range of choices".
2. **Restart heat-map ("where you always stop").** Mark the score positions where runs start and end across sessions, coloured by recency. Chaffin's work suggests these align with structural boundaries *or* with technical trouble spots. Classify each spot as "structural" (phrase or cadence boundary from DCML/WiR annotations) vs "technical" (mid-phrase, high-error).
   - F: high once runs are segmented.
   - E: Chaffin & Imreh 2002/2005; Rach3 Fig. 1/5.
   - R: segmentation errors. Show confidence.
3. **Practice-strategy timeline.** For each session, show the structure: blocks of looped segments, progressively lengthening segments, run-throughs (cf. Rach3 Fig. 5). It answers "how did I practise?" without judging.
   - F: medium. E: Rach3; Gruson (beginners repeat notes, experts repeat units). R: over-interpretation.
4. **Voicing-balance meter.** Per chord, the velocity difference between the melody (top voice or annotated voice via `estimate_voices`) and the accompaniment, as a within-performance z-score, compared across the user's passes and reference pianists.
   - F: high (MIDI velocity).
   - E: melody-lead / voicing literature (Goebl 2001; Repp 1996).
   - R: velocity calibration differs across instruments. Use relative measures only.
5. **Pedal–harmony mismatch detector.** Using harmony annotations (DCML / When in Rome) or estimated harmony, flag places where the sustain pedal is held across a harmony change *and* the overlapping sounding notes form a strongly dissonant blend. Also flag "pedal released before the new bass sounds" (gaps).
   - F: medium. It needs reliable CC64 and annotations. E: pedagogy of syncopated pedalling; partitura `pedal_feature`.
   - R: intentional blurring (Debussy, Beethoven Op. 31/2 recitative). Make it a question ("intended?"), never an error, and suppress where the score marks pedal.
6. **Consistency map (intention vs accident).** Across many passes of the same bar, compute the variance of timing and dynamics shape after removing global tempo. Stable deviations are *intentions*; highly variable ones may be uncontrolled. This is the operational substitute for an "accuracy score".
   - F: high once passes are aligned. E: expert performers reproduce expressive timing highly consistently (Repp; Palmer). R: early learning is inconsistent by nature. Show trends, not grades.
7. **Hesitation detector.** Detect local onset delays that precede pitch errors or occur at hand-position shifts. They are distinguished from rubato because they are (a) not reproduced across clean passes, (b) not phrase-aligned, and (c) co-occur with the next-note error or with a large hand displacement.
   - F: medium. E: error-related slowing is well known in motor performance. R: false positives on genuine agogic accents. Show only aggregated over passes.
8. **"Hear your shaping, exaggerated or neutralised."** Use `decode_performance` to resynthesise the user's pass with (a) their tempo/dynamic deviations scaled ×1.5, (b) flattened to deadpan, (c) transplanted with a reference pianist's tempo curve. It builds listening awareness rather than correctness.
   - F: high (partitura). E: Basis Mixer / decode tools. R: synthetic piano sound quality. Use a good sampler.
9. **Articulation profile: key vs sounding duration.** Compare legato overlap (key-level) with what was actually heard (pedal-extended), e.g. "your legato in the right hand comes from the pedal, not the fingers".
   - F: high with continuous CC64. E: articulation ratio literature; partitura articulation features. R: none serious. It is informational.
10. **Slow-practice transfer tracker.** For a passage practised at slow tempo, track how its timing/dynamic shape and error rate change as tempo rises toward the target. Show whether *shape* is preserved (good transfer) or collapses.
    - F: medium-high. E: practice research on tempo progression is mixed. R: none serious, beyond the claim that "transfer" is causal. Keep it descriptive.
11. **Difficulty-explained trouble spots.** Combine the user's error and restart heat-map with a passage difficulty decomposition: fingering-cost (Parncutt-style, parameterised by the user's hand span), pitch-entropy and polyphony (Ramoneda-style dimensions). This explains *why* a spot is hard and suggests targeted exercises.
    - F: medium. E: CIPI/Mikrokosmos-difficulty; Parncutt 1997. R: fingering is unobserved. The model may assume the wrong fingering, so let the user enter fingerings.
12. **Phrase-arch fitting.** Fit the classic tempo/dynamic "arch" (Todd's phrase-arch model) to annotated phrases. Show where the user shapes phrases and where they play flat or with opposite curvature, next to reference pianists.
    - F: medium; phrase annotations exist for Batik/Mozart (Annotated Mozart Sonatas).
    - E: Todd 1992; Widmer & Tobudic 2003 multilevel phrase decomposition.
    - R: the normative risk that arch = good. Frame it as a "lens".
13. **Melody-lead and chord-spread fingerprint.** Within-chord onset spread and melody lead per passage, compared across the user's passes and across pianists. Spread chords can be stylistic.
    - F: high. E: Goebl 2001; Vienna 4x22.
    - R: as Goebl showed, lead is largely a velocity by-product, and adsilent sensing timing is unknown. Use relative comparisons only (§4.4).
14. **Post-mistake recovery profile.** After a wrong or missed note, how many beats until tempo and dynamics return to the user's normal shape for that passage? Do they stop, restart, or play through? It is useful for performance preparation ("play-through practice") without counting mistakes.
    - F: medium. E: Rach3 mistake/rehearsal framing; Chaffin's performance cues. R: low.
15. **Session "map of attention" against harmonic structure.** Overlay time spent per bar on the DCML/When-in-Rome harmonic and formal annotation, e.g. "you practised the development 4× more than the recapitulation; the retransition was never practised slowly".
    - F: high once runs are localised. E: Chaffin (structure-guided practice). R: none beyond presentation.

---

## 11. Open questions / to verify
- adsilent model/version: does it send release velocity, continuous CC64, CC67? Is note-on timing hammer-model-based? (Measure; §9.4 step 5.)
- Matchmaker MIDI-input benchmark numbers (the paper tables extracted were audio). Check the repo's evaluation scripts or ask the authors.
- Licences: VirtuosoNet (no LICENSE file), piano-synmist (LICENSE file not read), Batik (LICENSE.md not read), PIG (terms page unreachable), hFT-Transformer and Transkun repos.
- Rach3 MIDI dataset terms and download access (paper says openly available via r3midi.rach3project.com).
- Chromium's current macOS MIDI timestamp path (verified only in an older Chromium tag); measure jitter locally.

## 12. Key sources
- W3C Web MIDI API WD: <https://www.w3.org/TR/webmidi/>; Chrome permission change: <https://developer.chrome.com/blog/web-midi-permission-prompt>; Firefox gating: <https://bugzilla.mozilla.org/show_bug.cgi?id=1796191>; Safari status: <https://caniuse.com/webmidi>, <https://bugs.webkit.org/show_bug.cgi?id=107250>; Chromium CoreMIDI timestamps: <https://chromium.googlesource.com/chromium/src/+/61.0.3154.1/media/midi/midi_manager_mac.cc>
- WebMIDI.js: <https://github.com/djipco/webmidi>; python-rtmidi: <https://pypi.org/project/python-rtmidi/>; mido: <https://mido.readthedocs.io/>
- Matchmaker: <https://github.com/pymatchmaker/matchmaker>, paper <https://arxiv.org/abs/2510.10087>
- parangonar: <https://github.com/sildater/parangonar>; TheGlueNote: <https://arxiv.org/abs/2408.04309>; (n)ASAP: <https://doi.org/10.5334/tismir.149>; Peter et al. SMC 2025: <https://arxiv.org/abs/2505.05078>; repeat inference: <https://arxiv.org/abs/2505.05055>
- Nakamura AlignmentTool: <https://midialignment.github.io/demo.html>; ISMIR 2017 paper: <https://archives.ismir.net/ismir2017/paper/000035.pdf>; outer-product HMM: <https://arxiv.org/abs/1404.2313>; AR-HSMM: <https://ismir2015.uma.es/articles/15_Paper.pdf>
- Arzt & Widmer any-time tracking: <https://www.cp.jku.at/research/papers/Arzt_Widmer_STAIRS_2010.pdf>; ACCompanion: <https://www.ijcai.org/proceedings/2023/0641.pdf>; Piano Precision: <https://archives.ismir.net/ismir2021/latebreaking/000036.pdf>
- Rach3 MIDI dataset paper (ISMIR 2025): <https://www.jku.at/fileadmin/gruppen/173/Research/Rach_3_Project/MorsiEtAl-ISMIR-2025.pdf>, Zenodo <https://zenodo.org/records/17811417>; piano-synmist: <https://github.com/Alia-morsi/piano-synmist>; Automatic practice logging: <https://archives.ismir.net/ismir2016/paper/000181.pdf>
- partitura: <https://partitura.readthedocs.io/>; match format: <https://arxiv.org/abs/2206.01104>
- RUMAA: <https://arxiv.org/abs/2507.12175>; Polytune: <https://arxiv.org/abs/2501.02030>; Ewert et al. ISMIR 2016: <https://archives.ismir.net/ismir2016/paper/000123.pdf>; STPD: <https://code.soundsoftware.ac.uk/projects/score-informed-piano-transcription-dataset>
- Datasets: ATEPP <https://github.com/BetsyTang/ATEPP>; Batik-plays-Mozart <https://github.com/huispaty/batik_plays_mozart>; PianoVAM <https://arxiv.org/abs/2509.08800>
- Goebl 2001 melody lead: <https://iwk.mdw.ac.at/goebl/papers/Goebl_JASA2001_melodyLead.pdf>
- Fingering/difficulty: PIG paper <https://arxiv.org/abs/1904.10237>; ArGNN/ThumbSet <https://repositori.upf.edu/items/aeb2d608-a144-4e86-a4af-0c348f24af80>; CIPI <https://arxiv.org/abs/2306.08480>; PSyllabus <https://arxiv.org/abs/2403.03947>
- Transcription: hFT-Transformer <https://arxiv.org/abs/2307.04305>; robust AMT (Edwards et al.) <https://arxiv.org/abs/2402.01424>; streaming AMT <https://arxiv.org/abs/2503.01362>; Transkun <https://github.com/Yujia-Yan/Transkun>; synctoolbox <https://github.com/meinardmueller/synctoolbox>
- Rendering: VirtuosoNet <https://github.com/jdasam/virtuosoNet>; ScorePerformer <https://github.com/ilya16/ScorePerformer>; Pianist Transformer <https://arxiv.org/abs/2512.02652>; RenCon 2025 <https://arxiv.org/abs/2605.02059>
