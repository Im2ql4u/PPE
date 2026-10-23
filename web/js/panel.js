import { h } from "preact";
import { useState } from "preact/hooks";
import htm from "htm";
import {
  harmonyOf, playSelection, select, selectLabel, setMode, setPrimary, setSpeed, setTranspose, stopPlayback,
  toggleLoop, togglePedal, toggleTrack,
} from "./actions.js";
import { useStore } from "./store.js";

const html = htm.bind(h);

const CLS_LABEL = {
  same: "Agree", key_frame: "Different key", inversion: "Different bass", extension: "Extra chord tone",
  other_quality: "Different quality", other_chord: "Different chord",
};
const MODE_ORDER = ["original", "blocked", "outer", "melody", "bass", "chord_tones", "progression"];

export function Panel() {
  const piece = useStore((s) => s.piece);
  const selection = useStore((s) => s.selection);
  const inspect = useStore((s) => s.inspect);
  if (!piece) return html`<aside class="panel"></aside>`;
  return html`
    <aside class="panel">
      ${selection && inspect && !inspect.empty
        ? html`<${Selection} piece=${piece} inspect=${inspect} selection=${selection} />`
        : html`<${Intro} piece=${piece} />`}
      <${Listen} piece=${piece} />
      <${Transform} piece=${piece} />
      <${Provenance} piece=${piece} />
    </aside>`;
}

function Intro({ piece }) {
  return html`
    <section class="intro">
      <h2>${piece.title}</h2>
      <p class="sub">${piece.composer} · ${piece.subtitle}</p>
      <p>Click a <b>note</b>, double-click for its <b>chord</b>, click empty space for a <b>measure</b>, or click a label under the staff for a <b>harmony</b>. Shift-click extends a selection.</p>
      <p class="keys"><kbd>←</kbd><kbd>→</kbd> step through the harmonies · <kbd>Space</kbd> play · <kbd>Esc</kbd> clear</p>
      ${piece.analyses.length > 1 && html`<p class="hint">Notes shown in <span class="disputed-sample">red</span> are those the two analysts disagree about: a chord tone for one, a passing or neighbour note for the other.</p>`}
    </section>`;
}

function Selection({ piece, inspect, selection }) {
  const primary = useStore((s) => s.primary);
  const chord = inspect.chord;
  const bassNote = inspect.bass;
  return html`
    <section class="selection">
      <header class="sel-head">
        <h2>${inspect.span.text}</h2>
        <button class="ghost" onClick=${() => select(null)} title="Clear (Esc)">Clear</button>
      </header>
      <div class="sounding">
        <div class="pcs">${inspect.pitch_classes.map((p) => html`<span class="pc">${p}</span>`)}</div>
        ${chord && html`<p class="chord-id">${chordName(chord)}${chord.bass !== chord.root && chord.root ? html`<span class="muted">, ${chord.bass} in the bass</span>` : ""}</p>`}
        ${!chord && inspect.intervals.length === 1 && html`<p class="chord-id">${inspect.intervals[0].low}–${inspect.intervals[0].high} <span class="muted">· ${inspect.intervals[0].name.toLowerCase()}</span></p>`}
        ${chord && inspect.intervals.length > 1 && html`<p class="intervals muted">Above ${bassNote}: ${inspect.intervals.slice(0, 5).map((i, k) => html`${k > 0 ? " · " : ""}<span class="iv">${i.high} <i>${i.name.toLowerCase()}</i></span>`)} <span class="figs" title="Figured-bass reading: intervals above the bass">(${inspect.intervals.map((i) => i.number).sort((a, b) => b - a).join("/")})</span></p>`}
      </div>
      <div class="readings">
        ${inspect.lenses.map((l) => html`<${Reading} piece=${piece} lens=${l} primary=${primary} selection=${selection} />`)}
      </div>
      ${inspect.comparisons.map((c) => html`<${Comparison} c=${c} piece=${piece} />`)}
      <${VoiceLeading} inspect=${inspect} primary=${primary} piece=${piece} />
    </section>`;
}

function chordName(c) {
  const name = (c.name || "").replace(/^enharmonic equivalent to /i, "");
  return c.root && c.is_tertian ? `${c.root} ${name}` : name;
}

