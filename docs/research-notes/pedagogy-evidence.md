# Pedagogy & learning-science evidence for the piano learning lab

> **Agent-produced research note, dated 2026-10-23. To be reviewed.**
> Written by a research sub-agent for the "computational piano learning laboratory" project. Every claim is tagged:
> **[confirmed]** = I read the paper, its abstract or its publisher/PubMed record during this session;
> **[reported]** = taken from a secondary source or from background knowledge I did not re-check this session (verify before relying on it);
> **[speculative]** = my inference or design proposal.
> Effect sizes are given in the metric the source used (r, d, g, % variance). Most music-practice studies are small (N = 10–40), use students or children, and test retention after 24–48 h, so read every "Strong" grade as "strong *for this literature*".
>
> **Status: v1.0 (complete first pass). Not exhaustive; several full texts were paywalled, so abstract-level confirmation is the norm.**

---

## 0. Summary for the impatient (TL;DR)

1. **How you practise matters more than how long.** Accumulated practice explains a real but modest share of variance in musical skill (≈21% in Macnamara et al. 2014; r_c ≈ .61 in Platz et al. 2014, but in a different and more practice-friendly set of studies). Among practisers with similar time, the ones who **find the exact error spot, fix it, vary tempo, and stop only once the correct version is stable** retain more (Duke, Simmons & Cash 2009, N = 17). The app should measure *practice behaviour*, not hours.
2. **Learning ≠ performance during practice.** Interleaving, spacing and less feedback often make practice *look* worse and retention *better*; learners (including trained pianists) misjudge this (Abushanab & Bishara 2013). Assess learning with **delayed, unassisted** probes (next day, cold), not end-of-session accuracy. **But** the music-specific interleaving evidence is genuinely mixed: a 2024 study of 20 advanced violinists found *blocked* practice best at 24 h (Mathias & Goldman 2024) — so the app should test schedules on the user rather than impose one.
3. **Feedback: less, later, higher-level, self-requested.** Continuous concurrent visual feedback risks dependence (guidance hypothesis); terminal, summary and bandwidth feedback are the safer defaults. But note: the "self-controlled feedback" and "external focus" advantages from Wulf's programme shrink to roughly zero after publication-bias correction (McKay et al. 2022, 2023, 2024). Treat them as *harmless options*, not engines of learning.
4. **Ear and inner hearing are load-bearing.** Auditory imagery/inner hearing predicts sight-reading (Kopiez & Lee 2008) and supports memorised performance (Highben & Palmer 2004); aural training/singing is among the few intervention types that improves sight-reading (Mishra 2014). Notational audiation is a real, measurable capacity (Brodsky et al. 2003).
5. **Audio–motor coupling forms fast and is specific.** Keyboard-to-pitch mappings start forming within ~20 minutes and strengthen over weeks (Bangert & Altenmüller 2003); motor areas activate when hearing music you have learned to play (Lahav et al. 2007). Design implication: always couple key action with sound, and train "hear → play" and "play → predict sound" loops.
6. **Structure-based (analytic) memory is what experts use.** Chaffin & Imreh's longitudinal case (Bach Italian Concerto, Presto) shows formal structure used as a retrieval scheme and performance cues as retrieval cues. Evidence that *teaching* analysis causally improves novices' memory is thinner.
7. **Improvisation draws on stored, recombined patterns plus rule-based generation** (Pressing 1988; Berliner 1994; Norgaard 2011, 2014). A formula→variation→generation progression is consistent with the evidence; good controlled trials of improvisation *pedagogy* for adults are almost absent.
8. **Evidence for "spaced repetition of music facts" transfers poorly to perception.** SRS works for declarative facts; harmonic hearing is perceptual learning with its own, more task-specific rules. Use SRS for *items you can retrieve* (voicings, progressions in a key, scale-degree hearing), but evaluate transfer separately.

---

## 1. Deliberate practice and what effective practisers do

### 1.1 How much does practice matter? The quantitative debate

- **Ericsson, Krampe & Tesch-Römer (1993)**, *Psychological Review* 100(3):363–406, doi:10.1037/0033-295X.100.3.363. Retrospective practice estimates of Berlin violin students tracked skill group; the "best" violinists had ~10,000 h by age 20. Claimed individual differences in expert performance are largely accounted for by deliberate practice (DP). [reported]
- **Macnamara, Hambrick & Oswald (2014)**, "Deliberate practice and performance in music, games, sports, education, and professions: A meta-analysis", *Psychological Science* 25(8):1608–1618, doi:10.1177/0956797614535810. 88 studies, >11,000 participants. DP explained **≈26% of variance in games, 21% in music, 18% in sports, 4% in education, <1% in professions.** Effects were *weaker* when practice was logged rather than retrospectively estimated and when performance was measured with standardised instruments. [confirmed — abstract-level, via press release & search summaries]
- **Platz, Kopiez, Lehmann & Wolf (2014)**, "The influence of deliberate practice on musical achievement: a meta-analysis", *Frontiers in Psychology* 5:646, doi:10.3389/fpsyg.2014.00646. 13 music studies, **r_c = .61** after correcting for unreliability; authors argue this is a lower bound and objected to converting it to "36% of variance". [confirmed — abstract/commentary]
- **Hambrick et al. (2014)**, "Facing facts about deliberate practice", *Frontiers in Psychology* 5:751, doi:10.3389/fpsyg.2014.00751 — response; maintains DP accounts for roughly a third of reliable variance at most, leaving room for other factors (working memory, starting age, genes). Also Hambrick, Oswald, Altmann, Meinz, Gobet & Campitelli (2014), *Intelligence* 45:34–45 ("Deliberate practice: Is that all it takes to become an expert?"). [confirmed/reported]
- **Macnamara & Maitra (2019)**, "The role of deliberate practice in expert performance: revisiting Ericsson, Krampe & Tesch-Römer (1993)", *Royal Society Open Science* 6:190327, doi:10.1098/rsos.190327. Direct replication with 39 violinists, blinded skill ratings. DP accounted for **≈26% of variance** (original implied ~48%); "best" violinists did *not* accumulate more practice than "good" ones. [confirmed — abstract & summaries]
- **Macnamara, Moreau & Hambrick (2016)**, sports meta-analysis, *Perspectives on Psychological Science* 11(3):333–350, doi:10.1177/1745691616635591: 18% overall, ~1% among elite athletes. [reported]
- Other predictors in music: Mosing, Madison, Pedersen, Kuja-Halkola & Ullén (2014), *Psychological Science* 25(9):1795–1803, doi:10.1177/0956797614541990 — twin study (N ≈ 10,500 Swedish twins): practice associated with musical *ability* across individuals, but within identical-twin pairs the twin who practised more did not have better auditory discrimination; practice heritability ~40–70%. [reported]

**Interpretation for this project.** For one adult learner the between-person debate is mostly irrelevant: practice is the only lever the app controls. What matters is the *within-person* claim that practice **quality** (feedback, specificity, effortful correction) matters, which these meta-analyses do not directly test (they mostly correlate cumulative hours with level).

### 1.2 What distinguishes effective practisers?

- **Duke, Simmons & Cash (2009)**, "It's not how much; it's how: Characteristics of practice behavior and retention of performance skills", *Journal of Research in Music Education* 56(4):310–321, doi:10.1177/0022429408328851. 17 graduate/advanced-undergraduate piano majors practised a difficult 3-bar passage from a Shostakovich concerto as long as they wished, then were tested the next day. **Neither practice time nor number of repetitions predicted retention.** Retention rank correlated with the percentage of all trials played correctly (r = −.51; negative because rank 1 = best), the percentage of *complete* trials played correctly (r = −.71), and the number of incorrect trials during practice (r = .48). The authors conclude strategies were more determinative than amount. [confirmed — abstract-level] The descriptive account of the top-ranked pianists: they (a) addressed errors **immediately**, (b) **identified the precise location and source** of each error, (c) **varied tempo systematically** (slowing, then restoring), and (d) **repeated correct performances until the correction stabilised** before moving on. [reported — from secondary summaries of the full text]
  *Caveats:* correlational, single session, one passage, N = 17, ranked rather than scaled outcome; the strong r for "% correct trials" may partly reflect that pianists who already played better produced more correct trials.
- **Hallam et al. (2012)**, "The development of practising strategies in young people", *Psychology of Music* 40(5):652–680, doi:10.1177/0305735612443868. ~3,300 learners: strategy use increased with level; "organisation" and goal-directed strategies were most associated with attainment; ineffective strategies (playing through from the beginning on error) declined with expertise. [reported]
- **Miksza (2007, 2011)** — band students: observed practice behaviours (slowing down, chunking, whole-part-whole) related to gains; frequency of effective strategies was low overall. Miksza (2011) "A review of research on practicing", *Bulletin of the Council for Research in Music Education* 190:51–92. [reported]
- **Chaffin & Imreh (2002)**, "Practicing perfection: Piano performance as expert memory", *Psychological Science* 13(4):342–349, doi:10.1111/1467-9280.00462. Concert pianist **Gabriela Imreh** (note: not Gabriela Montero) recorded 57 h of practice learning Bach's Italian Concerto, Presto. Practice starts and stops clustered at **formal boundaries** and at **performance cues** (structural, expressive, interpretive, basic/technical); she used formal structure as a retrieval scheme and engaged in extended retrieval practice "like expert memorists in other domains". Book: Chaffin, Imreh & Crawford (2002), *Practicing Perfection: Memory and Piano Performance*, Erlbaum. [confirmed]
  *Caveat:* single case, expert, retrospective self-report of cues; later replicated in other single cases (cellist, singer — Chaffin, Lisboa, Logan, Begosh 2010; Ginsborg & Chaffin 2011).

