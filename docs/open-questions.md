# Open questions

Each question names how it would be answered. Grouped by who or what can answer it.

## For the user

1. **Anthology source files.** Was the *Piano Anthology* engraved from MusicXML or MuseScore files you have? If yes, all nine pieces can be ingested exactly, with no OMR.
2. **Exact instrument.** When it arrives, which adsilent version is installed (adsilent 2 vs older/PRO), and which firmware? The manual we read is for adsilent 2 v1.00.
3. **Which Mac** (chip, RAM)? It decides which local models (LLM, Aria/AMT) are realistic.
4. **Priorities among the three fluencies** for the next 6 months: if one has to lead, is it physical, harmonic or musical?
5. **Tutor model.** Local only, or is an API model acceptable for open-ended dialogue (only derived facts would be sent)?

## Answerable by experiment (planned)

| Question | Experiment | Milestone |
|---|---|---|
| Does the adsilent send release velocity, continuous CC64, CC66/67, MIDI with the mute rail off? Note-off encoding? | Hardware characterisation (hardware.md H1–H4) | Hardware day |
| CoreMIDI multi-client and timestamp jitter on the user's Mac | Chrome + daemon on one device; IAC loopback | Hardware day / M4 |
| Is Verovio's engraving of the reference pieces good enough, vs OSMD? | E1-full: renderer bake-off on all packable reference pieces | M1 |
| Can RomanText and DCML labels be aligned to MusicXML from other sources (not their own score) without errors? | Lens alignment checks for BWV 846 (WiR vs ASAP MusicXML) | M1 |
| How well does an automatic analyser (AnalysisGNN / RNHybrid) agree with *each* expert on Moonlight and BWV 846, scored as "agrees with at least one expert"? | E4 (proposed) | Before M3 |
| How accurate is practice segmentation and alignment on simulated sessions and on Rach3? | E5 (proposed) | M4 |
| Does a frontier LLM answer the gold questions correctly from a fact packet, and does it change on transposed twins? | E6 (proposed) | M5 |
| Does the counterfactual-chord engine produce realisations that sound natural in the original texture? | Listening check on 20 chords | M3 |
| Is browser sampler latency on the Mac below 20 ms? | Measure | M2 |

## Open research questions (no planned answer yet)

- Does seeing expert disagreement help a learner hear more, or just confuse? (n-of-1 with ABX outcomes)
- Do rhythmic variants or slow practice beat equal-time normal practice for this user? (D7 design)
- Is a corpus-switchable expectation model meaningful to a learner's own sense of surprise? (A11)
- How should a "chord slice" be defined in arpeggiated piano textures for L1 computations? (E3 used label spans; alternatives untested)
- What is a useful definition of pedal "blur" against harmony, given sympathetic resonance? (no study found)
- Can transposition-probe collapse points predict where memory slips later? (C3 + mirror data)

## Unverified claims carried in the docs

- CoreMIDI multi-client behaviour [reported].
- Licences not yet checked: `manoskary/analysisgnn`, VirtuosoNet (no licence file), piano-synmist, Batik-plays-Mozart, PIG, BPS-Motif, Jazz Harmony Treebank, AMT weights, Rach3 terms.
- Audiveris licence (AGPL-3.0) [reported].
- The identity of "DT" for the Moonlight file specifically (other files say "Dmitri Tymoczko", some "and his computer").
