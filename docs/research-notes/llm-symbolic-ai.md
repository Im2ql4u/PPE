# LLMs and ML for symbolic music understanding, explanation and tutoring

> **Agent-produced research note, dated 2026-10-23. Needs review before anything depends on it.**
> A research subagent wrote this from web sources it reached in one session, which a usage limit interrupted once. Tags:
> **[confirmed]** = checked against a primary source (paper abstract/HTML, repo README, model card, or a local corpus file);
> **[reported]** = found only in secondary summaries, partial reads, or the agent's background knowledge without re-fetching (marked "bg");
> **[speculative]** = the author's inference, estimate or design proposal.
> Model names and dates are as given in the cited papers. Look up benchmark numbers in the papers before quoting them elsewhere.

---

## 0. Summary

1. **Frontier LLMs in 2026 can do useful local harmonic reasoning from text encodings. They are still unreliable on exact facts** (counting, locating, multi-step structure) **and very weak from score images.** The best 2025 model on MSU-Bench scores 49% on ABC text and 24% on PDF images. On harmony, texture and form questions, accuracy falls to about 38% [confirmed]. Mid-2026 informal tests suggest the newest models (Claude Opus 5, Gemini 3.1 Pro, GPT‑5.6) are clearly better at chord spelling and short Roman-numeral analyses. They still miss suspensions and modulations [reported]. **Design consequence: the LLM must never be the source of truth for score facts.** It reads facts the symbolic core has computed and cites them.
2. **Tool use measurably helps.** A ReAct agent calling 16 deterministic music21 functions raised GPT‑4.1‑mini from 50.8% to 66.7% on CSyMR-Bench [confirmed]. The agent "recovered from hallucinated CoT" by running key and Roman-numeral operators. This supports the project's established principle that symbolic facts come from the core and the LLM explains them.
3. **Music-specialised LMs are not tutors.** ChatMusician's own model card says it "suffers from hallucinations, and shouldn't be used for music education" [confirmed]. Their value lies in **embeddings for similarity search** (CLaMP 3, Aria‑embedding), **generation and infilling of variations** (NotaGen, Anticipatory Music Transformer, Aria, Moonbeam), and **OMR** (Legato/Legato 2). Most are MIT or Apache‑2.0 and under 1B parameters, so they run locally on Apple Silicon [confirmed for licences where stated].
4. **Representation.** LLMs read compact text such as ABC, RomanText, **kern and LilyPond much better than images. Raw MusicXML wastes tokens.** No controlled study isolates the format effect on frontier models [confirmed absence in the sources searched]. Recommendation: a custom compact event table with stable IDs plus aligned analysis layers [speculative but well motivated].
5. **Pedagogy evidence argues for guardrails.** The Harvard physics AI-tutor RCT found an effect of 0.63 SD (0.73–1.3 SD by quantile regression), using a tutor built on *pre-written expert solutions* and sequential guidance [confirmed]. Bastani et al. (PNAS 2025) found that unguarded GPT‑4 raised practice scores 48% and then lowered exam scores 17%. A guardrailed tutor removed the harm, but it did not produce an exam gain [reported, abstract-level]. A music tutor should make the learner predict and hear before it reveals an answer.
6. **Exercise generation.** Use deterministic transforms with validators (transposition, reduction, rhythmic variants, constraint-based voicing) as the backbone. ML difficulty estimation is still weak: the best CIPI model reaches 39.5% balanced accuracy over 9 levels [confirmed]. Use ML for ranking or suggestion only.
7. **Cost and privacy.** A local 20–35B open-weight model with tool calling can handle routine explanations over pre-computed facts. Use a frontier API model for open-ended analytical dialogue, debate mode and gold-set evaluation [speculative].

---

## 1. How good are current LLMs at music theory and score reading?

### 1.1 Benchmarks (chronological)

| Benchmark (date) | Input | Models / years | Metric and headline result | Limitations | Tag |
|---|---|---|---|---|---|
| **MusicTheoryBench**, in ChatMusician (Yuan et al., arXiv 2402.16153, Feb 2024; ACL Findings 2024) | Text MCQ; music knowledge + music reasoning; expert-curated | GPT‑4, GPT‑3.5, LLaMA2‑7B, ChatMusician (2023–24) | Zero-shot accuracy averaged over 5 option shuffles. **Knowledge: GPT‑4 58.2**, ChatMusician 39.5–40.2, GPT‑3.5 31.2. **Reasoning: GPT‑4 "marginally better than random"** (chance 25%) | Small, MCQ, 2023-era models; ChatMusician scored in perplexity mode | [confirmed] abstract/search snippet; [reported] exact reasoning figure. https://arxiv.org/abs/2402.16153 |
| **ZIQI-Eval** (Li et al., ACL Findings 2024, arXiv 2406.15885) | Text MCQ, >14,000 items, 10 categories / 56 subcategories | 16 LLMs (2024) | All "performed poorly". A later paper (SongSage, arXiv 2601.01153) reports GPT‑4 62.9%, GPT‑4o 76.1%, ChatMusician 24.6% | Mostly knowledge recall, not score reading | [confirmed] abstract; [reported] SongSage table. https://arxiv.org/abs/2406.15885 |
| **"Can LLMs 'Reason' in Music?"** (Zhou et al., ISMIR 2024, arXiv 2407.21531) | Symbolic (ABC), understanding + generation | GPT‑4 and others (2024) | "Poor performance in song-level multi-step music reasoning", and models "typically fail to leverage learned music knowledge"; weak on motif extraction, form, chord-conditioned melody | Older models; mostly qualitative | [confirmed] abstract. https://arxiv.org/abs/2407.21531 |
| **Pond & Fujinaga** (CSME 2025, arXiv 2503.22853) | RCM Level‑6-style theory exam questions in **ABC, Humdrum, MEI, MusicXML** | ChatGPT, Claude, Gemini (versions not given; early 2025) | Best without context: ChatGPT + MEI **52%**. Best with in-context teaching material: Claude + MEI **75%** | No model versions; small; per-format table hard to read | [confirmed] abstract. https://arxiv.org/abs/2503.22853 |
| **CMI-Bench** (Ma et al., ISMIR 2025, arXiv 2506.12285) | **Audio**-text instruction following over MIR tasks (key, chords, beat, melody…) | Audio LLMs (Qwen‑Audio, SALMONN, LTU, MusiLingo…) | "Significant performance gaps" vs supervised MIR models; cultural, chronological and gender biases | Audio, not symbolic; open audio LLMs only | [confirmed] abstract. https://arxiv.org/abs/2506.12285 |
| **WildScore** (arXiv 2509.04744, Sep 2025; v2 Jan 2026) | **Score images** + MCQ from 807 r/musictheory threads (2012–22) | GPT‑4.1‑mini 68.3% (text-only 65.8%), Qwen‑2.5‑VL 49.7%, Phi‑3‑V, Gemma‑3, InternVL, LLaVA; human expert 72% (n=100) | Accuracy. **Perception probe: GPT‑4.1‑mini read relevant visual features correctly in only 52% of 50 cases** | Questions often answerable *without* the image (text-only nearly as good); Reddit "ground truth" can be wrong | [confirmed] HTML v2. https://arxiv.org/abs/2509.04744 |
| **ABC-Eval** (Zhao et al., arXiv 2509.23350, Sep 2025) | ABC text; 1,086 items, 10 subtasks (bar count, next-bar prediction, bar sequencing, error detection, captioning, composer/genre…) | GPT‑5 **55.0%** overall, GPT‑5‑mini 53.5, DeepSeek‑reasoner 52.0, Gemini‑2.5‑pro 51.3, Gemini‑2.5‑flash 44.1, DeepSeek‑chat 40.2 | Basic syntax >90% for most models. **Error detection macro‑F1 only 6–27%.** Emotion/composer/genre near chance | No CoT; prompt sensitivity | [confirmed] HTML. https://arxiv.org/abs/2509.23350 |
| **MSU-Bench** (Dai et al., arXiv 2511.20697, Nov 2025; ACL 2026 Main) | 1,800 generative QA pairs on full scores (Bach, Beethoven, Chopin, Debussy…), 4 levels (onsets → notation → harmony → texture/form); **ABC vs PDF image** | Gemini 2.5 Pro, "ChatGPT‑5", GPT‑5‑mini, Claude Sonnet 4, Claude Opus 4, Grok 4, Qwen3‑VL‑235B, Llama 4 Scout… | LLM-judge accuracy. **ABC best: Gemini 2.5 Pro 49.4%** (L1 65.3 → L4 37.8). **PDF best: Claude Opus 4 24.2%.** Level-wise success (correct on all levels for a score) "nearly vanishes by L3". LoRA fine-tuning of Qwen3 0.6–4B helps substantially | Judges are also contestants (83% judge-human agreement); single run; Western common-practice only | [confirmed] HTML v4. https://arxiv.org/abs/2511.20697 |
| **CSyMR-Bench** (arXiv 2601.11556, Jan/Feb 2026) | 126 MCQ, scores OMR-converted to **kern | GPT‑4.1‑mini, GPT‑4.1, DeepSeek‑V3.1, Gemini 1.5 Pro, Claude 3.7 Sonnet | Zero-shot 46–52%. **GPT‑4.1‑mini + music21 ReAct agent: 66.7%** vs 50.8% zero-shot and 61.9% few-shot CoT. Tools *hurt* on genre/composer questions | Small n; OMR noise; LLM-generated distractors | [confirmed] HTML. https://arxiv.org/abs/2601.11556 |
| **LilyBench** (arXiv 2606.08722, Jun 2026) | LilyPond; ABC-Eval tasks adapted | 4 open-weight models | Zero-shot executable LilyPond generation works; "structural understanding tasks remain hard" | Open models only | [confirmed] abstract. https://arxiv.org/abs/2606.08722 |
| **MusICA-MetaBench** (arXiv 2607.06015, Jul 2026) | *Generates* MCQ benchmarks from any MusicXML via music21 ground truth; audio / PNG / ABC | **Gemini 3.1 Pro (preview) 59.0%** on ChoraleBricks (chance 20%); Qwen3‑Omni‑30B 46.3%; GPT‑5/GPT‑4o/Mistral combinations 39–42% | Most between-model variance came from the *symbolic* modality; audio hardest | 2 datasets; some distractors answerable without input | [confirmed] HTML. https://arxiv.org/abs/2607.06015 |
| **"LLMs can read music, but struggle to hear it"** (Carone et al., PMLR v303, Jan 2026) | MIDI vs audio; syncopation, transposition, chord quality | Gemini 2.5 Pro/Flash, Qwen2.5‑Omni | "Near ceiling on MIDI", large drops on audio; CoT/LogicLM give minimal gains | Simple perception tasks | [confirmed] abstract. https://proceedings.mlr.press/v303/carone26a.html |

