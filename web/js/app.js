import { h, render } from "preact";
import { useEffect } from "preact/hooks";
import htm from "htm";
import {
  loadPieces, openPiece, playSelection, select, setNoteColour, setTranspose, setZoom, step, toggleLens, toggleLoop,
  writeHash,
} from "./actions.js";
import { Keyboard } from "./keyboard.js";
import { Panel } from "./panel.js";
import { Score } from "./score.js";
import { getState, setState, useStore } from "./store.js";

const html = htm.bind(h);

function Header() {
  const pieces = useStore((s) => s.pieces);
  const pieceId = useStore((s) => s.pieceId);
  const piece = useStore((s) => s.piece);
  const lenses = useStore((s) => s.lenses);
  const noteColour = useStore((s) => s.noteColour);
  const zoom = useStore((s) => s.zoom);
  return html`
    <header class="top">
      <div class="brand"><span class="mark">𝄞</span>Passage Laboratory</div>
      <div class="piece-pick">
        <select value=${pieceId || ""} onChange=${(e) => openPiece(e.target.value)} aria-label="Piece">
          ${pieces.map((p) => html`<option value=${p.id} disabled=${!p.built}>${p.composer.split(" ").slice(-1)[0]} — ${p.title}${p.built ? "" : " (not built)"}</option>`)}
        </select>
      </div>
      <div class="spacer"></div>
      ${piece && piece.analyses.length > 0 && html`
        <div class="group" role="group" aria-label="Analyses shown under the staff">
          <span class="group-label">Readings</span>
          ${piece.analyses.map((a) => html`<button class=${"lens-chip" + (lenses.includes(a.id) ? " on" : "")} style=${`--lens:${a.colour}`}
            title=${a.analyst} onClick=${() => toggleLens(a.id)}><span class="dot"></span>${a.id}</button>`)}
        </div>
        <div class="group" role="group" aria-label="Note colouring">
          <span class="group-label">Notes</span>
          ${[["plain", "Plain"], ["chordtones", "Chord tones"], ...(piece.analyses.length > 1 ? [["disagreement", "Disagreement"]] : [])].map(([k, v]) => html`
            <button class=${"seg" + (noteColour === k ? " on" : "")} onClick=${() => setNoteColour(k)}>${v}</button>`)}
        </div>`}
      <div class="group zoom" role="group" aria-label="Zoom">
        <button class="seg" onClick=${() => setZoom(zoom - 4)} title="Smaller">−</button>
        <button class="seg" onClick=${() => setZoom(zoom + 4)} title="Larger">+</button>
      </div>
    </header>`;
}

function ErrorToast() {
  const error = useStore((s) => s.error);
  if (!error) return null;
  return html`<div class="toast" role="alert" onClick=${() => setState({ error: null })}>${error}<span class="x">×</span></div>`;
}

function Empty() {
  const pieces = useStore((s) => s.pieces);
  const loading = useStore((s) => s.loading);
  if (loading) return html`<div class="empty"><p>Opening the score…</p></div>`;
  if (pieces.length && !pieces.some((p) => p.built)) {
    return html`<div class="empty"><h2>No pieces built yet</h2><p>Run <code>uv run python -m ppe fetch</code> and <code>uv run python -m ppe build</code>, then reload.</p></div>`;
  }
  return html`<div class="empty"><p>Loading…</p></div>`;
}

function App() {
  const piece = useStore((s) => s.piece);
  const selection = useStore((s) => s.selection);
  const transpose = useStore((s) => s.transpose);
  const mode = useStore((s) => s.mode);
  useEffect(() => { writeHash(); }, [piece?.id, selection, transpose, mode]);
  useEffect(() => {
    loadPieces().catch((e) => setState({ error: String(e.message || e) }));
    const onKey = (e) => {
      if (e.target.closest("input, select, textarea")) return;
      if (e.key === " ") { e.preventDefault(); playSelection(); }
      else if (e.key === "ArrowRight") { e.preventDefault(); step(+1); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); step(-1); }
      else if (e.key === "Escape") select(null);
      else if (e.key === "l" || e.key === "L") toggleLoop();
      else if (e.key === "]") setTranspose(getState().transpose + 1);
      else if (e.key === "[") setTranspose(getState().transpose - 1);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);
  return html`
    <div class="app">
      <${Header} />
      <main class="stage">
        ${piece ? html`<${Score} />` : html`<${Empty} />`}
        <${Panel} />
      </main>
      <footer class="keys-area"><${Keyboard} /></footer>
      <${ErrorToast} />
    </div>`;
}

render(html`<${App} />`, document.getElementById("root"));
