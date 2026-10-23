# Computational musicology and music-cognition models for explorable explanations

> **Agent-produced research note, dated 2026-10-23. To be reviewed by a human before anything here is relied on.**
> Scope: models that could power interactive explanations of musical structure in the personal piano lab (symbolic core + expert annotations + algorithmic hypotheses; LLMs only explain grounded facts).
> **Evidence tags.** **[confirmed]**: checked during this session against a primary source, abstract, repository page or PyPI. **[reported]**: from a secondary summary, or recalled from the literature and not re-verified this session. **[speculative]**: my own inference or design judgement.
> **Benchmark caveat.** Every number quoted comes with its dataset and metric. Most of these validations are small (tens of stimuli, tens of listeners, mostly Western-enculturated participants), so treat them as "the model tracks *some* listeners on *some* stimuli", not as ground truth.
> **Repository checks.** The GitHub REST API was blocked (403) from this environment. Licence and activity data therefore come from the GitHub web pages via fetch, and from the PyPI JSON API, which worked. "Last upload" dates are PyPI upload timestamps.

---

## 0. Framing: why cognition models matter for this lab

The lab's symbolic core already holds *facts* (notes, metre, voices) and *expert interpretations* (DCML and When-in-Rome Roman numerals, cadences, phrases). Cognition and musicology models add a third kind of object: a **quantified hypothesis about how the music is heard or organised**. Examples are the surprise of a note, the tension of a chord, which notes are structural, how far voices move, which passages recur, and how typical a progression is for a given composer.

For a learning app, the pedagogically valuable property is often not a model's accuracy but its **legible disagreement**:

- model vs. listener (the learner's own prediction or rating),
- model vs. model (sensory vs. cognitive accounts of expectation; spiral-array vs. TPS tension),
- model vs. expert (an algorithmic reduction vs. a Schenkerian analysis),
- expert vs. expert (two Roman-numeral analyses, already found in Moonlight mvt 1; also GTTM and Schenkerian datasets with several analysts; see §3).

That extends the "interpretive disagreement" feature into a general design pattern: **every lens is shown as one lens among several, with its provenance and its known failure modes.**

---

## 1. Musical expectation

### 1.1 IDyOM (Information Dynamics of Music)

**What it computes.** For each event in a sequence, IDyOM returns a probability distribution over the next event. From that come **information content** IC = −log₂ p(eᵢ | context), read as surprise, and **entropy** H of the predictive distribution, read as uncertainty *before* the event. It uses variable-order Markov models (PPM*, with escape-method blending) over multiple **viewpoints**. Viewpoints are derived feature streams: chromatic pitch, pitch interval, scale degree, contour, inter-onset interval, and linked viewpoints such as interval⊗scale-degree. A **long-term model** (LTM), trained on a corpus, stands in for enculturation. A **short-term model** (STM), trained incrementally on the current piece, stands in for within-piece learning. Their predictions are merged by entropy-weighted combination. [reported: Pearce 2005, PhD thesis, City University London; Pearce 2018, "Statistical learning and probabilistic prediction in music cognition", *Annals NYAS* 1423:378–395, doi:10.1111/nyas.13654]

**Theoretical basis.** Statistical learning plus predictive processing: listeners implicitly absorb the statistics of their musical culture, and expectation *is* the resulting predictive distribution. Huron's **ITPRA** (Imagination–Tension–Prediction–Reaction–Appraisal; Huron 2006, *Sweet Anticipation*, MIT Press) supplies the affective story: accurate prediction is rewarded, and surprise produces a fast reaction followed by a slower appraisal. ITPRA is a conceptual framework, not a computational model. In practice IC and H are its operationalisation. [reported]

**Empirical validation.**

- *Behavioural ratings of melodic continuations.* Pearce & Wiggins (2006, *Music Perception* 23(5):377–405, doi:10.1525/mp.2006.23.5.377) report that IDyOM IC accounts for listeners' expectedness ratings better than Narmour-style rule models (Schellenberg's two-factor model) on the classic probe-tone continuation datasets (Cuddy & Lunney; Schellenberg; Manzara et al.). The metric was correlation or regression R² between IC and mean ratings. [reported] *Limitations:* short monophonic stimuli, small numbers of contexts, and mean ratings that hide individual differences.
- *EEG/ECoG.* Di Liberto et al. (2020, *eLife* 9:e51784, doi:10.7554/eLife.51784) recorded EEG (n=20) and ECoG (n=3 patients) while participants listened to monophonic Bach melodies. Temporal-response-function models with melodic-expectation regressors, from a corpus-plus-short-term statistical model, predicted cortical signals beyond acoustic features. Encoding was strongest at latencies up to about 350 ms, in Heschl's gyrus and planum temporale. [confirmed: abstract] *Metric:* gain in prediction correlation of the neural signal, which is small in absolute terms, as is typical of TRF studies.
- *MEG, IDyOM vs. a transformer.* Kern, Heilbron, de Lange & Spaak (2022, *eLife* 11:e80935, doi:10.7554/eLife.80935) compared IDyOM, the **Music Transformer**, and a Gestalt-like (Narmour-inspired) model. The statistical-learning models fit neural surprise responses better than the Gestalt model. Strikingly, the best fit came from **short contexts (under about 10 notes)**, even though the models were trained on long-term statistics. An EEG dataset replicated the result. [confirmed: abstract]
- *Pleasure.* Cheung, Harrison, Meyer, Pearce, Haynes & Koelsch (2019, *Current Biology* 29(23):4084–4092, doi:10.1016/j.cub.2019.09.067) modelled about 80,000 chords from US Billboard songs, stripped of melody and lyrics. Pleasure depended on the **interaction** of uncertainty and surprise: surprising chords in predictable contexts, and unsurprising chords in uncertain contexts, were rated most pleasurable. The interaction was mirrored in amygdala, hippocampus and auditory cortex. Nucleus accumbens tracked only uncertainty. [confirmed: abstract and press summaries] The chord model is, as far as I know, IDyOM-family, but the sources retrieved do not name it. [reported] Gold et al. (2019, *J. Neurosci.* 39(47):9397–9409) report a related inverted-U for liking as a function of IC and entropy. [reported]

**Implementations** (checked 2026-10-23):

| Implementation | Language | Licence | Status |
|---|---|---|---|
| **IDyOM** (github.com/mtpearce/idyom), the reference implementation | Common Lisp (SBCL + Quicklisp + SQLite) | GPL-3.0 | v1.8, news entry dated 2026-09-21; 618 commits. Active. [confirmed: repo page] |
| **py2lispIDyOM** (github.com/xinyiguan/py2lispidyom) | Python wrapper, needs Lisp IDyOM installed | Not stated on PyPI | PyPI v1.0.2, last upload 2022-11-01. Dormant. Guan, Ren & Pelofi 2022, *JOSS* 7(79):4738, doi:10.21105/joss.04738. [confirmed: PyPI, JOSS] |
| **IDyOMpy** (github.com/GuiMarion/IDyOMpy) | Pure Python reimplementation | GPL-3.0 | 227 commits, ~50 stars, not on PyPI. Marion, Gao, Gold, Di Liberto & Shamma, "IDyOMpy: A new Python-based model for statistical analysis of musical expectations", *J. Neurosci. Methods*, art. 110347, doi:10.1016/j.jneumeth.2024.110347. Viewpoints: pitch, length, interval, velocity. Adds silence probabilities and "genuine" entropies. Supports k-fold cross-validation. [confirmed: README, NSF-PAR record] |
| **GraphIDyOM** | Python, with memory stored as explicit graphs | Software licence not stated | Bono Rosselló, arXiv:2607.25787 (28 July 2026). Validated against Lisp IDyOM for single, projected and multiple-viewpoint configurations. Exposes internal memory structures; local server. [confirmed: abstract] Very new; check the repo before adopting. |
| **IRIDyOM** | Max for Live with a Python reimplementation | ? | ICCC 2026 paper; real-time compositional use. [reported] |

**Cost.** PPM training on a few thousand melodies takes seconds to minutes. Per-event prediction after training is sub-millisecond. Interactive use (recompute surprise after the learner edits a note) is entirely feasible. [speculative, based on algorithmic complexity]

**Interactive-learning fit: high.** A particularly good property is that IDyOM is *inspectable*: one can show which viewpoint and which context length drove a prediction ("this note was expected because after scale degrees 3-2 the corpus continues to 1 in 71% of cases"). GraphIDyOM's explicit memory structures make this easier. [speculative]

**Caveats.**
- IDyOM is fundamentally **monophonic**. Piano textures need a melody extraction (top voice, or a voice-separated stream, §4) or a chord-sequence viewpoint. [reported]
- **IC depends on the training corpus.** An LTM trained on Essen folk songs will find Chopin chromaticism very surprising. Rather than hiding this, the app could expose it: *"surprising to a listener raised on Bach chorales / Mozart sonatas / jazz standards."* [speculative]
- Kern et al.'s short-context result suggests low-order models are adequate proxies for neural surprise. That is good for cost, but it also means "deep" structural expectations (a delayed cadence after 16 bars) are *not* what the validated signal measures. [reported → speculative implication]

