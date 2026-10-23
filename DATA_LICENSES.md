# Data, samples and libraries: licences

The repository contains **code, documentation and piano samples only**. Scores and analyses are downloaded by `python -m ppe fetch` into `data/external/` and turned into packs in `data/packs/`; both folders are git-ignored and never redistributed.

| Material | Source | Licence | Where |
|---|---|---|---|
| Beethoven op. 27/2 i, Humdrum edition | Craig Stuart Sapp, github.com/craigsapp/beethoven-piano-sonatas (after Durand 1915, ed. Dukas) | No licence file: used locally only | fetched |
| Moonlight analyses (BPS-FH; Tymoczko) | When in Rome (Gotham et al.), github.com/MarkGotham/When-in-Rome | CC BY-SA 4.0 (original BPS-FH data per its authors) | fetched |
| BWV 846 score | (n)ASAP dataset, github.com/CPJKU/asap-dataset | CC BY-NC-SA 4.0 | fetched |
| BWV 846 analyses (Gotham et al.; AugmentedNet) | When in Rome | CC BY-SA 4.0 | fetched |
| Clair de lune score and harmonies; Moonlight reference edition | DCML corpora, github.com/DCMLab | CC BY-NC-SA 4.0 | fetched |
| Piano samples | Salamander Grand Piano V3, Alexander Holm (via tonejs.github.io/audio/salamander) | CC BY 3.0 | `web/samples/salamander/` |
| Preact, htm | preactjs | MIT | `web/vendor/` |
| Verovio | RISM Digital | LGPL-3.0-or-later | Python dependency |
| music21 | Cuthbert et al. | BSD-3-Clause | Python dependency |
| ms3 | DCML | GPL-3.0 | Python dependency (DCML import) |

Personal, non-commercial use. If this project is ever shared beyond that, the CC BY-NC-SA data and the unlicensed Humdrum edition need replacing or permission.