function Reading({ piece, lens, primary, selection }) {
  const [more, setMore] = useState(false);
  const an = piece.analyses.find((a) => a.id === lens.analysis);
  // readings come from the inspection (spelled in the current transposition)
  const labels = lens.readings || [];
  const lab = labels.find((l) => l.id === lens.primary) || labels[0];
  if (!lab) return null;
  const ex = lab.explanation;
  return html`
    <article class=${"reading" + (an.id === primary ? " primary" : "")} style=${`--lens:${an.colour}`}>
      <header>
        <button class="lens-name" onClick=${() => setPrimary(an.id)} title="Use this reading for the keyboard and chord-tone colours">
          <span class="dot"></span>${an.id}
        </button>
        <span class="analyst">${an.analyst}${an.kind === "automatic" ? html` <span class="tag">automatic</span>` : ""}</span>
      </header>
      ${labels.length > 1
        ? html`<div class="progression">${labels.map((l, i) => html`${i > 0 && html`<span class="arrow">→</span>`}<button class="fig small" onClick=${() => selectLabel(l)}>${l.display}</button>`)}</div>`
        : html`<div class="figure-line"><span class="fig">${lab.display}</span><span class="in">in ${lab.key.label}</span></div>`}
      ${ex.gist && html`<p class="gist">${ex.gist}</p>`}
      <p class="instance">${ex.instance}</p>
      ${lab.alternatives.length > 0 && html`<p class="alts">The analyst also considered: ${lab.alternatives.join(" · ")}</p>`}
      ${lens.notes.map((n) => html`<blockquote>“${n.text}”<cite>${an.id}, m. ${n.m}</cite></blockquote>`)}
      ${ex.general && html`<button class="more" onClick=${() => setMore(!more)}>${more ? "Less" : `About ${ex.family} chords`}</button>`}
      ${more && html`<p class="general">${ex.general}</p>`}
    </article>`;
}

function Comparison({ c, piece }) {
  if (c.cls === "same") {
    return html`<p class="compare same"><span class="badge">${CLS_LABEL.same}</span> ${c.a} and ${c.b} read this the same way.</p>`;
  }
  return html`
    <div class=${"compare " + c.cls}>
      <span class="badge">${CLS_LABEL[c.cls]}</span>
      <p>${c.text}</p>
      ${c.disputed_notes.length > 0 && html`<p class="muted small">${c.disputed_notes.length} selected note${c.disputed_notes.length > 1 ? "s" : ""} change role between the readings (red in the score).</p>`}
    </div>`;
}

function VoiceLeading({ inspect, primary }) {
  const lens = inspect.lenses.find((l) => l.analysis === primary);
  const vl = lens?.voice_leading;
  if (!vl) return null;
  return html`
    <div class="voice-leading">
      <h3>Moving on to ${vl.to}</h3>
      <p class="moves">${vl.moves.map((m) => html`<span class="move">${m.from}<span class="arr">${m.semitones === 0 ? "=" : m.semitones > 0 ? "↗" : "↘"}</span>${m.to}${m.semitones !== 0 ? html`<sub>${m.semitones > 0 ? "+" : ""}${m.semitones}</sub>` : ""}</span>`)}</p>
      <p class="muted small">${vl.common_tones.length ? `Common tone${vl.common_tones.length > 1 ? "s" : ""}: ${vl.common_tones.join(", ")}. ` : "No common tones. "}Smallest total motion: ${vl.total} semitone${vl.total === 1 ? "" : "s"}.</p>
    </div>`;
}

function Listen({ piece }) {
  const mode = useStore((s) => s.mode);
  const playing = useStore((s) => s.playing);
  const loop = useStore((s) => s.loop);
  const pedal = useStore((s) => s.pedal);
  const speed = useStore((s) => s.speed);
  const tracks = useStore((s) => s.tracks);
  const primary = useStore((s) => s.primary);
  const selection = useStore((s) => s.selection);
  const info = piece.modes[mode];
  const allOn = !tracks.length;
  return html`
    <section class="listen">
      <h3>Listen</h3>
      <div class="transport">
        <button class="play" onClick=${() => (playing ? stopPlayback() : playSelection({ restart: true }))}>
          ${playing ? "■ Stop" : selection ? "▶ Play" : "▶ Play all"}
        </button>
        <button class=${"toggle" + (loop ? " on" : "")} onClick=${toggleLoop} title="Loop (L)">Loop</button>
        ${piece.analyses.length > 0 && html`<button class=${"toggle" + (pedal ? " on" : "")} onClick=${togglePedal}
          title=${`Sustain pedal, changed at each harmony of ${primary}. A simulation: the score's own pedal marks are not used.`}>Pedal</button>`}
        <select class="speed" value=${speed} onChange=${(e) => setSpeed(Number(e.target.value))} title="Speed">
          ${[0.5, 0.67, 0.8, 1, 1.25].map((v) => html`<option value=${v}>${v === 1 ? "1×" : `${v}×`}</option>`)}
        </select>
      </div>
      <div class="modes">
        ${MODE_ORDER.filter((m) => piece.modes[m] && (!piece.modes[m].needs_analysis || piece.analyses.length)).map((m) => html`
          <button class=${"mode" + (mode === m ? " on" : "")} onClick=${() => setMode(m)}>${piece.modes[m].name}</button>`)}
      </div>
      <p class="mode-about">${info.about}${info.needs_analysis ? html` <span class="lens-inline" style=${`--lens:${piece.analyses.find((a) => a.id === primary)?.colour}`}>Using ${primary}.</span>` : ""}</p>
      ${piece.tracks.length > 1 && html`<div class="tracks">
        ${piece.tracks.map((t) => html`<button class=${"track" + (allOn || tracks.includes(t.id) ? " on" : "")} title=${t.rule} onClick=${() => toggleTrack(t.id)}>${t.name}</button>`)}
      </div>`}
    </section>`;
}