**Design consequence.** The MIDI stream lets the app *detect these behaviours directly*: where stops/restarts occur, whether the learner restarts from bar 1 vs. from the error locus, tempo variation across attempts, whether a session ends on a correct or incorrect attempt, run-length of consecutive correct repetitions before moving on. These are better "practice quality" signals than accuracy scores. [speculative]

---

## 2. Motor learning: schedules, spacing, sleep, mental practice, chunking

### 2.1 Contextual interference (blocked vs. interleaved/random)

- General motor learning: Shea & Morgan (1979), *J Exp Psych: Human Learning & Memory* 5:179–187 — random practice worse in acquisition, better in retention/transfer. Reviews: Magill & Hall (1990); Brady (2004) meta-analysis in *Quest* found the effect smaller and more variable in applied/complex tasks than in lab tasks. Wulf & Shea (2002), *Psychonomic Bulletin & Review* 9(2):185–211: principles from simple skills don't always generalise to complex skills; high-complexity tasks may benefit from more blocked practice early. [reported]
- **Stambaugh (2011)**, "When repetition isn't the best practice strategy: Effects of blocked and random practice schedules", *JRME* 58(4):368–383, doi:10.1177/0022429410385945. 41 beginning clarinet students (school-age), 3 practice sessions + retention. No acquisition differences; **at retention the random group played faster**; no differences in accuracy, evenness or transfer. [confirmed — abstract]
- **Carter & Grahn (2016)**, *Frontiers in Psychology* 7:1251, doi:10.3389/fpsyg.2016.01251. 10 advanced clarinettists; each practised two pieces blocked (12 min each) and two interleaved (3-min chunks). Expert ratings next day: **mixed**; one rater showed a significant interleaving advantage for concerto excerpts, another a marginal one for technical excerpts. Participants also reported preferring/perceiving interleaving positively after the experience. [confirmed]
- **Abushanab & Bishara (2013)**, "Memory and metacognition for piano melodies: Illusory advantages of fixed- over random-order practice", *Memory & Cognition* 41(6):928–937, doi:10.3758/s13421-013-0311-z. 25 piano-trained participants, within-subjects. **Fixed order faster in practice; random order faster at 2-day retention; participants predicted the opposite.** [confirmed — abstract]

- **Mathias & Goldman (2024)**, "How does increasing contextual interference in a musical practice session affect acquisition and retention?", *JRME* 72(4):357–375, doi:10.1177/00224294231222801. 20 advanced violinists; blocked vs. increasing CI (blocked → random) vs. interleaved; expert ratings after sight-reading, immediately after practice and at 24 h. **No differences immediately; at 24 h the blocked condition was rated best**; half the participants judged blocked most effective. [confirmed — abstract-level via search summaries; full text not read] *This is a direct failure to find the CI benefit in skilled musicians performing whole excerpts.*
- **Veniel-Martí, Botella-Nicolás, Omigie & Herrojo-Ruiz (2026)**, "Comparing interleaved and blocked practices in secondary school music performances", *Update: Applications of Research in Music Education*, doi:10.1177/87551233261474481. 60 secondary students (recorder): no difference at post-test; **at 4-week follow-up the interleaved group maintained performance while the blocked group declined significantly.** [confirmed — abstract-level]
- Stambaugh's later work with 19 seventh-graders (blocked vs hybrid vs serial, single 18-min session) found **no main effects** on accuracy or musicality at immediate or 24-h testing. [reported — repository abstract]
- Perceptual/categorical learning: **Wong, Chen & Lim (2021)**, "Learning melodic musical intervals: To block or to interleave?", *Psychology of Music* 49(4):1027–1046, doi:10.1177/0305735620922595 — novices identifying 6 ascending intervals: **interleaving > blocking when no reference songs/singing were used** (Exp. 2), no difference with those aids (Exp. 1); most participants wrongly believed blocking was better. Same group (2020, *JRME*): interleaving > blocking for learning composers' styles. [confirmed — abstract]