### 1.2 Harmonic and cadential expectation

- **Sears, Pearce, Caplin & McAdams (2018)**, "Simulating melodic and harmonic expectations for tonal cadences using probabilistic models", *JNMR* 47(1):29–52, doi:10.1080/09298215.2017.1367010. IDyOM was applied to 245 exemplars of the five most common classical cadence categories (Haydn string quartets). Terminal events in cadential contexts were more predictable than those in non-cadential contexts. [reported: search summary of the abstract]
- **Sears et al. (2019)**, *QJEP* 72(6), doi:10.1177/1747021818814472. Comparison of sensory and cognitive accounts of harmonic priming; the simulations favoured a *cognitive* (co-occurrence statistics) account. [reported]
- **Sears, Spitzer, Caplin & McAdams (2020)**, "Expecting the end: Continuous expectancy ratings for tonal cadences", *Psychology of Music* 48(3), doi:10.1177/0305735618803676. Perfect authentic cadences received the highest and earliest expectancy ratings; half cadences the lowest and latest. [reported]
- **Counterpoint:** Harrison & Pearce (ICMPC15/ESCOM10, 2018), "Dissociating sensory and cognitive theories of harmony perception through computational modeling", argued that much harmonic-priming evidence is parsimoniously explained by **Leman's (2000) auditory short-term-memory model**, i.e. by acoustic similarity to recent context rather than syntax. [reported] *Pedagogical gold:* "Is V→I expected because it is grammatical or because it *sounds like* what came before?" Two models can answer the question differently, side by side.
- **Chord-sequence surprisal.** Any autoregressive model over Roman numerals (n-gram, LSTM, small transformer) trained on DCML corpora (ABC, Mozart, Romantic piano: §6), When-in-Rome, or the iRealPro/JHT jazz data gives per-chord IC and H. With tens of thousands of chord tokens, an n-gram with Kneser–Ney or PPM smoothing trains in seconds. [speculative] DCML's ABC has about 30,000 chord labels across 16 quartets (press figure). [reported]

### 1.3 Neural surprisal from symbolic transformers

- The Music Transformer (Huang et al. 2019, ICLR) was used as a surprisal model in Kern et al. 2022 and performed on par with IDyOM against MEG. [confirmed: abstract]
- Audio-domain surprisal from a transformer over compressed audio latents predicted EEG responses to songs. [reported: arXiv:2501.07474, 2025]
- Tokenisers for local training: **MidiTok** (MIT, v3.1.0, PyPI upload 2026-09-30) [confirmed], **symusic** (MIT, v0.6.0) [confirmed].
- **Assessment:** transformer surprisal is a reasonable *second opinion* but is less interpretable than IDyOM. Its training data is usually huge pop/MIDI corpora, which embed an unknown "listener". For "explain grounded facts", IDyOM-style models with explicit corpora are preferable, and a transformer can be added as a disagreeing second voice. [speculative]

---

## 2. Tension

### 2.1 Lerdahl & Krumhansl (2007): TPS tension model

**What it computes.** Tension of each event as the sum of (a) **hierarchical tension**, inherited along the prolongational tree, (b) **sequential tension**, the distance in Lerdahl's Tonal Pitch Space (TPS) between successive chords, combining region, chord and basic-space distances, (c) **surface dissonance**, from inversion, non-chord tones and seventh chords, and (d) **melodic attraction**, an anchoring-strength / distance² formula. Lerdahl & Krumhansl, "Modeling tonal tension", *Music Perception* 24(4):329–366, 2007, doi:10.1525/mp.2007.24.4.329. Theory: Lerdahl 2001, *Tonal Pitch Space* (OUP). [confirmed: four components, per abstract]

**Validation.** Listeners gave continuous or segment-wise tension ratings for a Bach chorale and excerpts of Mozart and Wagner/chromatic music (including *Parsifal*, per lecture material). The model's predictions correlated well with mean ratings, and in places mismatches pointed to *alternative analyses* within the theory. [reported] A later review summarises that the model generally predicts harmonic tension well, but **the melodic attraction component has not received empirical support**. [reported: secondary review] Earlier: Bigand, Parncutt & Lerdahl (1996, *Perception & Psychophysics* 58(1):125–141) found TPS distance and sensory dissonance both contribute to chord tension ratings. [reported]

**Implementations.** No widely used, maintained library. **AuToTen** (Open University ORDO repository, Python; CSMC/MuMe 2020, zenodo.org/records/4285394) claims the first full automation of Lerdahl's tension model. Licence and maintenance unverified. [reported] The *hierarchical* component needs a prolongational tree, which in practice is the bottleneck (§3).

**Interactive fit: medium-high.** The sequential (TPS distance) and surface components are cheap and deterministic, and they can be computed directly from DCML or When-in-Rome Roman numerals plus keys. That is an excellent fit with the grounded-facts principle, because the input is *expert* analysis rather than an estimate. [speculative] The hierarchical component would require trusting an automatic tree, or annotating trees by hand for a few signature pieces.

### 2.2 Farbood (2012): parametric temporal model

"A parametric, temporal model of musical tension", *Music Perception* 29(4):387–428, doi:10.1525/mp.2012.29.4.387. Two experiments: (1) a web study of how individual parameters contribute to tension, and (2) a lab study with continuous responses to longer, complex stimuli. Parameters: harmony, pitch height, melodic expectation, dynamics, onset frequency, tempo, metre, rhythmic regularity, syncopation. Linear and nonlinear static models fit the continuous data poorly. The proposed model uses a **moving perceptual window** and **trend salience** (a rising trend in a parameter contributes to tension in proportion to its salience), and reports high correlation with the empirical tension curves. [confirmed: abstract] *Limitations:* small stimulus set; parameter weights fit to that data; no public reference implementation that I found. [speculative/reported]

**Why it matters for a pianist.** Farbood's model is the one that lets **performance parameters (dynamics, tempo, onset density)** raise or lower tension, not only harmony. That makes it the natural bridge between "analysis" and "how I play it". [speculative]

### 2.3 Herremans & Chew: tension ribbons (spiral array)

