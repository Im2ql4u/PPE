# Visualization, HCI and Interactive/Generative Systems for Music Understanding and Improvisation

> **Agent-produced research note, dated 2026-10-23. To be reviewed.**
> Scope: research prototypes and unconventional approaches relevant to a local, Chrome-based "computational piano learning laboratory" (MIDI piano in, macOS/Apple Silicon host).
> Evidence tags: **[confirmed]** = checked against a primary source (paper, repo, project page) during this session; **[reported]** = stated by a secondary source or by the authors without independent check, or recalled from prior knowledge and not re-verified this session; **[speculative]** = this note's own inference or proposal.
> Status: VERSION 2 (v1 written early because of interruption risk; v2 adds a verification pass). Items still marked *TODO-verify* need a primary-source check.

---

## 0. Executive summary

1. **Geometric harmony visualizations are mature as ideas but almost entirely unvalidated as learning tools.** Harmony Space (Holland), the Tonnetz family (HexaChord, IRCAM's web Tonnetz), Chew's Spiral Array (MuSA.RT), Tymoczko's ChordGeometries, Sapp's keyscapes and DCML's wavescapes all have strong theoretical motivation; user-study evidence is thin (small preliminary studies, classroom anecdotes). The project should treat them as *exploration instruments*, not proven pedagogy, and build in its own lightweight self-measurement. [confirmed for the paucity of evidence in sources found]
2. **The best-evidenced piano augmentation (P.I.A.N.O., CHI 2014) proves faster *note-playing*, not musical understanding or reading.** Its projected piano-roll beat Synthesia and sheet music on short-term accuracy (n=56 within-subjects; n=18 over one week), but by design bypasses notation. A 2022 survey of augmented-piano prototypes concludes it is "still not understood" whether these systems support learning and notes teacher scepticism about piano-roll overlays undermining sight-reading. [confirmed] → For this project: overlays should *translate* notation (anchor to the score) rather than *replace* it.
3. **Locally runnable generative models are now good enough for pedagogically meaningful interaction on Apple Silicon.** EleutherAI's **Aria** (Apache-2.0, LLaMA-3.2-1B architecture, MLX backend, real-time continuation demo; Aria-Duet turn-taking on a Disklavier) and the **Anticipatory Music Transformer** (Apache-2.0 code and 360M weights, infilling/accompaniment conditioned on a melody) are the two strongest candidates. **NotaGen** (MIT, ABC-notation output, 110M–516M params) is the best candidate for *score-level* counterfactuals in classical style. **Somax2** (GPL-3.0, Max+Python, native ARM) is the most mature co-improvisation engine but requires Max. Google's **ReaLchords/ReaLJam** line is the research state of the art for real-time melody→chord accompaniment, but I found no public weights. [confirmed except where noted]
4. **Counterfactual ("what-if") listening is under-researched.** No study was found that directly tests minimal-pair/contrastive listening for harmony learning. The nearest music evidence is that *interleaved* exposure to composers' styles beats blocked exposure for novices, even though learners believe the opposite (Wong et al. 2020, *JRME*); general category-learning literature supports contrastive designs, but harmony-specific evidence is a gap. This is an *opportunity* for the project's distinctive contribution. [confirmed absence in searches; mechanism claim is speculative]
5. **Expressive-performance visualization has good, reusable precedents**: the tempo–loudness Performance Worm (Langner & Goebl 2003; Dixon, Goebl & Widmer 2002), Sapp's correlation scape plots (Mazurka project, 2,500+ recordings of 49 mazurkas), and the Parangonada/Parangonar/Partitura alignment stack. All are directly applicable to the learner's own MIDI. [confirmed]

The most promising novel concepts (Section 9) are: **Counterfactual Score** (click a chord → hear N alternatives as minimal pairs, ranked by voice-leading distance), **Voice-Leading Strings** (animated voice paths in a score-anchored view and in orbifold space), **Improvise Inside the Piece** (corpus-driven accompaniment that keeps a piece's harmony while the learner improvises), **Self-Worm / Self-Scape** (performance worm and correlation scape of the learner vs. reference recordings), and **Tonnetz-to-Hand Morph** (the same chord path shown as Tonnetz trajectory and as hand-shape changes on the keyboard).

---

## 1. Visualizations of harmony and tonal space

### 1.1 Harmony Space (Simon Holland, 1989– )
- **What:** A 2-D grid of pitches arranged by thirds/fifths (after Longuet-Higgins and Balzano), on which chords, keys, progressions and modulations become shapes and paths; designed so novices can "sketch, analyse and experiment with harmony" using a single spatial metaphor. Variants: desktop, camera-tracked, and the whole-body **Song Walker Harmony Space** (users walk/step on a floor projection; collaborative roles for root, chord quality, key). [confirmed]
- **Citations:** Holland, S. (1994) *Learning about harmony with Harmony Space: an overview* (Open University repository) https://oro.open.ac.uk/59664 ; Holland, Wilkie, Bouwer, Dalgleish, Mulholland, "Whole Body Interaction in Abstract Domains" / "Song Walker Harmony Space: Embodied Interaction Design for Complex Musical Skills", in Holland et al. (eds.) *Music and Human-Computer Interaction*, Springer 2013, https://link.springer.com/10.1007/978-1-4471-2990-5_12 ; prototype: Holland et al., "Running up Blueberry Hill", TEI 2009, https://oro.open.ac.uk/17966 . [confirmed]
- **Evidence:** Thesis-era small-scale study claiming the interface "considerably reduces the prerequisites required for novices to learn about, sketch, analyse and experiment with harmony"; Song Walker preliminary study with beginners and experts doing performance/composition/analysis tasks (no effect sizes found); a 2019 classroom trial in Italy (blog write-up, not controlled) https://fass.open.ac.uk/research/groups/health-and-arts/blogs/teaching-music-harmony-to-school-children-using-technology . [confirmed that evidence is qualitative/preliminary]
- **Availability:** No maintained open-source implementation found. [reported]
- **Reuse/learn:** The design rationale is explicitly grounded in *image schemas* (containment, source–path–goal) — a good vocabulary for our design docs. The key learning: a single consistent spatial metaphor for chords, keys and modulation lets beginners reason spatially rather than symbolically. Its weakness for us: the grid is not the piano keyboard, so a mapping layer is required (→ Idea 9.B.1).

### 1.2 Tonnetz-based interfaces: HexaChord, IRCAM Tonnetz web, bach.tonnetz
- **What:** Louis Bigo's **HexaChord** represents any MIDI sequence as trajectories in the (3,4,5)-Tonnetz and the eleven other Tonnetze generated by 3-note interval structures, computes "compactness" of a piece in each space, and lets users apply geometric transformations (translations, rotations, reflections) to trajectories, which transform the music; results export as MIDI. The underlying simplicial complexes were computed in the spatial-computing language MGS. Companion: **bach.tonnetz** (Max, for composition) and the IRCAM **Tonnetz** web platform built on HexaChord's functionality, used in schools/workshops. [confirmed]
- **Citations:** Bigo, Giavitto, Spicher, "Building Topological Spaces for Musical Objects", MCM 2011 / Bigo & Andreatta papers on HAL: https://hal.archives-ouvertes.fr/hal-00925748 , https://hal.archives-ouvertes.fr/hal-01263349 ; ICMC-SMC 2014 paper on HexaChord: https://speech.di.uoa.gr/ICMC-SMC-2014/images/VOL_2/1112.pdf ; "The Tonnetz Environment: A Web Platform for Computer-aided…" (2021) https://www.scitepress.org/Papers/2021/105326/105326.pdf . [confirmed]
- **Evidence:** No controlled learning study found. Use in workshops reported. [confirmed absence in searches]
- **Availability:** HexaChord binaries historically from Bigo's page; licence and maintenance unclear. *TODO-verify.* The Tonnetz math is trivial to reimplement in JS/SVG (no dependency needed).
- **Reuse/learn:** (a) The *transformation-as-composition* idea — reflect a progression in the Tonnetz to get its "negative harmony"-like mirror, translate it to transpose — is a counterfactual generator in disguise (→ Idea 9.B.4). (b) "Compactness" of a piece in different Tonnetze is a nice explorable statistic ("Debussy lives in the whole-tone Tonnetz; Bach in the 3-4-5 one").

### 1.3 Spiral Array and MuSA.RT (Elaine Chew)
- **What:** The Spiral Array is a 3-D helical model where pitches lie on a helix of fifths; chords and keys are "centres of effect" (weighted centroids) inside it. **MuSA.RT** maps live MIDI onto the Spiral Array in real time, showing short- and long-term tonal context trackers and the nearest triad/key as music unfolds; demonstrated in concert at ISMIR 2008. [confirmed]
- **Citations:** Chew & François, "MuSA.RT: Music on the Spiral Array. Real-Time", ACM Multimedia 2003, https://kclpure.kcl.ac.uk/ws/files/266871545/ChewFrancois-MM03-957013.957106.pdf ; Chew, *Mathematical and Computational Modeling of Tonality*, Springer 2014; Stanford HCI seminar "Analytical Listening through Interactive Visualization" https://hci.stanford.edu/seminar/abstracts/07-08/080229-chew-francois.html . [confirmed]
- **Evidence:** Demonstrations and concert use; no learning study found. [confirmed absence]
- **Availability:** MuSA_RT 1.0 was released as a macOS app (historically on the Mac App Store); current status unknown. *TODO-verify.*
- **Reuse/learn:** The *centre of effect* is an excellent "physicist-friendly" abstraction — a running weighted centroid in a geometric embedding — and gives a continuous tonal trajectory for any MIDI stream, including the learner's improvisation. Cheap to reimplement in a few hundred lines of JS + three.js.

### 1.4 Voice-leading geometry: ChordGeometries (Dmitri Tymoczko)
- **What:** Free software accompanying Tymoczko's *Science* paper (2006) "The Geometry of Musical Chords". Represents n-note chords as points in orbifolds (T^n/S_n); voice leadings are paths; distance = voice-leading size in semitones. Input from a MIDI keyboard or on-screen keyboard; demos animate Chopin (e.g., E minor Prelude) moving through 4-D chord space. [confirmed]
- **Citations:** Tymoczko, D. (2006), *Science* 313:72–74; demo videos https://vimeo.com/20301089 , https://vimeo.com/20300784 ; Tymoczko, *A Geometry of Music*, OUP 2011. Download historically at music.princeton.edu/~dmitri/ChordGeometries.html (Mac OS X / Windows XP era). [confirmed for existence; current compatibility unknown]
- **Evidence:** None as a learning tool. [confirmed absence]
- **Reuse/learn:** The project does not need the full orbifold rendering (hard to read for a beginner), but the *quantity* — minimal voice-leading distance between chords, computed by optimal assignment — is a key building block for "counterfactual" ranking (Section 5) and for the "voice-leading strings" animation (Idea 9.A.2). For 3-note chords the 3-D orbifold (a twisted triangular prism with augmented triads at the centre) is visualizable and genuinely illuminating for a physicist.

### 1.5 Keyscapes and wavescapes
- **Keyscapes (Craig Sapp):** Triangular plots; x = time, y = analysis-window length; each cell coloured by the key found (Krumhansl–Schmuckler) in that window, so the apex shows the global key and the base shows local tonicizations. Sapp, "Visual Hierarchical Key Analysis", *ACM Computers in Entertainment* 3(4), 2005, https://esf.ccarh.org/254-old/254_LiteraturePack1/Harmony/Sapp_VisualHierKeyAnal05.pdf ; Humdrum `mkeyscape` (C++), manual at extras.humdrum.org/man/mkeyscape; ~5,000 keyscapes of MIDI files on Sapp's site. [confirmed]
- **Wavescapes (DCML/EPFL):** Viaccoz, Harasim, Moss & Rohrmeier, "Wavescapes: A visual hierarchical analysis of tonality using the discrete Fourier transform", *Musicae Scientiae* 27(2), 2023, 390–427, https://infoscience.epfl.ch/record/291958 . Replace key-finding by DFT coefficients of pitch-class distributions (coefficient k=5 ≈ diatonicity, k=3 ≈ hexatonic/augmented, k=4 ≈ octatonic, k=6 ≈ whole-tone, etc.), so the plot does not presuppose 24 major/minor keys; eight case studies from Josquin to Coltrane and Ligeti. Python library `wavescapes` on PyPI (v1.2.0, 2022-11) and the open-source web app **midiVERTO** (Harasim, Affatato, Moss), hosted at https://dcmlab.github.io/MIDFT , explicitly aimed at making DFT analyses accessible to students; paper https://ar5iv.arxiv.org/html/2203.13158 . [confirmed; code licence not found]
- **Evidence:** Analytical/musicological validity argued via case studies; no learner studies. [confirmed]
- **Reuse/learn:** For a physicist, the DFT-of-pitch-class-set view (Quinn, Amiot, Yust lineage) is the most natural "formal" entry point to tonality; the scape plot is a natural multi-scale representation. A keyscape/wavescape of the *piece being practised* is a beautiful "map" that can be linked bidirectionally to the score (click a triangle cell → highlight that span). midiVERTO is a direct precedent for a browser implementation. Licence of `wavescapes`/midiVERTO code: *TODO-verify*.

### 1.6 Pitch-class-set visualizations
- Clock diagrams (pc-set as polygon on a 12-gon), interval vectors, the DFT phase/magnitude spaces (Amiot 2016, *Music through Fourier Space*; Yust 2015 "Schubert's harmonic language and Fourier phase space", *JMT*). [reported]
- **Reuse:** A clock-face view under the keyboard is the single cheapest "geometry" display: transposition = rotation, inversion = reflection, and it directly prepares the Tonnetz and DFT views. Symmetry of chords (dim7, augmented, whole-tone) becomes visible as rotational symmetry — exactly the pattern a physicist will enjoy.

### 1.7 Isomorphic keyboard layouts and learnability
- **Layouts:** Wicki–Hayden (concertina/hexagonal), Bosanquet, Jankó (6-row piano keyboard), Lumatone (hexagonal, 280 keys, microtonal), Striso (Wicki-like, expressive). [reported]
- **Evidence (the only controlled studies found):**
  - MacRitchie & Milne (2017), "Exploring the effects of pitch layout on learning a new musical instrument", *Applied Sciences* 7(12):1218. N = 24 experienced musicians, iPad layouts. Adjacency of major seconds improved accuracy in training/retention (unless ceiling); shearing the layout so the pitch axis is vertical *reduced* training accuracy but *substantially improved* transfer to an untrained melody. [confirmed via abstract]
  - Stanford, Milne & MacRitchie (2018), "The effect of isomorphic pitch layouts on the transfer of musical learning", *Applied Sciences* 8(12):2514. Isomorphic (Wicki or Bosanquet) vs minimally non-isomorphic layouts; isomorphism helped musicians transfer learning; non-musician results mixed. https://researchers.westernsydney.edu.au/en/publications/the-effect-of-isomorphic-pitch-layouts-on-the-transfer-of-musical/ [confirmed via abstract]
  - Dataset: Western Sydney research data https://research-data.westernsydney.edu.au/published/d60069d0da7a11eda18a3d1ddaa0821f/ [confirmed]
- **What this means for us:** The learner plays a standard piano, so isomorphic hardware is out of scope. But the result that *structure-preserving layouts aid transfer* (for people who already have musical schemas) motivates a **virtual isomorphic projection**: show the piano-played chord simultaneously on an isomorphic/Tonnetz lattice where every major triad has the same shape, so the learner sees invariance that the piano keyboard hides (white/black key asymmetry). Claims by vendors that isomorphic layouts are "easier to learn" are not supported beyond these small studies. [confirmed for evidence; inference speculative]

---

## 2. Score-centric interaction research

### 2.1 Augmented/analytical scores
- **DCML annotation standard and tooling:** The Digital and Cognitive Musicology Lab (EPFL) annotates corpora (Beethoven sonatas & quartets, Mozart sonatas, Chopin mazurkas, etc.) with a Roman-numeral syntax embedded in MuseScore files; tools such as `ms3` parse them; DCML also released tree-annotation code (Finkensiep & Harasim, Zenodo 2020, https://zenodo.org/records/4153253). A DCML web score-annotation tool ("dez") is recalled from prior knowledge but **could not be located** in this session — treat as unverified. The **When in Rome** meta-corpus (Gotham et al.) unifies Roman-numeral analyses in RomanText — ready ground truth for harmony overlays. [reported; the project already has a `when_in_rome` corpus under `data/external/` — confirmed from the working directory]
- **Rendering stack:** **Verovio** (RISM Digital; MEI/MusicXML/Humdrum/ABC → SVG; C++ compiled to WASM/JS; **LGPL-3.0** — unmodified, dynamically linked use is fine for a local app; credit required) https://book.verovio.org/introduction/licensing.html [confirmed]. **OpenSheetMusicDisplay** (MusicXML → SVG via VexFlow; npm metadata says BSD-3-Clause, some older sources say MIT — permissive either way) [reported]. Verovio Humdrum Viewer (Sapp) shows analysis overlays from Humdrum filters. Both renderers emit per-note SVG element IDs — the key affordance for overlays and synchronization. [confirmed for Verovio]
- **Colour-coded notation evidence:** Colour-coded noteheads/harmony are common commercially (Hooktheory colour-by-scale-degree, Figurenotes, "Colourchord" lyric-sheets for four-part singing), but controlled evidence is weak and mostly about *reading*, not harmony: Rogers (1991, *JRME*, N=92 fifth/sixth-grade wind players, 12 weeks) found no clear advantage for colour-coded notation, with secondary accounts reporting *lower* sight-reading in the colour group (possible reliance on colour instead of notation); Rogers (1996) found a slight advantage for rhythm reading; a Missouri State thesis (Fair) found no effect on first-graders' rhythm reading but a strong preference for colour. The only harmony-specific study found is a small qualitative one (Universidade do Minho, four students, functional-harmony colour scheme). https://journals.sagepub.com/doi/abs/10.2307/3344609 , https://bearworks.missouristate.edu/theses/2672 [confirmed via abstracts/secondary summaries; Rogers 1991 result direction is contested between sources]
- **Implication:** Colour as a permanent layer risks becoming a crutch (the same concern as piano-roll overlays); colour as a *temporary, selection-scoped explanation* is the safer pattern. [speculative]
- **Lesson:** Overlays should be *toggleable layers* with a "fade" schedule (show analysis while listening; hide during playing), and the analysis should be a property of score spans (selection-based), not a permanent colouring.

### 2.2 Score–audio synchronization ("Soundslice-style")
- **Soundslice** (commercial): notation synchronized to real video/audio, loop/slow-down, per-note highlighting. [reported]
- Research lineage: score following / audio-to-score alignment (Dixon & Widmer MATCH 2005; Arzt & Widmer real-time tracking; Peter/Müller sync toolchains; `synctoolbox` from the Müller group (MIT licence *[reported]*)). For MIDI input from the learner's piano, symbolic score-following is much simpler: online DTW or HMM over expected onsets (as in Parangonar's matchers). [reported]
- **Reuse:** For the learner's own playing: MIDI → partitura score alignment → per-note highlight in Verovio SVG. For reference recordings: audio→MIDI transcription (e.g., Kong et al. high-resolution piano transcription, or Basic Pitch) → alignment. [reported]

### 2.3 Explorable explanations for music
- **Chrome Music Lab** (Google Creative Lab, 2016): Song Maker, Chords, Arpeggios, Harmonics, Spectrogram, Piano Roll, etc. Code on GitHub under Apache-2.0; the repository **was archived on 19 April 2026** (read-only). https://github.com/googlecreativelab/chrome-music-lab [confirmed]
- **Ableton Learning Music** (2017): browser lessons on beats, melodies, basslines, chords and song structure with Live-like clip grids, real-song examples and a playground exporting to Live. https://learningmusic.ableton.com (blog: https://ableton.com/en/blog/learn-music-in-your-browser) . Closed source. [confirmed]
- **Music Mouse** (Laurie Spiegel, 1986): an "intelligent instrument" where mouse movement in 2-D drives harmonized voices constrained by a selectable scale/harmony mode — an early example of *constraint-based exploration* where the system guarantees musical coherence and the user explores. Re-released by **Eventide in collaboration with Spiegel (February 2026)** for macOS 10.14+ (Intel/Apple Silicon) and Windows 11, now usable inside a DAW, recording MIDI, with optional UI guides and hint bar. Commercial. https://www.eventideaudio.com/?p=194675 , https://www.sonicstate.com/news/2026/02/18/music-mouse-is-back/ [confirmed]
- **Bret Victor / "explorable explanations" lineage** (Victor 2011 "Explorable Explanations"; Nicky Case's catalogue). For music, the lesson is: every number/label in the explanation should be *scrubbable* and audible immediately. [reported]
- **Evidence:** None of these report controlled learning outcomes. [confirmed absence]
- **Lesson:** Their interaction grammar — immediate audible feedback, single-concept screens, direct manipulation of the representation — is exactly the anti-dashboard aesthetic the user wants.

### 2.4 Listening guides and the Music Animation Machine
- **Music Animation Machine** (Stephen Malinowski, from 1985): scrolling bar-graph scores where colour codes voice, theme or tonality; huge YouTube reach. Rationale (Malinowski): vision can track multiple simultaneous streams. **No controlled evaluation was found**; scholarly support is argumentative (e.g., van Campen, *The Hidden Sense*). [confirmed absence in searches]
- **Listening maps (static):** small classroom studies — Beam-Barber (2002, FIU dissertation, 2nd graders): listening maps improved post-test scores and preference https://digitalcommons.fiu.edu/etd/1472 ; Gromko & Poorman (1998): children who *enacted* the music kinaesthetically and then *assembled* a map perceived form better than those who only read a map — "merely reading the listening map may not be sufficient". [confirmed via abstract summaries]
- **Lesson (important):** The evidence that exists favours **learner-constructed** representations over passively watched ones (generation effect). For our app: let the learner *draw/assemble* the form map or harmonic map while listening, then compare with the analysis — rather than playing a slick animation at them.

---

## 3. Piano-specific augmentation research

### 3.1 P.I.A.N.O. (Rogers, Röhlig, Weing, Gugenheimer, Könings, Klepsch, Schaub, Rukzio, Seufert, Weber — CHI 2014)
- **What:** Projector above a digital piano projects an "enhanced piano-roll" onto a board behind/above the keys so notes fall directly onto their keys, with colour cues for fingering and articulation; three modes: *listen* (attention), *practice* (retention, with correct/incorrect key colouring), *play* (reproduction, scored). Input via MIDI, songs from MusicXML. [confirmed]
- **Study 1** (within-subjects, n=56 novices, Latin-square; three 16-bar right-hand songs; P.I.A.N.O. vs Synthesia vs Finale with moving marker): P.I.A.N.O. yielded significantly more correctly pressed notes (rANOVA F(2,88)=121.6, η²=.73) and correct durations, fewer missed notes, but **more incorrectly pressed notes**; lower intrinsic and extraneous cognitive load and higher germane load than Finale; better AttrakDiff UX. [confirmed from PDF]
- **Study 2** (between-subjects, n=18, 6 per system, 5 days × 15 min on a simplified Schumann *Träumerei*): steeper learning curve for P.I.A.N.O. (≈88% correct durations on day 5, near-zero missed notes); 6 experts blind-rated recordings higher on pitch/duration accuracy, rhythm, continuity and overall impression. [confirmed from PDF]
- **Paper:** https://www.uni-ulm.de/fileadmin/website_uni_ulm/iui.inst.100/1-hci/hci-paper/2014/2014-gugenheimer-piano.pdf ; earlier UbiComp 2013 adjunct. [confirmed]
- **Critical reading:** The outcome measure is *reproducing a specific melody*, not reading, transfer, or understanding. The authors themselves frame the benefit as "does not require sight-reading skills". [confirmed] For a learner who wants to perceive structure, this is evidence that direct key-mapping massively lowers the *execution* barrier — useful for *getting sound into the ears quickly* — but it says nothing about comprehension.

### 3.2 Survey: "Has augmentation improved learning experiences?" (Deja, Mayer, Čopič Pucihar, Kljun — ISS 2022)
- Systematic review of augmented-piano prototypes plus expert interviews; four themes: synchronized movement/posture, sight-reading, motivation, improvisation. Conclusion: prototypes are well developed for synchronization, open for sight-reading, motivation and improvisation; "it is still not understood if these solutions are indeed supporting the learning process." Teachers sceptical that piano-roll overlays build reading. https://arxiv.org/abs/2208.09929 [confirmed]

### 3.3 Improvisation-oriented AR (Deja et al., HICUP Lab, Univ. of Primorska)
- "Teach Me How to ImproVISe" — co-design of an AR improvisation trainer, https://arxiv.org/abs/2402.02999 ; "Piano Learning and Improvisation through Adaptive Visualisation and Digital Augmentation" https://arxiv.org/abs/2211.04989 ; **ImproVisAR: designing augmented reality piano roll for teaching improvisation**, *Virtual Reality* 29:140 (2025), DOI 10.1007/s10055-025-01215-z, open access CC-BY. Reported reduced cognitive load over time, sustained engagement, higher expert ratings for rhythm, flow, musicality. N not verified. [confirmed bibliographic; outcomes reported]
- **Lesson:** This is the closest prior art for "visual guidance for improvisation" on a real piano. It projects *permissible/suggested notes* rather than a fixed sequence — the right abstraction for improvisation scaffolding.

### 3.4 Andante (Xiao, Tome, Ishii — NIME 2014)
- Animated figures "walk" along the keyboard (projected above a Disklavier), each step pressing a key, to make musical motion (phrasing, tempo, voice movement) embodied. Pianists Herbie Hancock and Vijay Iyer played with it. No learning study. https://nime.org/proc/nime2014_xxiao/ [confirmed]
- **Lesson:** Representing *voices as agents with momentum* is a lovely idea that transfers to on-screen keyboards: each voice is a small walker, so voice-leading becomes visible as walking (→ Idea 9.A.2).

### 3.5 Haptics: Mobile Music Touch / Passive Haptic Learning (Georgia Tech, Starner lab)
- Vibrating glove taps the fingers corresponding to a melody while the wearer does something else. A 2011 thesis pilot (n=12) and a planned n=24 study reported better learning curves; Markow's dissertation reports faster learning and better retention; a 2015 rehabilitation study (7 people/10 hands with incomplete SCI) found significant sensation improvements. Evidence is from small studies, theses and press; no independent replication found. https://repository.gatech.edu/entities/publication/379c0369-51ec-4ef0-aa32-facbf0571d8b [confirmed]
- **Lesson:** Out of scope for hardware, but the concept "passive rehearsal of motor sequences" is relevant: an app could offer *listening-only* passive rehearsal of a passage with synchronized keyboard animation for spaced exposure, which is cheap and harmless.

### 3.6 Head-mounted AR/MR and related prototypes
- **HoloKeys** (Hackl & Anthes, FMT 2017, CEUR Vol-2009, pp. 140–144): HoloLens overlay of keys-to-press on a real piano, songs from MIDI; marker-based tracking; proof of concept, no learning study. https://ceur-ws.org/Vol-2009/fmt-proceedings-2017-paper19.pdf [confirmed]. A different "Holokeys" (Stanbury, Said & Kang, VRST 2021) targets remote lessons via AR + IoT. [confirmed]
- **Music Everywhere** (Glickman, Lee, Hsiao, Das — NIME 2017, pp. 511–512): HoloLens + MIDI-over-Bluetooth piano; "mirror key overlay"; *improvisation* lessons (blues, rock, jazz, classical) with virtual hand demos and AR-projected virtual band; later a CMU spin-off startup. Demo paper, no outcome study. https://nime.org/proc/nime2017_sglickman/ [confirmed]
- **MirrorFugue** (Xiao & Ishii; CHI 2011 "Duet for Solo Piano"; MirrorFugue III): projects a recorded pianist's hands as a "reflection" on the piano's fallboard, synchronized with a player piano's moving keys; evaluated qualitatively with expert musicians; later *ReMirrorFugue* study (N=28) on the felt presence of past pianists. https://web.media.mit.edu/~x_x/mirrorfugue/mirrorfugue_chi.pdf [confirmed]. **Lesson:** seeing *hands* (gesture, not just notes) of a reference performance is a different and possibly richer channel than notes-on-keys; on screen, a reference performer's hand video synchronized to the learner's score position is cheap to approximate.
- **Haptics in MR** (Fang et al., KIT): HoloLens piano + haptic glove, N=16, little difference in learning rate between visual (active) and haptic (passive) cueing. https://publikationen.bibliothek.kit.edu/1000145297/148745237 [reported]
- **AR hand pose + EMS timing** (Mori, Ihara, Kawaguchi, OzCHI 2024 LBW): AR helps hand positioning qualitatively; quantitative gains not significant (small N). [reported]
- **"Following the Master's Hands"** (Labrou et al., CHI EA 2023): MR display of a teacher's 3-D hand traces. [reported]
- **PianoVision** (Meta Quest MR, commercial falling-notes onto a real piano): no peer-reviewed outcome data found. [reported]
- **Survey:** Wilson & Pfeiffer (2023, *Frontiers in Virtual Reality*) review AR/VR piano tutors; real-time feedback still limited by hardware. https://www.frontiersin.org/journals/virtual-reality/articles/10.3389/frvir.2023.1207397/full [reported]
- **Note:** I found **no main-track CHI 2024–2026 paper** on piano-learning feedback in searches (CHI EA/OzCHI/journals only). A direct ACM DL query is advisable. [confirmed absence in web search only]

### 3.7 Do falling-note displays hinder reading/understanding?
- **No head-to-head study** of long-term reading/understanding effects of falling-note displays was found. Evidence is indirect: P.I.A.N.O. outperforms notation for short-term reproduction *because* it bypasses reading; the 2022 survey records teacher concern that piano-roll learners don't build sight-reading. [confirmed for what exists]
- **Design consequence for this project [speculative but well-motivated]:** prefer score-anchored highlighting (the score is the primary view; the keyboard/roll is a *linked secondary view*), and use roll views for *analysis of what was played* (post-hoc) rather than as the *instruction* stream.

---

## 4. Generative / interactive AI for musical exploration

### 4.1 Comparison table (local-run focus)

| System | What it does | Local on Apple Silicon? | Licence | Latency/real-time | Status | Pedagogical use |
|---|---|---|---|---|---|---|
| **Aria** (EleutherAI; Bradshaw et al., ISMIR 2025) | Autoregressive piano-performance model, LLaMA-3.2-1B architecture, ~60k h transcribed solo piano; gen + embedding checkpoints | **Yes** — MLX backend + real-time demo in `demo/` | Apache-2.0 (code, models) | Aria-Duet: prefill latency 1–2 s mitigated by chunked continuous prefill; ~100–200 ms hand-over | Active 2025 | "Continue my phrase", turn-taking duet, style-aware embeddings for similarity search |
| **Anticipatory Music Transformer** (Thickstun, Hall, Donahue, Liang, TMLR 2024) | Infilling and accompaniment conditioned on control events (e.g., a given melody) | Probably (PyTorch; 360M "medium" model trained on Lakh MIDI; CUDA in examples, MPS/CPU plausible) | Apache-2.0 (code **and** weights, stanford-crfm/music-medium-800k) | Offline; not real-time by design | Maintained lightly | Counterfactual accompaniment, "rewrite the left hand", infill a bar |
| **NotaGen / NotaGen-X** (Wang et al., 2025, arXiv 2502.18008) | Classical sheet music in interleaved ABC, conditioned on period–composer–instrumentation | Small/medium likely on M-series; NotaGen-X "may require 8 GB GPU" | MIT (repo) | Seconds–minutes per piece | Active 2025 | Score-level "what would X have written here?", style counterfactuals |
| **MIDI-LLM** (Wu, Carlton, Miyakawa, Kim, Donahue, Huang; ISMIR 2026) | Text-to-MIDI and editing via Llama-3.2-1B with MIDI tokens | Plausible (1B) | Weights/code release **not confirmed** | vLLM-compatible | New | Natural-language edits ("make the bass walk") |
| **ReaLchords** (Wu et al., ICML 2024) / **ReaLJam** (Scarlatos et al., CHI EA 2025) | Online melody→chord accompaniment, RL-tuned; ReaLJam shows the agent's *planned* chords ahead of time | **No public weights found** | — | Designed for real time | Research | Gold-standard design reference for "AI that anticipates and shows its plan" |
| **Magenta.js** (Google) | MusicRNN, MusicVAE, ImprovRNN, PerformanceRNN, Coconet, Piano Genie in-browser (TF.js) | **Yes, in Chrome** | Apache-2.0 | Real-time (small RNNs) | Low activity; models dated (2017–19) | Quick prototypes: Coconet harmonization, MusicVAE interpolation |
| **Somax2** (IRCAM RepMus; Borg, Fiorini, Assayag, Bloch…) | Corpus-based reactive co-improvisation, MIDI or audio in/out | **Yes** (2.6 native macOS ARM) | GPL-3.0 (github.com/DYCI2/Somax2) | Real-time | Active (IRCAM, REACH/MERCI) | "Improvise inside a piece's corpus" |
| **OMax / DYCI2** (IRCAM; Nika, Bresson et al.) | Factor-oracle style learning of the live player; DYCI2 adds scenario (chord-chart) guidance; OM-DYCI2 runs a Python DYCI2 core | Max / OM# + Python | **Not confirmed** (IRCAM Forum terms) | Real-time | Research | Call-and-response with "your own vocabulary"; scenario = chord chart |
| **BebopNet** (Haviv Hakimi, Bhonker, El-Yaniv, ISMIR 2020) | Monophonic sax-style bebop solos over chord changes + *personalized* preference model via beam search | Small LSTM — easily local | Not checked | Offline | Research | "Licks tuned to my taste"; preference learning |
| **Jazz Transformer** (Wu & Yang, ISMIR 2020) | Transformer-XL on Weimar Jazz Database lead sheets incl. structure events; paper mainly documents *shortcomings* | Local | Not checked | Offline | Research | Cautionary: low loss ≠ musical structure |
| **Impro-Visor** (Keller, Harvey Mudd) | Jazz lead-sheet notation, grammar-based lick generation, trading, roadmaps (brick analysis) | Yes (Java) | GPL-2.0-or-later | Real-time playback | Last release 10.2 (Aug 2019) | Grammar-based licks; "bricks" roadmap analysis |

Citations for the table: Aria https://github.com/EleutherAI/aria , paper https://arxiv.org/abs/2506.23869 , Aria-Duet https://arxiv.org/abs/2511.01663 ; AMT https://github.com/chrisdonahue/anticipation , https://crfm.stanford.edu/2023/06/16/anticipatory-music-transformer.html ; NotaGen https://github.com/ElectricAlexis/NotaGen ; MIDI-LLM https://arxiv.org/abs/2511.03942 ; ReaLchords https://proceedings.mlr.press/v235/wu24c.html , ReaLJam https://arxiv.org/abs/2502.21267 ; Magenta.js https://github.com/magenta/magenta-js ; Somax2 https://github.com/DYCI2/Somax2 , https://forum.ircam.fr/article/detail/somax-2 ; Impro-Visor https://www.cs.hmc.edu/~keller/jazz/improvisor/ , https://github.com/Impro-Visor/Impro-Visor . [confirmed for licences of Aria, AMT code, NotaGen repo, Magenta.js, Somax2, Impro-Visor; others as marked]

### 4.2 Notes on individual systems
- **Piano Genie** (Donahue, Simon, Dieleman, IUI 2019): 8 buttons → 88 keys via a discrete-bottleneck autoencoder trained on ~1,400 e-Competition performances; in Magenta.js. Lesson: *contour-level control* (up/down/same) while the model handles pitch detail. For our learner, the inverse is interesting: show the *contour skeleton* of what they played. https://research.google/pubs/piano-genie/ [confirmed]
- **Bach Doodle / Coconet** (Huang et al., ISMIR 2019): >55 M harmonization queries in 3 days; 21.6 M harmonizations released as a dataset. Coconet (Huang et al., ISMIR 2017) is an orderless NADE trained on Bach chorales doing Gibbs-like infilling — exactly the right architecture for "fill in the alto and tenor under my soprano" and for counterfactual re-voicing. https://arxiv.org/abs/1907.06637 , https://magenta.tensorflow.org/datasets/bach-doodle [confirmed]
- **AI Duet** (Yotam Mann, 2016) — call-and-response with a small RNN; charming but musically shallow. [reported]
- **Music Transformer** (Huang et al., ICLR 2019) — relative attention; largely superseded by Aria for piano continuation. [reported]
- **Cococo** (Louie, Coenen, Huang, Terry, Cai — CHI 2020): Coconet-backed editor with *steering tools*: voice lock (generate only in chosen voices), example-based sliders ("more happy/sad", "more conventional/surprising"), semantic nudges, generate-small-chunks. Comparison study with 21 novices: increased control, ownership and sense of collaboration vs. a baseline. Key insight: novices are overwhelmed when the model generates too much at once; *small, local, steerable* generations are better. https://magenta.tensorflow.org/people-first-hci-ml-collaborations [confirmed via authors' project page]
- **ReaLJam's key UI insight:** show the agent's *planned future chords* on screen so the human can anticipate — "a shared lead sheet that writes itself slightly ahead". This is an important pattern for any accompaniment feature in our app. [confirmed]
- **On "GuitarLSTM-style jazz solo generators":** GuitarLSTM (GuitarML project) is, to my knowledge, a neural *guitar amplifier/pedal emulation* model, not a solo generator [reported; not re-verified]. The relevant symbolic jazz-solo generators are BebopNet, the Jazz Transformer, Impro-Visor grammars and the older ImprovRNN in Magenta.js. https://archives.ismir.net/ismir2020/paper/000132.pdf , https://arxiv.org/abs/2008.01307 [confirmed for the two papers]
- **Somax2 literature:** Borg, Malt, Assayag, Sluchin, Conforti, "Somax 2, a Reactive Multi-Agent Environment for Co-Improvisation", SMC 2022; Assayag, Bonnasse-Gahot, Borg in *Computer Music Journal* 46(4) on the REACH project; ICMC 2025 flute case study. No latency evaluation paper found. [reported]
- **Somax2** reacts to pitch/harmony/onset features of the live player by navigating a *corpus* (e.g., a set of MIDI files) — so if the corpus is a Chopin prelude, the machine answers in Chopin's vocabulary. v2.6 runs natively on Apple Silicon; requires Max 8.6+/9. A Python core exists but the shipped interface is Max patches; integration with a Chrome app would go via virtual MIDI (IAC Driver) or OSC. [confirmed for platform/licence; integration route speculative]

### 4.3 Which interactions are pedagogically meaningful? [speculative synthesis]
1. **Call-and-response with constrained answers** (the AI answers within the same harmony and register; the learner must imitate/vary) — trains aural memory and motivic thinking.
2. **"Continue my phrase" with N alternatives** — the learner hears several plausible continuations of their own idea and chooses; choice forces evaluation (a generative-comparison task).
3. **Counterfactual accompaniment** — same melody, different harmonizations (AMT/Coconet/rule-based) as minimal pairs.
4. **Infill** — mask one bar of a real piece; learner improvises the bar; then compare with model infills and the composer's original.
5. **Style transfer as contrast** — the same progression voiced "as Bach chorale", "as Chopin", "as Bill Evans" (rule-based voicing generators are more controllable than LLMs here).

Rule-based generators (voicing rules, guide-tone algorithms, partimento rules) should be preferred where *explainability* matters; ML models where *idiomatic richness* matters.

---

## 5. Counterfactual / "what-if" music interfaces

- **Hooktheory / Hookpad** (commercial): chord palette by function, borrowed chords and secondary dominants one click away, with a large crowd-analysed song database ("TheoryTab") — de facto the most widely used reharmonization explorer. [reported]
- **Tonnetz transformations (HexaChord)** and **orbifold neighbourhoods (ChordGeometries)** both define *neighbourhoods* of a chord — the set of chords reachable by small voice-leading — a principled candidate set for "what if this chord were different?". [confirmed for the tools; use speculative]
- **Neo-Riemannian P/L/R** operations and **Tymoczko's voice-leading lattices** give a small, explainable set of alternatives (parallel, relative, leading-tone exchange, chromatic mediants, tritone substitution). [reported]
- **Contrastive listening evidence:** I found no study of minimal-pair *harmony* training. Adjacent evidence: (i) **Wong, Low, Kang & Lim (2020), "Learning music composers' styles: To block or to interleave?", *Journal of Research in Music Education* 68(2)** — listeners with ≤4 years of musical experience learned 12 composers' styles; interleaved exposure beat blocked exposure on *new* pieces, although most participants *believed* blocking worked better (metacognitive illusion — relevant to UX: learners will prefer the less effective mode). https://journals.sagepub.com/doi/abs/10.1177/0022429420908312 [confirmed via abstract]; (ii) a follow-up auditory category-learning result reports an interleaving advantage for identifying musical intervals [reported]; (iii) perceptual-learning paradigms with feedback on tone/chord similarity (Frontiers 2012, "rapid learning" with novices) [reported]; (iv) the general category-learning literature (Kornell & Bjork 2008 on painters' styles; Kang's reviews) [reported]. Interleaving works partly by highlighting *between-category contrasts* — the same mechanism a minimal-pair interface exploits. Correlational work links musical discrimination to minimal-pair word learning (Smit, Milne & Escudero 2022, *Frontiers in Psychology*, https://www.frontiersin.org/articles/10.3389/fpsyg.2022.801263/full). [confirmed for the papers' existence; transfer to harmony learning is speculative]
- **Gap/opportunity:** A "minimal-pair harmony" interface (change exactly one note/chord, A/B/X listening, the learner predicts which is the original) is novel *as a researched learning tool*, and easy to self-evaluate with ABX accuracy over time.

---

## 6. Improvisation systems and jazz pedagogy technology

- **Impro-Visor** (Keller et al.): leadsheets, grammar-based lick generation (grammars learnable from transcriptions), "roadmap" analysis into idiomatic *bricks* (ii–V–I, turnarounds), trading choruses. GPL-2.0+, v10.2 (2019), effectively unmaintained but source available. https://www.cs.hmc.edu/~keller/jazz/improvisor/jazzCreativity.pdf [confirmed]
- **Play-along apps** (iReal Pro, Band-in-a-Box, Genius Jamtracks): ubiquitous; no adaptive pedagogy; discussed rather than evaluated in literature. [reported]
- **AM-I-BLUES** (Dias et al., 2020): keyboard with lights guiding novices to scale degrees fitting a generated blues harmony; no outcome data found. [reported]
- **ImproVisAR** (Section 3.3): AR piano-roll for improvisation; positive outcome claims (2025). [reported]
- **Evidence state:** Many system designs, small or self-reported evaluations; little independent controlled research on pianists' improvisation outcomes. A recent journal paper on a fine-tuned "music LLM" accompaniment system reports large gains (error rate 7.6%, SUS 82.4) but is from a low-tier venue and should not be relied on. [confirmed that evidence is thin]
- **Classical→jazz/improvisation bridges:**
  - **Partimento revival** (Gjerdingen, *Music in the Galant Style* 2007; *Child Composers in the Old Conservatories* 2020; Sanguinetti, *The Art of Partimento* 2012). **Monuments of Partimenti** (Gjerdingen's website) offers a Beginner's Guide, Rule of the Octave and thousands of partimento pages in modern notation; **UUPart** (Uppsala) catalogue. I found **no interactive partimento training software with feedback** — a clear gap. https://www2.musik.uu.se/UUPart/UUPart.php [confirmed absence in searches]
  - Galant **schemata** (Prinner, Romanesca, Monte, Fonte, Ponte, Quiescenza…) are a natural bridge: they are stock voice-leading patterns that work equally as analysis targets in Mozart/Haydn and as improvisation templates. Computational schema detection exists (e.g., Finkensiep, Neuwirth & Rohrmeier, "Generalized skipgrams for pattern discovery in polyphonic streams", ISMIR 2018 — *reported*).
  - **Improvising over Bach chorale harmony**: the chorale's figured-bass skeleton + soprano provide a "lead sheet" in 18th-century terms; the learner can improvise a new soprano over Bach's bass, or new inner voices under his soprano, checked against voice-leading rules. [speculative design]
- **Guide-tone lines:** 3rds/7ths of successive chords form smooth lines (the jazz analogue of minimal voice-leading). Generating them is a 20-line algorithm (choose 3rd/7th minimizing semitone motion). [reported for pedagogy; algorithm trivial]

---

## 7. Visualizing expressive performance

- **Performance Worm**: tempo (x) vs loudness (y) trajectory with fading trail; Langner & Goebl, "Visualizing Expressive Performance in Tempo–Loudness Space", *Computer Music Journal* 27(4), 2003, 69–83; Dixon, Goebl & Widmer, "The Performance Worm: Real time visualisation of expression based on Langner's tempo-loudness animation", ICMC 2002, https://webspace.eecs.qmul.ac.uk/s.e.dixon/pub/2002/icmc.pdf . Modern web reimplementation: **Performance Wormhole** (SInES, University of Vienna; Christoph Reuter), browser-based, MIT licence, accepts audio and CSV, exports PNG/PDF/video. https://sinestools.univie.ac.at/wormhole.htm [confirmed]
- **Scape plots of performance correlation (Craig Sapp, Mazurka Project / CHARM)**: >2,500 recordings of 49 Chopin mazurkas; triangular plots showing, for every sub-span, which other performance a given performance's tempo/dynamics correlate best with; famously exposed the Joyce Hatto hoax (a modified Eugen Indjic recording). Sapp, "Comparative analysis of multiple musical performances", ISMIR 2007, https://archives.ismir.net/ismir2007/paper/000497.pdf ; tools https://charm.rhul.ac.uk/analysing/p9_4.html [confirmed]
- **Parangonada / Parangonar / Partitura** (Peter, Cancino-Chacón, et al., JKU Linz): Partitura = Python I/O for scores and performances (MusicXML, MEI, MIDI, Kern, match files); Parangonar = symbolic score-to-performance note alignment (offline and online); Parangonada = browser tool to view and correct alignments (https://sildater.github.io/parangonada). https://pypi.org/project/parangonar/ ; Partitura paper https://www.arxiv.org/abs/2206.01071 [confirmed; Partitura licence Apache-2.0 per PyPI description (one metadata classifier says MIT) — reported; Parangonar licence not checked]
- **Datasets** for reference performances: (n)ASAP (aligned score–performance pairs, MAESTRO-derived), ATEPP (Zhang et al. 2022, transcribed expressive piano performances by virtuosi), Aria-MIDI (~60k h). [reported]
- **Lesson:** For a beginner, the most legible variants are (i) a tempo curve aligned to the score (bar axis, not seconds), (ii) the worm for a short phrase, (iii) "who do I sound like" correlation against a handful of reference recordings — Sapp's method scaled down.

---

## 8. Cross-cutting design lessons

1. **Translate, don't replace, notation.** (P.I.A.N.O. vs. survey critique.)
2. **Generate-small, steer-locally.** (Cococo.)
3. **Show the machine's intention before it acts.** (ReaLJam.)
4. **Learner-constructed representations beat watched animations.** (Gromko & Poorman 1998.)
5. **Structure-preserving views help transfer for learners who have schemas.** (Isomorphic layout studies.)
6. **Geometry is an exploration instrument whose pedagogical value is unproven; instrument your own use.** (Harmony Space/Tonnetz evidence gap.)
7. **Pick explainable generators (rules) for teaching claims; ML generators for idiomatic richness and surprise.**
8. **Interleave and contrast, even though it feels worse.** (Wong et al. 2020: learners preferred blocking but learned more from interleaving.) The UI should make the effective mode the default and quietly explain why.
9. **Show hands and gesture, not just notes, when the goal is performance.** (MirrorFugue; "Following the Master's Hands".)

---

## 9. IDEAS — interaction concepts

Format: *Description* · *Learning mechanism* · *Technical ingredients* · *Effort* · *Originality / prior art* · *Risks*.

### 9.A Established (strong prior art; low risk; build first)

**9.A.1 Score-anchored live highlighting with post-hoc roll ("Mirror")**
- *Description:* The score (Verovio SVG) is the primary view; as the learner plays, aligned notes light up; after a take, a piano-roll "mirror" appears beneath, aligned bar-for-bar, colouring timing deviation and velocity.
- *Mechanism:* Immediate knowledge of results without replacing reading; P.I.A.N.O.'s direct mapping benefit transferred to the score.
- *Ingredients:* Web MIDI, Verovio/OSMD, online alignment (Parangonar-style DTW/HMM ported to JS or via a local Python service).
- *Effort:* Med. *Originality:* Low (Soundslice, P.I.A.N.O., many apps). *Risks:* Alignment errors on beginner playing (wrong notes, restarts) — needs robust "where am I" recovery.

**9.A.2 Voice-Leading Strings**
- *Description:* In a chorale or chord progression, each voice is drawn as a coloured string connecting its notes across chords (on the staff and on a vertical keyboard), with string tension proportional to the interval moved; total voice-leading distance shown as a small number; Andante-style "walkers" optional.
- *Mechanism:* Makes the invisible linear dimension of harmony visible; links chord vocabulary to counterpoint.
- *Ingredients:* Voice assignment (given in chorales; optimal-assignment for block chords), SVG overlay on score.
- *Effort:* Low–Med. *Originality:* Med (Tymoczko's geometry, Andante's walkers, Malinowski's MAM lines; the score-anchored, tension-weighted variant appears new). *Risks:* Clutter with >4 voices; must be selection-scoped.

**9.A.3 Guide-Tone Line Generator + Shell-Voicing Trainer**
- *Description:* For any lead sheet or Roman-numeral sequence, display the guide-tone line (3rds/7ths with minimal motion) as a singable melody; learner plays it with left-hand shells while the app plays bass; then embellishes it.
- *Mechanism:* The standard jazz-pedagogy scaffold (target notes before embellishment); progressive complexity.
- *Ingredients:* Chord-symbol parser, rule-based voice-leading, Web Audio sampler.
- *Effort:* Low. *Originality:* Low (Impro-Visor, many method books). *Risks:* Dull if not tied to real repertoire — tie to standards and to classical progressions.

**9.A.4 Self-Worm and Tempo Map**
- *Description:* After a take, show the tempo–loudness worm of a selected phrase, overlaid on the worm of one or two reference performances (from aligned MIDI datasets).
- *Mechanism:* Contrastive self-perception of expressive shaping; links "feel" to measurable curves.
- *Ingredients:* Score–performance alignment, beat-level tempo, velocity→loudness proxy, canvas animation.
- *Effort:* Med. *Originality:* Low–Med (Worm 2002; Wormhole web tool; applying it to the learner's own MIDI in a practice loop is uncommon). *Risks:* Over-quantification of expression; beginners' tempo noise dominates — smooth and show at phrase scale.

**9.A.5 Keyscape / Wavescape of the Piece, linked to the Score**
- *Description:* A triangular wavescape above the score; hover any cell → that span is highlighted in the score and the DFT "colour" is explained ("diatonic, centred on G"); clicking plays that span.
- *Mechanism:* Multi-scale tonal overview; zoomable "map" for a piece one is learning.
- *Ingredients:* Pitch-class profile per window, DFT, canvas/WebGL; ports of `wavescapes` logic.
- *Effort:* Low–Med. *Originality:* Med (keyscapes/wavescapes exist; bidirectional score linking and audio scrubbing for learners appears new). *Risks:* Hard to interpret without a short guided intro.

### 9.B Plausible (some prior art; novel combination; moderate risk)

**9.B.1 Tonnetz-to-Hand Morph**
- *Description:* A chord path is shown on the Tonnetz; a slider morphs the lattice continuously into the piano keyboard (each lattice node slides to its key), so a P/L/R move (one node moves) becomes visibly "one finger moves a semitone/tone". Played chords from MIDI appear on both.
- *Mechanism:* Links abstract voice-leading geometry to motor schemas (hand shapes); dual coding.
- *Ingredients:* SVG/D3 with interpolated layouts; voicing choice (closest position).
- *Effort:* Med. *Originality:* High as far as found (Harmony Space and Tonnetz tools never morph to the keyboard). *Risks:* Pretty but possibly confusing; must be short and optional.

**9.B.2 Counterfactual Score ("What if?")**
- *Description:* Click any chord in a score; a fan of 4–8 alternatives appears (P/L/R, secondary dominant, tritone sub, modal mixture, model infills), sorted by voice-leading distance; each can be auditioned in context, A/B against the original, and "kept" to fork the score.
- *Mechanism:* Contrastive (minimal-pair) listening; makes the composer's choice *meaningful* by showing what it is not.
- *Ingredients:* Roman-numeral analysis (When in Rome / DCML annotations), rule-based substitution library, optimal voice-leading realization, optional AMT/Coconet infill, Verovio re-render.
- *Effort:* Med–High. *Originality:* Med (Hookpad has substitution palettes but not on real repertoire scores with voice-leading-aware realization; Cococo has infill but not theory-labelled alternatives). *Risks:* Voicing realizations sound mechanical; mitigate by keeping the original texture and only replacing pitches.

**9.B.3 Minimal-Pair Ear Lab (ABX from your repertoire)**
- *Description:* From the piece being studied, auto-generate ABX trials that differ in exactly one feature (one chord's quality, a suspension resolved or not, a bass inversion); learner identifies the original; spaced repetition schedules confusable pairs.
- *Mechanism:* Discrimination training with feedback; interleaving of confusable categories (Wong et al. 2020); repertoire-embedded transfer.
- *Ingredients:* Same substitution engine as 9.B.2; simple SRS.
- *Effort:* Med. *Originality:* Med–High (generic ear trainers exist; repertoire-derived minimal pairs not found). *Risks:* Becoming a drill/gamified — keep it quiet, short, optional; no streaks.

**9.B.8 Reference Hands ("MirrorFugue on a screen")**
- *Description:* For a passage, show a reference pianist's hands (from video, or synthesized from aligned MIDI as a hand-shape animation over the keyboard) synchronized to the learner's current score position; the learner can slow it, loop it, and toggle between "their hands" (from their MIDI) and "reference hands".
- *Mechanism:* Observational learning of gesture/fingering; hand-shape chunking.
- *Ingredients:* Score-position tracking; video sync or MIDI→hand-span heuristic (fingering estimation, e.g., PIG dataset models).
- *Effort:* Med. *Originality:* Low–Med (MirrorFugue, CHI 2011; Labrou et al. CHI EA 2023). *Risks:* Fingering estimation errors; video licensing.

**9.B.4 Tonnetz Transformation Composer**
- *Description:* Select a phrase; apply a geometric transformation to its Tonnetz trajectory (reflect → negative-harmony-like inversion; translate → transposition; rotate) and hear the result.
- *Mechanism:* Reveals harmony as structure-preserving maps; physicist-friendly group-theory intuition.
- *Ingredients:* HexaChord-style mapping; MIDI regeneration.
- *Effort:* Low–Med. *Originality:* Low–Med (HexaChord did this). *Risks:* Results can be musically odd; frame as exploration.

**9.B.5 "Same Progression Across Centuries"**
- *Description:* Choose a progression or schema (e.g., circle-of-fifths sequence, Prinner, ii–V–I, Andalusian cadence); the app retrieves real instances from corpora (Bach chorales, Mozart sonatas, Chopin, jazz standards, pop via When-in-Rome/DCML/other annotations) and plays them aligned by harmony, with voice-leading strings.
- *Mechanism:* Variability across contexts → abstraction of the invariant (classic category-learning principle).
- *Ingredients:* Annotated corpora (When in Rome in RomanText, DCML), pattern search over Roman numerals, excerpt rendering.
- *Effort:* Med. *Originality:* Med (corpus query tools exist; the curated, audible, aligned comparison as a learning interface appears uncommon). *Risks:* Corpus coverage for jazz/pop; licence of excerpts.

**9.B.6 Partimento Studio**
- *Description:* Show a partimento bass (Fenaroli/Durante from Monuments of Partimenti); learner plays the bass with LH and improvises RH; the app shows Rule-of-the-Octave suggested sonorities above each bass degree, detects schemata, flags parallel 5ths/8ves gently after the take, and can play model realizations.
- *Mechanism:* Historically validated improvisation pedagogy (conservatory partimento training) with modern feedback.
- *Ingredients:* Bass-degree analysis, RoO table, voice-leading checker (music21 rules), MIDI input.
- *Effort:* Med. *Originality:* High as interactive software (no partimento trainer with feedback found). *Risks:* Rule-checking feels like grading; present as "listen back" comparisons.

**9.B.7 Call-and-Response inside the Harmony**
- *Description:* The app plays a 1–2 bar motif over a loop (from the piece being studied or a ii–V–I); the learner answers; the app's next call is derived from the learner's answer (varied by transposition/inversion/rhythm-displacement); motif relations drawn as arcs.
- *Mechanism:* Aural memory, motivic development, conversational improvisation.
- *Ingredients:* Rule-based motif transforms; optional Aria for "freer" responses; Web MIDI.
- *Effort:* Med. *Originality:* Low–Med (AI Duet, Impro-Visor trading, OMax). *Risks:* Latency and timing; quantize the turn boundary to the bar.

### 9.C Experimental (high novelty or high technical risk)

**9.C.1 Improvise Inside a Chopin Prelude**
- *Description:* Take a piece (e.g., Chopin Op. 28 No. 4 or 20); the app keeps its harmony/LH texture as a living accompaniment (Somax2-style corpus navigation constrained to the piece's own material, or AMT conditioned on the original bass), while the learner improvises a new melody; harmonic "plan" shown a bar ahead (ReaLJam pattern).
- *Mechanism:* Inhabiting a composer's harmony from the inside; bridges classical repertoire and improvisation.
- *Ingredients:* Somax2 via IAC MIDI (GPL-3, Max) or a JS reimplementation of corpus navigation (factor oracle + harmonic labels); or AMT for offline pre-generated "accompaniment variants".
- *Effort:* High. *Originality:* Med (Somax2 does corpus-based co-improvisation; the pedagogical framing with plan-ahead display and score linking appears new). *Risks:* Max dependency; latency; musical incoherence.

**9.C.2 "Continue My Phrase" with Contrast Fan**
- *Description:* Learner plays 2–4 bars; Aria (MLX) proposes 4 continuations; they are displayed as small score snippets + Tonnetz trajectories; the learner auditions and plays back the one they prefer (or their own), and the app highlights what distinguishes them (register, harmony, rhythm density).
- *Mechanism:* Generative comparison; widening the space of imaginable continuations ("possibilities the user wouldn't think of").
- *Ingredients:* Aria via local Python/MLX service + WebSocket; MIDI→notation quantization for display.
- *Effort:* Med–High. *Originality:* Med (Aria demo does continuation; the contrast fan + explanation layer appears new). *Risks:* Model outputs expressive performance MIDI that quantizes poorly to notation; 1–2 s latency is fine for turn-based.

**9.C.3 Orbifold Walk of a Piece**
- *Description:* For three-voice reductions of a piece (or a trio texture), show its path through the 3-note orbifold (Tymoczko), with the score scrolling in sync; "jumps" vs "steps" visible; augmented triad at the centre as "maximally symmetric" point.
- *Mechanism:* Global geometric intuition of chromatic voice-leading (Chopin, Wagner, Schubert).
- *Ingredients:* Reduction to 3 voices, three.js rendering, OPTIC equivalence math.
- *Effort:* Med–High. *Originality:* Low–Med (ChordGeometries did this with Chopin; a score-synced, web, learner-facing version is new). *Risks:* Cognitive overload; only for motivated exploration sessions.

**9.C.4 Self-Scape: Correlation Scape against Reference Pianists**
- *Description:* After the learner has recorded a piece several times, compute Sapp-style correlation scapes of tempo curves vs. a set of reference performances (ATEPP/(n)ASAP/Aria-MIDI) — "in bars 1–8 your shaping resembles Rubinstein; in the climax, Cortot".
- *Mechanism:* Reflective listening; makes interpretation choices legible; motivates listening to many recordings.
- *Ingredients:* Alignment, tempo extraction, Pearson correlation over all sub-spans, triangular plot.
- *Effort:* Med. *Originality:* Med–High (Sapp's tool for scholars; personal-practice use appears new). *Risks:* Beginner tempo variance is mostly noise; requires a reasonably fluent level; can feel like grading if mis-framed.

**9.C.5 Embedding Map of Your Playing**
- *Description:* Using Aria's embedding checkpoint, place each of the learner's improvisations/takes as a point on a 2-D map alongside reference repertoire; trajectories over weeks show stylistic drift.
- *Mechanism:* Long-horizon self-awareness of style.
- *Ingredients:* Aria embedding model (Apache-2.0), UMAP, SVG.
- *Effort:* Med. *Originality:* High (no prior learner-facing use found). *Risks:* Embedding dimensions are opaque; may be "pretty but meaningless" — needs nearest-neighbour audition to ground it.

**9.C.6 Isomorphic Shadow Keyboard**
- *Description:* Beneath the standard keyboard display, a Wicki–Hayden "shadow" shows the same notes in an isomorphic lattice where every major triad/scale has one shape; learner sees invariance under transposition that the piano hides.
- *Mechanism:* Structure-preserving layouts aid transfer (MacRitchie & Milne 2017; Stanford et al. 2018).
- *Ingredients:* SVG hex grid; MIDI.
- *Effort:* Low. *Originality:* Med (isomorphic instruments exist; using one as a *visual shadow* of a normal piano is uncommon). *Risks:* Evidence is for playing isomorphic instruments, not viewing — benefit speculative.

**9.C.7 Learner-Built Listening Map**
- *Description:* While listening to a movement, the learner taps/marks section boundaries and labels (A, B, transition, cadence) on a timeline; afterwards the app reveals the analytical form (from DCML annotations or keyscape boundaries) and plays the disagreements.
- *Mechanism:* Generation effect; Gromko & Poorman's finding that constructing maps beats reading them.
- *Ingredients:* Timeline UI, audio/MIDI playback, annotated form data.
- *Effort:* Low–Med. *Originality:* Med. *Risks:* Annotated form data scarce beyond DCML corpora.

**9.C.8 Natural-Language Musical Edits**
- *Description:* "Make the left hand an Alberti bass", "add a suspension here", "jazz up this cadence" — executed by a symbolic LLM (MIDI-LLM if released; otherwise an LLM driving a music21 rule library), with the diff shown on the score.
- *Mechanism:* Lowers the cost of counterfactual exploration; vocabulary acquisition through naming.
- *Ingredients:* LLM + music21 tool calls (more controllable than end-to-end generation); diff rendering.
- *Effort:* Med–High. *Originality:* Med. *Risks:* Hallucinated theory; prefer tool-calling over raw generation.

---

## 10. Recommended build order for this project [speculative]

1. **Foundation (needed by almost everything):** Web MIDI input → Verovio SVG score → symbolic score-following → per-note IDs. Load Roman-numeral annotations (When in Rome / DCML) as span-level data.
2. **First "wow" with low risk:** 9.A.2 Voice-Leading Strings + 9.A.5 Wavescape-linked score + 9.A.4 Self-Worm.
3. **Distinctive core:** 9.B.2 Counterfactual Score and 9.B.3 Minimal-Pair Ear Lab sharing one rule-based substitution + voice-leading-realization engine (pure JS/TS; no ML needed).
4. **Improvisation track:** 9.A.3 Guide-tone lines → 9.B.6 Partimento Studio → 9.B.7 Call-and-response → 9.C.1 Improvise Inside a Piece.
5. **Local ML service (Python, Apple Silicon):** Aria (MLX) for continuation/duet and embeddings; Anticipatory Music Transformer for accompaniment infill; NotaGen for score-level style counterfactuals. Bridge to Chrome via WebSocket; keep everything optional so the app works without ML.
6. **Instrument the learner's own use** (which views are opened, ABX accuracy over time) so that the geometric views' value can be judged empirically for this one user — the literature cannot answer it.

## 11. Licence quick-reference (as found 2026-10-23)

| Component | Licence | Tag |
|---|---|---|
| Aria (code + weights) | Apache-2.0 | confirmed |
| Anticipatory Music Transformer (code + music-medium-800k weights) | Apache-2.0 | confirmed |
| NotaGen repo | MIT (weights' licence not separately checked) | confirmed (repo) |
| Magenta.js | Apache-2.0 | confirmed |
| Chrome Music Lab | Apache-2.0, archived 2026-04-19 | confirmed |
| Somax2 | GPL-3.0 (requires Max 8.6+/9) | confirmed |
| Impro-Visor | GPL-2.0-or-later, last release 10.2 (2019) | confirmed |
| Verovio | LGPL-3.0 | confirmed |
| OpenSheetMusicDisplay | BSD-3-Clause (some sources: MIT) | reported |
| Partitura | Apache-2.0 | reported |
| Performance Wormhole (SInES) | MIT | confirmed (page statement) |
| wavescapes / midiVERTO | open source; licence not found | reported |
| HexaChord, MuSA_RT, ChordGeometries | free binaries historically; no licence/maintenance info found | reported |
| DYCI2, BebopNet, Parangonar | not checked | — |
| ReaLchords / ReaLJam, MIDI-LLM | no public weights confirmed | — |

## 12. Open verification items (for a next pass)
- Licences: wavescapes/midiVERTO, HexaChord, DYCI2, Parangonar, BebopNet, NotaGen weights.
- ImproVisAR sample size and design (Springer full text was behind a redirect).
- ReaLJam participant count; any public ReaLchords checkpoint.
- MIDI-LLM weight release.
- Somax2 latency figures and whether a Max-free (Python-only) driving path is practical.
- A direct ACM DL search for CHI 2024–2026 piano-feedback papers.
- Original Rogers (1991) colour-notation result direction.

*(End of version 2.)*
