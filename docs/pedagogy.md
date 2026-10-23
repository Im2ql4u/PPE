# Pedagogy: design principles from the evidence

Digest of `research-notes/pedagogy-evidence.md` (full citations, effect sizes and caveats there), with additions from `research-notes/llm-symbolic-ai.md` §5 and `research-notes/visualization-hci-improvisation.md` §8.
Grades: **S** strong · **M** moderate · **W** weak · **Sp** speculative. "Strong" means strong *for this literature*: mostly small samples, students and children, 24–48 h retention.

## Principles the app is built on

| # | Principle | Grade | How the app implements it |
|---|---|---|---|
| P1 | **Measure learning with cold, unassisted probes** (next session, no aids), not end-of-session accuracy | S | Cold probes (C6) are the canonical measure; no in-session scores |
| P2 | **Analyse practice behaviour, not hours or % correct.** Effective practisers locate the exact error, fix it there, vary tempo, and repeat until stable (Duke et al. 2009, N = 17) | M | Mirror: restart map, strategy timeline, consistency map (D2–D4) |
| P3 | **Terminal, summary, bandwidth feedback**; concurrent visual feedback off by default | M | Feedback appears after a take; only deviations beyond tolerance |
| P4 | **Fade guidance** and schedule "blind takes" | M | Probes alternate aided and unaided passes |
| P5 | **Predict before reveal**: pretesting helps even when the answer is wrong; unguarded AI help can harm exam performance (Bastani 2025) | S (pretesting), M (AI) | State machine in every lens and in the tutor (C1, E-series) |
| P6 | **Functional, in-context ear training** (scale degrees, function in progressions), in piano timbre first, then varied | M | Repertoire-derived probes (C2, C5) |
| P7 | **Train inner hearing explicitly**: audiation predicts sight-reading; aural training is among the few interventions that improve it (small effects) | M | Audiation probes (C4); "hear in your head, then play" |
| P8 | **Couple notation, key action and sound** with low latency: audio-motor maps form within about 20 minutes of practice | M | Every visual is playable; < 20 ms sampler target |
| P9 | **Build structural memory**: sections, cadences, performance cues; start from any cue | M | Structure map (A6), cue-start drills (C7) |
| P10 | **Space practice across days**; interleave once material is minimally playable; block when brand new | S (spacing), mixed (interleaving for performance), M (interleaving for perceptual categories) | Scheduler with an *exposed* block/interleave ratio, tested on the user (D7) |
| P11 | **Interleave confusable perceptual categories** (chord qualities, functions) even though it *feels* worse | M | Minimal-pair ABX mixes confusables |
| P12 | **Discount watching**: demonstrations create an illusion of skill; require production after each demonstration | M | "Play it" follows every "hear it" |
| P13 | **Improvisation as imitate → vary → recombine → generate** | M (descriptive), W (pedagogy) | Improvisation track (F-series) |
| P14 | **Learner control for motivation, not efficiency** (self-control gains shrink to about zero after bias correction) | M / W | User chooses passages; the app doesn't claim this speeds learning |
| P15 | **Learner-built representations beat watched ones** (listening maps) | M | User analysis as a lens; draw-your-own tension; mark your own form |
| P16 | **Make the learning/performance gap visible** to counter metacognitive illusions | Sp | Calibration: predicted vs actual cold-probe results (D8) |

## What the evidence does *not* support (so the app treats these as experiments)

- Rhythmic-variant practice, slow practice per se, hands-separate practice: staples without controlled studies. **n-of-1 candidates (D7).**
- Spaced repetition for *motor-harmonic* patterns: plausible, untested.
- Geometric harmony views (Tonnetz etc.) for learning: no outcome evidence.
- Absolute-pitch training for adults: low yield (6 of 43 reached criterion after 12–40 h).
- Sleep-specific consolidation gains: contested. What holds is that end-of-session performance underestimates learning.

## n-of-1 method (for D7 and for testing the app's own premises)

Alternating-treatment designs over many matched passages. Pre-registered metric and window. Cold next-day and 7-day probes. Outcomes from MIDI: errors via alignment, IOI variability, hesitations, time-to-criterion. Randomisation tests or hierarchical models. Expect to detect only large effects. Details: pedagogy-evidence §11.