Herremans & Chew (2016), "Tension ribbons: Quantifying and visualising tonal tension", TENOR 2016. Three measures in Chew's **spiral array**: **cloud diameter** (spread of the pitch cloud in a window), **cloud momentum** (movement of the cloud's centroid between windows), and **tensile strain** (distance of the cloud from the key's centre). Validated qualitatively and against Farbood's (2012) empirical data; the measures were reported to correlate with perceived tension. [reported] Used for controlling tension in generation: MorpheuS (Herremans & Chew 2017, *IEEE Trans. Affective Computing*) and Guo et al. 2020 (CSMC+MuMe, a VAE controlled by tonal tension). [reported]

**Implementations.**
- **partitura** `partitura.musicanalysis.estimate_tonaltension` (Apache-2.0, PyPI v1.9.0, last upload 2026-05-25; actively maintained by JKU/CPJKU). Defaults: window 1 beat, onset-wise sampling, weights [0.516, 0.315, 0.168], α=β=0.75. Estimates key and pitch spelling if they are not supplied. [confirmed: docs and PyPI]
- **midi-miner** (github.com/ruiguo-bio/midi-miner, GPL-3.0, ~121 stars): MIDI in, bar- or beat-wise tension out, plus track separation. Needs a separately downloaded random-forest model. [confirmed: repo page]

**Cost:** milliseconds per piece. **Interactive fit: high**, and partitura is likely already in the stack. **Risk:** the measures are purely pitch-geometric. They ignore metre, dynamics, register and texture, so a fortissimo diminished-seventh arpeggio and a pianissimo one get the same tension. [speculative]

### 2.4 Navarro-Cáceres et al. (2020): Tonal Interval Space model

"A computational model of tonal tension profile of chord progressions in the Tonal Interval Space", *Entropy* 22(11):1291, doi:10.3390/e22111291 (open access, CC BY). Four components: dissonance (fitted weight 0.402), hierarchical tension (0.246), tonal distance (0.202) and voice leading (0.193). Compared with Lerdahl's model and MorpheuS on **12 chord progressions**, it reportedly outperformed both. [confirmed: abstract] *Limitation:* only 12 progressions, so this is a proof of concept rather than a validated model. TIV.lib (arXiv:2008.11529) provides the Tonal Interval Vector machinery for audio. [reported]

### 2.5 Perceived tension: empirical picture

- Continuous tension ratings show good within- and between-listener agreement. Lehne, Rohrmeier, Gollmann & Koelsch (2013, *Music Perception* 31(2):171–185; PDF hosted on stefan-koelsch.de) found that ratings of **outer-voice reductions** of Mozart and Mendelssohn piano pieces correlated highly with ratings of the originals. [reported] *Implication:* the soprano–bass frame carries most of the felt tension, which supports the "reduction" lens (§3).
- No 2023–2026 large-scale benchmark dataset of continuous tension ratings turned up in my searches. Validation of all tension models rests on **small, older datasets**. [confirmed: absence in searches; not proof of absence]

---

## 3. Reductions and hierarchical structure

### 3.1 GTTM implementations (Hamanaka, Hirata, Tojo)

- **ATTA / FATTA / σGTTM / deepGTTM**: Hamanaka, Hirata & Tojo, "Implementing 'A Generative Theory of Tonal Music'", *JNMR* 35(4):249–277, 2006, doi:10.1080/09298210701563238; later deep-learning variants (deepGTTM-I/II/III, around 2016–2017). They compute grouping structure, metrical structure, **time-span trees** and prolongational trees for *monophonic* melodies. [reported]
- **GTTM database:** Hamanaka, Hirata & Tojo, "Musical structural analysis database based on GTTM", ISMIR 2014, pp. 325–330. **300 pieces** (8-bar classical melodies) with analyses by a musicologist. When a second musicologist re-analysed them, **267 of 300 almost matched and 33 had different interpretations**. [confirmed: summary of paper] *This is a ready-made "interpretive disagreement" resource for hierarchical analysis.*
- **Melody morphing:** time-span-tree operations (subsumption, meet, join) let two melodies be interpolated, and **cutting the tree at depth d** yields an abstracted melody. Interactive demos exist (the "Melody Slot Machine", SMC 2019; MMM 2024 best demo award). US patent 8,278,545 B2 covers morphed-piece generation. [confirmed: summaries] *Prior art for a "reduction slider" on melodies.*
- **Availability:** analyzers were distributed from Hamanaka's lab pages; no maintained open-source Python package was found. Licences are unclear. [reported]

### 3.2 Automatic Schenkerian analysis

- **Marsden (2010)**, "Schenkerian analysis by computer: A proof of concept", *JNMR* 39(3):269–289, doi:10.1080/09298215.2010.503898. Chart-parsing over elaboration operations; showed the search space is huge and needs heuristics. [reported]
- **Kirlin (2014 PhD, UMass Amherst; Kirlin & Jensen, AAAI 2015, "Learning to uncover deep musical structure", doi:10.1609/aaai.v29i1.9476).** A probabilistic model of hierarchical analysis using maximal outerplanar graphs (MOPs, following Yust 2006), with parameters learned from **SCHENKER41**, a corpus of 41 textbook analyses. Presented as the first large-scale data-driven approach. [confirmed: abstract; the SCHENKER41 linkage is from a related Kirlin paper]
- **Ni-Hahn et al. (ISMIR 2024)**, "A new dataset, notation software, and representation for computational Schenkerian analysis", arXiv:2408.07184, pp. 866–873. **145 analyses** by four analysts. Mostly Bach and Pachelbel fugue subjects, plus Mendelssohn, Brahms, Bartók, Shostakovich and Gentle Giant. Stored as JSON, represented as heterogeneous-edge graphs. **Available by request only; licence unstated.** The authors also built a notation tool (Vue + Electron, on request). [confirmed: paper]
- **AutoSchA** (Ni-Hahn, Zhu, Yin, Jiang, Rudin, Mak; arXiv:2512.18232, AAAI 2026). A GNN with multi-relational node-isolation pooling that predicts, per note, whether it is retained at each depth, plus a voice role (treble/bass/inner). Trained on 88 fugue subjects (3,807 notes, ×12 transpositions). Best validation accuracy **0.749 ± 0.015** (vs. R-GCN 0.729, MLP 0.714, GCN 0.663). In an expert survey (5 experts, 9 scores) AutoSchA scored GPA 3.22 vs. human 3.55, and musicality 7.20 vs. 8.04 on a 0–10 scale. 67% of its analyses were judged to contain awkward portions vs. 33% for the human analyses. [confirmed: paper] *Limitations:* only Baroque fugue subjects, a tiny survey, and an expert-chosen threshold. **Not usable for Beethoven or Chopin piano textures without retraining.** Supplement at github.com/stephenHahn88/AutoSchA_Supplement (URL to verify).
- **Finkensiep & Rohrmeier, proto-voices** ("Modeling and inferring proto-voice structure in free polyphony", ISMIR 2021, pp. 189–196; Finkensiep PhD 2024, EPFL, doi:10.5075/epfl-thesis-9403). A grammar of primitive operations (neighbour, passing, horizontalisation of simultaneities) that builds voice-like structures in **free keyboard textures** without assuming notated voices, parsed with a chart parser. [confirmed: abstract] This is the most theoretically appropriate model for piano music, but it is a research codebase (Haskell, to my knowledge) with heavy inference. [reported/speculative]
- **"SchenkerDiff" / "Hauptwerk":** I found no evidence of a dataset or model under these names. Hauptwerk is a virtual pipe-organ product. Treat both as non-existent unless a source turns up. [confirmed: not found]

### 3.3 Chordal and harmonic reduction tools

- **music21** (v10.5.1, PyPI upload 2026-10-22, BSD-3, actively maintained) [confirmed: PyPI; licence from prior knowledge]. `analysis.reduceChords.ChordReducer` (collapse arpeggios, remove short time-spans, remove vertical dissonances, split by bass, reduce to N chords per measure), `analysis.reduction.ScoreReduction`, and `Stream.chordify()`. [confirmed: docs] These are heuristic surface→chord reductions with no hierarchy. They are useful as a *first rung* of a reduction ladder.
- **Outer-voice reduction** (soprano + bass): trivial to compute after voice separation. Lehne et al. 2013 suggests it preserves felt tension well. [reported]
- **Expert-annotation-driven reduction:** with DCML labels (chord root, inversion, chord tones), the lab can filter notes to *chord tones on chord onsets*. That is deterministic and grounded in expert labels. [speculative]

**Reduction ladder proposal.** surface → chordified (music21) → chord tones only (DCML labels) → outer voices → one chord per harmonic rhythm unit → phrase-level Roman skeleton (cadence points). The deeper "Ursatz-like" levels come only from *hand-made* analyses for signature pieces, or from a model clearly flagged as a hypothesis. [speculative]

---

## 4. Voice leading

### 4.1 Tymoczko's geometry

- Tymoczko (2006), "The geometry of musical chords", *Science* 313:72–74, doi:10.1126/science.1126287. Callender, Quinn & Tymoczko (2008), "Generalized voice-leading spaces", *Science* 320:346–348, doi:10.1126/science.1153021. Tymoczko (2011), *A Geometry of Music* (OUP). n-note chords are points in the orbifold Tⁿ/Sₙ; voice leadings are paths, and their size is a norm (taxicab/L1 in semitones, or L2/L∞). The two-note case is a Möbius strip. Three-note chords live in a twisted triangular prism with augmented triads at the centre, which is why near-even chords (triads, seventh chords) admit efficient voice leading. [reported; well established]
- **Minimal voice-leading algorithm:** Tymoczko (2006, *Music Theory Spectrum*/JMT) gives an O(n²)-ish procedure for the minimal bijective voice leading between pitch-class sets, using the fact that minimal voice leadings are uncrossed. **Voiceleading_utilities** (Tymoczko's routines, GPL-style, reported on a GitLab mirror) implements `bijective_vl` and related functions. [reported] It is easy to reimplement: for sets of size n, try the n cyclic alignments of sorted pitch classes and the octave offsets.
- **Visualisation prior art:** Tymoczko's **ChordGeometries** (Mac/Windows XP era, 2006): chords as balls in a cone or prism, playable via MIDI, paths through circular pitch-class space and 4-D slices. It is probably no longer maintained. [confirmed: demo pages and 2006 press] Morlando (2026, *MusMat* journal) builds a discrete 12-TET voice-leading orbifold. [reported]
- **Huron (2001)**, "Tone and voice: A derivation of the rules of voice-leading from perceptual principles", *Music Perception* 19(1):1–64, and Huron (2016), *Voice Leading: The Science behind a Musical Art* (MIT Press). Voice-leading rules derived from auditory scene analysis (pitch proximity, toneness, avoiding parallel perfect intervals to preserve stream independence). [reported] This gives a *perceptual* rationale for each textbook rule, which is excellent explanation material.

**Interactive fit: very high, very cheap** (microseconds per chord pair). See ideas 5 and 6.

### 4.2 Voice separation

- **Chew & Wu (2004)**, "Separating voices in polyphonic music: A contig mapping approach", CMMR 2004, LNCS 3310. Contigs are segments with a constant number of voices, which are then linked by minimal pitch distance. About 90% precision on Bach. [reported] **Implemented in partitura** (`partitura.musicanalysis.voice_separation`). [confirmed: docs]
- **Duane & Pardo (2009)**: streaming/voice separation as clustering with learned features (ISMIR 2009). [reported; not re-verified]
- **Karystinaios, Foscarin & Widmer (2023)**, "Musical voice separation as link prediction: Modeling a musical perception task as a multi-trajectory tracking problem", IJCAI 2023. A heterogeneous GNN with one node per note predicts same-voice successor links, regularised toward at most one in-link and one out-link per node. Reported state of the art on classical music of several styles. Code: github.com/manoskary/vocsep_ijcai2023. [confirmed: abstract]
- **Foscarin, Karystinaios, Nakamura, Widmer et al. (2024)**, "Cluster and Separate: a GNN approach to voice and staff prediction for score engraving", ISMIR 2024. Handles **piano** textures, including chords and cross-staff voices; code on the CPJKU GitHub. [confirmed: program page] **MusGConv** (IJCAI 2024, arXiv:2405.09224) improves several score-graph tasks, including voice separation. **GraphMuse** (PyPI v0.0.5, 2024-11) is the supporting library. [confirmed]
- **For the lab:** DCML MuseScore files already carry *notated* voices. Algorithmic separation is needed mainly for (a) MIDI or performance input and (b) **implicit polyphony** (compound melody in Bach, Alberti-bass inner voices), where proto-voice models (§3.2) are the principled tool. [speculative]

---

## 5. Pattern and motif discovery; similarity; schemata

### 5.1 Point-set pattern discovery (SIA family)

- **SIA/SIATEC**: Meredith, Lemström & Wiggins (2002), "Algorithms for discovering repeated patterns in multidimensional representations of polyphonic music", *JNMR* 31(4):321–345, doi:10.1076/jnmr.31.4.321.14162. Notes are points (onset, morphetic/chromatic pitch). SIA finds maximal translatable patterns (O(n² log n)); SIATEC finds all their translational occurrences (O(n³)). **COSIATEC / SIATECCompress / Forth's algorithm** select compact covering sets (compression-based "explanations" of a piece). [reported]
- **Implementation:** **OMNISIA** (github.com/chromamorph/omnisia, Java), Meredith's own suite. The licence was not visible on the page and must be checked. [confirmed: repo exists]
- **MIREX "Discovery of Repeated Themes & Sections" (2013–2017)** on **JKU-PDD**: 5 pieces (Bach, Beethoven, Chopin, Gibbons, Mozart), 26 annotated patterns, symbolic and audio, monophonic and polyphonic variants. [confirmed: secondary] Metrics: establishment, occurrence and three-layer precision/recall/F1 (implemented in **mir_eval.pattern**). [confirmed: docs] SIATECCompress (MIREX 2016) reached a mean **three-layer F1 of about 0.49** across the 5 JKU-PDD pieces. A review chapter reports the best algorithms at mean F1 ≈ 0.49, with single pieces up to 0.71. [reported] *Limitations:* 5 pieces, with annotations of what experts *chose* to mark. Algorithms find many "valid" repeats that are not annotated, so precision is underestimated.
- **BPS-Motif** (Hsiao, Hung, Chen & Su, ISMIR 2023): note-level motif annotations for **32 Beethoven sonata first movements**: 263 motives, 4,944 occurrences, 36,652 motif notes (28.9% of 126,943 notes), with peer review of annotations. [confirmed: poster] This is highly relevant to a piano learner. Licence and download location need checking (archives.ismir.net/ismir2023/paper/000032.pdf).
- **Motif transformations:** Taieb, Greenberg & Sober (arXiv:2603.26478, March 2026), "Probabilistic multilabel graphical modelling of motif transformations in symbolic music". A multilabel CRF models which transformation families co-occur, and in which musical contexts, using BPS-Motif + BPSD on Beethoven sonatas. No code stated. [confirmed: abstract] Detecting inversion, retrograde, augmentation/diminution and sequence is straightforward with point-set or interval-string matching under the relevant transformation group. SIA handles translation natively. Inversion = reflection in pitch; augmentation = scaling in time. [speculative/standard]

### 5.2 Melodic similarity and embeddings

- **Classical measures:** edit distance on interval strings, n-gram overlap, correlation on step-function contours, and earth mover's distance. Müllensiefen & Frieler's SIMILE/FANTASTIC work validated similarity measures against expert similarity judgments. Janssen, van Kranenburg & Volk (2017, *JNMR*) compared measures for finding melodic segments in folk songs. [reported]
- **MusicBERT** (Zeng et al., ACL Findings 2021, arXiv:2106.05630; OctupleMIDI, bar-level masking, over a million songs); **MidiBERT-Piano** (arXiv:2107.05223, a public piano corpus). Wang & Su (ISMIR 2025, arXiv:2507.04776) propose a 12-task benchmark. [confirmed: abstracts] Their embeddings have **no validated relation to perceived similarity**. Treat them as retrieval tools, not explanations. [speculative]
- **CLaMP 3** (Wu et al., Findings of ACL 2025, pp. 2605–2625, doi:10.18653/v1/2025.findings-acl.133, arXiv:2502.10362). Contrastive alignment of sheet music (ABC), performance MIDI, audio and multilingual text. M4-RAG has 2.31 M music–text pairs; the WikiMT-X benchmark has 1,000 triplets. Demo on Hugging Face (sander-wood/clamp3). [confirmed: abstract] Useful for "find pieces like this" and text→score search across the user's repertoire. Not on PyPI; check the licence before use.

### 5.3 Galant schemata and partimenti

- **Gjerdingen (2007)**, *Music in the Galant Style* (OUP): schemata (Romanesca, Prinner, Fonte, Monte, Meyer, Do-Re-Mi, Quiescenza, Ponte...) as paired outer-voice scale-degree skeletons with typical metrical placement. [reported]
- **Finkensiep, Déguernel, Neuwirth & Rohrmeier (2020)**, "Voice-leading schema recognition using rhythm and pitch features", ISMIR 2020. **Skipgrams** generate schema candidates (non-contiguous note n-grams); a classifier on pitch and rhythm features filters them. Evaluated on a **schema-annotated Mozart piano sonata dataset** released with the paper. [confirmed: abstract] Earlier: Finkensiep, Neuwirth & Rohrmeier (2018), generalised skipgrams for pattern discovery. Code: github.com/DCMLab/schemata_code (notebooks with ipywidgets for semi-automatic schema annotation). [confirmed: repo exists] Whether Prinner and Fonte are among the annotated types is unconfirmed (likely, given Gjerdingen's core list). [reported]
- **Carter-Enyi & Rabinovitch (2021)**, "Onset and contiguity: Melodic feature reduction and pattern discovery", *Music Theory Online* 27(4). Simple n-gram matching over reduced melodies located all Prinner and Meyer instances in Mozart K. 545/i that Gjerdingen identified; freely available software. [confirmed: summary]
- **Partimenti:** **Monuments of Partimenti** (Gjerdingen, Northwestern; transcriptions, MIDI) and the **Uppsala Partimento Database (UUPart)**, which is searchable by pitch sequence and by Gjerdingen "Gj" numbers. [confirmed: summaries] **No machine-readable corpus of partimento *realisations*** was found. That is a gap, and the lab could build a small one. [confirmed: not found]

---

## 6. Corpus statistics and generative grammars as explanation

### 6.1 DCML corpora and corpus studies

- **ABC (Annotated Beethoven Corpus)**: Neuwirth, Harasim, Moss & Rohrmeier (2018), *Frontiers in Digital Humanities* 5:16, doi:10.3389/fdigh.2018.00016. All 16 string quartets, about 30k chord labels. [confirmed]
- **Moss, Neuwirth, Harasim & Rohrmeier (2019)**, "Statistical characteristics of tonal harmony: A corpus study of Beethoven's string quartets", *PLoS ONE* 14(6):e0217242, doi:10.1371/journal.pone.0217242. Findings: a power-law-like rank-frequency distribution (few chords dominate); transitions are directional (asymmetric, e.g. V→I ≫ I→V in specific contexts); predictability depends on chord features; and chord-level and key-level behaviour differ. [confirmed: abstract]
- **Annotated Mozart Sonatas**: Hentschel, Neuwirth & Rohrmeier (2021), *TISMIR* 4(1), doi:10.5334/tismir.63. Harmony, cadence and phrase labels. [confirmed]
- **Romantic piano corpus**: Hentschel, Rammos, Moss, Neuwirth & Rohrmeier, "An annotated corpus of tonal piano music from the long 19th century", *Empirical Musicology Review* 18(1):84–95 (2024 per DCML). 264 pieces: Beethoven sonatas, Chopin mazurkas, Debussy *Suite bergamasque*, Dvořák *Silhouettes*, Liszt *Années*, Medtner *Tales*, Schumann *Kinderszenen*, Tchaikovsky *Seasons*, Grieg *Lyric Pieces*. **CC BY-NC-SA 4.0**. MuseScore 3 + TSV. [confirmed: Zenodo summary]
- **Tooling:** **ms3** (GPL-3.0-only, v2.6.5, 2026-09-17) parses MuseScore + DCML labels; **DiMCAT** (GPL-3.0-or-later, PyPI v3.4.1, 2026-07-28; the GitHub README still says "under heavy development / 1.0 alpha", so expect API churn); docs at dimcat.readthedocs.io. [confirmed] **musif** (MIT, v1.3.0) does feature extraction. [confirmed]
- **GPL note:** ms3 and DiMCAT are GPL. For a *personal* local app that is unproblematic, but distributing a combined app would require GPL compatibility. The NC clause on the corpora forbids commercial use. [speculative/legal-lite]

**Explanatory use:** "How typical is this progression for Beethoven vs. Chopin?" is a **conditional probability with a confidence interval** over a specified corpus. With about 30k (ABC) plus a few thousand labels per Romantic sub-corpus, bigram estimates for common chords are stable. Rarer trigrams need smoothing, and the interface should show the counts (*"this occurs 3 times in 264 pieces"*) rather than bare probabilities. [speculative] Prior art for next-chord probabilities: **Hooktheory Trends** (a Markov model over a TheoryTab database of 40k+ pop songs, with a public API). [confirmed: blog/API docs] It is *pop*, not composer-specific, and has no confidence information.

### 6.2 Generative grammars of harmony

- **Rohrmeier (2011)**, "Towards a generative syntax of tonal harmony", *J. Mathematics and Music* 5(1):35–53, doi:10.1080/17459737.2011.573676 (the GSM). **Rohrmeier (2020)**, "The syntax of jazz harmony: Diatonic tonality, phrase structure, and form", *Music Theory and Analysis* 7(1):1–63. Harmony is a context-free-like tree of *prolongation* and *preparation* (dominant/applied chains), with recursive applied dominants and substitution rules. [reported]
- **Harasim, Rohrmeier & O'Donnell (2018)**, "A generalized parsing framework for generative models of harmonic syntax", ISMIR 2018, pp. 152–159. Probabilistic Abstract CFGs; enumerates all parses of long chord sequences; parameters learned by stochastic variational inference on jazz standards. Outperforms a standard CFG with fewer parameters. [confirmed: abstract] Extended with rhythm in ISMIR 2019. [reported]
- **Jazz Harmony Treebank** (Harasim, Finkensiep, Ericson, O'Donnell & Rohrmeier, ISMIR 2020, pp. 207–215): expert-verified hierarchical analyses of **about 150 jazz standards** from the open iRealPro collection, in JSON, with an open-source web tree editor. [confirmed: abstract/poster] Repository on GitHub (DCMLab). Licence not verified.

**Interactive fit:** a parse tree over a ii–V–I chain, showing *why* a chord is there (it prepares the next one, recursively), is among the most explanatory artefacts available for jazz harmony. The treebank gives *expert* trees for real standards, so the grounded-facts principle holds. Ambiguous parses (several trees with probabilities) are, again, disagreement made visible. [speculative]

---

## 7. Psychoacoustics of harmony

### 7.1 Models

- **Plomp & Levelt (1965)**, *JASA* 38:548–560: dissonance of pure-tone pairs peaks at about 25% of the critical bandwidth. **Sethares (1993)**, *JASA* 94(3):1218–1228, and *Tuning, Timbre, Spectrum, Scale* (Springer 1998/2005): a parametric fit summed over all partial pairs, weighting by min(aᵢ, aⱼ) in newer versions. **Hutchinson & Knopoff (1978)**, **Vassilakis (2001/2005)**: roughness with amplitude-fluctuation terms. [reported: classic]
- **Harrison & Pearce (2020)**, "Simultaneous consonance in music perception and composition", *Psychological Review* 127(2):216–244, doi:10.1037/rev0000169 (open access, PMC7032667). Reanalysed many consonance datasets and modelled consonance as a composite of **interference (roughness)**, **periodicity/harmonicity**, and **cultural familiarity**. The released **incon** R package bundles their composite model and 15+ others. [confirmed]
- **incon** (github.com/pmcharrison/incon, R, **MIT**, 17 models): periodicity/harmonicity (gill_09, har_18, milne_13, parn_88, parn_94_complex, stolz_15), interference (bowl_18, huron_94, **hutch_78 default**, parn_94_pure, seth_93, vass_01, wang_13), culture (jl_12, har_19_corpus), numerosity (parn_94_mult) and the composite har_19_composite. Lifecycle "maturing", 59 commits, **no Python port**. [confirmed]
- **Python options:** `dissonant` (PyPI v0.1.1, 2018, no licence field; Sethares 1993, Vassilakis, with corrected formulas) [confirmed]; Sethares' MATLAB→Python gist [confirmed]; or reimplementing Hutchinson–Knopoff and Harrison's har_18 harmonicity, each about 100 lines. Calling incon through rpy2 is also possible. [speculative]
- **Marjieh, Harrison, Lee, Deligiannaki & Jacoby (2024)**, "Timbral effects on consonance disentangle psychoacoustic mechanisms and suggest perceptual origins for musical scales", *Nature Communications* 15:1482, doi:10.1038/s41467-024-45812-z. Five large online studies, **235,440 judgments** (US and South Korea). Timbre manipulations (stretched or compressed partials) **shift consonance peaks**, even toward inharmonic intervals. The updated model combines liking of harmonicity, disliking of fast beats (roughness) and liking of slow beats. [confirmed: abstract]
- **Parncutt, Engel & Radovanovic (2023)**, *Psychological Topics* (open access): all 19 trichords with organ-like and **piano** tones, close and open voicings, and inversions. Ratings correlated closely with simple roughness and harmonicity models; **roughness performed better**; roughness, harmonicity and familiarity all contribute. [confirmed: summary]
- A follow-up mentioned in search results reports that the Harrison–Pearce model explained 62% of rating patterns across 9 datasets and a revised model 73%. The source is unclear (possibly a 2025 thesis, Velthuis, Leiden LIACS). [reported; verify]

### 7.2 Piano-specific considerations

- **Inharmonicity.** Stiff strings stretch the partials, fₙ ≈ n·f₀·√(1 + Bn²), and B is largest in the bass and the high treble. Roughness models that assume harmonic spectra mis-estimate low-register chords. Feeding *piano-like stretched spectra* into Sethares-style models is cheap and better motivated, and Marjieh et al. 2024 show that stretched spectra genuinely shift perceived consonance. [reported physics; speculative application]
- **Register.** Critical bandwidth is proportionally wider in the low register, so a close-position triad below about C3 is rough while the same chord at C5 is not. This is the psychoacoustic basis of the "low-interval limits" rule taught to jazz pianists. [reported: classic psychoacoustics; LIL as pedagogy is folk knowledge]
- **Voicing shape.** A 2026 **preprint** (arXiv:2603.29710, not peer reviewed) analysed about 19.3 M playable piano voicings. It reports that the gap distribution (skewness) predicts roughness about 5.8× better than overall spread. [reported; preprint, treat cautiously]
- **Pedal.** The damper pedal adds sympathetic resonance, raising effective partial density and, with it, roughness when harmonies change under the pedal. I found **no psychoacoustic study quantifying pedal blur vs. perceived dissonance**. A roughness model over the *sounding set* (all notes still sustained under the pedal, with decay) is a plausible proxy but unvalidated. [speculative; flagged as a gap]

**Interactive fit: very high** for a voicing explorer. The models run in microseconds per chord, and incon's validation data gives honest correlation figures to display.

---

## 8. Rhythm, metre, microtiming and expressive performance

- **Repp (1992)**, "Diversity and commonality in music performance: An analysis of timing microstructure in Schumann's *Träumerei*", *JASA* 92(5):2546–2568, doi:10.1121/1.404425. **28 recorded performances**. Timing reflects hierarchical grouping: big ritardandi at section ends and lengthening of accented tones. Within gestures, timing follows a **parabolic** function whose curvature varies between artists, essentially one degree of freedom. Cortot and Horowitz stand out as individual. [confirmed: abstract] Repp later found that **diversity shrinks at longer time scales**: everyone slows at major boundaries. [confirmed: summary]
- **Todd (1992)**, "The dynamics of dynamics: A model of musical expression", *JASA* 91(6):3540–3550. Tempo and dynamics as a function of phrase hierarchy ("faster-louder, slower-softer" arches at each level, summed). [reported]
- **Friberg & Sundberg (1999)**, "Does music performance allude to locomotion? A model of final ritardandi derived from measurements of stopping runners", *JASA* 105(3):1469–1484. Final-ritard tempo curves match the velocity curves of decelerating runners, and the curvature that fit the runners lay within listeners' preferred range. [confirmed: the 1996 ASA abstract on the same work]
- **KTH rule system / Director Musices**: Friberg, Bresin & Sundberg (2006), "Overview of the KTH rule system for musical performance", *Advances in Cognitive Psychology* 2(2–3):145–161. About 25 rules covering phrasing (phrase arch), micro-timing, metrical patterns and grooves, articulation, *harmonic and melodic charge* (tonal tension → dynamics and tempo), intonation, ensemble, noise. **Director Musices 3.1.5** (multiplatform, released 2024-05-30, KTH download page); free software in Common Lisp; real-time variant **pDM** (Pd). [confirmed: summaries] Each rule has an interpretable parameter "k", so rules can be switched on one at a time.
- **Data-driven models:** Cancino-Chacón, Grachten, Goebl & Widmer (2018), "Computational models of expressive music performance: A comprehensive and critical review", *Frontiers in Digital Humanities* 5:25, doi:10.3389/fdigh.2018.00025. [confirmed] The JKU **Basis Mixer** models expressive parameters as functions of score basis features. **partitura** handles performance–score alignment (match files) and expressive feature extraction. Datasets of aligned performances (ASAP / (n)ASAP, Vienna 4x22, Batik-plays-Mozart) let the lab show *real* timing curves of famous pianists for the same passage. [reported]

**Explanatory use:** the user plays a passage (MIDI keyboard), the app aligns it to the score with partitura, and plots the tempo and loudness curve next to (a) a KTH-rule rendering with named rules and (b) curves from professional recordings in an aligned dataset. The learner sees *which structural facts* (phrase boundary, harmonic charge, metrical position) the experts' timing tracks. [speculative]

---

## 9. IDEAS: interactive features built on these models

Format for each: **Model** · **Learning mechanism** · **Feasibility / cost** · **Misleading risk** · **Originality / prior art** · **Evidence tag**.

### Idea 1. "Predict-then-hear" expectation game (melody)
- **Model:** IDyOM (IDyOMpy or GraphIDyOM; Lisp IDyOM as reference), LTM trained on a chosen corpus plus a per-piece STM.
- **Mechanism:** playback pauses before a note. The learner chooses or plays the next pitch (and duration), then hears the real note and sees the model's distribution, their guess, IC and H. This is retrieval practice and prediction error, which drives learning, and it trains *audiation* (imagination). Over sessions, the learner's hit rate vs. the model's becomes a personal metric.
- **Feasibility:** high; pure Python, sub-ms prediction; melody extraction needed for piano works.
- **Risk:** model IC ≠ the learner's surprise (different enculturation; monophonic reduction loses harmony). Mitigate by showing which corpus is "the listener", and by letting the learner record their own surprise rating so their disagreement with the model is data, not error.
- **Prior art:** probe-tone and betting paradigms in research (Pearce lab; "betting" tasks à la Huron), ear-training apps that ask for the next note but lack a probabilistic model. **A model-grounded, corpus-switchable version in a pianist's own repertoire appears novel** [speculative].
- **Evidence:** IDyOM–behaviour/EEG links [confirmed]; learning benefit of the game [speculative].

### Idea 2. Surprise × uncertainty map ("the Cheung plane")
- **Model:** a chord-level n-gram or IDyOM over DCML Roman numerals; plots IC vs. H per chord.
- **Mechanism:** each chord of a piece becomes a point in the (H, IC) plane. Clicking a point plays it. The learner discovers that the "magic" moments (the Neapolitan, a deceptive cadence) sit in the low-H/high-IC corner, as Cheung et al. found for pleasure.
- **Feasibility:** high; DCML labels exist for many target pieces.
- **Risk:** the Cheung result was for *pop chord sequences in isolation*; transfer to Beethoven is untested. Label it as a hypothesis.
- **Prior art:** the plane comes from Cheung et al. 2019 as a research figure. **I have not found it as an interactive analysis tool** [speculative].
- **Evidence:** [confirmed] for the pop study; [speculative] for transfer.

### Idea 3. "Two theories of expectation" split view (syntax vs. sound)
- **Model:** a cognitive chord n-gram (DCML-trained) vs. Leman's (2000) auditory short-term-memory / periodicity-pitch similarity model (as in Harrison & Pearce 2018; Harrison's R packages implement it, to my knowledge).
- **Mechanism:** for each chord, two bars: "grammatically expected" and "acoustically primed". Cases where they disagree (a chromatic mediant that shares tones with its predecessor; a V–I with little overlap) teach that "expected" has more than one meaning.
- **Feasibility:** medium; the Leman model needs reimplementation (pitch-images with leaky integration; moderate effort).
- **Risk:** both models are approximations, and listeners combine them. Present it as a debate, not as a verdict.
- **Originality:** **likely novel as a learning feature** [speculative]; research prior art in Sears et al. 2019 and Harrison & Pearce 2018.
- **Evidence:** [reported].

### Idea 4. Tension-curve overlay with "rate it yourself"
- **Model:** spiral-array tension ribbons (partitura) + the TPS sequential/surface components from DCML labels + Farbood-style parameter trends (dynamics, onset density) + IDyOM IC.
- **Mechanism:** the learner first draws their own tension curve while listening (continuous-response paradigm; mouse or touch slider, like Farbood and Lehne). Model curves are then revealed. Where they disagree, the app explains which component drives each model. This is metacognition: the learner's perception becomes an object of study.
- **Feasibility:** high for the spiral array and TPS-sequential; Farbood needs reimplementation from the paper (moderate).
- **Risk:** high. Tension models are validated on tiny datasets and ignore expressive dynamics (except Farbood). Never present a model curve as "the" tension.
- **Prior art:** Herremans & Chew visualise tension ribbons; continuous-rating interfaces are standard in research. **A multi-model comparison against the learner's own curve on their repertoire seems new** [speculative].
- **Evidence:** [confirmed] for the components, [speculative] for the pedagogy.

### Idea 5. Voice-leading odometer and orbifold view
- **Model:** Tymoczko minimal bijective voice leading (L1 semitones), plus Huron's perceptual voice-leading principles.
- **Mechanism:** for each chord change, show the voice-leading vector (e.g. (0, −1, +1, 0)), its size, and how it compares to the minimal one. A 3-D view for triads (prism) and a 2-D Möbius view for dyads, with the piece's path animated. The learner sees *why* common-tone and stepwise motion feel smooth, and spots where Chopin chooses *non*-minimal leadings for effect. Keyboard geometry link: highlight which fingers move by how much.
- **Feasibility:** very high (microseconds). The 3-D view is a three.js prism; tetrachords need projection or slices.
- **Risk:** low for the math. Moderate for perception: L1 distance ignores register, doubling and voice salience, and the soprano matters more than inner voices.
- **Prior art:** **ChordGeometries** (Tymoczko 2006) did the visualisation; Tonnetz viewers abound. **Linking it to the learner's actual fingering and to expert Roman numerals is new-ish** [speculative].
- **Evidence:** [confirmed] theory; [speculative] learning benefit.

### Idea 6. Voicing / consonance landscape explorer (piano-aware)
- **Model:** incon's composite (Harrison & Pearce 2020) via rpy2, or a Python reimplementation of Hutchinson–Knopoff roughness + har_18 harmonicity + corpus familiarity; spectra **stretched by piano inharmonicity**; register-dependent critical bandwidth; optional "pedal-sustained set".
- **Mechanism:** the learner holds a chord on the MIDI keyboard. The app shows the roughness, harmonicity and familiarity bars and a heat-map of "where to put the next note" across the keyboard (each candidate key coloured by the change in each component). Jazz use: rootless voicings, low-interval limits and drop-2 spacing explained by psychoacoustics, not by rule.
- **Feasibility:** high (milliseconds per chord, 88 candidates per frame).
- **Risk:** medium. Consonance ≠ "good"; familiarity is corpus-specific; the pedal and inharmonicity components are unvalidated extrapolations (flag them).
- **Prior art:** Sethares' dissonance-curve demos; William Sethares/Erlich-style tuning tools; various "dissonance calculators". **A keyboard-mapped, multi-factor, validated-model voicing explorer for pianists appears novel** [speculative].
- **Evidence:** models [confirmed]; piano inharmonicity effect [reported]; pedal [speculative].

### Idea 7. Reduction slider (surface → skeleton), with multiple analysts
- **Model:** a ladder: music21 chordify/ChordReducer → DCML chord-tone filter → outer voices → harmonic-rhythm skeleton → hand-made (or AutoSchA/proto-voice) deep levels. For melodies, GTTM time-span-tree depth cuts.
- **Mechanism:** a slider removes elaboration level by level. The learner *plays* each level (and is invited to improvise elaborations back onto it, which also builds jazz and partimento skills). Where the GTTM database or the Ni-Hahn dataset have **several analysts**, offer a "second analyst" toggle.
- **Feasibility:** shallow levels high; deep levels require hand annotation or unreliable models (AutoSchA covers only fugue subjects; 0.75 per-note accuracy).
- **Risk:** **high at deep levels**: an algorithmic Ursatz is easily wrong, and Schenkerian "correctness" is contested. Show the provenance of each level.
- **Prior art:** Hamanaka's melody morphing / time-span reduction demos; Schenkerian animation videos; textbook reduction exercises. **A playable multi-level ladder grounded in expert labels, with analyst disagreement, is mostly novel** [speculative].
- **Evidence:** GTTM inter-analyst 267/300 [confirmed]; Lehne outer-voice result [reported].

### Idea 8. Schema detector across the learner's repertoire (+ partimento practice)
- **Model:** Finkensiep et al. 2020 skipgram + classifier (DCMLab/schemata_code), or Carter-Enyi & Rabinovitch reduction + n-gram; trained and evaluated on the Mozart schema annotations.
- **Mechanism:** "Your pieces contain 14 Prinners, 6 Fontes, 3 Romanescas." Click to hear each instance; compare realisations across Mozart, Clementi and the learner's own pieces. Then a **partimento mode**: given a schema's bass, the learner realises upper voices at the keyboard, and the app checks the schema's outer-voice degrees and voice-leading quality (Idea 5 metrics).
- **Feasibility:** medium; the code is research-grade; performance on Romantic repertoire is unknown (expect many false positives).
- **Risk:** medium; schemata are style-bound (about 1720–1780). Detecting a "Prinner" in Chopin may be music-theoretically spurious.
- **Prior art:** Finkensiep's ipywidgets annotation tool; Gjerdingen's Monuments of Partimenti; UUPart search; schema apps in conservatory teaching. **Cross-repertoire detection plus a realisation-checking loop is novel to my knowledge** [speculative].
- **Evidence:** algorithm and dataset [confirmed]; generalisation [speculative].

### Idea 9. "How typical is this progression?" corpus lens with uncertainty
- **Model:** conditional chord n-gram counts over DCML sub-corpora (Beethoven quartets and sonatas, Mozart, Chopin mazurkas, Schumann, Grieg...), with Bayesian (Dirichlet) intervals; DiMCAT/ms3 pipeline.
- **Mechanism:** select any span of Roman numerals and see its frequency per composer with credible intervals, the top-k continuations per composer, and links to the actual occurrences (which can be played). This turns style into evidence: "Chopin's mazurkas use ♭VI→V 4× more often than Mozart's sonatas, n=…".
- **Feasibility:** high; small data; deterministic.
- **Risk:** label-convention differences between corpora and annotators (DCML vs. When-in-Rome), and small-n artefacts. Show counts, not just probabilities.
- **Prior art:** **Hooktheory Trends** (pop, no composer split, no uncertainty); DCML papers (static figures). **Composer-conditional, uncertainty-aware, playable is new** [speculative].
- **Evidence:** corpus facts [confirmed]; pedagogy [speculative].

### Idea 10. Jazz harmony parse-tree explorer
- **Model:** the Jazz Harmony Treebank (expert trees, about 150 standards) + the Harasim et al. 2018 PACFG parser for user-entered changes (n-best parses with probabilities).
- **Mechanism:** a lead sheet's changes are shown as a tree (prolongation/preparation). Collapse a subtree and hear the substituted, simpler progression. Enter a reharmonisation and see whether it still parses, and how. Ambiguous parses are shown side by side, the jazz analogue of the Moonlight disagreement.
- **Feasibility:** expert trees: high (JSON). Parser: medium (research code; reimplementing a CKY over a small grammar is feasible).
- **Risk:** low-moderate; grammar coverage of modern or modal tunes is weak.
- **Prior art:** the JHT web tree editor; Rohrmeier's papers. **An interactive, playable tree explorer for a learner is novel** [speculative].
- **Evidence:** [confirmed] dataset and parser.

### Idea 11. Motif tracker with transformation labels
- **Model:** SIATEC/COSIATEC (OMNISIA, Java) or a Python reimplementation, extended to inversion and augmentation groups; evaluated on BPS-Motif (Beethoven first movements); expert annotations shown when available.
- **Mechanism:** a motif is highlighted and every occurrence lights up, coloured by transformation (transposed, inverted, rhythmically augmented, sequenced). A timeline shows the motif's "life" across the sonata form. Exercise: the learner finds occurrences first, then compares with the algorithm and with BPS-Motif annotators.
- **Feasibility:** high for the algorithms (O(n² log n) for SIA on a few thousand notes is interactive); BPS-Motif licence unverified.
- **Risk:** pattern-discovery algorithms over-generate (MIREX F1 ≈ 0.5 on JKU-PDD). Use expert annotations as primary and algorithms as "candidates".
- **Prior art:** MIREX systems; music-analysis tools (e.g. Humdrum pattern search). **A learner-facing, annotation-grounded tracker is moderately novel** [speculative].
- **Evidence:** [confirmed] dataset and benchmark numbers with caveats.

### Idea 12. Expressive timing coach: "why did they slow down here?"
- **Model:** partitura alignment + KTH rules (Director Musices; phrase arch, final ritard à la Friberg–Sundberg runners, harmonic charge) + Repp-style curves from aligned professional performances + Todd's phrase-arch model.
- **Mechanism:** the learner plays; their tempo and dynamics curves overlay the rules' predictions and the professionals' range (a band). Each deviation is annotated with the structural fact it relates to (phrase end, harmonic charge peak, metrical accent). A "turn on one rule at a time" synthesis lets the learner *hear* the contribution of each rule.
- **Feasibility:** medium; Director Musices is Lisp (call it via file export) or rules can be reimplemented in Python (phrase arch and final ritard are simple formulas); alignment via partitura is mature.
- **Risk:** medium-high; it risks normativity ("play like the average"). Repp shows diversity is legitimate; frame the band as "common practice", not as correctness.
- **Prior art:** Director Musices and pDM themselves; Widmer group's "Con Espressione" demos; research on performance feedback systems. **Combining rules + real-pianist bands + structural explanation for self-practice is moderately novel** [speculative].
- **Evidence:** Repp and KTH [confirmed/reported]; pedagogy [speculative].

### Idea 13. "Surprising to whom?" corpus-swap listener
- **Model:** IDyOM LTMs trained on different corpora (Bach chorales, classical sonatas, Romantic piano, jazz standards), plus a model trained *on the learner's own practised repertoire* (an evolving "you" model).
- **Mechanism:** the same passage gets a different surprise profile per "listener". The "you" model shows how the learner's enculturation shifts as they practise, an explorable account of statistical learning.
- **Feasibility:** high.
- **Risk:** the "you" model is a caricature; the learner hears far more music than they practise.
- **Originality:** **likely novel** [speculative]; research uses corpus-specific LTMs (e.g. cross-cultural enculturation studies, IDyOMpy's enculturation modelling).
- **Evidence:** [reported] enculturation modelling; [speculative] feature.

### Idea 14. Model-disagreement dashboard ("lenses that argue")
- **Model:** meta-feature aggregating disagreements: two Roman-numeral analyses (DCML vs. When-in-Rome), two tension models, syntax vs. sensory expectation, algorithmic vs. expert motifs, GTTM analyst A vs. B.
- **Mechanism:** a timeline marks bars where lenses disagree most (normalised divergence). These are the bars to *study*: each comes with an LLM explanation grounded in both lenses' outputs.
- **Feasibility:** high once the individual lenses exist.
- **Risk:** disagreement magnitude across heterogeneous models is not commensurable; use ranks, not raw differences.
- **Originality:** **genuinely novel as a design principle**, to my knowledge [speculative]. Closest prior art: When-in-Rome hosting multiple analyses of the same work, and model-comparison figures in papers.
- **Evidence:** [speculative].

### Idea 15. Partimento realisation corpus builder (the gap)
- **Model:** UUPart / Monuments of Partimenti basses + Idea 5/6 metrics + schema labels.
- **Mechanism:** the learner's realisations are recorded, scored (voice-leading size, parallels, schema fidelity, roughness), and accumulate into a personal corpus, which becomes an IDyOM "you" corpus (Idea 13).
- **Feasibility:** medium (basses need transcription to MusicXML for some sources).
- **Risk:** automated checking of style is crude.
- **Originality:** **novel**, since no machine-readable realisation corpus was found [confirmed: not found].

---

## 10. Summary judgement: which models to adopt first

| Priority | Model / tool | Why |
|---|---|---|
| 1 | IDyOMpy or GraphIDyOM (+ Lisp IDyOM as reference for validation) | Best-validated cognition model (behaviour, EEG, MEG, ECoG), cheap, interpretable, powers Ideas 1, 2, 13 |
| 1 | DCML corpora + ms3/DiMCAT corpus statistics | Grounded, expert data; Ideas 2, 9; directly matches the core principle |
| 1 | Tymoczko voice-leading math (reimplement) | Trivial cost, exact, high explanatory value (Ideas 5, 8, 15) |
| 2 | incon models (rpy2 or reimplement) + piano spectra | Validated consonance; Idea 6 |
| 2 | partitura (tension ribbons, voice separation, alignment) | Already Apache-2.0 and maintained; Ideas 4, 12 |
| 2 | Jazz Harmony Treebank | Expert trees for jazz; Idea 10 |
| 3 | Schema detection (DCMLab), BPS-Motif, OMNISIA | Valuable but research-grade; Ideas 8, 11 |
| 3 | Director Musices / KTH rules | Interpretable performance rules; Idea 12 |
| Avoid as truth | AutoSchA / automatic Schenker, TPS hierarchical tension, transformer embeddings | Narrow training data or unvalidated perceptual meaning; show only as flagged hypotheses |

**Key gaps found:** (1) no maintained open-source TPS/Lerdahl–Krumhansl implementation; (2) no Python port of incon; (3) no public large Schenkerian dataset (Ni-Hahn: by request); (4) no partimento realisation corpus; (5) no study quantifying pedal resonance vs. perceived dissonance; (6) no recent large continuous-tension-rating dataset.

---

## 11. References (primary, as cited)

- Bono Rosselló, L. (2026). GraphIDyOM. arXiv:2607.25787.
- Callender, C., Quinn, I., & Tymoczko, D. (2008). Generalized voice-leading spaces. *Science* 320:346–348. doi:10.1126/science.1153021
- Cancino-Chacón, C. E., Grachten, M., Goebl, W., & Widmer, G. (2018). Computational models of expressive music performance. *Front. Digit. Humanit.* 5:25. doi:10.3389/fdigh.2018.00025
- Carter-Enyi, A., & Rabinovitch, G. (2021). Onset and contiguity. *Music Theory Online* 27(4).
- Cheung, V. K. M., et al. (2019). Uncertainty and surprise jointly predict musical pleasure... *Current Biology* 29(23):4084–4092. doi:10.1016/j.cub.2019.09.067
- Chew, E., & Wu, X. (2004). Separating voices in polyphonic music: A contig mapping approach. CMMR 2004, LNCS 3310.
- Di Liberto, G. M., et al. (2020). Cortical encoding of melodic expectations in human temporal cortex. *eLife* 9:e51784. doi:10.7554/eLife.51784
- Farbood, M. M. (2012). A parametric, temporal model of musical tension. *Music Perception* 29(4):387–428. doi:10.1525/mp.2012.29.4.387
- Finkensiep, C., Déguernel, K., Neuwirth, M., & Rohrmeier, M. (2020). Voice-leading schema recognition using rhythm and pitch features. ISMIR 2020.
- Finkensiep, C., & Rohrmeier, M. (2021). Modeling and inferring proto-voice structure in free polyphony. ISMIR 2021, 189–196.
- Foscarin, F., Karystinaios, E., et al. (2024). Cluster and Separate. ISMIR 2024.
- Friberg, A., Bresin, R., & Sundberg, J. (2006). Overview of the KTH rule system for musical performance. *Adv. Cogn. Psychol.* 2(2–3):145–161.
- Friberg, A., & Sundberg, J. (1999). Does music performance allude to locomotion? *JASA* 105(3):1469–1484.
- Gjerdingen, R. (2007). *Music in the Galant Style*. OUP.
- Guan, X., Ren, Z., & Pelofi, C. (2022). py2lispIDyOM. *JOSS* 7(79):4738. doi:10.21105/joss.04738
- Hamanaka, M., Hirata, K., & Tojo, S. (2006). Implementing "A Generative Theory of Tonal Music". *JNMR* 35(4):249–277.
- Hamanaka, M., Hirata, K., & Tojo, S. (2014). Musical structural analysis database based on GTTM. ISMIR 2014, 325–330.
- Harasim, D., Rohrmeier, M., & O'Donnell, T. J. (2018). A generalized parsing framework for generative models of harmonic syntax. ISMIR 2018, 152–159.
- Harasim, D., Finkensiep, C., Ericson, P., O'Donnell, T. J., & Rohrmeier, M. (2020). The Jazz Harmony Treebank. ISMIR 2020, 207–215.
- Harrison, P. M. C., & Pearce, M. T. (2020). Simultaneous consonance in music perception and composition. *Psychological Review* 127(2):216–244. doi:10.1037/rev0000169
- Hentschel, J., Neuwirth, M., & Rohrmeier, M. (2021). The Annotated Mozart Sonatas. *TISMIR* 4(1). doi:10.5334/tismir.63
- Hentschel, J., Rammos, Y., Moss, F. C., Neuwirth, M., & Rohrmeier, M. (2024). An annotated corpus of tonal piano music from the long 19th century. *Empirical Musicology Review* 18(1):84–95.
- Herremans, D., & Chew, E. (2016). Tension ribbons. TENOR 2016.
- Hsiao, Y.-T., Hung, T.-W., Chen, T.-P., & Su, L. (2023). BPS-Motif. ISMIR 2023.
- Huron, D. (2001). Tone and voice. *Music Perception* 19(1):1–64. / (2006) *Sweet Anticipation*. MIT Press. / (2016) *Voice Leading*. MIT Press.
- Karystinaios, E., Foscarin, F., & Widmer, G. (2023). Musical voice separation as link prediction. IJCAI 2023.
- Kern, P., Heilbron, M., de Lange, F. P., & Spaak, E. (2022). Cortical activity during naturalistic music listening reflects short-range predictions based on long-term experience. *eLife* 11:e80935. doi:10.7554/eLife.80935
- Kirlin, P. B., & Jensen, D. D. (2015). Learning to uncover deep musical structure. AAAI-15. doi:10.1609/aaai.v29i1.9476
- Lehne, M., Rohrmeier, M., Gollmann, D., & Koelsch, S. (2013). The influence of different structural features on felt musical tension in two piano pieces by Mozart and Mendelssohn. *Music Perception* 31(2):171–185.
- Lerdahl, F., & Krumhansl, C. L. (2007). Modeling tonal tension. *Music Perception* 24(4):329–366. doi:10.1525/mp.2007.24.4.329
- Marion, G., Gao, F., Gold, B. P., Di Liberto, G. M., & Shamma, S. (2024). IDyOMpy. *J. Neurosci. Methods*, 110347. doi:10.1016/j.jneumeth.2024.110347
- Marjieh, R., Harrison, P. M. C., Lee, H., Deligiannaki, F., & Jacoby, N. (2024). Timbral effects on consonance... *Nature Communications* 15:1482. doi:10.1038/s41467-024-45812-z
- Marsden, A. (2010). Schenkerian analysis by computer. *JNMR* 39(3):269–289.
- Meredith, D., Lemström, K., & Wiggins, G. A. (2002). Algorithms for discovering repeated patterns... *JNMR* 31(4):321–345.
- Moss, F. C., Neuwirth, M., Harasim, D., & Rohrmeier, M. (2019). Statistical characteristics of tonal harmony. *PLoS ONE* 14(6):e0217242. doi:10.1371/journal.pone.0217242
- Navarro-Cáceres, M., et al. (2020). A computational model of tonal tension profile of chord progressions in the Tonal Interval Space. *Entropy* 22(11):1291. doi:10.3390/e22111291
- Neuwirth, M., Harasim, D., Moss, F. C., & Rohrmeier, M. (2018). The Annotated Beethoven Corpus (ABC). *Front. Digit. Humanit.* 5:16. doi:10.3389/fdigh.2018.00016
- Ni-Hahn, S., et al. (2024). A new dataset, notation software, and representation for computational Schenkerian analysis. ISMIR 2024, 866–873. arXiv:2408.07184
- Ni-Hahn, S., Zhu, R., Yin, J., Jiang, Y., Rudin, C., & Mak, S. (2026). AutoSchA. AAAI 2026. arXiv:2512.18232
- Parncutt, R., et al. (2023). [Consonance of the 19 trichords with piano and organ-like tones]. *Psychological Topics* (open access; pt.ffri.hr). Exact title, co-authors and pages to verify.
- Pearce, M. T. (2018). Statistical learning and probabilistic prediction in music cognition. *Ann. NYAS* 1423:378–395. doi:10.1111/nyas.13654
- Pearce, M. T., & Wiggins, G. A. (2006). Expectation in melody. *Music Perception* 23(5):377–405.
- Repp, B. H. (1992). Diversity and commonality in music performance. *JASA* 92(5):2546–2568.
- Rohrmeier, M. (2011). Towards a generative syntax of tonal harmony. *J. Math. Music* 5(1):35–53. / (2020) The syntax of jazz harmony. *Music Theory and Analysis* 7(1):1–63.
- Sears, D. R. W., Pearce, M. T., Caplin, W. E., & McAdams, S. (2018). Simulating melodic and harmonic expectations for tonal cadences using probabilistic models. *JNMR* 47(1):29–52.
- Sears, D. R. W., Spitzer, J., Caplin, W. E., & McAdams, S. (2020). Expecting the end. *Psychology of Music* 48(3). doi:10.1177/0305735618803676
- Sethares, W. A. (1993). Local consonance and the relationship between timbre and scale. *JASA* 94(3):1218–1228.
- Taieb, R., Greenberg, Y., & Sober, B. (2026). Probabilistic multilabel graphical modelling of motif transformations in symbolic music. arXiv:2603.26478.
- Todd, N. P. M. (1992). The dynamics of dynamics. *JASA* 91(6):3540–3550.
- Tymoczko, D. (2006). The geometry of musical chords. *Science* 313:72–74. doi:10.1126/science.1126287 / (2011) *A Geometry of Music*. OUP.
- Wu, S., et al. (2025). CLaMP 3. Findings of ACL 2025, 2605–2625. doi:10.18653/v1/2025.findings-acl.133
- Zeng, M., et al. (2021). MusicBERT. Findings of ACL 2021. arXiv:2106.05630

**Software (checked 2026-10-23):** mtpearce/idyom (GPL-3.0, v1.8); GuiMarion/IDyOMpy (GPL-3.0); py2lispidyom (PyPI 1.0.2, 2022); pmcharrison/incon (MIT, R); partitura (Apache-2.0, 1.9.0, 2026-05); music21 (10.5.1, 2026-10-22); ms3 (GPL-3.0, 2.6.5); dimcat (GPL-3.0+, 3.4.1); musif (MIT, 1.3.0); miditok (MIT, 3.1.0); symusic (MIT, 0.6.0); graphmuse (0.0.5, 2024); dissonant (0.1.1, 2018); ruiguo-bio/midi-miner (GPL-3.0); chromamorph/omnisia (Java, licence unverified); DCMLab/schemata_code; manoskary/vocsep_ijcai2023; Director Musices 3.1.5 (KTH, 2024-05-30).
