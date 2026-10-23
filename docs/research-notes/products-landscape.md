# Products landscape: existing learning software for a "computational piano learning laboratory"

> **Agent-produced research note, dated 2026-10-23. To be reviewed.** Not independently verified by a human. All URLs accessed 2026-10-23 unless stated otherwise.
>
> Evidence tags: **[confirmed]** = checked against a primary source (official docs/help centre/repo/paper) during this session; **[reported]** = from credible secondary sources (press, reviews, store listings, forums) and not checked against a primary source; **[speculative]** = the agent's own inference.
>
> Caveat on method: several vendor marketing pages returned empty shells or HTTP 403 to the fetch tool (Skoove, Playground Sessions, Yousician help centre). Where that happened, claims rest on search-result snippets of the official page or on secondary reviews and are tagged accordingly. Forum consensus (r/piano, Piano World, Pianostreet) could not be sampled directly this session; statements about "community consensus" are therefore weaker than they look and are marked [reported] at best.

Companion notes in this folder: `performance-capture-analysis.md` (alignment, score following and capture in depth), `pedagogy-evidence.md`, `cognition-and-models.md`. This note covers the product and project landscape only.

---

## 0. Executive summary

1. **The "falling notes + wait mode + note-correctness feedback" loop is a solved, commoditised problem.** Simply Piano, flowkey, Yousician, Skoove, Playground Sessions, La Touche Musicale, Synthesia, PianoVision and a dozen small apps all implement it. All of them measure essentially the same thing: *was the right pitch pressed, roughly when?* None of this needs re-inventing; nor is it what this project is for.
2. **Score-following of the player (not the playback) exists but is narrow.** Antescofo's engine (Metronaut) follows the performer to drive accompaniment and mark wrong notes; Newzik's AudioScore follows to turn pages; SmartMusic grades against the score with a microphone. None expose the *alignment itself* (per-note timing deviation, tempo curve, voicing balance) as a learning object.
3. **Ear training is mature but decontextualised.** EarMaster, Functional Ear Trainer, Complete Ear Trainer, ToneGym, teoria and musictheory.net cover intervals/chords/progressions/dictation well. None ties exercises to the repertoire the learner is actually playing, and almost none use a MIDI keyboard as a first-class answer device in a functional (scale-degree) frame.
4. **Harmony visualisation is split between songwriting tools (Hookpad, Scaler 3, Captain Chords) and research/education toys (Harmony Space, Tonnetz explorers, Chrome Music Lab).** Hookpad's scale-degree/Roman-numeral palette is the best pedagogical model; nobody connects it to classical repertoire analysis *and* live keyboard input *and* score.
5. **Jazz tools are still built on 1990s–2010s paradigms** (iReal Pro, Band-in-a-Box, Impro-Visor). The interesting 2024–2026 work (Google DeepMind ReaLchords/ReaLJam, IRCAM Somax2) is research-grade, not a learner product.
6. **2025–2026 "AI tutors" are mostly LLM voice wrappers on the same note-hitting core** (ROLI AI Music Coach with Airwave hand tracking; PianoVision's "Ludwig"; Musiah; Artie by ArtMaster). ROLI's camera-based technique sensing is the only genuinely new sensing modality in a consumer product.
7. **Biggest real gaps:** (a) performance analytics beyond correctness (timing/dynamics/voicing/pedal as *musical* quantities, compared against references); (b) linking a passage the learner is playing to its harmonic/structural analysis in real time; (c) ear training generated from the learner's own repertoire; (d) open, inspectable data (the learner owns their MIDI history); (e) cross-domain "relationship" views (notation ↔ keyboard geometry ↔ harmony ↔ sound).

---

## 1. Piano-learning apps

### 1.1 Comparison table

| Product | Input | What it measures | Pedagogy model | Pricing model | Verdict |
|---|---|---|---|---|---|
| Simply Piano (Simply, ex-JoyTunes) | Mic (default), USB MIDI; Bluetooth MIDI officially unsupported but works for many | Correct notes, approximate timing | Linear gamified course, pop arrangements, short lessons; also Vision Pro (Dec 2024) and Android XR (2025) versions | Subscription | Ignore (learn: onboarding friction is very low) |
| flowkey | Mic, MIDI, Bluetooth MIDI | Note correctness in Wait Mode | Song library with video of real hands + score; Wait Mode, loop, slow | Subscription | Learn (video-of-hands + score sync) |
| Piano Marvel | MIDI (primary); mic assessment announced 2023 | Note + rhythm accuracy; SASR sight-reading level 100–1900 | Method books + large library + leveled sight-reading test | Subscription; teacher/school plans | Learn (SASR adaptive staircase) |
| Playground Sessions | MIDI required | Notes and timing in real time | "Bootcamp" curriculum (Rookie/Intermediate/Advanced), pop songs | Subscription / lifetime | Ignore |
| Yousician (piano) | Mic, MIDI, Bluetooth MIDI | Note + timing ("perfect timing" ball) | Gamified paths, Practice vs Perform modes | Subscription | Ignore |
| Skoove | Mic, MIDI | Note correctness; claims "AI feedback" | Short structured lessons incl. some chord/theory content | Subscription; frequent lifetime deals | Ignore |
| Synthesia | MIDI, touch | Correct note in Melody Practice (waits) | Falling notes + optional sheet; finger hints; MusicXML import since 10.8 | One-time unlock | Learn (cheap MIDI-file workflow); limited development |
| La Touche Musicale | MIDI/USB only (no acoustic) | Note correctness, waits | Falling notes; MIDI import; loop/slow/hand-separate; "Piano Convert" AI transcription | Subscription | Ignore (learn: MIDI import is key for a power user) |
| PianoVision (Meta Quest MR) | MIDI via desktop bridge; virtual keyboard via hand tracking | Notes; adaptive sectioning | Notes projected over real keys; AI teacher "Ludwig" (v2.0, Jan 2025) | Paid app + "Plus" subscription | Learn (spatial overlay on real keys) |
| Pianote (Musora) | None (video platform) | Nothing automatic | Video courses, challenges, community, coaches | Musora subscription | Ignore for tech; learn for human-teacher framing |
| Piano Maestro (JoyTunes) | Mic/MIDI | Notes/rhythm | Teacher-assigned, kid-oriented, method-book integration | Free for teachers historically | Ignore |
| ROLI Learn + AI Music Coach (2026) | MIDI + Airwave IR hand-tracking camera | Notes + "how you play" (hand pose) | Voice-driven LLM coach, decides progression | Airwave hardware (~£299) + app sub (~£13/mo) | Learn (only consumer product sensing technique) |
| Metronaut (Antescofo) | Mic | Score position, wrong notes | Accompaniment follows player's tempo | Subscription | Learn/reuse ideas (follow-the-player) |

### 1.2 Notes per product

**Simply Piano.** Listens via the device microphone, or a wired MIDI connection, which the vendor itself describes as the way to "achieve 100% note recognition accuracy" ([welcome.hellosimply.com/midi-sp](https://welcome.hellosimply.com/midi-sp)) [confirmed]. Its help centre says Bluetooth MIDI is *not* officially supported in Simply Piano ([help.joytunes.com](https://help.joytunes.com/en/articles/3987010-bluetooth-headphones-and-bluetooth-midi)) [confirmed via search snippet of official page]. Released for Apple Vision Pro (Dec 2024) and Android XR (2025) ([Wikipedia: Simply](https://en.wikipedia.org/wiki/Simply_(software_company))) [reported]. Criticisms in reviews: cannot see hands so technique is untaught, gamified progress ≠ skill, pricing and billing complaints, curriculum "too simple" beyond beginner level ([pianistscompass.com](https://pianistscompass.com/?p=9588), [kimola app-store analysis](https://kimola.com/reports/unlock-insights-simply-piano-user-feedback-analysis-app-store-us-148133)) [reported; many such review sites are affiliate-driven]. The general r/piano attitude (from the agent's prior knowledge, not sampled this session) is that such apps are fine for the first few months and then become a ceiling [speculative/unverified]. **Verdict: ignore**; for this user (already playing Moonlight mvt 1) it is below level and embodies the anti-goal.

**flowkey.** Wait Mode works with mic or MIDI/Bluetooth; settings via "Microphone & MIDI Settings" on desktop ([App Store listing](https://apps.apple.com/app/id1020357408); [help.flowkey.com headphones article](https://help.flowkey.com/en/articles/651019-practicing-with-headphones)) [confirmed: store listing]. Distinctive element: synced video of a real pianist's hands above the score, plus looping and hand-separation [reported]. Reported issues: wait mode occasionally skips notes, no printable score (licensing) [reported, single review]. **Verdict: learn** — the "real hands video ↔ score ↔ keyboard" triangulation is a good relationship view, but the library is arrangements, not urtext.

**Piano Marvel.** Its Standard Assessment of Sight-Reading (SASR) is the most interesting measurement idea in this category: thousands of short excerpts across 18 levels/90 sub-levels; accuracy >80% steps up, below steps down; test ends after three failures; score 100–1900 ([pianomarvel.com/en/info/get-your-score](https://pianomarvel.com/en/info/get-your-score); [pianomarvel.com/article/the-ultimate-sight-reading-test](https://pianomarvel.com/article/the-ultimate-sight-reading-test)) [confirmed for the existence and score range; the staircase rule is reported by secondary sources]. The free online "sample" only asks self-ratings (Easy/Manageable/Difficult/Impossible) [confirmed]. Scoring is note+rhythm accuracy only [reported]. MIDI-first; microphone assessment for acoustic pianos was announced for 2023 ([pianomarvel.com acoustic article](https://pianomarvel.com/article/how-to-use-piano-marvel-with-an-acoustic-piano)) [reported]. **Verdict: learn** — adaptive staircases on a calibrated item bank are exactly the right psychometric tool for sight-reading, and could be rebuilt over public-domain excerpts with a richer score (timing, continuity, not just accuracy).

**Playground Sessions.** Requires a MIDI keyboard; tracks performance in real time; "Bootcamp" curriculum with Rookie/Intermediate/Advanced levels; heavy use of pop songs ([toptenreviews](https://toptenreviews.com/playground-sessions-review); [musicradar](https://www.musicradar.com/reviews/playground-sessions-review)) [reported; official site did not render]. **Verdict: ignore.**

**Yousician.** Official help centre documents MIDI, Bluetooth MIDI (iOS), USB host on Android, latency buffer ≤256, and a calibration screen; it recommends a 61-key instrument ([support.yousician.com set-up](https://support.yousician.com/hc/en-us/articles/204799551-Choosing-your-set-up-for-piano), [sound recognition issues](https://support.yousician.com/hc/en-us/articles/46277319890449-Piano-sound-recognition-issues)) [confirmed via search snippets of official pages; direct fetch returned 403]. Older reviews say desktop was mic-only [reported, likely outdated]. Gamified falling-ball timing display, Practice vs Perform modes ([pianistscompass](https://pianistscompass.com/?p=15355)) [reported]. **Verdict: ignore** (multi-instrument game engine; piano is not its strength).

**Skoove.** First released 2015; markets "AI and human expertise" for personalised feedback ([Wikipedia: Skoove](https://en.wikipedia.org/wiki/Skoove)) [reported]. Official site did not render for the fetch tool. **Verdict: ignore**; nothing visible beyond the standard loop.

**Synthesia.** Falling notes and/or sheet music; Melody Practice waits for the correct note; hands separately with the app playing the other hand; finger hints; MusicXML loading added in 10.8, though initially without using the extra notation information ([synthesiagame.com/news](https://www.synthesiagame.com/news)) [confirmed via official news page snippet]. One-time purchase. Development pace is slow (10.9 Dec 2022, 10.9.2 on App Store) [reported]. **Verdict: learn** — demonstrates that for a MIDI-equipped power user, "bring your own file" + wait mode is 80% of the value of commercial apps, cheaply.

**La Touche Musicale.** Web platform (Chrome/Opera for Web MIDI) plus apps; MIDI/USB only, no acoustic support; MIDI import turns any file into a tutorial; loop, slow motion, one-hand, metronome; "Piano Convert" AI transcription (2023) ([latouchemusicale.crunch.help compatibility](https://latouchemusicale.crunch.help/en/english/what-types-of-pianos-are-compatible-with-la-touche-musicale), [connect to computer](https://latouchemusicale.crunch.help/en/english/how-do-i-connect-my-piano-to-my-computer), [Maddyness 2023](https://www.maddyness.com/2023/07/19/touche-musicale-intelligence/)) [confirmed for MIDI-only and browser requirement; reported for Piano Convert]. **Verdict: ignore**, but it is an existence proof that a Chrome + Web MIDI piano trainer is viable as a product.

**PianoVision (Meta Quest).** Mixed-reality notes over real keys; MIDI keyboard connected via a desktop bridge app that relays to the headset; virtual keyboard with hand tracking; v2.0 (Jan 2025) added "Ludwig", an AI teacher giving real-time feedback, answering technique questions and recommending songs; ~1,000 public-domain songs free, 10,000+ licensed songs with Plus; MIDI upload ([mixed-news.com, 2025-01-03](https://mixed-news.com/en/piano-vision-update-2-0/)) [reported]. Hand tracking can miss inputs or ghost notes in poor lighting ([pianoers.com review](https://pianoers.com/pianovision-review/)) [reported]. Academic paper exists ([SBC SVR 2022](https://sol.sbc.org.br/index.php/svr_estendido/article/view/23617)) [reported]. **Verdict: learn** — spatial annotation of the physical keyboard (fingering, chord tones, voice-leading arrows) is a powerful idea; a headset is out of scope for a Chrome app but the *on-screen keyboard geometry* view can borrow the semantics.

**Pianote.** A Musora video-lesson platform (Lisa Witt and others): courses, 30-day challenges, "Master Harmony", classical collection; no automatic feedback found on the official site ([pianote.com](https://www.pianote.com/)) [confirmed for absence on home page]. **Verdict: ignore technically.**

**Piano Maestro (JoyTunes).** Teacher-assigned, child-oriented sibling of Simply Piano [reported, prior knowledge; not re-verified this session]. **Verdict: ignore.**

### 1.3 2024–2026 "AI piano tutor" newcomers

- **ROLI AI Music Coach (Feb 2026, beta).** Voice-driven coach inside ROLI Learn, paired with **Airwave**, an infrared camera device tracking 27 hand joints at 90 fps; works with any keyboard; the coach "sees not just what you play but *how* you play"; voice in 40 languages; decides when you're ready to progress; closed beta for Airwave owners from 5 Feb 2026, public beta planned by end of March 2026 ([roli.com/blog/introducing-ai-music-coach](https://roli.com/blog/introducing-ai-music-coach)) [confirmed]. The official page does **not** specify what technique features are detected (fingering? wrist height?) [confirmed absence]. Pricing ~£299 Airwave, Learn app from £13/month ([djmag](https://djmag.com/tech/roli-announces-ai-music-coach)) [reported]. Hands-on preview positive but vendor-arranged ([musictech](https://musictech.com/news/gear/roli-ai-music-coach-airwave-first-look/)) [reported]. ROLI ran its own "can you learn if the teacher can't see your hands" experiment ([roli.com blog](https://roli.com/blog/can-you-learn-piano-if-your-teacher-cant-see-your-hands)) [reported; vendor study]. **Verdict: learn** — confirms a market belief that *hand/technique sensing* is the next frontier; for this project a webcam + MediaPipe hand landmarks could be explored, but accuracy for fingering identification is unproven [speculative].
- **PianoVision "Ludwig"** (see above).
- **Musiah** — markets itself as "the world's first piano lessons app with an AI teacher" ([musiah.com](https://www.musiah.com/)) [reported; claims unverified].
- **Artie (ArtMaster, Prague)** — "AI-powered piano learning app"; $2.4M seed round with Moises participating, 21 Oct 2026 ([musicindustryweekly](https://musicindustryweekly.com/ai-piano-tutor-startup-artmaster-closes-2-4m-seed-round/)) [reported]; no technical details published.
- **Metronaut** (see §2).

General observation [speculative]: "AI tutor" in 2025–26 marketing mostly means (i) an LLM conversational layer (voice Q&A, encouragement, routing to content) and (ii) adaptive sequencing; the underlying measurement is still note correctness. None of the reviewed products publishes what its model measures about expressive performance.

---

## 2. Score-based practice platforms and score following

| Product | Score source | Follows the *player*? | MIDI input | Notable | Verdict |
|---|---|---|---|---|---|
| Soundslice | MusicXML, Guitar Pro, PDF/photo scanner | No (follows its own playback / synced recordings) | Note entry in editor only (Oct 2023), not practice | Score synced to real recordings/video; loop snapping; speed trainer; scale-degree pitch names (May 2026); auto-latency detection | Learn heavily (interaction design) |
| MuseScore Studio 4.x | Native/MusicXML | No | Note entry only | Free, high-quality playback (Muse Sounds); no wait/follow mode per forum | Reuse as authoring/export tool only |
| musescore.com app | Community scores | No | — | Huge catalogue, licensing complexities | Ignore |
| SmartMusic (MakeMusic) | Publisher library | Grades against score via mic | — | Green/red/yellow note marking; % score; very sensitive to note onsets | Learn (and avoid its failure modes) |
| Tomplay | Publisher + recorded accompaniment | No (auto-scroll with audio) | — | 80–100k titles, professional recordings, annotation, self-record | Ignore (content business) |
| Newzik | PDF → "LiveScores" via OMR | Yes, for page turning (AudioScore, mic) | — | AI transposition, MusicXML export | Learn (OMR + follow) |
| forScore | PDF | No; turns via face gestures/MIDI/pedal | MIDI as control messages | Robust annotation, setlists | Ignore |
| Metronaut (Antescofo) | Own catalogue | Yes — accompaniment follows tempo; wrong notes marked for pianists | — | Built on IRCAM Antescofo engine | Learn (reference design for follow-the-player) |
| Real Piano Score, midipiano.app, MidiSlayer | User MusicXML/MEI | Wait mode only | Yes | Small apps; show that MusicXML + wait mode is easy | Learn/possibly reuse |

**Soundslice** — the strongest *interaction design* in this space. Piano practice page lists: syncing notation with real MP3/video performances, drag-to-loop snapping to notes/barlines, slowdown without pitch change, gradual speed training, visual keyboard with LH/RH views, hand focus/muting, pitch names and rhythm counts, transposition, PDF/photo scanner, MusicXML import ([soundslice.com/practice-piano](https://soundslice.com/practice-piano)) [confirmed]. MIDI is only for note entry in the editor (not Safari/iOS) ([soundslice blog 260](https://soundslice.com/blog/260/midi-note-entry)) [confirmed]. May 2026 release: automatic audio latency detection, scale-degree pitch-name option, per-instrument MIDI/MP3/PDF export, "Performances" section ([soundslice blog 310](https://www.soundslice.com/blog/310/new-features-and-fixes-may-2026/)) [confirmed]. Soundslice does **not** listen to the player or grade them [confirmed absence on official pages]. **Verdict: learn** — especially "notation synced to a real recording", which is the natural way to compare one's own performance with reference recordings (e.g., several Clair de lune recordings).

**MuseScore Studio 4.x** — MIDI keyboard is for note input; forum answers state MuseScore "is not capable of waiting for/proofing MIDI input in a follow-along kind of fashion"; a user built a forked MS 3.0 with such a mode; feature requests for a "tutor panel" exist ([musescore.org/en/node/329447](https://musescore.org/en/node/329447), [node/340075](https://musescore.org/en/node/340075), [node/370294](https://musescore.org/en/node/370294)) [confirmed: forum primary sources]. **Verdict: reuse as authoring/cleanup tool** (MusicXML export of IMSLP-derived scores), not as runtime.

**SmartMusic** — microphone assessment marks notes green (correct), red (wrong pitch), yellow (early/late); grade = % green; school FAQs warn it is very sensitive to note beginnings/endings and to mic sensitivity/background noise ([everettsd.org FAQ](https://www.everettsd.org/Page/10823), [Common Sense Education](https://www.commonsense.org/education/reviews/smartmusic)) [reported]. **Verdict: learn what not to do** — a single % score of binarised note events is exactly the "superficial accuracy score" anti-goal; it is also brittle at onsets.

**Tomplay** — interactive sheet music with professionally recorded accompaniments, auto-scroll, tempo control, looping, self-recording, annotation; 80k–100k+ titles across 26 instruments; ABRSM partnership ([thestrad.com](https://thestrad.com/news/play-along-with-an-orchestra-with-the-tomplay-sheet-music-catalogue/13053.article), [ABRSM press release](https://tomplay.com/storage/press/abrsm/Press_Release_ABRSM_Tomplay.pdf)) [reported]. **Verdict: ignore** (content licensing business; doesn't listen).

**Newzik** — AudioScore listens via mic to locate the player and turn pages; LiveScores converts PDF to an interactive score via AI OMR (free tier: 3 scores / 10 pages); playback and MusicXML export; AI transposition ([newzik.com AI features page, 2026-07-28](https://newzik.com/en/resources-sheet-music-app/best-sheet-music-app-ai-features), [App Store](https://apps.apple.com/app/id966963109)) [reported via official resource page snippet]. **Verdict: learn** — PDF→MusicXML via OMR is a real friction point for this user (IMSLP PDFs); OMR quality on dense Romantic piano scores is an open question [speculative].

**forScore** — face-gesture page turns (Pro), MIDI control messages for actions, pedals ([forscore.co/face-gestures](https://forscore.co/face-gestures/)) [confirmed]. Mixed user reports on face gestures ([Hauptwerk forum](https://forum.hauptwerk.com/viewtopic.php?p=140074)) [reported]. **Verdict: ignore.**

**Metronaut / Antescofo** — real-time score following is "the core engine behind Metronaut"; adaptive accompaniment follows the musician's tempo; "Magic Mode"; AI feedback marking right/wrong notes for pianists; subscription after 7-day trial ([platform.antescofo.com](https://platform.antescofo.com/), [App Store](https://apps.apple.com/us/app/metronaut-sheet-music/id1202148484), [Antescofo user guide](https://antescofo-doc.ircam.fr/UserGuide/intro/)) [confirmed: official platform page and store listing]. No independent accuracy evaluation found [confirmed absence in search]. **Verdict: learn** — Antescofo's research lineage (Cont, IRCAM) is the canonical reference for score following; for MIDI input (no audio ambiguity), a much simpler online DTW/HMM follower is feasible in the browser [speculative but well-grounded].

---

## 3. Ear training

| Tool | Format | Input | Context model | Pricing | Verdict |
|---|---|---|---|---|---|
| EarMaster 7 (Pro/Cloud) | Desktop/iOS; 2,500+ exercises; courses | Mouse, MIDI keyboard, mic (sing-back, clap-back since 7.1) | Mostly isolated items + jazz workshops; sight-singing | One-time Pro licence / cloud for schools | Learn (MIDI answers, sing-back) |
| Functional Ear Trainer (Benbassat) | Mobile | Tap | Cadence establishes key; identify scale degree of a tone and its resolution | Freemium / small IAP | Reuse the *method* |
| Complete Ear Trainer | Mobile | Tap | 150+ drills, 28 chapters, 4 levels; progressive | One-time $4.99 iOS | Learn (curriculum ladder) |
| ToneGym | Web/app | Tap/virtual keyboard | Daily 5-game workouts; Melody Hunter; Performance Index | Freemium; Pro sub | Ignore (gamified) |
| SoundGym | Web | Tap | Audio-engineering (EQ, compression) | Sub | Ignore |
| teoria.com | Web | Click | Highly configurable drills + theory reference | Free/partial paid | Learn (configurability) |
| musictheory.net | Web | Click | Lessons + exercises up to Neapolitan; lacks secondary dominants | Free; paid apps | Reuse as reference |
| Toned Ear / ToneSavvy | Web | Click | Intervals, chords, progressions, dictation | Free | Ignore |

**EarMaster 7** — call-response mode for melody sing-back and rhythm clap-back; sight-singing with pitch and timing feedback via microphone; 7.1 added microphone clap input; jazz workshops (jazz chords, progressions, swing rhythms, sing-back on standards such as "St. Louis Blues"); MIDI instrument can be used to answer ([earmaster.com shop](https://earmaster.com/shop/product/earmaster-pro-7.html), [v7 new features (FR)](https://earmaster.com/fr/component/content/article/nouveautes-de-la-v7.html.md)) [confirmed via official pages]. **Verdict: learn** — the most complete classical ear-training package; answering by playing on a MIDI keyboard is the right input modality for a pianist.

**Functional Ear Trainer** (Alain Benbassat, kaizen9) — a cadence/chord progression establishes the key, then a tone is played and the learner identifies its *function* (scale degree); claims that the skill transfers across keys; "10 minutes a day"; custom levels with tonic, scale and cadence settings ([App Store](https://apps.apple.com/app/id1088761926)) [confirmed: store listing]. The pedagogical rationale (hear tones as functions within a key rather than as isolated intervals) matches the user's "system of relationships" goal well [speculative]. **Verdict: reuse the method**, re-implemented with the keyboard as answer device and with cadences drawn from the user's repertoire.

**Complete Ear Trainer** — 150+ drills, 4 levels, 28 chapters, 11 drill types; one-time purchase ([App Store](https://apps.apple.com/app/id1012455471)) [confirmed]. **Verdict: learn** — a dense, sensibly ordered curriculum.

**ToneGym / SoundGym** — daily workout of five games, weekly contests, "ToneGym Performance Index", 400k+ users claimed ([tonegym.co](https://www.tonegym.co/), [App Store](https://apps.apple.com/app/id6748112656)) [reported]. **Verdict: ignore** (gamification anti-goal).

**teoria.com / musictheory.net** — free, web-based; teoria is the most configurable drill site; musictheory.net lessons build sequentially up to Neapolitan chords ([teoria help](https://teoria.com/en/help/web-help.php); [library guides](https://libraryguides.mcgill.ca/musicianship)) [reported]. **Verdict: reference material, not reuse.**

**"Earbeater"** — not found in search this session; existence unverified.

**Research-backed tools.** Search found no consumer ear-training product that publishes efficacy evidence. Relevant research for design:
- Little, Cheng & Wright (2019), *Attention, Perception & Psychophysics*: musical-interval comparison learning occurred only when task practice was combined with periods of passive stimulus exposure; practice alone produced no learning; gains generalised to an untrained interval-identification task ([PMC6384134](https://pmc.ncbi.nlm.nih.gov/articles/PMC6384134)) [confirmed via abstract].
- Blocked vs interleaved learning of melodic intervals ([SMU repository](https://ink.library.smu.edu.sg/soss_research/4316)) [reported; result not checked].
- Van Hedger et al., "Absolute pitch can be learned by some adults" (8-week training, 1 of 6 reached AP criteria) ([PMC6759182](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6759182/)) [confirmed]; Wong et al. 2025, *Psychonomic Bulletin & Review*: 12 adult musicians, mean ~7 pitches at ≥90% after 8 weeks ([ScienceDaily 2025-02-12](https://sciencedaily.com/releases/2025/02/250212134435.htm)) [reported].
These are covered in more depth in the companion notes (pedagogy-evidence.md, cognition-and-models.md).

---

## 4. Harmony / theory visualisation

| Tool | What it shows | Input | Strength | Limit | Verdict |
|---|---|---|---|---|---|
| Hookpad / TheoryTab (Hooktheory) | Melody+chords in scale degrees/Roman numerals; chord palette per key | Mouse, MIDI | Function-first notation; 50k+ analysed pop songs | Pop-centric; lead-sheet abstraction, no real voicings/voice leading | Learn heavily |
| Aria (Hooktheory AI) | Generates chords for melody / melody for chords | — | Trained on TheoryTab | Add-on +$14.99/mo | Ignore |
| Chordify | Chord-symbol timeline from audio | Audio/YouTube | Fast | Chord recognition errors on classical; no function | Ignore |
| Chrome Music Lab | Toy experiments (Spectrogram, Harmonics, Arpeggios, Kandinsky) | Mouse | Beautiful, open source | Not for advanced learners | Learn (aesthetic of experiments) |
| Ableton Learning Music / Learning Synths | Browser tutorials with live editing | Mouse | Exemplary "explorable explanations" | Electronic/pop basics | Learn (format) |
| Harmony Space (Holland) | Tonnetz-like grid; chords as shapes; progressions as paths | Mouse; whole-body (Song Walker) | Research-backed spatial metaphor; image schemas | Largely ignores rhythm; software not available | Learn (theory) |
| TonnetzViz (cifkao) | Live Tonnetz of MIDI input | Web MIDI | Open source, browser | Pitch-class only | Reuse |
| Scaler 3 | Chord sets, detection from MIDI/audio, voice leading | DAW plugin | Auto voice-leading; key detection | Songwriting oriented | Ignore (learn voice-leading UI) |
| Captain Chords (Mixed In Key) | Chord progression generator | DAW plugin | Fast ideation | Shallow theory | Ignore |

**Hookpad** — chords written as Roman numerals/Nashville numbers and melody as scale degrees relative to a key; chord palette shows which chords fit together in a key; paid tier has MIDI export; TheoryTab database of user analyses (figures 13k–50k+ by date); Aria AI as separate subscription ([hooktheory.com/faq](https://www.hooktheory.com/faq), [hookpad/plus](https://www.hooktheory.com/hookpad/plus)) [confirmed via official FAQ snippets]. **Verdict: learn heavily** — scale-degree colouring and a functional chord palette is the best mainstream representation of "harmony as relationships". The gap: it does not handle real piano textures (Chopin's figuration, Debussy's planing) or voice leading.

**Harmony Space** — based on Longuet-Higgins and Balzano's theories; notes, chords, progressions, key areas and modulations all manipulable through one spatial metaphor; toroidal diatonic grid; whole-body and "Song Walker" variants; critique: rhythm largely ignored ([oro.open.ac.uk/59664](https://oro.open.ac.uk/59664), [Song Walker chapter](https://dare.uva.nl/id/dd7d65dd-ff7b-41e9-8dd1-f4733802d6a1), [Ethan Hein on image schemas](https://www.ethanhein.com/wp/2012/image-schemas-in-music-software/)) [confirmed: OU repository abstracts]. **Verdict: learn** — the strongest theoretical precedent for a "harmony as geometry" view; software is not usable today [reported].

**Tonnetz explorers** — TonnetzViz: browser, Web MIDI, real-time Tonnetz rendering, built-in synth ([github.com/cifkao/tonnetz-viz](https://github.com/cifkao/tonnetz-viz)) [confirmed: repo]. The Tonnetz Environment (academic web platform, SMIR/IRCAM-associated; [scitepress 2021](https://www.scitepress.org/Papers/2021/105326/105326.pdf), [EuroMAC](https://europeanmusictheory.eu/a-tonnetz-online-interactive-environment/)) [reported]. harmonic-atlas (GitHub JmsDiG) [reported, licence unchecked]. **Verdict: reuse** TonnetzViz as reference code; but a pitch-class Tonnetz discards register and voicing, which matter for piano [speculative].

**Scaler 3** — 2025 release; automatic voice leading across selected chords, voice grouping, key/scale detection from MIDI and audio, 1,000+ chord sets by mood/artist/genre; VST/AU/AAX/standalone; ~$79–99 ([Sound On Sound](https://www.soundonsound.com/news/scaler-music-introduce-scaler-3)) [reported]. **Verdict: ignore**, but its voice-leading visualisation is worth a look.

**Chordify, Chrome Music Lab, Ableton Learning Music, Captain Chords** — not re-verified in detail this session; descriptions from prior knowledge [reported]. Ableton's [learningmusic.ableton.com](https://learningmusic.ableton.com/) and [learningsynths.ableton.com](https://learningsynths.ableton.com/) are the best examples of "explorable explanations" in music; Chrome Music Lab experiments are open source on GitHub [reported].

---

## 5. Jazz / improvisation tools

| Tool | Paradigm | Input | Status | Verdict |
|---|---|---|---|---|
| iReal Pro | Chord-chart play-along; 50 styles; loop, auto-tempo increase, auto-transpose | None (no listening) | Active; 2025 real drum audio; Windows native 2026; no subscription | Reuse as play-along; learn its chart format |
| Band-in-a-Box (PG Music) | Generate arrangements from chords; RealTracks audio | Chords; audio chord recognition | Active; 2026 version FLAC-only RealTracks; stem splitter | Ignore (heavy, Windows-centric) |
| Impro-Visor (Keller, Harvey Mudd) | Lead-sheet notation, grammar-based lick generation learned from solos, roadmaps of "bricks", note colouring | MIDI/mouse | Free/GPL; last release 10.2 (2019) | Learn (roadmap bricks, note colouring) |
| Aebersold-style play-alongs | Recorded rhythm sections | None | Static content | Ignore |
| Learn Jazz Standards / Open Studio / Jazzedge | Video courses, community, live classes | None | Active | Ignore technically |
| Chord Trainer (browser) | Voicing speed drills: shell, rootless A/B, inversions, ii–V–I in 12 keys, weakness analysis | Web MIDI | Small free tool | Learn/reuse |
| ReaLchords (DeepMind/Mila, ICML 2024) | Online chord accompaniment to a live melody, RL-tuned | MIDI | Research | Learn |
| ReaLJam (CHI 2025 EA) | Live human–AI jamming with visual display of AI's plan | MIDI | Research; no public app found | Learn |
| Somax2 (IRCAM) | Reactive multi-agent co-improvisation, corpus-based | MIDI/audio | Research software (Max + Python) | Possibly reuse offline |

**iReal Pro** — 2025 releases added real drum recordings for jazz styles, root-of-key count-in, double/half time; Windows native (March 2026); explicitly no subscription; 50 styles; loop selection; automatic tempo increase and key transposition ([irealpro.com/version-history](https://irealpro.com/version-history), [news](https://www.irealpro.com/news/real-drums-and-windows-beta/), [App Store](https://apps.apple.com/th/app/id298206806)) [confirmed: official version history]. It never listens to the player [confirmed absence]. **Verdict: reuse** (play-along, and its `irealb://` chart format is widely shared and parseable [reported]).

**Impro-Visor** — free notation tool for monophonic lead sheets; grammar-based lick generation; grammars learnable from transcribed solos; roadmap generator showing keys and chord "bricks"; automatic backing from chord symbols; note colouring indicating chord/colour/approach/outside tones; last stable 10.2 (Aug 2019); source on GitHub ([sourceforge](https://sourceforge.net/projects/impro-visor/), [Wikipedia](https://wikipedia.com/wiki/Impro-Visor)) [confirmed: project page]. **Verdict: learn** — the *roadmap* (Elliott/Keller "bricks" analysis of standards into idiomatic units such as ii–V, turnarounds) and *note colouring* of the learner's own solo against the changes are directly reusable ideas. The software itself is Java/dated.

**ReaLchords / ReaLJam** — ReaLchords: online accompaniment model, pretrained then RL-fine-tuned with a reward model for harmonic and temporal coherence, plus distillation from a teacher that sees future melody; recovers from sudden transposition better than MLE baseline ([PMLR v235 Wu et al. 2024](https://proceedings.mlr.press/v235/wu24c.html), [arXiv 2506.14723](https://arxiv.org/abs/2506.14723)) [confirmed: paper]. ReaLJam: interface/protocol for real-time jamming where the agent continually predicts and *visually displays its planned chords* so the human can anticipate; user study with experienced musicians ([arXiv 2502.21267](https://arxiv.org/abs/2502.21267)) [confirmed: paper]. A 2026 follow-up on real-time LM jamming exists ([arXiv 2606.11886](https://arxiv.org/pdf/2606.11886)) [reported, not read]. **Verdict: learn** — the "AI shows its plan" idea is pedagogically valuable (makes harmonic anticipation visible). Models/weights availability not verified.

**Somax2** — real-time improvising agents based on corpus-based generation and cognitive modelling; learns from MIDI corpora; listens continuously and adapts; multi-agent networks; Max + Python implementation (v2.5) ([reach.ircam.fr Somax2](https://reach.ircam.fr/index.php/2024/01/27/somax2/), [SMC 2022 paper](https://isidore.science/document/10670/1.6850a30f2c2ee2ab4f71fa664230f18a95e3dc0e)) [confirmed: IRCAM project page]. **Verdict: possibly reuse** as an external Max patch talking MIDI to the web app; likely too heavy for a first version [speculative].

**Voicing trainers** — "Chord Trainer" (free, browser, MIDI, 9 voicing types incl. rootless A/B, ii–V–I in 12 keys, per-chord timing/weakness analysis); VoicingWorkout (iPad, MIDI, by ear); Rootless Voicings (iOS, MIDI not stated); VoicingLab (lookup, 468 chords × 16 voicing styles, with an MCP server) ([AlternativeTo: Chord Trainer](https://alternativeto.net/software/telaaron-piano-chord-trainer/about), [App Store VoicingWorkout](https://apps.apple.com/st/app/voicingworkout/id6748817790)) [reported]. An r/JazzPiano thread (~2025) reported no good voicing-drill app and recommended Phil DeGreg's *Jazz Keyboard Harmony* [reported]. **Verdict: learn** — voicing drills with MIDI are easy to build; the open space is *voice-leading-aware* drills (minimal motion between voicings through a progression) and *ear-led* drills (hear a voicing, reproduce it).

**Open Studio** — members-only jazz piano platform (Peter Martin, Adam Maness): video courses, live daily classes, "Magic Voicing System", "Harmony Games", "Improv Games" ([openstudiojazz.com instructors](https://www.openstudiojazz.com/?p=1275975)) [reported]. **Verdict: ignore technically**; good curricular ideas (games framing of harmony) that are pedagogical, not software.

---

## 6. Open-source projects and research prototypes close to the concept

No single open-source project combines **interactive engraved score + harmonic/structural analysis + live MIDI keyboard + performance analytics**. The pieces exist separately, mostly at small scale. (Alignment/following libraries are covered in depth in the companion note `performance-capture-analysis.md`; here they are listed only for landscape completeness.)

### 6.1 Practice front-ends (browser / desktop)

| Project | What it is | Stack / licence | Maturity | Verdict |
|---|---|---|---|---|
| [ftrain/sightreading](https://github.com/ftrain/sightreading) | Web sight-reading trainer: 23 procedurally generated levels (circle of fifths, rhythms), RH→LH→both, mastery gating, tempo ramps from 30 BPM; MIDI correctness colouring (teal/red) | Vite + TypeScript + **Verovio** (MusicXML→SVG) + Tone.js + Web MIDI; Playwright/Vitest tests; LGPL-3.0 | Small (≈34 commits, 15 stars) | **Reuse as reference** — almost exactly our intended rendering + input stack [confirmed: repo] |
| [huytd/sightread](https://github.com/huytd/sightread) (fork of sightread/sightread; [sightread.dev](https://sightread.dev)) | Free web app "for learning to play Piano", falling-notes oriented, MIDI recommended | Next.js + TypeScript | Small fork; upstream more active [reported] | Learn |
| [PianoBooster](https://github.com/pianobooster/PianoBooster) | MIDI-file player that shows notation and *waits/follows* the player; can play one hand | C++/Qt, FluidSynth; GPL | Mature, old | Learn |
| [Neothesia](https://github.com/PolyMeilex/Neothesia) | Open-source Synthesia (falling notes from MIDI) | Rust, wgpu | Active [reported] | Ignore (falling notes) |
| Clementi | Desktop MIDI-file trainer with wait mode ([linuxaudio wiki](https://wiki.linuxaudio.org/_export/xhtml/apps/all/clementi)) | — | Small | Ignore |
| [Toccata](https://github.com/ange-yaghi/toccata) | MIDI analyser: bar recognition, average jitter and deviation from "perfect" time, inferred tempo; dynamics metrics and a per-piece MIDI database *planned* | C++ (inferred) | WIP since 2021, 64 commits | **Learn** — evidence that even timing analytics are unfinished in OSS [confirmed: repo] |
| [Czerny](https://jtauber.com/blog/2010/07/19/czerny/) (James Tauber, 2010) | Python: aligns performance to score with Needleman–Wunsch; reports timing and velocity deviations, not just wrong notes; Core MIDI input | Python | Dormant prototype | Learn (early precedent) |
| [TonnetzViz](https://github.com/cifkao/tonnetz-viz) | Live Tonnetz of Web MIDI input | JS | Stable small | Reuse |
| [liotier/AkaiMPC](https://github.com/liotier/AkaiMPC) | Browser app with Roman-numeral analysis, keyboard diagrams, Web MIDI | Vanilla JS | Small | Learn [reported] |
| [music21j](https://www.npmjs.com/package/music21j-port) | JS port of music21 with Web MIDI, keyboards, metronome | JS | Theory features ≈ music21 c. 2012 | Possibly reuse for client-side theory objects [reported] |
| Chrome Music Lab | Experiments on Web Audio/Web MIDI/Tone.js; source published by Google ([developers.googleblog.com](https://developers.googleblog.com/introducing-chrome-music-lab/)) | JS, Apache-2.0 [reported] | Stable | Learn (aesthetic) |
| [PianoPlayer](https://docsearch.algolia.com/mcp/docs/repo/marcomusy/pianoplayer) (marcomusy) | Automatic piano fingering from MusicXML/MIDI via hand model; CLI/GUI/Web API | Python, MIT | Mature-ish | Reuse for fingering suggestions (quality unverified) [reported] |
| Music Coach (Staffordshire student project, 2026) | Web MIDI app capturing pitch/velocity/timestamps for pitch/timing/dynamics feedback ([PDF](https://gradex.staffs.ac.uk/wp-content/uploads/2026/05/5563_Music_Coach_Project_Jemima_Orakwue_GradEx.pdf)) | Web | Prototype | Ignore |

### 6.2 Alignment, following and analysis back-ends (Python)

- **Matchmaker** (`pymatchmaker`, KAIST + JKU; ISMIR 2024 LBD, ISMIR 2025 paper): real-time score following for piano; for MIDI input offers `pthmm` (default), `arzt`, `dixon`, `outerhmm`, `hmm`; live MIDI device input or byte streams (e.g. from a WebSocket); MusicXML/MIDI scores; **Apache-2.0**; evaluated on ASAP, Batik, Vienna4x22 ([docs](https://pymatchmaker.readthedocs.io), [arXiv 2510.10087](https://arxiv.org/abs/2510.10087)) [confirmed: docs]. **Reuse.**
- **parangonar + partitura** (CPJKU): offline/online note alignment (AutomaticNoteMatcher, DualDTWNoteMatcher, neural "TheGlueNoteMatcher"), Parangonada web viewer; partitura for MusicXML/MIDI/match I/O and performance features ([PyPI](https://pypi.org/project/parangonar), [partitura docs](https://partitura.readthedocs.io/en/latest/introduction.html)) [confirmed: PyPI/docs]. **Reuse.**
- **music21** (MIT): Roman numeral analysis (`roman.romanNumeralFromChord`), corpora; MCP-server wrappers exist (e.g. [music21-mcp-server](https://glama.ai/mcp/servers/brightlikethelight/music21-mcp-server)) [reported]. **Reuse.** The project already holds the *When in Rome* Roman-numeral corpus locally (`data/external/when_in_rome`), which provides expert harmonic analyses for many classical pieces — a resource no commercial app exposes to learners [confirmed: local directory exists; coverage of target repertoire not checked].
- **Expressive timing scripts** (Hu et al., TISMIR 2026; [github.com/huispaty/expressive_timing](https://github.com/huispaty/expressive_timing)) [reported] — reference metrics for timing analysis.

### 6.3 LLM / "AI tutor" prototypes (2024–2026)

- **Peachnote Piano Tutor** — Vladimir Viro, ISMIR 2025 demo "From Notes to Nuance: A Conversational AI for Affective Piano Performance": listens (MIDI or mic), aligns to a reference score in real time, and after the student pauses gives spoken teacher-style feedback on *expressive nuance* with synchronised score highlights via a multimodal LLM; WebRTC client–server; **no paper, poster, video or evaluation published** ([ismir2025program.ismir.net/lbd_451](https://ismir2025program.ismir.net/lbd_451.html)) [confirmed]. Closest prior art to this project's "listen → align → reflect" loop. **Learn** (and note the absence of evaluation).
- **PianoQuest Live** — Gemini Live hackathon build combining camera, mic and Web MIDI; captures per-note velocity and timing "to ground its coaching" ([dev.to write-up](https://dev.to/jayiscoding/building-a-real-time-ai-piano-coach-with-gemini-live-api-4h08)) [reported].
- **Lyra** (Devpost) — voice-first browser piano companion with USB-MIDI; per search snippet the team "hit the current limits of LLMs for music theory comprehension" and limited v1 to chords and scales ([devpost](https://devpost.com/software/lyra-ai-d5m1uw)) [reported; page returned 403].
- **LLM symbolic-music competence benchmarks** — ChatMusician/MusicTheoryBench (2024) found LLMs weak on college-level theory ([arXiv 2402.16153](https://www.arxiv-vanity.com/papers/2402.16153)); ABC-Eval (2025, 1,086 items, notable limitations in seven LLMs; [arXiv 2509.23350](https://arxiv.org/abs/2509.23350v1)); WildScore (EMNLP 2025, score images; [arXiv 2509.04744](https://arxiv.org/abs/2509.04744)); CSyMR-Bench (LLM agent + music21 tools gains 5–7 points; [arXiv 2601.11556](https://www.arxiv.org/abs/2601.11556)) [reported from abstracts/snippets]. Implication [speculative but consistent across sources]: an LLM should **not** be trusted to do harmonic analysis from raw notes; it should narrate and question over *tool-computed* analysis (music21, corpus annotations, alignment output).
- **Google A.I. Duet** (2016; [github](https://github.com/googlecreativelab/aiexperiments-ai-duet)) and **schollz/PianoAI** (Go, GPL-3.0; [github](https://github.com/schollz/PIanoAI)) — call-and-response generative accompaniment; no pedagogy [reported].

### 6.4 Small commercial tools worth knowing

- **Hanon Pro** (Furnace Creek Software, Aug 2024; iOS/Mac): technique exercises + repertoire; with MIDI, evaluates "accuracy, tempo and dynamics", auto page turns; does not document how dynamics are scored ([listing](https://mwm.ai/apps/hanon-pro/6473125727)) [reported].
- **Scale Study** (iOS): MIDI scale checking, records fastest clean tempo; no evenness/velocity reporting ([appfollow](https://apps.appfollow.io/ios/scale-study-tempo-practice/6758663846?country=fr)) [reported].
- **Yamaha Piano Diary** (iOS, free): records and archives every MIDI performance, counts practice days/time/notes; cloud backup; requires cable connection ([yamaha.com](https://au.yamaha.com/en/musical-instruments/pianos/products/apps/piano-diary)) [confirmed: official page snippet]. **Learn** — the only "practice archive" product found, and it does no analysis.
- **Henle Library** (iOS/Android): urtext scores with *selectable alternative fingerings from named pianists* superimposed on the unchanged score, annotation, recording, metronome ([henle-library.com/en/features](https://henle-library.com/en/features/)) [confirmed]. **Learn** — "multiple expert interpretations overlaid on one urtext" is a strong pattern to generalise (fingerings, pedalling, phrasing, tempo maps).
- **Music Plus One** (Christopher Raphael, Indiana): Listen (HMM) / Predict (Kalman-like timing model trained over rehearsals) / Play (time-stretched orchestral recording) — the classical precedent for an accompanist that *learns the soloist's interpretation* ([what.html](https://music.informatics.indiana.edu/~craphael/music_plus_one/what.html), [ICML 2010](https://icml.cc/imls/conferences/2010/papers/904.pdf)) [confirmed: author pages]. **Learn.**

---

## 7. Reuse / learn / ignore — consolidated

| Reuse (code, data, format) | Learn (design pattern) | Ignore |
|---|---|---|
| Verovio, OSMD (rendering); Web MIDI; Tone.js | Soundslice: notation synced to real recordings, loop snapping, LH/RH keyboard view | Simply Piano, Yousician, Skoove, Playground Sessions, Piano Maestro |
| Matchmaker, parangonar, partitura (alignment/following) | Piano Marvel SASR: adaptive staircase over a calibrated excerpt bank | ToneGym/SoundGym gamification |
| music21 + When in Rome / other RN corpora | Functional Ear Trainer: cadence-anchored scale-degree hearing | Tomplay, forScore, musescore.com |
| PianoPlayer (fingering hypotheses) | Hookpad: scale-degree colouring + functional chord palette | Band-in-a-Box (for this user) |
| TonnetzViz (reference code) | Harmony Space: one spatial metaphor for notes/chords/keys/modulation | Neothesia/falling-notes UIs |
| iReal Pro charts as play-along source | Impro-Visor: roadmap "bricks", colouring of solo notes vs. changes | Chordify (for classical) |
| ftrain/sightreading (architecture reference) | Henle: multiple expert fingerings over urtext | Captain Chords, Scaler 3 (except voice-leading UI) |
| MuseScore Studio (authoring/cleanup only) | ReaLJam: AI displays its *plan* ahead of time; Music Plus One: accompanist learns from rehearsals | SmartMusic-style single % score |
| | Peachnote Tutor: speak only after the player pauses | |
| | ROLI Airwave: hand/technique sensing as a frontier | |

---

## 8. GAPS — what nobody offers well

Each gap lists the evidence that it is real. "Nobody" means "none of the ~50 products/projects reviewed here"; absence of evidence in a web search is weaker than a documented negative, and this is flagged.

**G1. Performance analytics beyond correctness (timing, dynamics, voicing balance, pedalling, articulation) presented as *musical* quantities.**
Evidence: every commercial tutor reviewed measures note correctness and approximate timing (§1). SmartMusic's grade is % correct notes/rhythms [reported]. Peachnote's ISMIR 2025 demo explicitly positions itself against commercial tutors that "mainly check note accuracy" [confirmed]. Open-source attempts at timing/dynamics metrics (Toccata, Czerny) are unfinished or dormant [confirmed]. A Piano World thread titled "app that shows unevenness" exists (content behind a paywall to the fetch tool) [reported]. Hanon Pro claims "dynamics" analysis without documenting it [reported]. Strength of evidence: **strong** for commercial products; moderate for "nobody at all".

**G2. Comparing one's own performance with reference interpretations, at note level.**
Evidence: Soundslice syncs notation to recordings but never to *the learner's* playing [confirmed]; no tutor overlays the learner's tempo/dynamics curve with, e.g., three reference pianists' curves. Research datasets (ASAP, Vienna4x22, Batik) and alignment tools make this feasible (§6.2) but are not productised [confirmed: tools exist; absence in products is from this survey]. **Strong.**

**G3. Live linkage between what is being played and its harmonic/structural analysis on real classical repertoire.**
Evidence: Hookpad does function-first analysis only for its own lead-sheet abstraction of pop songs [confirmed]; Chordify outputs chord symbols from audio with no function and with anecdotal accuracy problems [reported]; Tonnetz tools show pitch classes without key context or voice leading [confirmed]; no score-based practice platform (Soundslice, MuseScore, Newzik, Tomplay) shows Roman numerals, cadences, or form [confirmed absence on official feature pages]. Expert analyses exist (When in Rome, DCML corpora) but no learner-facing app uses them [speculative/absence]. **Strong.**

**G4. Ear training generated from the learner's own repertoire and keyboard.**
Evidence: all ear trainers reviewed use generic item banks (§3); EarMaster accepts MIDI answers but on its own content [confirmed]; Functional Ear Trainer's cadence method is not tied to pieces [confirmed]. No product turns "the progression in bars 1–4 of Moonlight" into a dictation, a "sing the bass", or a "which voice moved?" exercise [absence]. **Moderate–strong.**

**G5. Learner-owned, inspectable, longitudinal practice data.**
Evidence: Yamaha Piano Diary archives MIDI but analyses nothing and stores to vendor cloud [confirmed]; practice-log apps are manual or audio-timers [reported]; commercial tutors keep data in proprietary accounts and expose gamified progress [reported]. No tool found that records every session automatically and lets the user query it (e.g., "how has my bar-17 rubato changed over six weeks?"). **Strong** (consistent across searches; also logically implied by business models).

**G6. Practice-*process* analysis (what the learner did, not just the final take).**
Evidence: no product reviewed segments practice into attempts, loops, slow-practice phases, or error-repair episodes; all evaluate a "performance" run [absence; speculative that none exist]. Research covers it (see `performance-capture-analysis.md` §5 and `pedagogy-evidence.md`). **Moderate.**

**G7. Voice-leading-aware harmony/voicing training on the keyboard.**
Evidence: voicing trainers drill isolated voicings or ii–V–I in 12 keys (Chord Trainer) [reported]; r/JazzPiano thread reports no good app and recommends a book [reported]; Scaler 3 automates voice leading for composition but does not train it [reported]. **Moderate.**

**G8. Honest, tool-grounded AI explanation.**
Evidence: 2025–26 AI tutors (ROLI, PianoVision Ludwig, Musiah, Artie) do not document what their models measure [confirmed for ROLI; reported for others]; LLM benchmarks show weak raw symbolic-music reasoning, improved with music21 tools (CSyMR-Bench) [reported]; Lyra's team hit LLM theory limits [reported]. A design where the LLM narrates *verifiable* computed facts (with links to the bars and numbers) is not offered by anyone found. **Moderate–strong.**

**G9. Cross-representation "relationship" views.**
Evidence: products typically offer two linked views at most (score + falling notes; score + video; chords + timeline). Harmony Space showed one metaphor for multiple harmonic levels but ignored rhythm and is unavailable [confirmed]. No tool links notation ↔ keyboard geometry ↔ harmonic function ↔ sound ↔ the learner's performance in one synchronised cursor [absence]. **Moderate** (hard to prove a negative; but none of the surveyed feature lists come close).

**G10. Technique sensing for an adult on an acoustic-action instrument without special hardware.**
Evidence: ROLI's Airwave is the only consumer technique-sensing product, requires £299 hardware, and does not document what it detects [confirmed]; PianoVision hand tracking is unreliable in poor light [reported]. For this project, MIDI velocity/timing can only *infer* technique; webcam hand tracking is an open research question [speculative]. **Moderate** — and possibly not worth pursuing early.

---

## 9. IDEAS — non-obvious features inspired by the survey

Format: **Idea** — learning mechanism · feasibility (with this user's stack: macOS, Chrome, USB MIDI, Python available) · originality relative to the surveyed landscape. All feasibility/originality judgements are [speculative].

1. **"Interpretation overlay" (Henle-fingerings generalised to expression).** Overlay the learner's per-beat tempo curve and per-voice velocity profile on curves extracted from 2–4 reference performances (MIDI from datasets, or audio→MIDI transcription), aligned to the same score. *Mechanism:* contrastive perception — hearing/seeing *where* interpretations diverge sharpens the learner's own intent rather than prescribing a "correct" one. *Feasibility:* high for MIDI references (parangonar/partitura); medium for audio references (needs transcription + alignment). *Originality:* high; no product does note-level comparison against named interpretations.

2. **Harmonic cursor.** As the score follower advances (Matchmaker), the current Roman numeral, local key, cadence type and voice-leading lines light up on score, keyboard and a Tonnetz/Harmony-Space-like map simultaneously; pausing on a chord plays its reduction (block chord, bass+soprano only). *Mechanism:* dual coding and attention-guiding while the motor system is engaged; builds harmony-as-relationships from the user's own repertoire. *Feasibility:* medium (needs RN analysis aligned to measures; When in Rome covers some pieces; music21 can propose others for manual correction). *Originality:* high (fills G3, G9).

3. **Repertoire-mined ear training.** Automatically derive exercises from the pieces in the user's library: cadence + "what scale degree is the melody on at the downbeat of bar n?", "play back the bass line of bars 1–4", "which voice moved?" between two voicings from Clair de lune, functional dictation of a Chopin progression re-voiced. Answers via MIDI keyboard. *Mechanism:* transfer-appropriate processing — skills trained in the context where they will be used; Functional-Ear-Trainer-style tonal anchoring; Little et al. (2019) suggest interleaving practice with passive exposure, which listening to the piece provides. *Feasibility:* medium–high (music21 extraction + Web MIDI). *Originality:* high (G4).

4. **Planned-motion display for accompaniment (ReaLJam-style "plan visibility") applied to classical study.** When an accompanist or the app plays the left hand (or orchestra reduction), show a short look-ahead of upcoming harmonies and the expected tempo; for jazz, show the next two bars of changes as functional arrows. *Mechanism:* training *anticipation* (predictive listening), which expert sight-readers and improvisers rely on. *Feasibility:* high for deterministic accompaniment; research-grade if generative. *Originality:* medium–high.

5. **Accompanist that learns your rubato (Music Plus One revisited, MIDI-only).** For pieces with a second part (Bach two-part inventions with app-played voice, concerto reductions, jazz comping), fit a per-piece timing model over rehearsals so the app follows *your* phrasing better each time; expose the learned tempo map as an object the user can inspect and edit. *Mechanism:* ensemble-like feedback without a partner; making one's interpretation explicit and editable. *Feasibility:* medium (Kalman/HMM timing on symbolic input is simpler than Raphael's audio case). *Originality:* medium (precedent exists in research, absent in products).

6. **Always-on silent-piano flight recorder + practice-process timeline.** A background CoreMIDI logger records every session; afterwards, segments sessions into attempts, loops, tempo changes and repaired errors, and maps them onto the score as a "heat-and-history" layer ("you looped bars 9–12 34 times; error rate fell after you slowed to 60%"). *Mechanism:* metacognition — making practice strategy visible supports deliberate practice; learner-owned data (G5, G6). *Feasibility:* high for capture; medium for segmentation (alignment of fragmented practice is discussed in `performance-capture-analysis.md` §3.4). *Originality:* high relative to products (Yamaha Piano Diary only archives).

7. **Adaptive sight-reading staircase on public-domain excerpts, scored for *continuity* not just accuracy.** Rebuild Piano Marvel's SASR idea over IMSLP/MusicXML excerpts (Bach chorales, Czerny, Bartók Mikrokosmos where licensing permits), but score keeping the pulse, recovering after errors, and look-ahead (time-to-first-note after page turn). *Mechanism:* psychometric staircase keeps items near the edge of competence; scoring continuity rewards the skill that actually matters in sight-reading. *Feasibility:* medium (item calibration needs many trials; could start with heuristic difficulty features). *Originality:* medium (SASR exists; continuity scoring does not).

8. **Voice-leading gym.** Given a progression (from the user's repertoire or a jazz standard), the user plays successive voicings; the app shows total semitone motion, parallel fifths/octaves, common tones held, and the minimal-motion alternative on the keyboard diagram; ear mode: hear two voicings, identify which voice moved and by how much. *Mechanism:* links keyboard geometry to harmonic function and to hearing; jazz and classical share the same underlying skill. *Feasibility:* high (pure symbolic computation + Web MIDI). *Originality:* medium–high (G7).

9. **"Explain with receipts" LLM layer.** An LLM tutor may only make claims that cite computed evidence: bar numbers, measured values, RN labels from corpus or music21, alignment output; each claim is clickable to the score region and the data. It speaks only after the player pauses (Peachnote pattern) and asks questions ("did you intend the ritardando at bar 15?") more than it judges. *Mechanism:* reflective dialogue, self-explanation; avoids hallucinated theory (G8). *Feasibility:* high (tool-use LLM over local analysis APIs). *Originality:* medium–high (AI tutors exist; grounded, auditable ones do not).

10. **Bricks-for-classics roadmap.** Port Impro-Visor's "roadmap of bricks" idea to classical repertoire: segment a piece into idiomatic units (cadential 6/4, Romanesca, Prinner, sequences by fifths, pedal points — in the spirit of galant schemata) and show them as a map; the same schema can be practised in all keys and recognised across pieces. *Mechanism:* chunking — experts perceive music in larger learned units; cross-piece recognition builds the "interconnected system" view. *Feasibility:* medium (schema detection is research-grade; start with manual/corpus labels). *Originality:* high in a learner product.

11. **Transposition-as-probe.** Ask the user to play a passage they know in another key (or in parallel minor, or re-harmonised) and measure where fluency collapses; collapse points reveal whether the passage is stored as motor sequence vs. harmonic understanding. *Mechanism:* diagnostic transfer task; encourages encoding by function and geometry rather than by finger memory. *Feasibility:* high (MIDI comparison with transposed score). *Originality:* high (no product uses transposition diagnostically).

12. **Pedal and resonance lab (silent-piano specific).** Visualise sustain-pedal MIDI CC64 timing against harmonic changes (did the pedal change catch the new bass? did it blur a non-chord tone?) on Clair de lune / Chopin; offer A/B audition of the same passage re-rendered with alternative pedalling. *Mechanism:* links an invisible motor action to its harmonic/sonic consequence. *Feasibility:* high for CC64 analysis; re-rendering needs a good piano sampler (e.g. via the silent system or a software piano). *Originality:* high — no product surveyed analyses pedalling.

---

## 10. Open questions and things not verified

- Official feature pages for Skoove, Playground Sessions and Yousician could not be fetched (empty shells / 403); some claims rest on secondary reviews.
- Community consensus on r/piano, Piano World and Pianostreet was **not** sampled directly (paywalled or not returned by search). Statements about forum attitudes are the agent's prior knowledge and should be checked.
- "Earbeater" could not be found.
- ROLI AI Music Coach: what the hand-tracking actually detects is undocumented; public beta status after March 2026 not checked.
- Availability of ReaLchords/ReaLJam models or code was not verified.
- Whether When in Rome covers the user's target pieces (Moonlight mvt 1, Clair de lune, Chopin) was not checked.
- Newzik OMR quality on dense piano scores is unknown; worth a hands-on test with an IMSLP PDF.
- MuseScore Studio 4.5/4.6 release notes were not checked for any newly added practice features (forum evidence says none as of the threads found).
- Pricing figures change frequently; treat all prices as indicative.
