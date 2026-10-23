# E3: a playable reduction ladder from expert labels (*Clair de lune*)

**Question.** Can a "harmonic X-ray" (surface → chord tones → structure → outer voices) be computed *deterministically from expert harmony labels*, without an automatic analyser? Does it hold up on Debussy, where added notes, planing and non-functional chords stress tertian labels?

**Input.** DCML `debussy_suite_bergamasque`, `l075-03_suite_clair`: notes and harmonies TSV, 150 expert labels (DCML standard v2.3.0).

**Run.** `uv run python experiments/e3_reduction_ladder/ladder.py`. Writes four MIDI files (one per level) and a piano-roll figure to `out/`. Other DCML pieces: `ladder.py <repo_dir> <stem>`.

## Levels

| Level | Definition |
|---|---|
| L0 surface | every note |
| L1 label tones | notes whose *spelled* pitch (line-of-fifths TPC, not just pitch class) the label accounts for: chord tones, suspensions/retardations, added tones, plus the structural chord |
| L2 structural | root + chord-type intervals only, without suspensions or added tones |
| L3 outer voices | per harmony span: the lowest and highest structural note, sustained |

## Results (2026-10-23)

- **94.3%** of the 1,558 note attacks are accounted for by the expert label at their onset (L1). **86.5%** are structural chord tones (L2).
- The remaining 5.7% (passing and neighbour notes, appoggiaturas) cluster in mm. 23, 33, 41–42, 7, 18, 56, 21.
- Visual check of the piano roll for mm. 1–16 (`out/l075-03_suite_clair_ladder.png`): L2 keeps the parallel-chord texture readable. L3 gives a clean soprano–bass frame that can be sung.
- **Data subtlety found:** for labels where a suspension displaces the root (e.g. `ii(2)`, `I6(2)`), DCML's derived `chord_tones` column omits the displaced root, even though the root keeps sounding (the E♭ octave bass in m. 15). A naive "is this note in `chord_tones`" test therefore marks the bass as unexplained. Fix: L1 = label tones ∪ structural tones. Any code consuming DCML `chord_tones` must handle this.

## Interpretation

- A first-version "harmonic X-ray" needs **no ML** wherever expert labels exist. The reduction is deterministic and inherits its authority, and its debatable points, from the named analyst.
- Debussy's harmony is more label-reducible under the DCML scheme than expected. This says as much about the annotation standard (which can encode added notes and changes) as about the music. Planing passages labelled as a sequence of chords are "explained" chord by chord, even though a listener may hear them as one coloured line. **The ladder can show what an analysis claims, not whether the claim is the best hearing.** That belongs in the UI copy.
- L3 is a direct implementation of Lehne et al.'s (2013) outer-voice reduction, which preserved perceived tension in Mozart and Mendelssohn (see `docs/research-notes/cognition-and-models.md` §2.5). Testing that on Debussy would be an n-of-1 listening probe, not something we can claim.

## Limits

- One piece. MIDI rendering is deadpan at a fixed tempo (♩ = 50). No pedal.
- L3 takes extremes per label span. For long spans with registral leaps this flattens real voice motion. A voice-separation step (partitura `estimate_voices` or notated voices) would be better.
- No deeper levels (prolongation, Schenkerian background): those would need hand-made analyses or flagged model hypotheses.
