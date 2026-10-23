# Reference repertoire and data coverage

The user's *Piano Anthology, Vol. I* (2026; nine works "arranged for study and performance"; PDF in the repo root, not committed) lists the pieces they intend to learn, short and long term.
These are the project's **reference pieces**: test cases for every subsystem, not its boundary.

Coverage checked 2026-10-23 against the local When in Rome clone, the DCML Distant Listening Corpus README, the (n)ASAP `metadata.csv`, and the MAESTRO v3 metadata CSV.

| # | Piece | Expert harmony analysis | Machine-readable score | Aligned reference performances | Notes |
|---|---|---|---|---|---|
| 1 | Bach, Prelude in C, BWV 846 (WTC I) | **When in Rome** `WTC_I/01/analysis.txt` (Mark Gotham, "manually, through judicious automation, and in collaboration with colleagues and students"), plus an AugmentedNet automatic analysis for comparison | Many (kernscores, OpenScore/MuseScore, ASAP MusicXML) | **(n)ASAP** `Bach/Prelude/bwv_846`: MusicXML score + MAESTRO performances with note alignments | Best-covered piece: score, expert and automatic analysis, and professional performances aligned note by note. A one-voice-texture arpeggio piece, so an ideal first test of reduction (it *is* an arpeggiated chorale). |
| 2 | Chopin, Prélude in E minor, op. 28/4 | **None found** (When in Rome has only op. 28/20; DCML has none) | Public domain. Sources to find (OpenScore, kernscores) | MAESTRO has two "24 Preludes" sets (whole-cycle recordings; no ASAP alignment) | A famous case of chromatic voice-leading whose harmony is notoriously ambiguous (published analyses differ widely). A natural candidate for the user's *own* analysis compared with an automatic draft. |
| 3 | Tiersen, *Comptine d'un autre été* | None | Only the user's arrangement (copyright) | None | Diatonic loop harmony. Automatic analysis is reliable here, and the loop structure makes it the obvious **improvisation bridge** piece. |
| 4 | Tiersen, *La Valse d'Amélie* | None | Only the user's arrangement (copyright) | None | As above. Waltz texture. |
| 5 | Beethoven, op. 27/2 i ("Moonlight") | **Two analyses** in When in Rome (BPS: Chen & Su; DT: Tymoczko). They agree 0.66 (strict, E2) | DCML `14-1` (MuseScore, no labels); Sapp `sonata14-1.krn` | None for mvt. 1 ((n)ASAP has only mvt. 3) | Used in E1/E2. |
| 6 | Liszt, Consolation No. 3, S. 172 | None (DCML Liszt covers *Années* only) | Public domain. Sources to find | None found | Note: DCML's Années de pèlerinage annotations give Liszt style data for comparison. |
| 7 | Debussy, *Clair de lune* | **DCML** (150 labels, cadences, phrases); also converted in When in Rome | DCML `l075-03_suite_clair` (MuseScore) | MAESTRO has one *Suite bergamasque* (not aligned) | Used in E3. 94% of note attacks explained by the labels. |
| 8 | Rachmaninoff, Concerto No. 2, ii (solo arrangement) | None (DCML `rachmaninoff_piano` covers solo pieces, not this) | Only the user's arrangement | None (arrangement) | Long-term piece. The arrangement makes all external data inapplicable. |
| 9 | Chopin, Fantaisie-Impromptu, op. 66 | None | Public domain. Sources to find | **Not in MAESTRO v3 or (n)ASAP** | Long-term piece. Technique-heavy (4-against-3 polyrhythm), so a good test of performance capture and timing analysis. |

## What this means

1. **Expert analyses exist for three of nine pieces** (BWV 846, Moonlight, Clair de lune). Aligned professional performances exist for one (BWV 846). Clean public-domain scores are obtainable for six.
2. The app must therefore work well in **three data regimes**:
   - **Rich**: expert analyses (possibly several), aligned reference performances. Show the lenses, let them argue.
   - **Partial**: score only. Automatic analysis as a labelled draft. The user's own analysis becomes a first-class lens. Correction propagation (masked completion, see ecosystem C.3) is the relevant research.
   - **Private arrangement**: the user's own engraving of a copyrighted or arranged piece. Ingestion from the user's files (MusicXML if they have it, otherwise OMR then correction), analysis drafted automatically, nothing redistributable.
3. **Ask the user**: is the anthology engraved from MusicXML or MuseScore source files they have? If so, ingestion of all nine pieces is trivial and OMR is unnecessary. The engraving style suggests notation-software output.
4. The set spans four very different harmonic languages (Baroque figuration, Classical/early-Romantic functional harmony, Impressionist colour harmony, contemporary loop-based diatonicism). Any single harmonic model will fit some badly. That is another argument for lenses with provenance rather than one analysis.
