# Products landscape: existing learning software for a "computational piano learning laboratory"

> **Agent-produced research note, dated 2026-10-23. To be reviewed.** Not independently verified by a human. All URLs accessed 2026-10-23 unless stated otherwise.
>
> Evidence tags: **[confirmed]** = checked against a primary source (official docs/help centre/repo/paper) during this session; **[reported]** = from credible secondary sources (press, reviews, store listings, forums) and not checked against a primary source; **[speculative]** = the agent's own inference.
>
> Caveat on method: several vendor marketing pages returned empty shells or HTTP 403 to the fetch tool (Skoove, Playground Sessions, Yousician help centre). Where that happened, claims rest on search-result snippets of the official page or on secondary reviews and are tagged accordingly. Forum consensus (r/piano, Piano World, Pianostreet) could not be sampled directly this session; statements about "community consensus" are therefore weaker than they look and are marked [reported] at best.

(Draft v1, written early because of interruptions; extended below.)

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

## 6. Open-source projects close to the concept

(Section in progress — see below.)

---

## 7. GAPS

(In progress.)

## 8. IDEAS

(In progress.)