function Transform({ piece }) {
  const transpose = useStore((s) => s.transpose);
  const info = useStore((s) => s.transposeInfo);
  const alt = useStore((s) => s.alternatives);
  const sub = useStore((s) => s.substitution);
  const selection = useStore((s) => s.selection);
  const firstKey = piece.analyses[0]?.labels[0]?.key;
  const keyName = info?.key_names ? (firstKey?.mode === "minor" ? `${info.key_names.minor} minor` : `${info.key_names.major} major`) : "";
  const lab = harmonyOf(selection);
  return html`
    <section class="transform">
      <h3>Transform</h3>
      <div class="row transpose">
        <span class="label">Transpose</span>
        <button class="step" onClick=${() => setTranspose(transpose - 1)} title="Down a semitone ([)">−</button>
        <span class="value">${transpose === 0 ? "Original key" : `${transpose > 0 ? "+" : ""}${transpose} · ${keyName}`}</span>
        <button class="step" onClick=${() => setTranspose(transpose + 1)} title="Up a semitone (])">+</button>
      </div>
      ${transpose !== 0 && html`<p class="muted small">Score, sound and keyboard move; the scale degrees under the keys don't. That sameness is the relationship.</p>`}
      ${alt && lab && html`
        <div class="substitute">
          <p class="label">What if this chord were different? <span class="muted">Original: ${alt.original.display} (${alt.original.pitches.join("–")})</span></p>
          <button class=${"cand original" + (!sub ? " on" : "")} onClick=${() => playSelection({ restart: true })}>
            <span class="fig small">${alt.original.display}</span><span class="pitches">as written</span><span class="play-ico">▶</span>
          </button>
          ${alt.candidates.map((c) => html`
            <button class=${"cand" + (sub?.figure === c.figure ? " on" : "")} title=${c.gist}
              onClick=${() => playSelection({ restart: true, substitution: c.figure })}>
              <span class="fig small">${c.display}</span>
              <span class="pitches">${c.pitches_text}</span>
              <span class="dist" title="Smallest total voice-leading motion from the original chord">${c.distance} st</span>
              <span class="play-ico">▶</span>
            </button>`)}
          <p class="muted small">Each chord tone moves to the nearest note of the same role (root to root, third to third); the rhythm and texture stay as written. Rule-based, not a model.</p>
        </div>`}
      ${!lab && html`<p class="muted small">Select a harmony (click a label under the staff, or double-click a note) to try other chords in its place.</p>`}
    </section>`;
}

function Provenance({ piece }) {
  const [open, setOpen] = useState(false);
  const v = piece.validation;
  return html`
    <section class="provenance">
      <button class="more" onClick=${() => setOpen(!open)}>${open ? "Hide" : "Sources, licences and checks"}</button>
      ${open && html`
        <dl>
          <dt>Score</dt><dd>${piece.score.source}<br /><span class="muted">${piece.score.licence}</span></dd>
          ${piece.analyses.map((a) => html`<dt style=${`color:${a.colour}`}>${a.id}</dt><dd>${a.analyst}. ${a.source}. <span class="muted">${a.licence}</span>
            ${v.alignment?.[a.id] && html`<br /><span class="muted">Alignment check: ${(v.alignment[a.id]["0"] * 100).toFixed(1)}% of notes are chord tones at the analysis' position (vs ≤${(Math.max(v.alignment[a.id]["-1 beat"], v.alignment[a.id]["+1 beat"]) * 100).toFixed(0)}% when shifted by a beat).</span>`}
            ${a.issues.length > 0 && html`<br /><span class="warn">Data notes: ${a.issues.join(" · ")}</span>`}</dd>`)}
          <dt>Notation check</dt><dd>${(v.crosscheck_agreement * 100).toFixed(1)}% of notes agree between Verovio and an independent ${v.independent_parser} parse.${v.known_discrepancy_note ? html`<br /><span class="muted">${v.known_discrepancy_note}</span>` : ""}</dd>
          ${v.reference && html`<dt>Edition check</dt><dd>${v.reference.agreeing} of ${v.reference.reference_notes} noteheads agree with a second encoding. <span class="muted">${v.reference.note}</span></dd>`}
          ${piece.comparisons.map((c) => html`<dt>${c.a} vs ${c.b}</dt><dd>Same reading for ${(c.summary.strict_agreement * 100).toFixed(0)}% of the piece's duration; same chord in a different key ${(c.summary.fractions.key_frame * 100).toFixed(0)}%; an extra chord tone ${(c.summary.fractions.extension * 100).toFixed(0)}%.</dd>`)}
        </dl>`}
    </section>`;
}