**Grade: Weak–Moderate and mixed** for "interleave passages within a session" in performance learning (Stambaugh 2011, Carter & Grahn 2016, Abushanab & Bishara 2013, Veniel-Martí 2026 favour it, mostly on speed or longer-delay retention; Mathias & Goldman 2024 and Stambaugh's 7th-grade study do not). **Moderate** for interleaving in *perceptual category learning* (intervals, styles, chord qualities) — this matches the much stronger category-induction literature (Kornell & Bjork 2008; Brunmair & Richter 2019 meta-analysis, *Psych Bull* 145:1029–1052, g ≈ 0.42 overall, strongest for similar-looking categories [reported]). Wulf & Shea's caveat argues for **blocked practice when a passage is brand new or complex**, then interleaving across passages/days.

### 2.2 Spacing / distributed practice

- Verbal learning: Cepeda, Pashler, Vul, Wixted & Rohrer (2006), *Psychological Bulletin* 132(3):354–380 — robust spacing effect; optimal gap scales with retention interval. [reported]
- Motor: Lee & Genovese (1988) meta-analysis, *Research Quarterly for Exercise and Sport* 59:277–287 — distributed > massed for continuous tasks; Donovan & Radosevich (1999), *J Applied Psychology* 84:795–805 — overall d ≈ 0.46, smaller for complex tasks. [reported]
- Music: **Simmons (2012)**, "Distributed practice and procedural memory consolidation in musicians' skill learning", *JRME* 59(4):357–368, doi:10.1177/0022429411424798 — distributing practice with rest intervals produced better overnight retention of a keyboard sequence in musicians. [reported]
- Duke and colleagues: short rest breaks *within* practice improved learning of a keyboard melody (Simmons, Allen, Cash & Duke, ~2019 "effects of early break intervals"). [reported — via UT Austin lab listing]

**Grade: Moderate–Strong** that spreading practice of the same material over days beats one block; **Weak** for any specific within-session break schedule.

### 2.3 Sleep consolidation

- **Walker, Brakefield, Morgan, Hobson & Stickgold (2002)**, "Practice with sleep makes perfect: Sleep-dependent motor skill learning", *Neuron* 35(1):205–211, doi:10.1016/S0896-6273(02)00746-8 — finger-tapping sequence speed improved ~20% after a night of sleep vs. ~2% across 12 h awake; overnight gain correlated with stage-2 NREM sleep late in the night. [confirmed — abstract & press coverage]
- **Simmons & Duke (2006)**, "Effects of sleep on performance of a keyboard melody", *JRME* 54(3):257–269, doi:10.1177/002242940605400308 — music students learning a short keyboard melody improved accuracy/speed after sleep but not after equivalent waking time. [reported]
- **Critique: Pan & Rickard (2015)**, "Sleep and motor learning: Is there room for consolidation?", *Psychological Bulletin* 141(4):812–834, doi:10.1037/bul0000009. Meta-analysis: much of the "sleep gain" in explicit finger-sequence tasks is explained by confounds (time-of-day, fatigue/reactive inhibition building up during training, averaging artefacts); after controls, sleep-specific enhancement is small or absent. Debate continues (Adi-Japha & Karni 2016 comment; Rickard & Pan 2017 reply, *Psych Bull* 143(4):454–458; **Rickard, Pan & Gupta 2022**, *JEP:LMC* — severe publication bias in the sleep-motor literature). [confirmed — bibliographic & summary level]

**Practical reading:** Next-day performance often *is* better than end-of-session performance, at least partly because end-of-session performance is depressed by fatigue. Either way: **don't judge learning at the end of a session**, and make the "cold, first attempt next day" the canonical measure. Whether sleep *specifically* adds anything is uncertain. **Grade: Strong** for "end-of-session performance underestimates learning"; **Weak/contested** for "sleep-specific consolidation gains".

### 2.4 Mental practice

- **Bernardi, De Buglio, Trimarchi, Chielli & Bricolo (2013)**, "Mental practice promotes motor anticipation: evidence from skilled music performance", *Frontiers in Human Neuroscience* 7:451, doi:10.3389/fnhum.2013.00451. Expert pianists; mental practice (MP) improved performance of difficult sequences, less than physical practice (PP); both produced anticipatory movement patterns; **auditory imagery vividness related to anticipation**, motor imagery to velocity changes. [confirmed]
- **Highben & Palmer (2004)**, "Effects of auditory and motor mental practice in memorized piano performance", *Bulletin of the Council for Research in Music Education* 159:58–65. Pianists learned pieces under conditions removing auditory and/or motor feedback during practice; pianists with **higher aural-skills scores were less hurt by the absence of auditory feedback** — evidence that auditory imagery substitutes for feedback in memory formation. [reported]
- **Bernardi et al. (2013b)**, "Mental practice in music memorization: an ecological-empirical study", *Music Perception* 30(3):275–290 — MP + PP combinations; MP alone allowed some pianists to memorise. [reported]
- General: Driskell, Copper & Moran (1994) meta-analysis, *J Applied Psychology* 79(4):481–492 — mental practice d ≈ 0.53 overall, larger for cognitive than physical tasks; less than physical practice. [reported] A 24-year follow-up/replication (Toth, McNeill, Hayes, Moran & Campbell 2020, *Psychology of Sport and Exercise* 48:101672) over 37 studies (1995–2018) found a **smaller** effect, r ≈ .13, moderated by duration, task type and imagery type. [reported — effect size from search snippet] I found **no music-specific meta-analysis** of mental practice.
- Pascual-Leone et al. (1995), *J Neurophysiology* 74:1037–1045 — mental practice of a 5-finger piano exercise produced similar motor-cortex map changes to physical practice; performance gains smaller. [reported]

**Grade: Strong** that MP < PP but MP > nothing; **Moderate** that MP is most useful *combined* with PP and for skilled/aurally-strong players; **Weak** for beginners specifically.

### 2.5 Slow practice, tempo variation, rhythmic variants

- Slow practice: strongly endorsed by pedagogy; empirical support mostly indirect — Duke et al. (2009) top performers varied tempo; studies on tempo manipulation in practice (e.g., Henley 2001; Miksza 2007) show mixed results. No good RCT shows "slow practice" per se beats practising at target tempo for the same total time, and motor-learning theory (specificity of practice) warns that very slow practice can rehearse a *different* movement (different force/timing/kinematics). [reported/speculative]
- **Rhythmic variants** (dotted, reversed-dotted, groupings): I could not locate any controlled study. The mechanism would be variable practice (Schmidt's schema theory) + forced chunk boundaries + attention to each note. **Evidence: none found / Speculative.**
- Variable practice (schema theory: Schmidt 1975, *Psych Review* 82:225–260): practising variations of a movement class improves generalisation to novel variants; meta-evidence is mixed for adults but positive for children (Van Rossum 1990; Shea & Kohl 1990). [reported]

### 2.6 Chunking and planning

- Sakai, Kitaguchi & Hikosaka (2003), *Experimental Brain Research* 152:229–242 — motor sequences become organised into chunks with characteristic inter-response-time boundaries. [reported]
- Palmer & Drake (1997), *Canadian J Exp Psych* 51:369–384; **Drake & Palmer (2000)**, "Skill acquisition in music performance: relations between planning and temporal control", *Cognition* 74(1):1–32 — with skill, pianists' planning span (eye/memory "look-ahead", measured from serial-ordering errors) grows and errors become more structurally plausible (anticipations dominate over perseverations). **Palmer & Pfordresher (2003)**, *Psychological Review* 110(4):683–712 — range model: planning span ~2–4 events, increasing with skill and slower tempo. [reported]

**Design consequence.** Inter-onset-interval (IOI) discontinuities in MIDI are a *direct* chunk-boundary signal; anticipation vs. perseveration error ratios are a skill/planning signal the app can compute. [speculative]

---

## 3. Feedback

### 3.1 Classic principles

- **Guidance hypothesis** (Salmoni, Schmidt & Walter 1984, *Psychological Bulletin* 95(3):355–386, doi:10.1037/0033-2909.95.3.355): frequent/immediate augmented feedback boosts practice performance but can **reduce learning** measured in no-feedback retention because learners rely on it instead of intrinsic (proprioceptive/auditory) feedback. [reported]
- Reduced-frequency, **faded**, **bandwidth** (feedback only when error exceeds tolerance; Sherwood 1988; Lee, White & Carnahan 1990), **summary** (feedback after N trials; Schmidt, Young, Swinnen & Shapiro 1989) and **delayed/terminal** feedback often equal or beat 100%-frequency feedback at retention. Effects smaller and less consistent than textbooks suggest; summary feedback benefit reverses for very complex tasks (Wulf & Shea 2002). [reported]
- **Concurrent feedback is especially prone to dependence** (Schmidt & Wulf 1997, *Human Factors*; Sigrist, Rauter, Riener & Wolf 2013 review, *Psychonomic Bulletin & Review* 20:21–53, doi:10.3758/s13423-012-0333-8). Sigrist et al. note concurrent *visual* feedback is most dependence-inducing; **concurrent auditory feedback/sonification may avoid it** in some tasks, and the guidance hypothesis is not universal. [reported — via citing sources]
- **KR vs KP**: Knowledge of results (outcome) vs knowledge of performance (movement characteristics). For complex skills, KP that is *prescriptive* tends to help more than descriptive KP; in music, "outcome" is itself auditory and available intrinsically, so augmented feedback is most valuable for things the learner *cannot hear yet* (e.g., velocity unevenness of 5–10 MIDI units, micro-timing). [reported/speculative]

### 3.2 Self-controlled feedback and attentional focus — strong claims, weak evidence

- Wulf & Lewthwaite (2016), OPTIMAL theory, *Psychonomic Bulletin & Review* 23:1382–1414: autonomy (self-controlled practice), enhanced expectancies and external focus enhance learning. [reported]
- **McKay, Yantha, Hussien, Carter & Ste-Marie (2022)**, "Meta-analytic findings of the self-controlled motor learning literature: Underpowered, biased, and lacking evidential value", *Meta-Psychology* 6, doi:10.15626/MP.2021.2803. Naive g = .44 (k = 52, N = 2061), but **only published studies showed a benefit**; after bias correction the effect is small/near zero. Preregistered replications (e.g., Bacelar, Parma, Murrah & Miller 2022; St. Germain et al. 2022) found no self-control benefit. [confirmed — abstract]
- **McKay, Bacelar, Parma, Miller & Carter (2023)**, *Psychonomic Bulletin & Review* — robust Bayesian reanalysis of self-controlled and enhanced-expectancy meta-analyses: "true effects appear small, uncertain, and potentially null"; average statistical power ~6%. [confirmed — abstract]
- **Chua, Jimenez-Diaz, Lewthwaite, Kim & Wulf (2021)**, "Superiority of external attentional focus…", *Psychological Bulletin* 147(6):618–645, doi:10.1037/bul0000335 — external > internal focus. **McKay et al. (2024)** "Reporting bias, not external focus" (robust Bayesian meta-analysis; SportRxiv preprint / later journal version) — after bias correction g ≈ 0.01 (performance), 0.15 (retention), 0.09 (transfer). [confirmed — preprint abstract]

**Implication:** the app should *offer* learner control over feedback (good for autonomy/SDT and harmless) but **should not be designed on the assumption that self-control produces learning gains.** For a pianist, "external focus" maps naturally to *focus on the sound* (an effect of movement) rather than finger mechanics — reasonable but not strongly evidenced.

### 3.3 Augmented visual feedback in music

- **Brandmeyer, Timmers, Sadakata & Desain (2011)**, "Learning expressive percussion performance under different visual feedback conditions", *Psychological Research* 75(2):107–121, doi:10.1007/s00426-010-0291-6. Conservatory percussion students imitated teacher recordings with (a) **high-level** real-time feedback on expressive style (Bayesian model-based), (b) **low-level** real-time feedback on raw timing/dynamics, or (c) none. **Neither feedback form reduced timing or dynamics errors**; high-level feedback improved imitation of expressive *style*; authors note real-time visual feedback may be **disruptive to timing via extraneous cognitive load**. [confirmed — abstract read]
- Singing: Welch (1985), *Psychology of Music* 13(1):3–18 schema model; Welch, Howard & Rush (1989) — real-time visual pitch displays helped children's pitch matching; Hoppe, Sadakata & Desain (2006), *J Computer Assisted Learning* 22:308–316 review of real-time visual feedback in singing — benefits common in short-term studies, transfer/retention without display less studied. [reported]
- Sadakata, Hoppe, Brandmeyer, Timmers & Desain (2008), "Real-time visual feedback for learning to perform short rhythms with expressive variations in timing and loudness", *J New Music Research* 37(3):207–220 — modest benefits; learners differed in whether visual feedback helped. [reported]
- Augmented-piano prototypes: Deja et al. (2022) survey, arXiv:2208.09929 ("A survey of augmented piano prototypes: has augmentation improved learning experiences?") — most systems (falling-note/light-up keys) evaluated on immediate performance or usability, rarely on retention without the augmentation. [reported — title/abstract seen in search]
- **Hsieh, Visser, Eisemann & Marroquim (2026)**, "Skill-adaptive ghost instructors: Enhancing retention and reducing over-reliance in VR piano learning", CHI 2026, arXiv:2603.06253, doi:10.1145/3772318.3791437. Within-subjects N = 30; a ghost hand showing fingerings with **fixed** vs **performance-adaptive (fading)** transparency; tested *without guidance* immediately and after 10 min: adaptive fading → higher pitch and fingering accuracy, comparable timing. [confirmed — abstract] Very short retention interval, but it is direct piano-specific support for the "fade the guidance" principle.

**Grade: Moderate** for "concurrent visual feedback can impair timing and create dependence; prefer post-hoc views". **Strong** that most piano-tech evaluations don't test retention without the aid — so vendor claims are uninformative.

---

## 4. Auditory imagery, audiation, sight-reading, memorisation

### 4.1 Audiation / notational audiation

- Gordon's "audiation" (Gordon 1980/2012, *Learning Sequences in Music*, GIA): hearing and comprehending music not physically present. Influential, but much of the supporting research is Gordon's own aptitude-test programme; the Music Learning Theory sequence has little controlled outcome evidence. [reported]
- **Brodsky, Henik, Rubinstein & Zorman (2003)**, "Auditory imagery from musical notation in expert musicians", *Perception & Psychophysics* 65(4):602–612, doi:10.3758/BF03194586. Expert musicians silently read scores containing well-known themes embedded in embellished variations, then judged whether a heard tune was the embedded theme. **Phonatory interference (humming) impaired recognition more than rhythmic or auditory interference** → notational audiation involves covert vocal (kinaesthetic-phonatory) processes. [confirmed — abstract] The authors also report that a substantial fraction of trained musicians did *not* reliably pass the task, i.e., audiation from notation is not automatic even in professionals. [reported — exact proportion not verified]
- Brodsky et al. (2008), *JEP:HPP* 34(2):427–445 — follow-up with larynx EMG: covert vocal-fold activity during notational audiation. [reported]

### 4.2 Sight-reading

- **Mishra (2014)**, "Improving sight-reading accuracy: A meta-analysis", *Psychology of Music* 42(2):131–156, doi:10.1177/0305735612463770. 92 quasi-experimental studies. **Overall treatment effect small (d ≈ 0.18)**; only treatment type moderated; **aural training, controlled reading, creative activities (improvisation/composition) and singing/solfège** had significant positive effects. Control groups also improved substantially (pre-post d ≈ 0.48) — sight-reading improves with general exposure. [confirmed — abstract]
- Mishra (2014b), "Factors related to sight-reading accuracy: A meta-analysis", *JRME* 61(4):452–465: strongest correlates include **improvisation ability, technique, ear-playing, music reading experience**; weak relation to general IQ. [reported]
- **Kopiez & Lee (2006)**, *Music Education Research* 8(1):97–120 ("Towards a dynamic model of skills involved in sight reading music") and **Kopiez & Lee (2008)**, "Towards a general model of skills involved in sight reading music", *Music Education Research* 10(1):41–62, doi:10.1080/14613800701871363. 52 piano students; best predictors: **trilling speed, sight-reading experience before age 15, speed of information processing, and inner hearing (auditory imagery)** — together ~60% of variance. [confirmed — abstract]
- **Lehmann & Ericsson (1996)**, "Performance without preparation: Structure and acquisition of expert sight-reading and accompanying performance", *Psychomusicology* 15:1–29 — accompanying/sight-reading experience (hours spent accompanying) predicted sight-reading better than total practice; sight-reading is a partially separate skill needing its own practice. [reported]
- Eye–hand span: Sloboda (1974, 1977); **Furneaux & Land (1999)**, *Proc R Soc B* 266:2435–2440 — eye–hand span ~1 s in time; in notes it grows with skill (~4 notes experts vs ~2 novices). Reviews: Puurtinen (2018), *J Eye Movement Research* 11(2); Perra, Poulin-Charronnat, Baccino & Drai-Zerbib (2021/2022), "Review on eye-hand span in sight-reading of music", *J Eye Movement Research*. Experts fixate fewer, more structurally informative places (chunking). [reported]
- Sight-reading and pattern recognition: Waters, Underwood & Findlay (1997), *Perception & Psychophysics* 59(4):477–488 — skilled readers encode note groups (chunks) faster. [reported]

### 4.3 Memorisation

- **Chaffin & Imreh (2002)** — see §1.2. Performance-cue model: structural, expressive, interpretive and basic cues are rehearsed until they become retrieval points; during performance the pianist can recover from errors by jumping to the next cue. [confirmed]
- **Ginsborg (2002)** (singers; memorising words+music concurrently best); **Ginsborg & Chaffin (2011)**, *Psychology of Music* 39(2):137–158 — singer and pianist: performance cues shared in rehearsal. [reported]
- **Mishra (2005)**, "A theoretical model of musical memorization", *Psychomusicology* 19(1):75–89; Mishra (2010) on memorisation strategies (serial, segmented, holistic) — mixed findings, considerable individual differences. [reported]
- Analysis → memory, older experiments: Rubin-Rabson (1937–1941) found that **studying the score away from the keyboard before practice (analytic pre-study)** reduced trials to memorise in pianists. Hallam (1997) interviews: professionals report multiple memory types (aural, visual, kinaesthetic, analytic); novices rely heavily on kinaesthetic (motor) memory, which is the most fragile under stress. [reported]
- Lisboa, Chaffin & Logan (2011) and later work: memory failures under stress are typically recovered at *structural landmarks*. [reported]

**Grade: Moderate** for "build explicit, multi-modal memory (structural map + aural + motor) rather than relying only on motor memory". Causal evidence that *analysis instruction* improves memory in amateurs is thin and old (Rubin-Rabson) — treat as plausible.

---

## 5. Ear training, harmonic perception and perceptual learning

### 5.1 Implicit knowledge in non-musicians

- **Bigand & Poulin-Charronnat (2006)**, "Are we 'experienced listeners'? A review of the musical capacities that do not depend on formal musical training", *Cognition* 100(1):100–130, doi:10.1016/j.cognition.2005.11.007 — non-musicians show many of the same implicit sensitivities as musicians (harmonic priming, tension/relaxation, cadence completion); differences are smaller than expected and mostly in *explicit* labelling. [reported]
- **Tillmann, Bharucha & Bigand (2000)**, "Implicit learning of tonality: A self-organizing approach", *Psychological Review* 107(4):885–913 — self-organising network learns tonal hierarchies from exposure. [reported]
- Harmonic priming: Bharucha & Stoeckig (1986); Bigand & Pineau (1997); Tillmann et al. — target chords processed faster when functionally expected (e.g., tonic after dominant context), even in non-musicians. [reported]
- Krumhansl & Kessler (1982), *Psych Review* 89:334–368 — key profiles. [reported]

**Implication:** The learner already has implicit tonal expectations. Ear training should **attach labels to existing implicit categories** (scale-degree function, tension) rather than drill context-free acoustic categories. [speculative but well-motivated]

### 5.2 Interval vs. functional (scale-degree) training; transfer

- Interval identification is notoriously **context-dependent**: musicians identify intervals more poorly in tonal context or as harmonic dyads than in isolation, and interval training has limited transfer to melodic dictation. Karpinski (2000), *Aural Skills Acquisition* (OUP), argues for scale-degree/functional hearing as the core skill for dictation; empirical support mainly from classroom studies. [reported]
- **Little, Cheng & Wright (2019)**, "Inducing musical-interval learning by combining task practice with periods of stimulus exposure alone", *Attention, Perception & Psychophysics* 81:344–357 (PMC6384134) — listeners practised picking which of two intervals was a perfect 4th; **active practice blocks combined with blocks of passive background exposure** to the trained interval (while doing an unrelated visual task) produced the best learning; generalisation to an untrained timbre was tested but I did not verify that result. [confirmed — design/abstract] *Design hint: passive exposure to target sounds between active drills is cheap and may help.*
- **Nichols & Springer (2025)**, "Piano history, aural skills, and working memory predict melodic dictation performance", *Frontiers in Psychology* (PMC12341474). N = 34 music majors; tonal working memory (R² ≈ .15), **years of piano lessons** (β ≈ .41) and aural-skills semesters predicted dictation; **self-reported auditory imagery vividness/control did not** (r ≈ .14, ≈ .00). [confirmed — full text summary] Small, correlational, but a useful counterweight to over-claiming "imagery" — questionnaire imagery ≠ task-based imagery.
- Perceptual learning generally is **stimulus- and task-specific** (Wright & Zhang 2009 on auditory perceptual learning; Amitay et al.). Expect training on piano-timbre root-position triads to transfer imperfectly to inversions, other timbres, and progressions in context. [reported]
- Categorical perception of intervals: Burns & Ward (1978), *JASA* 63:456–468 — trained musicians perceive intervals categorically with category widths ~1 semitone; non-musicians do not. Siegel & Siegel (1977). Categories are learned. [reported]

### 5.3 Absolute vs relative pitch in adults

- **Van Hedger, Heald & Nusbaum (2019)**, "Absolute pitch can be learned by some adults", *PLoS ONE* 14(9):e0223047, doi:10.1371/journal.pone.0223047. ~8 weeks of training (~32 h); **the best learner passed all AP criteria** and retained ability ≥4 months; **most participants showed only modest improvements**. Small sample. [confirmed — abstract]
- **Wong, Lui, Yip & Wong (2020)**, "Is it impossible to acquire absolute pitch in adulthood?", *Attention, Perception & Psychophysics* 82(3):1407–1430, doi:10.3758/s13414-019-01869-3. Three experiments, 12–40 h gamified training, 3 → 12 pitch classes; **6/43 (14%)** reached ≥90% accuracy on 12 pitches (semitone errors counted wrong). Follow-up work by the same group (2024–25, *Psychonomic Bulletin & Review*) continues to argue AP is not strictly critical-period-bound, while noting methodological open questions. [confirmed — abstract/summary]

**Implication:** AP training is a low-yield, high-cost investment for this user; **relative-pitch, scale-degree hearing** is more directly useful for harmony, improvisation and dictation. An optional AP "reference tone" practice could be an n-of-1 experiment but should not be core. **Grade: Moderate.**

---

## 6. Expertise and perception

- **Halpern & Bower (1982)**, "Musical expertise and melodic structure in memory for musical notation", *American Journal of Psychology* 95(1):31–50 — musicians recalled briefly-presented notation of "good" (structured) melodies better than "bad" ones, nonmusicians did not differ; the musician advantage **shrank from good → bad → random** melodies; musicians used musical groupings (chunks), nonmusicians a simple visual strategy — the musical analogue of Chase & Simon's chess chunks. [confirmed — abstract]
- **Sloboda (1976, 1984)**: skilled sight-readers "proof-read" errors in scores (fail to notice misprints that are musically plausible) → reading is driven by expectations/schemas. [reported]
- **Drake & Palmer (2000)**; Palmer (1997) "Music performance", *Annual Review of Psychology* 48:115–138 — expert pianists' representations are hierarchical (phrase structure governs timing/dynamics; errors are structurally constrained). [reported]
- **Lehmann & Ericsson (1997)** "Research on expert performance and deliberate practice: implications for the education of amateur musicians and music students", *Psychomusicology* 16:40–58 — experts build three representations: of the **goal** (desired sound), of **current performance**, and of **how to produce** it; practice aims to refine all three. [reported]
- Theory → performance transfer: Correlational evidence that harmony/theory knowledge relates to sight-reading and memory (Mishra 2014b; Kopiez & Lee's "inner hearing"); **little causal evidence** that classroom theory instruction improves performance. A plausible reading: theory helps when it *changes what is perceived/chunked*, not as declarative knowledge alone. [reported/speculative]

---

## 7. Improvisation

- **Pressing (1988)**, "Improvisation: methods and models", in J. Sloboda (Ed.), *Generative Processes in Music*, OUP, pp. 129–178 — improvisation as a sequence of event clusters generated from a **referent** (tune/form), a **knowledge base** (stored patterns, rules), with continuous choice between continuation-by-association and interruption; expertise reduces cognitive load via automated motor programmes. Pressing (1998), "Psychological constraints on improvisational expertise and communication", in Nettl & Russell (Eds.), *In the Course of Performance*, Chicago UP. [reported]
- **Berliner (1994)**, *Thinking in Jazz: The Infinite Art of Improvisation*, U Chicago Press — ethnography of ~50 jazz musicians: learning through **transcription/imitation of recordings, learning tunes by ear, a vocabulary of licks that is then varied, transposed and recombined**, and aural absorption of the idiom. [reported]
- **Norgaard (2011)**, "Descriptions of improvisational thinking by artist-level jazz musicians", *JRME* 59(2):109–127, doi:10.1177/0022429411405669 — 7 artist-level musicians improvised over a blues with drums only, then described their thinking while listening to the recording and viewing notation. They made **"sketch plans"** of upcoming features that became more explicit as the moment approached; **continuously evaluated** their output, feeding later plans; were sometimes **surprised** by what they played. Four note-generation strategies were identified, the first being **recalling and inserting well-learned ideas from memory** [confirmed — abstract]; the others (from my background knowledge of the paper) are choosing notes from **harmonic priority** (chord/scale), **melodic priority** (developing previous material), and occasionally free choice. [reported]
- **Norgaard (2014)**, "How jazz musicians improvise: The central role of auditory and motor patterns", *Music Perception* 31(3):271–287, doi:10.1525/mp.2014.31.3.271 — 48 Charlie Parker solos: **most notes begin a recurring four-interval pattern**; patterns up to 49 intervals; supports pattern insertion alongside rule-based generation. Norgaard, Bales & Hansen (2023), *Cognition* — one pianist's MIDI-like data (velocity, microtiming) extends this. [confirmed — abstract]
- **Biasutti (2015)**, "Pedagogical applications of cognitive research on musical improvisation", *Frontiers in Psychology* 6:614, doi:10.3389/fpsyg.2015.00614 — process-oriented model (anticipation, use of repertoire, emotive communication, feedback, flow) with reflection/metacognition. Biasutti & Frezza (2009), *Creativity Research Journal* 21(2–3):232–242 — five dimensions rated by improvisers. [confirmed]
- Neuroscience: Limb & Braun (2008), *PLoS ONE* 3(2):e1679 — pianists improvising showed DLPFC deactivation & medial PFC activation (N = 6, fMRI, small); Beaty (2015), *Neuroscience & Biobehavioral Reviews* — review: control and generative networks both involved; expertise changes the balance. [reported]
- Improvisation and other skills: Mishra (2014b) — improvisation ability correlates with sight-reading; Norgaard, Stambaugh & McCranie (2019), *JRME* — jazz improvisation instruction and executive function in middle-school students (small effects). [reported]
- **Adult learners:** I found no controlled trials of improvisation pedagogy specifically for adult beginner pianists. [confirmed absence in my searches; not exhaustive]

**Implication:** a progression **imitate → vary → recombine → generate under constraint** fits both Berliner's ethnography and Norgaard's corpus/pattern evidence. Evidence grade **Moderate** (descriptive), **Weak** for pedagogy outcomes.

---

## 8. Adult learners: motivation, plateaus, desirable difficulties, illusions of competence

- **Self-determination theory** in music: Evans (2015), "Self-determination theory: An approach to motivation in music education", *Musicae Scientiae* 19(1):65–83; Evans, McPherson & Davidson (2013), *Psychology of Music* 41(5):600–619 — thwarted needs for **competence, autonomy, relatedness** predicted ceasing music. [reported]
- Adult piano learners: Jutras (2006), "The benefits of adult piano study as self-reported by selected adult piano students", *JRME* 54(2):97–110 — personal benefits (skill, fulfilment, accomplishment) ranked highest; Roulston, Jutras & Kim (2015) on adult beginners' challenges (time, self-criticism, plateaus). [reported]
- **Desirable difficulties**: Bjork (1994); Bjork & Bjork (2011) in *Psychology and the Real World*; **Soderstrom & Bjork (2015)**, "Learning versus performance: An integrative review", *Perspectives on Psychological Science* 10(2):176–199, doi:10.1177/1745691615569000 — practice performance is an unreliable index of learning; spacing, interleaving, variation, reduced feedback and testing degrade practice performance but improve retention/transfer. [reported]
- **Illusions of competence / fluency**: Abushanab & Bishara (2013) for piano (see §2.1); Kornell & Bjork (2008), *Psychological Science* 19:585–592 — learners prefer massed but learn better interleaved. Watching expert performance or tutorials produces a strong *feeling of knowing* without motor capacity — **Kardas & O'Brien (2018)**, "Easier seen than done: Merely watching others perform can foster an illusion of skill acquisition", *Psychological Science* 29(4):521–536, doi:10.1177/0956797617740646: 6 experiments, N = 2,225; repeated watching (darts, moonwalk, a game) raised predicted ability but not actual performance; viewers learn *what steps* to take but not *how they feel*; briefly handling the object (e.g., holding juggling pins) tempered the illusion. [confirmed — abstract]
- **Retrieval practice / testing effect**: Roediger & Karpicke (2006); Rowland (2014) meta-analysis, *Psych Bull* 140:1432–1463 (g ≈ 0.50). Mostly verbal materials; music applications sparse. The only direct musical test I found is **Telesco et al. (2021)**, "Does retrieval practice enhance memorization of piano melodies?", *College Music Symposium* 61(2), doi:10.18177/sym.2021.61.sr.11525 — conditions such as playing from the score 10× vs 5× from score + 5× from memory vs alternating; the authors note no prior systematic studies existed; **I could not access the results**. [confirmed existence/design; results unknown] Using SRS for chord voicings/progressions is plausible for declarative/procedural *recall* (can you play ii–V–I in A♭ with rootless voicings from memory?) but untested. [speculative]
- **Practice amount realities:** Adult amateurs typically practise far less than conservatory students (often 30–60 min/day or less, irregular); age-related declines in motor speed and memory are real but modest relative to practice effects; older pianists maintain skill via deliberate practice (Krampe & Ericsson 1996, *JEP: General* 125(4):331–359 — older experts maintained music-specific speed with continued deliberate practice). [reported]
- Plateaus: Little direct music research; the motor-skill learning curve is approximately a power/exponential law with apparent plateaus often reflecting strategy shifts or measurement insensitivity (Gray & Lindstedt 2017 on plateaus and dips). [reported]

---

## 9. Embodied / sensorimotor coupling

- **Bangert & Altenmüller (2003)**, "Mapping perception to action in piano practice: a longitudinal DC-EEG study", *BMC Neuroscience* 4:26, doi:10.1186/1471-2202-4-26. Beginners trained by ear (no notation) over 10 × 20-min sessions in 5 weeks; "map" group (normal key–pitch mapping, N = 9) vs "no-map" group (randomised key–pitch assignment, N = 8). **Auditory–sensorimotor co-activation appeared within the first 20 min** and grew over 5 weeks; right anterior activity specific to the map group. [confirmed — abstract]
- **Bangert, Peschel, Schlaug et al. (2006)**, *NeuroImage* 30(3):917–926 — shared networks for auditory and motor processing in professional pianists (listening activates motor areas; silent playing activates auditory areas). [reported]
- **Lahav, Saltzman & Schlaug (2007)**, "Action representation of sound: Audiomotor recognition network while listening to newly acquired actions", *Journal of Neuroscience* 27(2):308–314, doi:10.1523/JNEUROSCI.4822-06.2007. Non-musicians learned to play a short piece by ear on a keyboard; fMRI: listening to the **trained** piece activated a frontoparietal motor-related network, whereas an untrained piece made of the **same notes in a different order** did not. [confirmed — design summary from citing sources; training schedule and exact regions not verified]
- **de Manzano, Kuckelkorn, Ström & Ullén (2020)**, "Action-perception coupling and near transfer: Listening to melodies after piano practice triggers sequence-specific representations in the auditory-motor network", *Cerebral Cortex* 30(10):5193–5203, doi:10.1093/cercor/bhaa018 — after non-musicians learned two melodies on piano, MVPA could decode the *specific* trained melodies from both auditory and motor regions during listening; training-dependent (control experiment). [confirmed — abstract]
- Haueisen & Knösche (2001), *J Cognitive Neuroscience* 13(6):786–792 — pianists listening to piano music show motor-cortex activation, finger-specific. Drost, Rieger, Brass, Gunter & Prinz (2005) — pianists show interference when heard notes mismatch the key pressed (automatic audio-motor binding). [reported]
- Novembre & Keller (2014), *Frontiers in Human Neuroscience* 8:603 — review of action–perception coupling in music performance. [reported]
- Pfordresher (2006, 2012): altered auditory feedback studies — **asynchronous feedback disrupts timing**, **altered pitch content disrupts sequencing**; implying that audio latency in an app must be very low (<~20–30 ms) and pitch feedback must be faithful. [reported]

**Implication:** Every keyboard interaction should produce correct, low-latency sound; "play-by-ear" and "predict-then-hear" tasks exploit the fast-forming audio-motor map. Silent ("dumb keyboard") practice is a *mental practice* variant (useful, but different). **Grade: Moderate** (neuroimaging small-N, but consistent; behavioural pay-off for learning not directly shown).

---

## 10. Design implications (evidence-graded)

Grades: **Strong** = meta-analytic or repeatedly replicated, including in musical/motor tasks; **Moderate** = consistent direction across several small studies, or strong in adjacent domains with plausible transfer; **Weak** = one or two small studies, or contested; **Speculative** = mechanism-based inference.

| # | Principle | Grade | Main support | Caveats |
|---|---|---|---|---|
| P1 | **Measure learning with delayed, cold, unassisted probes** (first attempt next session, no visual aid), not end-of-session accuracy. | **Strong** | Soderstrom & Bjork 2015; Salmoni et al. 1984; Abushanab & Bishara 2013; Pan & Rickard 2015 (fatigue depresses end-of-session) | Cold probes are noisy for a single take; need several probes/passages. |
| P2 | **Make practice *behaviour* the primary analytics object** (error localisation, restart point, tempo variation, consecutive-correct run length before moving on), not hours or a % score. | **Moderate** | Duke et al. 2009; Hallam et al. 2012; Miksza 2011; Macnamara 2014 (hours explain modest variance) | Duke: N = 17, correlational, one passage. Behaviours could be markers rather than causes. |
| P3 | **Default to terminal, summary feedback** (after a take or after N takes), with **bandwidth** (only show deviations beyond tolerance). Concurrent visual displays off by default. | **Moderate** | Salmoni et al. 1984; Sigrist et al. 2013; Brandmeyer et al. 2011 (real-time visual didn't reduce timing errors; load) | Guidance hypothesis less clear for complex skills and for *auditory* concurrent feedback; early in learning, more feedback may help. |
| P4 | **Fade augmented feedback/guidance** within and across sessions (performance-contingent), and schedule periodic "no-display" takes. | **Moderate** | Guidance hypothesis literature; Winstein & Schmidt 1990 (faded KR); Hsieh et al. 2026 (adaptive-fading ghost hand > fixed, VR piano, N = 30) | Mostly simple lab tasks; piano study had a 10-min retention interval. |
| P5 | **Prefer feedback about what the learner cannot yet hear** (micro-timing, velocity evenness, pedal timing) and present it as *audio contrast* (e.g., "your take vs. quantised/smoothed take" A/B) rather than numbers. | **Speculative–Moderate** | Brandmeyer 2011 (high-level > low-level for style); Sigrist 2013 (auditory feedback less dependence-prone); Lehmann & Ericsson 1997 (goal representation) | A/B audio contrast as a feedback form is not directly tested. |
| P6 | **Interleave passages/pieces once each is minimally playable; block when brand new — and treat the schedule as a per-user experiment.** | **Weak–Moderate (mixed)** for performance; **Moderate** for perceptual categories (intervals, chord qualities, styles) | For: Stambaugh 2011; Carter & Grahn 2016; Abushanab & Bishara 2013; Veniel-Martí et al. 2026; Wong et al. 2021 (intervals). Against: Mathias & Goldman 2024 (blocked best at 24 h, advanced violinists) | Small Ns; benefits mostly speed or long-delay; complex passages may need blocking (Wulf & Shea 2002). |
| P7 | **Space practice of each passage across days**; schedule passages for revisit based on cold-probe performance. | **Strong (general) / Moderate (music)** | Cepeda et al. 2006; Donovan & Radosevich 1999; Simmons 2012 | Optimal gaps for motor-musical material unknown. |
| P8 | **Don't over-claim sleep**; but do end sessions on a correct, stable rendition and re-test next day. | **Weak** (sleep-specific) / **Moderate** (end on correct) | Walker 2002 vs Pan & Rickard 2015; Duke 2009 | — |
| P9 | **Train inner hearing explicitly** (sing/imagine before playing; audiation checks from notation). | **Moderate** | Kopiez & Lee 2008; Mishra 2014; Highben & Palmer 2004; Bernardi 2013; Brodsky 2003 | Mostly correlational; Mishra effect sizes small; self-report imagery did not predict dictation in Nichols & Springer 2025 — measure imagery with *tasks*, not questionnaires. |
| P10 | **Ear training should be functional and in-context** (scale degrees, chord function within progressions, voicings in piano timbre, then varied timbres), not isolated intervals only. | **Moderate** | Bigand & Poulin-Charronnat 2006; perceptual-learning specificity; Karpinski 2000 | Few RCTs comparing functional vs interval training. |
| P11 | **Treat AP training as optional/experimental**; core is relative pitch. | **Moderate** | Van Hedger 2019; Wong 2020 (14% success after 12–40 h) | — |
| P12 | **Support a structural "map" of each piece** (sections, cadences, harmonic landmarks) and let the learner mark **performance cues**; practise starting from any cue. | **Moderate** | Chaffin & Imreh 2002; Ginsborg & Chaffin 2011; Hallam 1997 | Expert case studies; causal benefit for novices weakly tested. |
| P13 | **Pair every visual/notational representation with sound and key action**; minimise audio latency (< ~20 ms target). | **Moderate** | Bangert & Altenmüller 2003; Lahav 2007; Pfordresher altered-feedback work | Neuro evidence ≠ learning outcome evidence. |
| P14 | **Build improvisation as imitate → vary → recombine → generate**, with stored vocabulary explicitly managed. | **Moderate** (descriptive) / **Weak** (pedagogy outcome) | Berliner 1994; Pressing 1988; Norgaard 2011, 2014; Biasutti 2015 | Mostly expert descriptions; no adult-learner trials. |
| P15 | **Offer learner control** (choose when to get feedback, which passage next), but for autonomy/motivation, not as a learning-efficiency claim. | **Moderate** (SDT motivation) / **Weak** (learning) | Evans 2015; McKay et al. 2022, 2023 | Self-control learning benefit likely near zero. |
| P16 | **Make the learning/performance gap visible to the learner** (show that interleaved/spaced items were "worse yesterday, better today"), to counter metacognitive illusions. | **Speculative** | Abushanab & Bishara 2013; Kornell & Bjork 2008; Soderstrom & Bjork 2015 | Untested whether showing this changes behaviour. |
| P17 | **Discount "watching" (videos, falling notes, demonstrations) as practice**; require a production attempt after each demonstration. | **Moderate** | Kardas & O'Brien 2018; general retrieval-practice literature | Observational learning *does* help some motor learning (modelling); Cash et al. 2014 on hearing a model before practice — mixed. |
| P18 | **Use retrieval (produce from memory) for harmonic vocabulary** — voicings, progressions in all keys — on an expanding spacing schedule. | **Moderate** (verbal) / **Speculative** (music) | Rowland 2014; Cepeda 2006 | Retrieval of motor-harmonic patterns untested; scheduling via SRS may need motor-specific intervals. |
| P19 | **Practise sight-reading as its own skill**, at a level slightly below current playing level, with forced continuity (keep going). | **Moderate** | Lehmann & Ericsson 1996; Kopiez & Lee 2008; Mishra 2014 | — |
| P20 | **Avoid aggregate "accuracy %"**; present *distributions* and *specific events* (which note, which beat, which voice). | **Speculative** (but consistent with P2–P5 and the user's anti-goals) | — | — |

---

## 11. Feature ideas grounded in the evidence, each with an n-of-1 evaluation design

General n-of-1 method for all ideas below [speculative design]:
- Use **alternating-treatment / multiple-baseline designs**: split comparable material (e.g., 8 four-bar passages of similar difficulty from the same piece or style) randomly between condition A and B; practise each with a fixed time budget; measure on **cold next-day and 7-day probes**.
- Outcome metrics derived from MIDI: note-level error count vs. score (via alignment, e.g., DTW/HMM score follower), IOI coefficient of variation relative to an expressive target, velocity SD within voice, number of stops/hesitations (> 1.5× local IOI), and time-to-criterion (attempts until 3 consecutive clean takes).
- Pre-register the comparison in a local note (hypothesis, metric, window) before starting; analyse with randomisation tests or a Bayesian hierarchical model over passages; expect only *large* effects to be detectable in a few weeks.

### Idea 1 — Audiation-first loop ("hear it, then play it")
**Mechanism:** Before each attempt, the learner sings/imagines the passage from notation (app silent), then plays; app then plays the score audio for comparison. Trains notational audiation and the "goal representation" (Lehmann & Ericsson 1997; Brodsky 2003; Kopiez & Lee 2008; Bernardi 2013 for imagery→anticipation).
**Variant:** occasional "audiation check" — app plays a version with one altered note/rhythm; learner says whether it matches the score (Brodsky-style embedded-melody paradigm).
**n-of-1:** Passages randomised to audiation-first vs. play-first with equal time. Outcomes: cold-probe errors and hesitation count; secondary: audiation-check accuracy over weeks.

### Idea 2 — Interleaved & spaced passage scheduler with a cold-probe gate
**Mechanism:** contextual interference + spacing + "test, don't assume" (Stambaugh 2011; Carter & Grahn 2016; Cepeda 2006). The app picks the next passage based on its last cold-probe result (Leitner-style queue for *passages*), blocking only for new material until a "minimally playable" criterion (e.g., 2 clean takes at 60% tempo) is reached.
**n-of-1:** Alternating weeks of "scheduler on" vs "free practice", or passage-level randomisation; outcome = 7-day retention per passage; also log learner's *predicted* retention to quantify their own Abushanab-type illusion. Because Mathias & Goldman (2024) found the opposite of the CI effect in skilled violinists, the scheduler should expose its interleave/block ratio as a parameter and the app should *estimate* which ratio works for this user rather than hard-code interleaving.

### Idea 3 — Error-locus coach (Duke behaviours, detected not imposed)
**Mechanism:** Detects when the learner restarts from the beginning after an error rather than from the error locus; suggests a minimal loop window around the error (e.g., from the previous beat to one beat after), with a target of N consecutive correct reps before widening; tracks whether sessions end on a correct take (Duke et al. 2009).
**n-of-1:** For half the passages the coach is active; compare time-to-criterion and next-day cold performance. Also measure whether the learner's own unprompted behaviour shifts (fading of the coach).

### Idea 4 — Faded, bandwidth, terminal feedback with "blind takes"
**Mechanism:** Guidance hypothesis. Feedback appears only after a take, only for deviations beyond a bandwidth (e.g., IOI deviation > 15% from the learner's own intended tempo map, velocity outliers > 2 SD within a voice), and the bandwidth widens/frequency drops as the passage stabilises. Every k-th take is a "blind take" with no feedback, used as the learning signal.
**n-of-1:** Randomise passages to "100% immediate visual feedback" vs "faded bandwidth terminal feedback"; compare blind-take and next-day metrics. Expect A to look better *during* practice and B to be ≥ at retention — that pattern is itself the test.

### Idea 5 — Audio A/B feedback instead of graphs ("hear your deviation")
**Mechanism:** Learner hears their take, then a version with only one dimension corrected (e.g., velocities of the melody voice equalised to their mean, or onsets realigned to intended rubato curve, or pedal changed at the harmonic boundary). Keeps attention on sound (external, effect-related focus; Sigrist 2013 on auditory modality), trains the perceptual discrimination needed to self-monitor, and avoids visual dependence.
**n-of-1:** Compare A/B audio feedback vs a numeric/graphic display of the same deviation on matched passages; outcome = unaided reduction of that specific deviation on cold probes, and a perceptual discrimination test (can the learner detect a 10% voicing imbalance?).

### Idea 6 — Functional ear-training in the learner's own repertoire
**Mechanism:** Ear training items drawn from passages being studied (Moonlight Sonata's C♯ minor progressions, Clair de lune's D♭ voicings): "what scale degree is the top note?", "is the next chord V or vii°/V?", "which voice moved?" — trained in piano timbre and then transposed and re-voiced to promote transfer (perceptual learning specificity; Bigand 2006; Karpinski 2000).
**n-of-1:** Train a subset of harmonic categories (e.g., cadential 6/4, Neapolitan) and leave matched categories untrained; test identification in *new* pieces and in transposition. Transfer gap = trained-in-repertoire minus novel-context accuracy.

### Idea 7 — Structure map + cue-based starts (memory by landmarks)
**Mechanism:** Learner annotates sections, harmonic landmarks and performance cues (Chaffin & Imreh 2002). Practice mode "start anywhere": the app names a cue (e.g., "return of the theme in E major", "bar 32 pedal change") and the learner must start there from memory. Builds retrieval cues that allow recovery after slips.
**n-of-1:** Two pieces/sections of comparable difficulty memorised with vs without cue-start drills; outcomes: recovery time after an induced interruption (app stops the learner at random points and asks to resume), memory-performance errors 1 and 4 weeks later.

### Idea 8 — Predict-then-hear (audio–motor prediction training)
**Mechanism:** Before pressing, learner predicts the sound (sings it); or app plays a melody and learner reproduces it by ear; or app shows a keyboard shape and learner predicts the chord quality before hearing it. Exploits fast-forming audio-motor mapping (Bangert & Altenmüller 2003; Lahav 2007) and play-by-ear's association with reading/improvising skill (Mishra 2014b; McPherson 1995/2005 on playing by ear).
**n-of-1:** Weekly "play-by-ear" probe on novel 4–8-note melodies and chord progressions (first-attempt accuracy, attempts to criterion); compare slopes during weeks with vs without daily 5-min predict-then-hear blocks (ABAB design).

### Idea 9 — Improvisation vocabulary SRS with transformation drills
**Mechanism:** Learner stores licks/voicings (captured from MIDI, tagged by harmonic function). Review is not "replay the lick" but "**produce it over a new chord / key / rhythmic displacement**" (Berliner's transposition and variation practice; Norgaard 2014's pattern evidence; retrieval practice). Spacing by expanding interval, with item difficulty updated from production quality.
**n-of-1:** Half of a new vocabulary set enters the SRS with transformation drills, half is practised in a weekly block; measure (a) recall-in-all-keys at 2 and 6 weeks, (b) *spontaneous use* in free improvisation over a backing track (automatic pattern-matching of stored items in improvisation MIDI — usage rate and appropriate-context rate).

### Idea 10 — Variable-practice generator (tempo, rhythm, articulation, dynamic variants)
**Mechanism:** Schema theory / variable practice; Duke's tempo variation; forced chunk boundaries. The app proposes variants (dotted rhythms, accent shifted, staccato, hands separate, transposed for patterns) with the explicit caveat that rhythmic-variant practice is **untested**.
**n-of-1:** This is the cleanest candidate for a genuine contribution: randomise passages to "variants" vs "same-time, normal-rhythm slow→fast" practice; outcomes: cold-probe IOI evenness and error count at target tempo.

### Idea 11 — Metacognitive calibration journal
**Mechanism:** Before each cold probe, learner predicts their performance (e.g., errors expected, 1–5 confidence). The app plots predicted vs actual over time and by practice condition — making the learning–performance distinction (Soderstrom & Bjork 2015) personally visible and countering illusions from watching (Kardas & O'Brien 2018) or blocked practice (Abushanab & Bishara 2013).
**n-of-1:** Outcome is calibration itself (Brier score or prediction–performance correlation) and whether the learner's chosen practice schedule shifts toward the empirically better condition.

### Idea 12 — Pedal-and-voicing perception probes
**Mechanism:** With continuous damper data and release velocity, the app can resynthesise a take with pedal changed slightly earlier/later or voicing altered; learner judges which is cleaner. Builds the goal representation for pedalling — a dimension adult learners often cannot yet hear.
**n-of-1:** Track discrimination thresholds (e.g., pedal-change offset in ms that is reliably detected) via an adaptive staircase over weeks; correlate with blurring metrics (overlap of pedal-down with harmony changes) in actual playing.

---

## 12. Limits of the evidence and open questions

1. **Population mismatch.** Most music-practice studies use children, school band students or conservatory students; adult beginners/intermediates (this user) are under-studied. Motor-learning studies mostly use simple lab tasks (finger tapping, key-press sequences, aiming), not polyphonic, expressive piano playing.
2. **Small samples and publication bias.** Music-education experiments typically have N = 10–50; the motor-learning literature (self-control, external focus, sleep) has been shown to be heavily inflated by reporting bias (McKay et al. 2022–2024; Rickard et al. 2022). Expect true effects of practice-schedule manipulations to be smaller than published.
3. **Outcome measures.** Retention is usually tested after 24–48 h; months-scale retention, musicality and expressive quality are rarely measured. Expert ratings are often unreliable (Carter & Grahn: raters disagreed).
4. **Correlational expertise studies.** Expert–novice differences (chunking, eye–hand span, inner hearing) don't show that training the expert *behaviour* causes expertise.
5. **Augmented-feedback technology** (falling-note displays, light-up keys) is rarely evaluated against no-aid retention; usability ≠ learning.
6. **Theory-to-performance transfer** is largely untested causally.
7. **Rhythmic variants, slow practice and "hands separate" practice** — staples of piano pedagogy — lack controlled studies (none found in this search). These are prime candidates for the app's own n-of-1 experiments.
8. **Single-user experimentation** is feasible because the MIDI stream gives rich, objective, repeated measures; but carry-over effects (learning in condition A helps condition B), regression to the mean on hard passages, and motivation effects (the learner knows the condition) limit inference. Use many passages, randomise, and pre-specify.

---

## 13. Source list (key references)

*(Tags as in text. DOIs given where known; [reported] DOIs should be checked.)*

- Abushanab, B., & Bishara, A. J. (2013). Memory and metacognition for piano melodies: Illusory advantages of fixed- over random-order practice. *Memory & Cognition*, 41(6), 928–937. doi:10.3758/s13421-013-0311-z [confirmed]
- Bangert, M., & Altenmüller, E. O. (2003). Mapping perception to action in piano practice: a longitudinal DC-EEG study. *BMC Neuroscience*, 4, 26. doi:10.1186/1471-2202-4-26 [confirmed]
- Berliner, P. F. (1994). *Thinking in Jazz: The Infinite Art of Improvisation*. University of Chicago Press. [reported]
- Bernardi, N. F., De Buglio, M., Trimarchi, P. D., Chielli, A., & Bricolo, E. (2013). Mental practice promotes motor anticipation: evidence from skilled music performance. *Frontiers in Human Neuroscience*, 7, 451. doi:10.3389/fnhum.2013.00451 [confirmed]
- Biasutti, M. (2015). Pedagogical applications of cognitive research on musical improvisation. *Frontiers in Psychology*, 6, 614. doi:10.3389/fpsyg.2015.00614 [confirmed]
- Bigand, E., & Poulin-Charronnat, B. (2006). Are we "experienced listeners"? *Cognition*, 100(1), 100–130. doi:10.1016/j.cognition.2005.11.007 [reported]
- Brandmeyer, A., Timmers, R., Sadakata, M., & Desain, P. (2011). Learning expressive percussion performance under different visual feedback conditions. *Psychological Research*, 75(2), 107–121. doi:10.1007/s00426-010-0291-6 [confirmed]
- Brodsky, W., Henik, A., Rubinstein, B.-S., & Zorman, M. (2003). Auditory imagery from musical notation in expert musicians. *Perception & Psychophysics*, 65(4), 602–612. [confirmed]
- Carter, C. E., & Grahn, J. A. (2016). Optimizing music learning: Exploring how blocked and interleaved practice schedules affect advanced performance. *Frontiers in Psychology*, 7, 1251. doi:10.3389/fpsyg.2016.01251 [confirmed]
- Brunmair, M., & Richter, T. (2019). Similarity matters: A meta-analysis of interleaved learning and its moderators. *Psychological Bulletin*, 145(11), 1029–1052. [reported]
- Cepeda, N. J., Pashler, H., Vul, E., Wixted, J. T., & Rohrer, D. (2006). Distributed practice in verbal recall tasks. *Psychological Bulletin*, 132(3), 354–380. [reported]
- Chaffin, R., & Imreh, G. (2002). Practicing perfection: Piano performance as expert memory. *Psychological Science*, 13(4), 342–349. [confirmed]
- Chua, L.-K., Jimenez-Diaz, J., Lewthwaite, R., Kim, T., & Wulf, G. (2021). Superiority of external attentional focus for motor performance and learning. *Psychological Bulletin*, 147(6), 618–645. doi:10.1037/bul0000335 [confirmed]
- Drake, C., & Palmer, C. (2000). Skill acquisition in music performance. *Cognition*, 74(1), 1–32. [reported]
- Duke, R. A., Simmons, A. L., & Cash, C. D. (2009). It's not how much; it's how. *JRME*, 56(4), 310–321. doi:10.1177/0022429408328851 [confirmed citation]
- Ericsson, K. A., Krampe, R. T., & Tesch-Römer, C. (1993). The role of deliberate practice in the acquisition of expert performance. *Psychological Review*, 100(3), 363–406. [reported]
- de Manzano, Ö., Kuckelkorn, K. L., Ström, K., & Ullén, F. (2020). Action-perception coupling and near transfer. *Cerebral Cortex*, 30(10), 5193–5203. doi:10.1093/cercor/bhaa018 [confirmed]
- Halpern, A. R., & Bower, G. H. (1982). Musical expertise and melodic structure in memory for musical notation. *American Journal of Psychology*, 95(1), 31–50. [confirmed]
- Hsieh, T.-H., Visser, C. M. S., Eisemann, E., & Marroquim, R. (2026). Skill-adaptive ghost instructors: Enhancing retention and reducing over-reliance in VR piano learning. *CHI 2026*. arXiv:2603.06253 [confirmed]
- Hambrick, D. Z., et al. (2014). Facing facts about deliberate practice. *Frontiers in Psychology*, 5, 751. [confirmed]
- Highben, Z., & Palmer, C. (2004). Effects of auditory and motor mental practice in memorized piano performance. *Bulletin of the Council for Research in Music Education*, 159, 58–65. [confirmed citation]
- Kardas, M., & O'Brien, E. (2018). Easier seen than done. *Psychological Science*, 29(4), 521–536. doi:10.1177/0956797617740646 [confirmed]
- Little, D. F., Cheng, H. H., & Wright, B. A. (2019). Inducing musical-interval learning by combining task practice with periods of stimulus exposure alone. *Attention, Perception, & Psychophysics*, 81, 344–357. [confirmed]
- Mathias, T., & Goldman, A. (2024). How does increasing contextual interference in a musical practice session affect acquisition and retention? *JRME*, 72(4), 357–375. doi:10.1177/00224294231222801 [confirmed — abstract-level]
- Nichols, B. E., & Springer, D. G. (2025). Piano history, aural skills, and working memory predict melodic dictation performance. *Frontiers in Psychology*. (PMC12341474) [confirmed]
- Telesco, P., et al. (2021). Does retrieval practice enhance memorization of piano melodies? *College Music Symposium*, 61(2). doi:10.18177/sym.2021.61.sr.11525 [confirmed existence; results not read]
- Toth, A. J., McNeill, E., Hayes, K., Moran, A. P., & Campbell, M. (2020). Does mental practice still enhance performance? A 24 year follow-up and meta-analytic replication and extension. *Psychology of Sport and Exercise*, 48, 101672. [reported]
- Veniel-Martí, F., Botella-Nicolás, A. M., Omigie, D., & Herrojo-Ruiz, M. (2026). Comparing interleaved and blocked practices in secondary school music performances. *Update: Applications of Research in Music Education*. doi:10.1177/87551233261474481 [confirmed — abstract]
- Wong, S. S. H., Chen, S., & Lim, S. W. H. (2021). Learning melodic musical intervals: To block or to interleave? *Psychology of Music*, 49(4), 1027–1046. doi:10.1177/0305735620922595 [confirmed]
- Kopiez, R., & Lee, J. I. (2008). Towards a general model of skills involved in sight reading music. *Music Education Research*, 10(1), 41–62. [confirmed]
- Lahav, A., Saltzman, E., & Schlaug, G. (2007). Action representation of sound. *Journal of Neuroscience*, 27(2), 308–314. [confirmed citation]
- Lehmann, A. C., & Ericsson, K. A. (1996). Performance without preparation. *Psychomusicology*, 15, 1–29. [reported]
- Macnamara, B. N., Hambrick, D. Z., & Oswald, F. L. (2014). Deliberate practice and performance in music, games, sports, education, and professions: A meta-analysis. *Psychological Science*, 25(8), 1608–1618. doi:10.1177/0956797614535810 [confirmed]
- Macnamara, B. N., & Maitra, M. (2019). The role of deliberate practice in expert performance: revisiting Ericsson, Krampe & Tesch-Römer (1993). *Royal Society Open Science*, 6, 190327. doi:10.1098/rsos.190327 [confirmed]
- McKay, B., Yantha, Z. D., Hussien, J., Carter, M. J., & Ste-Marie, D. M. (2022). Meta-analytic findings of the self-controlled motor learning literature. *Meta-Psychology*, 6. doi:10.15626/MP.2021.2803 [confirmed]
- McKay, B., Corson, A., Seedu, J., et al. & Carter, M. J. (2024). Reporting bias, not external focus: A robust Bayesian meta-analysis… (SportRxiv preprint; check journal version). [confirmed preprint]
- Mishra, J. (2014). Improving sightreading accuracy: A meta-analysis. *Psychology of Music*, 42(2), 131–156. doi:10.1177/0305735612463770 [confirmed]
- Norgaard, M. (2011). Descriptions of improvisational thinking by artist-level jazz musicians. *JRME*, 59(2), 109–127. [reported]
- Norgaard, M. (2014). How jazz musicians improvise: The central role of auditory and motor patterns. *Music Perception*, 31(3), 271–287. [confirmed]
- Pan, S. C., & Rickard, T. C. (2015). Sleep and motor learning: Is there room for consolidation? *Psychological Bulletin*, 141(4), 812–834. [confirmed citation]
- Platz, F., Kopiez, R., Lehmann, A. C., & Wolf, A. (2014). The influence of deliberate practice on musical achievement: a meta-analysis. *Frontiers in Psychology*, 5, 646. doi:10.3389/fpsyg.2014.00646 [confirmed]
- Pressing, J. (1988). Improvisation: methods and models. In J. Sloboda (Ed.), *Generative Processes in Music* (pp. 129–178). Oxford: Clarendon. [reported]
- Salmoni, A. W., Schmidt, R. A., & Walter, C. B. (1984). Knowledge of results and motor learning. *Psychological Bulletin*, 95(3), 355–386. [reported]
- Sigrist, R., Rauter, G., Riener, R., & Wolf, P. (2013). Augmented visual, auditory, haptic, and multimodal feedback in motor learning: A review. *Psychonomic Bulletin & Review*, 20(1), 21–53. [reported]
- Simmons, A. L., & Duke, R. A. (2006). Effects of sleep on performance of a keyboard melody. *JRME*, 54(3), 257–269. [reported]
- Soderstrom, N. C., & Bjork, R. A. (2015). Learning versus performance. *Perspectives on Psychological Science*, 10(2), 176–199. [reported]
- Stambaugh, L. A. (2011). When repetition isn't the best practice strategy. *JRME*, 58(4), 368–383. doi:10.1177/0022429410385945 [confirmed]
- Van Hedger, S. C., Heald, S. L. M., & Nusbaum, H. C. (2019). Absolute pitch can be learned by some adults. *PLoS ONE*, 14(9), e0223047. [confirmed]
- Walker, M. P., Brakefield, T., Morgan, A., Hobson, J. A., & Stickgold, R. (2002). Practice with sleep makes perfect. *Neuron*, 35(1), 205–211. [confirmed]
- Wong, Y. K., Lui, K. F. H., Yip, K. H. M., & Wong, A. C.-N. (2020). Is it impossible to acquire absolute pitch in adulthood? *Attention, Perception, & Psychophysics*, 82(3), 1407–1430. [confirmed]
- Wulf, G., & Shea, C. H. (2002). Principles derived from the study of simple skills do not generalize to complex skill learning. *Psychonomic Bulletin & Review*, 9(2), 185–211. [reported]