### 1.2 Roman-numeral analysis specifically

- **No peer-reviewed study was found that benchmarks frontier LLMs on Roman-numeral analysis against expert RomanText/DCML annotations** (e.g., When in Rome, ABC/BPS). [confirmed absence in the searches run; this is a research gap the project could fill with its own gold set, §9.]
- An informal blog test (Augmented Fifth, 6 Aug 2026) sent **LilyPond** excerpts to Grok 4.5 Expert, Gemini 3.1 Pro and **Claude Opus 5**. On a Bach chorale (BWV 269), Gemini scored 95% and Grok 80%. On Chopin's Nocturne Op. 9/1, Gemini 100% and Grok 92%. Grok recognised the piece by name, which raises the memorisation concern. On Scriabin Op. 2/1, Grok 40%, Gemini 75%, **Opus 5 88%**. All three missed the suspensions in m. 4 and the A♯ signalling the modulation in m. 5. Only Opus 5 attempted cadence labelling. The author reports that LilyPond and MusicXML work but images and PDFs "do not". [reported; single non-expert-panel blog; https://aug5th.substack.com/p/llms-vs-harmonic-analysis]
- The same blog (30 Jul 2026) used 12 deliberately hard chord-spelling questions (e.g., iiø6/5 of ♭VI in F). 2026 models scored 75–100% (GPT‑5.6 "Sol" 100%, Sonnet 5 91%, GPT‑5.5 83%). Most 2025 models scored 0–25%, except Gemini 2.5 Pro at 91%. **The author declares that benchmark saturated.** [reported; https://aug5th.substack.com/p/testing-llms-on-undergraduate-music]
- Dedicated non-LLM analysis models remain the right *algorithmic layer*: AugmentedNet (ISMIR 2021), AnalysisGNN (arXiv 2509.06654), and Karystinaios, Hentschel, Neuwirth & Widmer, "From Prediction to Collaboration: Interactive Symbolic Music Analysis" (ISMIR 2026, arXiv 2607.13587). The ISMIR 2026 framework supports full analysis, *targeted correction* and *masked completion from partial labels*, evaluated on the "Dilemmadata" benchmark. That makes it a natural "algorithmic analyst" alongside the human analysts in the core. [confirmed abstract for 2607.13587; others reported]

### 1.3 Is this outdated? Assessment for October 2026

- **Partly.** Most published numbers are on 2024–mid‑2025 models (GPT‑4.1, Claude 3.7/4, Gemini 2.5). The informal 2026 evidence shows a large jump in *local, rule-like* skills such as chord spelling and short RN passages [reported]. The only 2026 formal benchmark with a current frontier model (MusICA, Gemini 3.1 Pro preview) shows **59% on chorale questions generated from music21 ground truth**, which is far from reliable [confirmed].
- **Persistent failure classes** that a tutor must design around [confirmed across MSU-Bench, ABC-Eval, WildScore, CSyMR]:
  1. *Locating and counting* (bar numbers, beat positions, how many times X occurs).
  2. *Error detection* and *long-range structure* (form, texture, multi-level consistency).
  3. *Image perception* of notation, at less than half the accuracy of text input.
  4. *Shortcutting* via prior knowledge: questions answerable without the score, recognising famous pieces. **Moonlight and Clair de lune are among the most-discussed pieces in existence. An LLM "analysis" of them may be recalled commentary, not reading.** [speculative but strongly suggested by the WildScore text-only results and the Grok piece-identification episode]
- **Implication [speculative]:** a 2026 frontier model is good enough to *explain* a correct, pre-computed analysis fluently, and to make plausible interpretive suggestions in ambiguous passages. It is not good enough to *produce* facts unsupervised. That matches the project's established principle.

---

## 2. Music-specialised models: what each is good for

| Model | What it is | Size / licence | Useful for the lab? | Apple-Silicon local | Tag / source |
|---|---|---|---|---|---|
| **ChatMusician** (2024) | LLaMA2‑7B continually pretrained on ABC + music text (MusicPile) | 7B; MIT | **No as tutor**: the card says it "shouldn't be used for music education", supports only strict-format closed instructions, and is Irish-folk heavy | Yes (7B quantised) but pointless | [confirmed] https://huggingface.co/m-a-p/ChatMusician |
| **MuPT** (ICLR 2025) | ABC-notation GPT with synchronised multi-track ABC | 110M–1.3B (a 1.97B checkpoint also listed); Apache‑2.0 | Melody/accompaniment continuation in ABC; weaker than NotaGen for classical | Yes | [confirmed] https://huggingface.co/m-a-p/MuPT-v1-8192-1.97B |
| **NotaGen** (IJCAI 2025, arXiv 2502.18008) | Classical sheet-music generation in interleaved ABC; pretrain → fine-tune on ~9K classical works → CLaMP‑DPO RL; conditioned on period–composer–instrumentation | 110M / 244M / 516M; **MIT** | "Romantic-style piano piece" generation; *stylistic counterexamples* for listening. Not fine-grained control | NotaGen‑X inference ≈8 GB GPU memory, so a 16 GB+ Mac via MPS should work [reported] | [confirmed] https://github.com/ElectricAlexis/NotaGen |
| **CLaMP 2 / CLaMP 3** (CLaMP 3: ACL Findings 2025, arXiv 2502.10362) | Contrastive embeddings aligning ABC/MusicXML, MIDI (MTF), audio (MERT features), images and multilingual text | 768‑d global or per-timestep vectors; **MIT**; XLM‑R‑base text encoder | **Cross-piece similarity search** ("pieces like this passage"), text→score retrieval, clustering your repertoire. Limit 512 bars / 512 MIDI messages | Likely CPU/MPS feasible (BERT-sized); README assumes CUDA | [confirmed] https://github.com/sanderwood/clamp3 |
| **Aria** (EleutherAI, ISMIR 2025, arXiv 2506.23869) | Piano-performance MIDI LM (LLaMA‑3.2‑1B architecture; ~60k h of solo-piano transcriptions); gen + **embedding** checkpoints | ~1B; **Apache‑2.0** | Piano continuation ("what could come next?"), **performance-style embeddings**, real-time duet demo | **Native MLX implementation and real-time demo** | [confirmed] https://github.com/EleutherAI/aria |
| **Anticipatory Music Transformer** (Thickstun et al., TMLR 2024, arXiv 2306.08620) | Infilling / accompaniment conditioned on "anticipated" control events (Lakh MIDI) | 128M / 360M / 780M; code **Apache‑2.0**; weight licence not stated on README | **Infilling** (regenerate bars 5–8 keeping melody), accompaniment for a given melody, generating "alternatives" for counterexample features | Small enough for MPS/CPU; README uses CUDA | [confirmed] https://github.com/jthickstun/anticipation |
| **Moonbeam** (Guo & Dixon, arXiv 2505.15559, May 2025) | MIDI foundation model with relative attention; finetunes for understanding + conditional generation and infilling | 309M / 839M; open-sourced (licence not verified) | Infilling and classification; a research option | Probably feasible | [confirmed] abstract |
| **Text2midi** (AAAI 2025) | Caption (FLAN‑T5 encoder) → MIDI decoder | **MIT**; explicit MPS requirements file | "Generate a slow waltz in A minor" exercise drafts; low precision of control | **Yes (MPS supported)** | [confirmed] https://github.com/AMAAI-Lab/Text2midi |
| **MIDI-LLM** (Wu, Kim, Huang; NeurIPS 2025 AI4Music workshop, arXiv 2511.03942) | Llama‑3.2‑1B with MIDI tokens added to the vocabulary; text→multitrack MIDI; beats Text2midi | 1B | Same as above, better quality; vLLM-friendly | Yes | [confirmed] abstract |
| **MIDI-LLaMA** (ICASSP 2026, arXiv 2601.21740) | MusicBERT encoder + Llama‑3‑8B; MIDI captioning/QA; beats an ABC-text baseline | 8B; release unclear | Evidence that *native MIDI encoders* can beat ABC text for description, but not a usable artefact | — | [confirmed] abstract |
| **MusicBERT** (Microsoft, 2021) / **MidiBERT-Piano** (2021) | Encoder pretraining on OctupleMIDI / REMI-like tokens | ~100M; MusicBERT under MIT (muzic repo) | Classification baselines, embedding features | Yes | [reported, bg] |
| **Legato / Legato 2** (ICLR 2026, arXiv 2506.19065; arXiv 2607.05769) | End-to-end OMR → ABC; Legato 2 reads system-by-system and also transcribes text | Weights status unverified | **Importing scores you only have as PDFs**; Legato 2 reports "symbolic transcriptions complement visual inputs for frontier LMs" | Unknown | [confirmed] abstracts |

**Mapping to lab tasks [speculative synthesis]:**

- *Similarity search across pieces* has two stages. First, symbolic n-gram search over RN/bass/interval sequences, which is exact, explainable and cheap. Second, CLaMP 3 (score-level) and Aria embeddings (performance/texture) for "feels similar" retrieval. Always show *why* items matched (shared RN n-gram, shared bass line) next to any embedding score.
- *Motif retrieval*: deterministic first. Pattern search over interval/rhythm strings with transposition and inversion invariance (music21, or partitura with numpy), optionally with CRIM-Intervals-style n-grams. Embedding motif search is unreliable at sub-bar granularity.
- *Variations and counterexamples*: deterministic transforms first (§6). Use AMT or Aria infilling for "plausible alternatives", filtered by validators.
- *Harmonisation*: rule- or constraint-based voice-leading generators are more trustworthy for pedagogy. The music21-mcp-server's `harmonize_melody` is heuristic. Model-based harmonisation, e.g. AMT conditioned on a melody, gives *style* but no correctness guarantees.

---

## 3. Tool-using tutor architectures

### 3.1 Existing music21 MCP servers (as of Oct 2026)

- **brightlikethelight/music21-mcp-server** is MIT. It exposes 13 tools: import/list/info/export/delete score, analyze_key, analyze_chords, analyze_harmony, analyze_voice_leading, recognize_patterns, harmonize_melody, generate_counterpoint, imitate_style. A protocol-independent `services.py` core sits behind MCP, HTTP (FastAPI), CLI and Python adapters. 28 stars, 196 commits. **Its own README rates the MCP transport at "40–50%" success**, without evidence, and the enterprise features were removed as unstable. **Verdict:** a useful reference for the *adapter-over-core* layering. Its tool granularity is "analyse the whole score". It lacks the selection-addressed, provenance-carrying outputs this project needs. [confirmed] https://github.com/brightlikethelight/music21-mcp-server
- Others found: FernandoDaSilva‑T/music21‑mcp (key/harmony/motif/counterpoint; 0 stars), viktorkelemen/music21‑composer‑mcp (inactive), tskovlund/mcp‑score (MuseScore/Dorico/Sibelius live editing), and an "Encoding Music" hosted MCP built on music21 + CRIM Intervals (SICSS 2026 workshop guide; could not be fetched). [reported] https://glama.ai/mcp/servers/brightlikethelight/music21-mcp-server
- **Recommendation [speculative]:** build a project-specific tool layer, using MCP or plain function calling from the local backend, over the symbolic core. The hard part is data design (IDs, layers, provenance), not the protocol.

### 3.2 Evidence that tool grounding works

- **CSyMR-Bench:** the music21 ReAct agent beat CoT few-shot by about 5 points and zero-shot by about 16 points. In a case study it corrected a hallucinated rationale by calling key-estimation and RN operators. A separate "Tooler" ran the code and returned *natural-language evidence*, so the reasoner never saw code. [confirmed]
- **MusICA-MetaBench** shows the inverse use: **music21 can generate ground truth for evaluating LLMs**. That is exactly the evaluation approach proposed in §9. [confirmed]
- **Kestin et al.** found pre-written expert solutions in the prompt were *necessary* for accuracy: "the authors avoided relying solely on GPT‑4 to generate solutions". This is the education analogue of grounding. [confirmed]

### 3.3 Intelligent tutoring systems for music: lineage and evidence

- **Dannenberg et al., Piano Tutor (CMU, 1990–93).** An expert-system tutor for beginning piano: score following to detect errors, targeted feedback rather than listing every error, and interruption on conditions such as erratic tempo. Four publications (ICMC 1990; *Interface/JNMR* 19(2–3) 1990; 1992 chapter; "Results from the Piano Tutor Project", 1993). Dannenberg later said it "worked really well" but was expensive to create and maintain, and it survived as a demo. **No quantitative evaluation results were retrievable online.** [confirmed bibliography] https://www.cs.cmu.edu/afs/cs/Web/People/rbd/bib-ptutor.html
  - *Lesson [speculative]:* the 1990 architecture (score model, performance alignment, error taxonomy, pedagogical policy for what to say) still holds. LLMs mostly lower the authoring cost of the last step, the cost that killed the original.
- **General ITS meta-analysis:** Kulik & Fletcher (Review of Educational Research, 2016) report a median effect of about 0.66 SD over conventional instruction, larger on locally developed tests. [reported] https://www.ida.org/research-and-publications/publications/all/e/ef/effectiveness-of-intelligent-tutoring-systems-a-meta-analytic-review
- **LLM music tutors with learner outcomes are scarce.** The closest is "Chat Melody", an LLM *teachable agent* (the learner teaches the agent) for music analysis, at a CHI 2025 workshop (arXiv 2504.00636). n = 28 Chinese university students, control n ≈ 12 after attrition. Higher post-test scores and lower cognitive load. Preliminary. [reported] https://arxiv.org/abs/2504.00636
- **No 2025–2026 peer-reviewed RCT of an LLM music-theory or piano tutor was found.** [confirmed absence in searches run]

---

## 4. Representing scores for LLM context

### 4.1 Evidence

- **Text beats images:** on MSU-Bench, ABC text scored 49% against 24% for PDF images on the same questions and models [confirmed]. WildScore's perception probe found 52% correct visual feature reading for GPT‑4.1‑mini [confirmed]. The Aug 2026 blog says LilyPond and MusicXML were usable while PDFs were not [reported].
- **Format comparisons:** Pond & Fujinaga (2025) is the only multi-format comparison found (ABC/Humdrum/MEI/MusicXML). The *best* cells were MEI (52% no-context, 75% with context), but the table is poorly reported and the models were early-2025 [confirmed abstract]. No controlled token-matched study on 2026 frontier models was found.
- **ABC is shortest and LM-friendly:** MuPT and ChatMusician argue for ABC over MIDI-derived tokens for LMs. A 2026 paper says ABC yields "significantly shorter sequences than MIDI or MusicXML" [reported]. **kern's tab-separated spines align voices vertically, which helps some reading tasks and hurts others [reported].
- **Native encoders can beat text:** MIDI-LLaMA (MusicBERT embeddings into Llama‑3‑8B) beat an ABC-text baseline on captioning/QA [confirmed abstract]. This only matters if you fine-tune, which is out of scope for an API tutor.

### 4.2 Token efficiency: rough estimates [speculative; measure on the corpus]

For the first 4 bars of the Moonlight 1st movement (triplets plus bass octaves plus melody; about 60 note events):

| Format | Approx. chars | Approx. tokens | Comment |
|---|---|---|---|
| MusicXML (partwise) | 30–60k | 8–15k | One `<note>` is about 300–600 chars. Never put raw MusicXML in context |
| MEI | 15–30k | 4–8k | Verbose but semantically rich |
| **kern | 1–2k | 0.5–1k | Compact; spines; less familiar to LLMs than ABC |
| ABC (voice-interleaved) | 0.6–1.2k | 0.3–0.7k | Shortest; key-signature-relative accidentals need care; bar numbers are implicit |
| RomanText (analysis only) | 0.1–0.2k | ~50–100 | Extremely efficient for the harmony layer |
| Compact JSON events (proposed) | 4–8k | 1.5–3k | Larger than ABC, but **every item is addressable and explicit**: absolute pitch spelling, measure, beat |

**Recommendation [speculative]:** for *tutor context*, send a **hybrid packet** (§8.2):

1. a compact **note-event table** for the selected passage only, with stable IDs (`m12.b2.5.RH.v1.n3`), spelled pitch, MIDI number, onset (measure, beat, quarter-offset), duration, tie/staff/voice, **without** key-relative accidental inference;
2. aligned **analysis layers** (per-analyst RN label with key, inversion figure, and onset/offset spans; cadences; form labels);
3. optionally a short **ABC or kern rendering** of the same span as a "gestalt" view, because LLMs have seen a lot of ABC;
4. **computed facts** the question needs (pitch-class sets, intervals, bass line, voice-leading moves) so the model does not derive them.

**Experiment to run (cheap, high value) [speculative]:** for 50 gold questions (§9.3), compare accuracy for ABC-only vs kern-only vs JSON-only vs hybrid, using one frontier and one local model. Use *transposed and retitled* variants to control for memorisation.

---

## 5. Explanation quality and pedagogy for AI tutors

### 5.1 Key empirical results

- **Kestin, Miller, Klales, Milbourne & Ponti, "AI tutoring outperforms in-class active learning", *Scientific Reports* (3 Jun 2025).** Randomised crossover; Harvard intro physics; N = 194; GPT‑4-based tutor at home vs in-class active learning, one topic each over two weeks. **Effect 0.63 SD by linear regression (an underestimate due to ceiling); 0.73–1.3 SD by quantile regression.** Post-test medians 4.5 vs 3.5 from a 2.75 pre-test, i.e. gains more than double. Median time 49 min vs 60. 83% rated AI explanations at least as good as human instructors'. **Design:** system prompt on active engagement, cognitive-load management and growth mindset; **content prompts built on pre-written step-by-step expert solutions**; **sequential part-by-part guidance**, because the system prompt alone did not keep order; feedback only in response to student input. **Limitations:** single course; immediate post-test only (no retention); months of development; the paper names *when to give vs withhold answers* as open. [confirmed] https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/
- **Bastani et al., "Generative AI without guardrails can harm learning", PNAS 122(26), 2025** (DOI 10.1073/pnas.2422633122). About 1,000 high-school maths students in Turkey; arms GPT Base (ChatGPT-like), GPT Tutor (hint-giving prompts with teacher-provided solutions), and control. **Practice: +48% (Base), +127% (Tutor). Unassisted exam: Base −17% vs control; Tutor ≈ control.** The authors attribute the harm to using GPT as a "crutch". [reported, abstract-level] https://papers.ssrn.com/abstract=4895486
  - *Reading:* guardrails *prevented harm* but did **not** convert large practice gains into exam gains. "Socratic prompting" alone is not enough; what matters is whether the learner does the cognitive work.
- **Pretesting / prequestion effect:** answering *before* instruction improves learning even when the answers are wrong. St. Hilaire, Chan & Ahn, *Psychonomic Bulletin & Review* 31:411–441 (2024), meta-analysis. Pan & Sana (2021, 5 experiments, N = 1,573): pretesting beat posttesting. Pan & Rivers (2023): learners don't believe it works. That last point matters, because an optional "predict first" button will be skipped. Akgun & Toker (arXiv 2504.10249, 2025): GenAI-assisted pretesting helped most for complex, exploratory tasks. [reported] https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12292081/ , https://arxiv.org/abs/2504.10249
- **Industry guardrail modes:** OpenAI "Study Mode" (29 Jul 2025) and Anthropic "Learning Mode" (Claude for Education, 2025) apply Socratic questioning instead of answers [reported]. Google's LearnLM work (arXiv 2407.12687; 2025 Gemini 2.5 integration) turned learning-science principles into 7 benchmarks and turn-level pedagogy rubrics (e.g., "does not reveal the answer", "monitors motivation") [reported]. Most of this evidence is vendor-produced.

### 5.2 Implications for a music tutor [speculative unless tagged]

1. **Ear and analysis first, label later.** The music analogue of "giving the answer" is announcing "this is a Neapolitan sixth" before the learner has heard the darkening and seen the ♭2 in the bass. Default policy: *listen → predict/describe → compare with the analysts → name*.
2. **Pre-written expert content beats generated content (Kestin).** The DCML and When-in-Rome annotations play the role of the pre-written solutions: the tutor scaffolds *toward* them and does not invent them.
3. **Sequenced micro-steps** enforced by the *application*, not by the prompt (Kestin found prompts alone unreliable for ordering). A state machine (selection → hearing task → prediction → reveal layer 1 → …) should decide what the LLM is allowed to show.
4. **Levels of explanation**, chosen explicitly: (L0) perceptual ("the bass drops a semitone; the colour darkens"); (L1) notational ("D♮ in the bass, under F♯–A"); (L2) functional ("pre-dominant; ♭II6 in c♯"); (L3) contextual/stylistic ("Beethoven's recurring use of N6 in this movement, mm. 3, 16, 18, 21, 50…"); (L4) interpretive/aesthetic (labelled as opinion).
5. **Misconception detection** with a *typed error taxonomy* that the backend can check: wrong inversion figure, root confused with bass, key-relative vs absolute numeral (V/iv in b vs V in e), enharmonic confusions (D♭ major vs C♯ minor contexts; E major region in Clair de lune), confusing a tonicisation with a modulation, quality errors (ø7 vs o7). The LLM classifies a learner's answer into one of these types. The *backend* decides whether the answer is right.
6. **Make "predict first" the default, not optional** (Pan & Rivers). Allow a cheap skip, but log it.
7. **Separate claim types** visibly: fact / analysis (whose) / pedagogical advice / aesthetic opinion (§8.3).

---

## 6. Automatic exercise and variation generation

### 6.1 What exists

- **Difficulty estimation (symbolic):** Ramoneda et al., "Combining piano performance dimensions for score difficulty classification", *Expert Systems with Applications* 238 (2024). CIPI dataset (Henle difficulty labels matched to public-domain scores, expert-corrected). **Best: 39.5% balanced accuracy, 1.1 median squared error, 9 levels.** Combining fingering-based and expressiveness-based representations helped. Code, data and models are public (github.com/PRamoneda/difficulty-prediction-CIPI). [confirmed] https://arxiv.org/abs/2306.08480
- **Difficulty from audio:** PSyllabus, 7,901 recordings across 11 levels, 1,233 composers, from ABRSM/RCM/Trinity syllabi; IEEE TASLP 2025; "research use only". [confirmed] https://zenodo.org/records/14794592
- **Difficulty-aware sight-reading generation:** Ramoneda, Suzuki, Maezawa & Serra (arXiv 2509.16913, Sep 2025). Control tokens plus an auxiliary difficulty-prediction objective to prevent "conditioning collapse"; automatic metrics and expert judgements. [confirmed abstract]
- **Evolutionary generation from expert models:** Pierce et al., *Frontiers in AI* (2021). Features learned from graded books (AMEB/ABRSM/Trinity, Grades 1–2: key, metre, range, rests/ties, contour). Mostly flute material. [reported] https://pmc.ncbi.nlm.nih.gov/articles/PMC7948302/
- **Libraries:** music21 (transposition, `chordify`, reductions, voice-leading checks, RomanText I/O); partitura (alignment, performance features); tonal.js (MIT; JS chord, scale, key and voicing utilities for client-side keyboard displays). [reported, bg]

### 6.2 What is robust (recommendations) [speculative]

| Exercise type | Robust method | ML/LLM role |
|---|---|---|
| Transpositions of a passage to all keys / nearby keys | music21 `transpose` with enharmonic spelling policy (prefer keys ≤ 5 accidentals; choose spelling by key signature) | None, beyond explaining why a key was chosen |
| Reductions (surface → chordal → outer voices → RN skeleton) | `chordify` + beat-strength sampling + bass/soprano extraction, aligned to DCML/WiR labels | LLM narrates each level; model-free |
| Rhythmic variants (augmentation, displacement, simplification of triplets to block chords) | Deterministic onset transforms; Moonlight triplet → block-chord realisation is a classic practice method | — |
| Harmony drills from your repertoire (e.g., "spell all N6 chords in Moonlight") | Query the analysis layer for RN = N6; generate spelled-chord tasks; auto-grade by pitch-class set and bass | LLM generates hint text only |
| Voicing exercises (play ii–V–I in 3 voicings) | Constraint solver: range, spacing, common tones, parallel 5ths/8ves check (music21 voice-leading module) | None, or ranking voicings by hand-span/ergonomics |
| Sight-reading at graded difficulty | Rule-based generator (key, range, rhythm vocabulary, hand-position changes) + **validators** + a difficulty *estimate* used only for ordering | Possibly Ramoneda-style models as rankers; NotaGen/AMT as "stylistic" sources with filtering |
| "Composer-like" variations / continuations | AMT infilling, Aria continuation | Mark as *generated*; never present as the composer's text |

**Robustness rule:** every generated item passes validators (playable span ≤ a configured hand-span, no unintended parallels in voice-leading drills, spelling consistent with key, rhythm sums to the bar) and carries a provenance tag `generated_by: {tool, version, seed, source_span}`.

---

## 7. Cost and privacy: local vs API

- **Local stack on macOS/Apple Silicon:** llama.cpp (Metal), Ollama, LM Studio, MLX/mlx-lm. Sparse MoE models with about 3B active parameters (Qwen3 / "Qwen 3.6‑35B‑A3B"-class), gpt-oss‑20b and Gemma‑class models run at interactive speed on 32–64 GB Macs. Tool-calling reliability varies by runtime and chat template. One 2026 guide says llama.cpp/Ollama still handle tool-call formats better than MLX servers. [reported; blog-grade sources, e.g. https://bestllmfor.com/guides/mlx-local-llm-apple-silicon/ ; verify on own hardware]
- **Music models locally:** Aria has native MLX. Text2midi has MPS requirements. NotaGen‑X needs about 8 GB. CLaMP 3 is BERT-sized. AMT runs 128–780M. All are feasible on an M-series Mac with 16–32 GB [confirmed per READMEs; MPS behaviour of CLaMP 3/AMT not verified].
- **Privacy:** the scores are public-domain or CC-licensed (DCML is **CC BY‑NC‑SA**: a non-commercial restriction to respect if the lab is ever shared). The *sensitive* data is the learner's performance recordings and learning history. Keep these local. Send only derived, minimal facts to an API model if needed [speculative].

**Task-to-model matrix [speculative]:**

| Task | Needs frontier? | Why |
|---|---|---|
| Rendering pre-computed facts into prose at a chosen level | No (local 8–30B) | Constrained paraphrase of a fact packet |
| Hint generation in the predict-reveal loop | Local OK, frontier better | Needs pedagogical judgement but low factual risk if facts are supplied |
| Classifying learner answers into a misconception type | Local OK with few-shot | Backend verifies correctness; the LLM only types the error |
| Open-ended "why did Beethoven…" dialogue, analyst-debate mode | **Frontier** | Interpretive reasoning, music-historical knowledge, nuance |
| Claim extraction for verification (§9) | Local OK (structured output) | Extraction, not judgement |
| Gold-set evaluation / LLM-as-judge | Frontier (and a different family from the tutor) | Avoid self-judging bias (cf. MSU-Bench judges = contestants) |
| Similarity / embeddings / generation | Specialised local models | Not an LLM task |

---

## 8. Architecture notes for the tutor

### 8.1 Tool list (function-calling) [speculative design]

Read-only fact tools. Every return includes `provenance`.

1. `get_selection(selection_id)` returns the current UI selection: measure/beat span, staff/voice filter, note IDs.
2. `get_notes(span, staves?, voices?)` returns the compact event table (spelled pitch, MIDI, onset, duration, tie, staff, voice, fingering if present).
3. `get_analysis(span, layer, analyst?)` returns RN labels with key, figure and span; cadences; phrases; form. Sources include `WiR:BPS(Chen&Su)`, `WiR:DT`, `DCML`, `algo:AugmentedNet@v`, etc.
4. `compare_analyses(span, analyst_a, analyst_b)` returns a **computed** diff: identical label; same pitch content but different label (e.g., key-relative re-labelling); different granularity; genuine disagreement.
5. `chord_facts(note_ids | span_beat)` returns pitch-class set, bass, root candidates, quality, inversion, non-chord tones with their type (music21).
6. `voice_leading(span)` returns motions between successive verticalities, parallels, resolutions of sevenths and leading tones.
7. `key_context(span)` returns local key per analyst, plus an algorithmic key profile with confidence.
8. `find_pattern(query, scope)` searches RN n-grams, interval/rhythm motifs and bass lines across the repertoire and corpus. It returns hits with locations and the matching criterion.
9. `similar_passages(span, method={clamp3, aria, rn_ngram}, k)` returns ranked hits, a **why** field and a similarity score.
10. `render_audio(span, variant?)` / `render_score(span, variant?)` for playback and display (no claims).
11. `make_variant(span, transform, params)` covers transpose, reduce, rhythmic simplify, reharmonise-to-label, remove-NCTs, revoice. It returns a **new artefact with provenance** `generated`.
12. `learner_state(concept?)` returns mastery estimates, past errors and spaced-repetition due items.
13. `log_prediction(selection, prediction)` / `grade_prediction(...)` provide backend-side grading against annotations.

*Write tools* (annotations by the learner) should be separate and tagged `analyst: learner`.

### 8.2 Context packet schema (sketch) [speculative]

Note-level values are placeholders for illustration; the analysis items are taken from the local WiR files.

```json
{
  "piece": {"id": "beethoven_op27no2_m1", "title": "...", "edition_source": "...", "licence": "..."},
  "selection": {"id": "sel_42", "span": {"start": "m15.b1", "end": "m17.b2"}, "staves": ["RH","LH"]},
  "notes": [{"id": "m16.b1.LH.v1.n1", "pitch": "C3", "midi": 48, "onset": {"m":16,"beat":1.0,"qoff":120.0},
             "dur_q": 1.0, "staff": "LH", "voice": 1, "tie": null}],
  "analyses": [
    {"layer": "roman", "analyst": "BPS (Chen & Su 2018), via When in Rome (Gotham)", "source_uri": "...analysis.txt#L25",
     "items": [{"span": "m16.b1–m17.b1", "key": "b", "label": "N6"}]},
    {"layer": "roman", "analyst": "DT, via When in Rome", "source_uri": "...analysis_DT.txt#L20-22",
     "items": [{"span": "m16.b1–m16.b2.5", "key": "e", "label": "VI", "alternatives": ["VImaj7", "Ger43"]},
               {"span": "m16.b2.5–m17.b1", "key": "e", "label": "viio7/V"}],
     "analyst_note": "chords here are pretty hard to identify ... VI or Ger or viio7/V"}],
  "computed": {"chord_facts": [...], "diff": [...], "algo_key": {"label": "e", "confidence": 0.61}},
  "learner": {"level": "L1-L2", "recent_errors": ["key-relative-numeral"], "prediction": null},
  "policy": {"reveal_allowed": ["L0","L1"], "must_ask_prediction": true}
}
```

The `policy` block comes from the app's state machine. The LLM is told it may not use labels outside `reveal_allowed`. A post-filter enforces this, because prompting alone is not reliable (Kestin).

### 8.3 Provenance and claim rendering [speculative]

- The LLM must emit **structured output**: a list of segments `{text, claim_type ∈ {fact, analysis, advice, opinion}, citations: [tool_call_id / note_ids / analysis item ids]}`.
- The UI renders: **facts** in plain text with a small location chip (click to highlight the notes); **analysis** as "BPS: N6 · DT: VI (alts Ger4/3)" chips with analyst colour; **advice** in the tutor voice; **opinion** in italics with "interpretation" or "taste" labels.
- **Uncited facts are blocked or visibly flagged** ("unverified"). Location chips are generated from IDs, never from LLM-written bar numbers. That removes the most common error class (locating and counting).

### 8.4 Claim verification and evaluation plan [speculative]

**A. Automatic claim checking (runtime and offline).**

1. Extract claims from tutor output into a typed schema: `ChordLabel(span, analyst?, label, key)`, `PitchContent(span, pcs|notes)`, `Interval(a,b,quality)`, `KeyArea(span,key)`, `Cadence(location,type)`, `Count(pattern, scope, n)`, `Relation(span1, span2, "same"/"sequence"/...)`, `Attribution(analyst, claim)`.
2. Check each claim against the core with music21/partitura, the analysis tables and the pattern search. Results are `verified | contradicted | not-checkable (interpretive)`.
3. **Metrics:** verified-claim precision, contradiction rate per 100 claims, citation validity (does the cited ID contain what is claimed?), attribution accuracy (did it say BPS when the label is DT's?), and leakage (labels revealed outside the policy).
4. Run as a **regression suite** on every prompt or model change. Use transposed and anonymised variants to detect memorisation-driven answers.

**B. Pedagogical evaluation** (small-N, self-study). Use LearnLM-style turn rubrics: asks for a prediction before revealing, keeps to the selected level, no answer leakage, correct misconception typing. Have a frontier model of a *different* family label a sample, and spot-check it yourself. Learning outcome: a delayed unassisted quiz (Bastani lesson) on concepts practised with vs without the tutor (crossover à la Kestin, n = 1, many items).

### 8.5 Gold question set: Moonlight I and Clair de lune (seed items)

Derived from the local When in Rome files. **[confirmed]** against `data/external/when_in_rome/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op027_No2(Moonlight)/1/analysis.txt` (BPS, Chen & Su, converted and proof-read by Gotham), `.../analysis_DT.txt` (analyst "DT"), and `.../Keyboard_Other/Debussy,_Claude/Suite_Bergamasque,_L.75/3_Clair/analysis.txt` (DCML, CC BY‑NC‑SA; DCMLab/debussy_suite_bergamasque @691842d). Answers about *pitch content* must still be checked against the actual score. Items marked † need that check.

| # | Question | Expected answer (source) | Checks |
|---|---|---|---|
| M1 | What metre and opening key do the analyses give for Moonlight I? | 2/2; c♯: i at m1 (both) | Header/key parsing |
| M2 | Where does the music first move to E major, and how is the pivot labelled? | m7 beat 2. BPS: `E: ii`. DT: `iv` in c♯ = `ii` in E (explicit pivot) | Key areas, pivot notation, analyst attribution |
| M3 | How do BPS and DT label m. 4? | BPS: V7 for the whole bar. DT: V7, b1.5 i64, b2 V, b2.5 V7 (finer granularity) | Diff type = granularity |
| M4 | What do the analysts say about m. 16? | BPS: N6 (key b, set at m12). DT: VI in e (key change at m15 b2), alternatives VImaj7 / Ger4/3, then viio7/V at b2.5; DT notes the chords are "pretty hard to identify". † Both labels imply a C-rooted sonority (♭II of b = C; VI of e = C). Verify against notes | Diff type = same-sonority-different-key; uncertainty reporting |
| M5 | At m. 15 beat 2, are BPS's `V/iv` and DT's `e: V` the same chord? | In b minor, V/iv = V of e = B major, so the same chord with a different key interpretation (tonicisation vs local key) † | Key-relative numeral reasoning |
| M6 | How is the m. 32 dominant labelled? | BPS: V7. DT: V9[b9] | Extension disagreement |
| M7 | What does DT say about m. 39 beat 2? | V9[b9b5]; DT note: "'flat five' dominant ninth (D7/G♯ in C♯ minor)" | Attribution and quoting an analyst note |
| M8 | Name every measure BPS labels N6. | 3 (b2), 16, 18, 21, 50, 52, 54 | Count + locate (the classic LLM failure) |
| M9 | Where do BPS's section labels place Development, Recapitulation and Coda? | Development m23, Recap m42 (m42–46 = m5–9), Coda m60 | Form layer; repeat-equivalence notation |
| M10 | How does the movement end harmonically? | Alternating i–V7 (or V65) through mm. 60–65, ending i at m66 (both) | Span reasoning |
| C1 | What is Clair de lune's opening harmony per DCML? | D♭: I6 at m1, i.e. tonic in first inversion, not root position † | Inversion reasoning |
| C2 | Where does DCML show modal mixture with ♭III6? | m27 b3, m28 b3, m35 b3; later mm. 67, 69, 70 (with i64) | Pattern count |
| C3 | Where is the shift to the E-major area, and to what is E enharmonically related in D♭? | m36 b3 (`E: I6`). E = F♭, ♭III of D♭ † (interpretive) | Enharmonic reasoning; the interpretive part tagged |
| C4 | Where does D♭ major return? | m43 (`Db: V7[no3][add4]`) | Key area |
| C5 | What harmony is in force at m42, which has no label line? | ii7 in E, continuing from m41 (RomanText convention: a label holds until the next one) | **Label persistence semantics**. A likely tool/LLM bug |
| C6 | What do the `[no3][add4]` suffixes in m8 vi43 mean? | Third omitted, fourth added: a suspension-like or added-note sonority, resolved at b2 to plain vi43 | DCML label grammar |
| C7 | What is the final chord? | I at m71 | — |

Grow this to about 150 items: about 60 factual (auto-graded), about 50 analytical with expert answer sets (multiple acceptable labels), and about 40 interpretive (rubric-graded, opinion-tagged). Add transposed or anonymised twins for 30 items as a memorisation check.

---

## 9. IDEAS: non-obvious AI-enabled features

Feasibility: H/M/L. Hallucination risk is after mitigation.

1. **Two-analyst debate mode (BPS vs DT on Moonlight; later DCML vs algorithmic).** `compare_analyses` computes the diff first and classifies it (granularity, same-sonority/different-key, extension, genuine disagreement). The LLM then voices each analyst's *likely reasoning* and asks the learner to adjudicate by listening. The m16 case (N6 of b vs VI of e vs Ger4/3) is a perfect first lesson. *Feasibility H. Risk: medium; the LLM may invent motives for an analyst, so tag them "reconstructed rationale, not the analyst's words". Originality: high; no analysis-disagreement tutor found. Evidence: [speculative]; the diffs are [confirmed] from the files.*
2. **Predict-then-reveal, enforced by the state machine.** Before showing m3 b2's label, ask: "the bass moves to D♮; predict the function." Grade against the annotations (accepting any analyst's label) and only then reveal. *Feasibility H. Risk: low (backend grades). Originality: medium (pretesting is known; music-specific enforcement is new). Evidence: pretesting literature [reported], Kestin sequencing [confirmed], Bastani crutch effect [reported].*
3. **Explain by minimal counterexample.** Generate the passage with one change: V7 instead of V9♭9 at m32, root-position I instead of I6 at Clair m1, resolving N6 directly to V without i64. Play original vs counterexample A/B, and the learner says which is Beethoven/Debussy and why. *Feasibility M–H (deterministic edits via music21; audio via the existing synth). Risk: low for facts; medium for the narrative of "why it's worse" (tag as opinion). Originality: high. Evidence: [speculative]; contrasting cases are a known learning-science technique [reported, bg].*
4. **Progression concordance: "where else does this happen?"** An RN n-gram search (key-relative, with optional inversion-insensitivity) over the learner's repertoire and the WiR/DCML corpora, e.g. every `N6 → i64 → V` with locations and a playable list, plus CLaMP 3 "texturally similar" hits clearly separated. *Feasibility H (symbolic), M (embeddings). Risk: low; hits are computed. Originality: medium-high in a learner tool. Evidence: [confirmed] the tools exist; usefulness [speculative].*
5. **Uncertainty heat-map ("where the experts disagree or the algorithm hesitates").** Overlay inter-analyst disagreement plus AugmentedNet/AnalysisGNN entropy on the score; those spots become the "interesting places" for discussion. *Feasibility M. Risk: low. Originality: high. Evidence: [speculative]; masked-completion RN models [confirmed, ISMIR 2026 abstract].*
6. **Claim badges with live verification.** Every tutor sentence has a fact-type badge. Facts show ✓ (verified by the core), ✗ (contradicted, auto-retracted) or "interpretive". The learner can click "show me" to highlight the evidence notes. *Feasibility M (structured output + checker). Risk: this is the mitigation itself. Originality: medium (citation UIs exist; music-specific verification is new). Evidence: CSyMR tool-grounding gains [confirmed].*
7. **Reduction ladder.** Use a slider: surface (triplets) → block chords → outer voices → bass + RN → tonal skeleton. Play each rung, ask "what survived?", and the tutor explains at the matching level. *Feasibility H (deterministic). Risk: low; the higher rungs (Schenker-like) are interpretive, so tag them. Originality: medium. Evidence: [speculative].*
8. **Blind-transposed probe (defeats memorisation for both learner and LLM).** Present m15–m18 transposed to another key with the title hidden; the learner analyses, then sees it is Moonlight. It doubles as the LLM memorisation check in evaluation. *Feasibility H. Risk: low. Originality: medium-high. Evidence: memorisation concern [reported] (Grok identified Chopin; WildScore text-only ≈ image).*
9. **Misconception-typed feedback.** The learner's wrong label (e.g., "V/V" for DT's viio7/V) is classified by a deterministic comparator (quality vs root vs key vs inversion error). The LLM only phrases feedback for that error type and picks a targeted follow-up from your repertoire. *Feasibility H. Risk: low. Originality: medium. Evidence: ITS tradition [reported].*
10. **Performance-diff tutor (Piano Tutor, 2026 edition).** Align your MIDI performance with the score (partitura). Compute timing, dynamics and pedal deviations per beat, and relate them to harmonic events ("you rush the N6 arrivals at mm. 16 and 18; many pianists lean into them"). Tag the last clause as advice/opinion and, ideally, ground it in reference-performance data. *Feasibility M. Risk: medium for advice and style claims. Originality: high in combination with the harmonic layer. Evidence: Dannenberg lineage [confirmed]; performance-harmony coupling [speculative].*
11. **Inner-hearing check with generated alternatives.** Before playing m40–41, the learner imagines the continuation. The app plays three AMT/Aria-generated continuations plus the real one, and the learner picks which matches the sound they imagined. The reveal discusses expectation (possibly an IDyOM-style surprise estimate). *Feasibility M. Risk: generated items must be clearly labelled; licence of AMT weights unstated. Originality: high. Evidence: [speculative].*
12. **Keyboard-geometry narrator.** For a progression, compute hand-shape transitions (finger-distance, black/white pattern, common-tone fingers) and explain why it "feels" as it does under the hand; for example the Moonlight triplet figure's shifting shape across N6. *Feasibility M (geometry deterministic; fingering models like PIG-trained ones optional). Risk: low-medium. Originality: high. Evidence: [speculative].*
13. **Repertoire-derived spaced repetition.** Cards are made from *your* pieces ("hear m3 b2 → name function", "spell N6 in b"), scheduled by FSRS, with answers drawn from the analysis layers. *Feasibility H. Risk: low. Originality: medium. Evidence: spacing/retrieval practice [reported, bg].*
14. **Teach-the-tutor mode (teachable agent).** The learner explains m25 ("the key shift here is very elusive", per DT) to a deliberately naive agent. The agent asks probing questions and the backend checks the learner's factual statements. *Feasibility M. Risk: medium (agent may accept wrong claims; backend must flag them). Originality: medium (Chat Melody precedent). Evidence: [reported] n = 28 study.*
15. **Analysis-language translator.** Convert between RomanText, DCML labels, figured bass and plain-English description (e.g., `#viio2[no5][no3][add6][add4]/vi` from Clair m2 → "a leading-tone seventh of vi with notes omitted and added…"). Generate the translation by deterministic label parsing; the LLM only smooths the prose. *Feasibility H. Risk: low if the parse is deterministic. Originality: medium. Evidence: [speculative].*

---

## 10. Open questions and next steps

1. Run the **representation experiment** (§4.2) and the **gold-set baseline** (§8.5) on 2–3 models (one frontier API, one local about 30B MoE) before building the UI. That tells you how much the claim-checker has to catch.
2. Decide on the **algorithmic RN analyst** (AugmentedNet vs AnalysisGNN vs the ISMIR 2026 interactive model). Check licences and Apple-Silicon inference.
3. Verify the **licences of model weights** (AMT on HF, Moonbeam, Legato) before integrating.
4. Keep track of **DCML CC BY‑NC‑SA** obligations if anything is ever shared.
5. Watch: MSU-Bench follow-ups with 2026 models, MusICA-style auto-generated benchmarks (directly reusable as the eval harness), Legato 2 releases (PDF import).

## Sources (primary unless noted)

- ChatMusician / MusicTheoryBench: https://arxiv.org/abs/2402.16153 ; model card https://huggingface.co/m-a-p/ChatMusician
- ZIQI-Eval: https://arxiv.org/abs/2406.15885 ; SongSage (secondary numbers): https://arxiv.org/abs/2601.01153
- Can LLMs "Reason" in Music?: https://arxiv.org/abs/2407.21531
- Pond & Fujinaga 2025: https://arxiv.org/abs/2503.22853
- CMI-Bench: https://arxiv.org/abs/2506.12285
- WildScore: https://arxiv.org/abs/2509.04744
- ABC-Eval: https://arxiv.org/abs/2509.23350
- MSU-Bench: https://arxiv.org/abs/2511.20697
- CSyMR-Bench: https://arxiv.org/abs/2601.11556
- LilyBench: https://arxiv.org/abs/2606.08722
- MusICA-MetaBench: https://arxiv.org/abs/2607.06015
- Carone et al. 2026: https://proceedings.mlr.press/v303/carone26a.html
- Augmented Fifth blog (informal): https://aug5th.substack.com/p/llms-vs-harmonic-analysis ; https://aug5th.substack.com/p/testing-llms-on-undergraduate-music
- Karystinaios et al. ISMIR 2026: https://arxiv.org/abs/2607.13587 ; AnalysisGNN: https://arxiv.org/abs/2509.06654 ; AugmentedNet: https://archives.ismir.net/ismir2021/paper/000050.pdf
- NotaGen: https://arxiv.org/abs/2502.18008 , https://github.com/ElectricAlexis/NotaGen
- MuPT: https://huggingface.co/m-a-p/MuPT-v1-8192-1.97B
- CLaMP 3: https://arxiv.org/abs/2502.10362 , https://github.com/sanderwood/clamp3
- Aria: https://arxiv.org/abs/2506.23869 , https://github.com/EleutherAI/aria
- Anticipatory Music Transformer: https://arxiv.org/abs/2306.08620 , https://github.com/jthickstun/anticipation
- Moonbeam: https://arxiv.org/abs/2505.15559
- Text2midi: https://github.com/AMAAI-Lab/Text2midi
- MIDI-LLM: https://arxiv.org/abs/2511.03942
- MIDI-LLaMA: https://arxiv.org/abs/2601.21740
- Legato / Legato 2: https://arxiv.org/abs/2506.19065 , https://arxiv.org/abs/2607.05769
- music21-mcp-server: https://github.com/brightlikethelight/music21-mcp-server
- Piano Tutor bibliography: https://www.cs.cmu.edu/afs/cs/Web/People/rbd/bib-ptutor.html
- Kestin et al. 2025: https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/
- Bastani et al. 2025: https://papers.ssrn.com/abstract=4895486 (PNAS DOI 10.1073/pnas.2422633122)
- Pretesting: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12292081/ ; Akgun & Toker: https://arxiv.org/abs/2504.10249
- Chat Melody teachable agent: https://arxiv.org/abs/2504.00636
- LearnLM (secondary): https://arxiv.org/abs/2407.12687
- CIPI difficulty: https://arxiv.org/abs/2306.08480 ; PSyllabus: https://zenodo.org/records/14794592 ; difficulty-aware generation: https://arxiv.org/abs/2509.16913 ; Pierce et al.: https://pmc.ncbi.nlm.nih.gov/articles/PMC7948302/
- ITS meta-analysis (Kulik & Fletcher): https://www.ida.org/research-and-publications/publications/all/e/ef/effectiveness-of-intelligent-tutoring-systems-a-meta-analytic-review
- Local LLM guide (blog-grade): https://bestllmfor.com/guides/mlx-local-llm-apple-silicon/
