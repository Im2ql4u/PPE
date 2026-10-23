# E2: How often do expert harmonic analyses agree?

**Why.** Automatic Roman-numeral analysis is usually reported as accuracy against *one* reference analysis (e.g. ≈ 0.58 strict accuracy for the best 2026 model, see `docs/ecosystem-research.md` §C.3). Without knowing how often *experts* agree under a similar metric, that number can't be interpreted. The When in Rome meta-corpus holds 339 pieces with two or more independent analyses. This experiment measures their agreement.

**Run.** `uv run python experiments/fetch_data.py when_in_rome && uv run python experiments/e2_expert_agreement/agreement.py && uv run python experiments/e2_expert_agreement/summarize.py`. Takes about 12 minutes. Output goes to `out/` (gitignored): `pairs.csv`, `diffs.csv`, `summary.md`.

## Method

- Every file `analysis_X.txt` is compared with the same piece's `analysis.txt` (343 pairs). 22 files failed to parse in music21 (listed in `out/failures.csv`).
- Analyses are parsed with music21's RomanText parser. Each label becomes (local key, chord pitch-class set, root, bass).
- **Alignment by (measure number, offset within measure)**, sampled every sixteenth note, over measures present in both analyses. An earlier version aligned by absolute time. That produced false disagreement wherever files encoded an anacrusis differently (e.g. Mozart K. 284/iii: agreement 0.07 → 0.71 after the fix). A measure-number shift of −1/0/+1 is also tried per pair, keeping the best by chord agreement. Only 2 pairs used a shift.
- Pairs whose total lengths differ by more than 5% are excluded (14 pairs): likely different repeat handling.

**Metrics** (fraction of shared duration on which the two analyses agree):

| Metric | Agree when |
|---|---|
| key | same local tonic pitch class and mode |
| chord pcs | same set of chord pitch classes (ignores key, label spelling, inversion) |
| root / bass | same root / bass pitch class |
| triad core | same root, third and fifth (ignores sevenths and extensions) |
| strict | key **and** chord pcs **and** bass all agree |

"Strict" is our closest analogue to the ML "Roman numeral" metric (key + degree + quality + inversion). Differences: we compare sounding pitch content, so `V/V` vs `II` (same chord, different name) counts as agreement here, while an ML label comparison might not. Sampling is time-weighted, not onset- or note-weighted.

## Results (2026-10-23, final run)

| Pair type | n pairs | key | chord pcs | strict (time-weighted) | median strict per piece |
|---|---|---|---|---|---|
| TAVERN encoder a vs b (Beethoven and Mozart variations; designed double annotation) | 27 | 1.00 | 0.93 | **0.89** | 0.91 |
| Bach chorales: individual analysts vs BCMH corpus | 100 | 0.97 | 0.93 | **0.90** | 0.92 |
| Beethoven sonatas: When in Rome main vs Tymoczko ("DT") | 32 | 0.93 | 0.96 | **0.88** | 1.00 |
| Mozart sonatas: DCML vs 16 named theorists | 45 | 0.93 | 0.88 | **0.78** | 0.79 |
| Beethoven sonatas: main vs DCML | 49 | 0.83 | 0.85 | **0.71** | 0.80 |
| Corelli trio sonatas: DCML vs "Tymoczko and his computer" | 41 | 0.81 | 0.79 | **0.64** | 0.62 |
| Chopin mazurkas: DCML vs "Tymoczko and his computer" | 28 | 0.72 | 0.72 | **0.53** | 0.59 |
| **All kept pairs** | 329 | 0.90 | 0.89 | **0.79** | 0.85 |
| *Moonlight mvt. 1: BPS (Chen & Su) vs DT* | 1 | 0.78 | 0.83 | **0.66** | |

## Interpretation (with caveats)

1. **Expert agreement on full Roman-numeral readings is far from 100%.** It ranges from about 0.9 (chorales, a designed double annotation) down to 0.5–0.6 (Chopin mazurkas, chromatic Romantic repertoire). Key-relative disagreement (tonicisation vs. modulation) is a large component: compare the "key" and "chord pcs" columns.
2. **The best 2026 model's ≈ 0.58 strict accuracy should be read against this ceiling.** On the Romantic-piano part of its benchmark (DCML's Distant Listening Corpus), the comparable human–human figure in our data is roughly 0.5–0.7. So the model is not obviously far below inter-expert agreement there. **This is suggestive, not a like-for-like comparison:** different pieces, granularity, metric details and label normalisation. A proper comparison would score the model against *both* analyses of the same pieces (e.g. "agrees with at least one expert").
3. **Some "DT" analyses are partly computer-generated** ("Dmitri Tymoczko and his computer"). The Corelli and Chopin rows are therefore human-vs-semi-automatic. The Mozart (16 named theorists) and TAVERN rows are the cleanest human-vs-human estimates.
4. **Residual artefacts depress the low tail.** In the Beethoven main-vs-DCML group the 10th percentile is 0.36. Inspecting the worst pair (op. 10/3/i) shows the *same figures in different keys* (A major vs F♯ minor) over 100+ bars. That looks like a key-conversion artefact in one converted file, not a musical disagreement. Per-piece medians are more robust than the time-weighted means. Treat group means as lower bounds.
5. For the project: **disagreement is common and structured, and it concentrates where the music is ambiguous** (Moonlight: m. 4 granularity, m. 12 tonicisation, mm. 15–16 key frame, mm. 32–39 ♭9 as chord tone or not; see E1 for the note-level map). That supports "lenses that argue" as a core design principle rather than an edge case.

## Limits

- RomanText conversions of DCML labels were made by When in Rome's converter. Conversion errors are attributed to "experts" here.
- music21's handling of edge cases (`Ger4/3`, `Cad64`, `[no3][add4]`) affects chord-pc sets. We did not audit label by label.
- The 22 parse failures and 14 length-mismatched pairs are excluded, possibly not at random (more complex pieces).
