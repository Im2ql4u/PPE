// Coordination: selection -> inspection -> keyboard/panel, playback, transformation.
import * as api from "./api.js";
import * as audio from "./audio.js";
import { getState, setState } from "./store.js";
import { labelAt, notesIn, spanOf, stepHarmony } from "./util.js";

let inspectSeq = 0;

export async function loadPieces() {
  const pieces = await api.listPieces();
  setState({ pieces });
  const link = readHash();
  const saved = link.piece || localStorageGet("ppe.piece");
  const first = pieces.find((p) => p.id === saved && p.built) || pieces.find((p) => p.built);
  if (!first) return;
  await openPiece(first.id);
  if (first.id === link.piece) await applyLink(link);
}

// Deep links: #piece=moonlight&s=60&e=64&t=2&mode=blocked&lens=DT  (s/e in quarter notes)
function readHash() {
  const p = new URLSearchParams(window.location.hash.slice(1));
  const num = (k) => (p.has(k) ? Number(p.get(k)) : null);
  return { piece: p.get("piece"), s: num("s"), e: num("e"), t: num("t"), mode: p.get("mode"), lens: p.get("lens"), colour: p.get("notes") };
}

async function applyLink(link) {
  const patch = {};
  if (link.t) patch.transpose = link.t;
  if (link.mode) patch.mode = link.mode;
  if (link.colour) patch.noteColour = link.colour;
  if (link.lens) patch.primary = link.lens;
  setState(patch);
  if (link.s != null && link.e != null) {
    const lab = labelAt(primaryLabels(), link.s);
    const isLabel = lab && Math.abs(lab.on - link.s) < 1e-6 && Math.abs(lab.end - link.e) < 1e-6;
    await select(isLabel ? { kind: "harmony", start: lab.on, end: lab.end, label: lab.id } : { kind: "span", start: link.s, end: link.e });
  }
}

export function writeHash() {
  const st = getState();
  if (!st.pieceId) return;
  const p = new URLSearchParams({ piece: st.pieceId });
  if (st.selection) { p.set("s", +st.selection.start.toFixed(4)); p.set("e", +st.selection.end.toFixed(4)); }
  if (st.transpose) p.set("t", st.transpose);
  if (st.mode !== "original") p.set("mode", st.mode);
  const h = "#" + p.toString();
  if (window.location.hash !== h) history.replaceState(null, "", h);
}

export async function openPiece(id) {
  audio.stop();
  setState({ loading: true, error: null, pieceId: id, piece: null, selection: null, inspect: null,
             transpose: 0, alternatives: null, substitution: null, playing: false });
  try {
    const piece = await api.getPiece(id);
    const ids = piece.analyses.map((a) => a.id);
    setState({ piece, loading: false, lenses: ids.slice(0, 2), primary: ids[0] || null,
               noteColour: ids.length > 1 ? "disagreement" : "plain", tracks: [], mode: "original" });
    localStorageSet("ppe.piece", id);
  } catch (e) {
    setState({ loading: false, error: String(e.message || e) });
  }
}

export function primaryLabels() {
  const { piece, primary } = getState();
  return piece?.analyses.find((a) => a.id === primary)?.labels || [];
}

export async function select(sel) {
  const { pieceId } = getState();
  if (!sel) {
    setState({ selection: null, inspect: null, alternatives: null, substitution: null });
    return;
  }
  setState({ selection: sel, alternatives: null, substitution: null });
  const seq = ++inspectSeq;
  try {
    const result = await api.inspect(pieceId, sel);
    if (seq !== inspectSeq) return;
    setState({ inspect: result });
    // A selection that sits within one harmony offers chord substitutions.
    const lab = harmonyOf(sel);
    if (lab) {
      const alt = await api.alternatives(pieceId, lab.id);
      if (seq === inspectSeq) setState({ alternatives: alt });
    }
  } catch (e) {
    if (seq === inspectSeq) setState({ error: String(e.message || e) });
  }
}

/** The primary analysis' label that contains the whole selection, if any. */
export function harmonyOf(sel) {
  if (!sel) return null;
  const lab = labelAt(primaryLabels(), sel.start);
  return lab && sel.end <= lab.end + 1e-9 ? lab : null;
}

export function selectNote(noteId, extend) {
  const { piece, selection } = getState();
  const n = piece.notes.find((x) => x.id === noteId);
  if (!n) return;
  if (extend && selection) {
    const start = Math.min(selection.start, n.on);
    const end = Math.max(selection.end, n.on + n.dur);
    return select({ kind: "span", start, end });
  }
  return select({ kind: "note", ids: [n.id], start: n.on, end: n.on + n.dur });
}

export function selectChordAt(noteId) {
  const { piece } = getState();
  const n = piece.notes.find((x) => x.id === noteId);
  const lab = n && labelAt(primaryLabels(), n.on);
  if (lab) return selectLabel(lab);
  const vertical = piece.notes.filter((x) => Math.abs(x.on - n.on) < 1e-9);
  return select({ kind: "chord", ids: vertical.map((x) => x.id), ...spanOf(vertical) });
}

export const selectLabel = (lab) => select({ kind: "harmony", start: lab.on, end: lab.end, label: lab.id });

export function selectMeasure(number, extend) {
  const { piece, selection } = getState();
  const m = piece.measures.find((x) => x.n === number);
  if (!m) return;
  if (extend && selection) {
    return select({ kind: "span", start: Math.min(selection.start, m.on), end: Math.max(selection.end, m.on + m.dur) });
  }
  return select({ kind: "measure", start: m.on, end: m.on + m.dur, measure: number });
}

export function step(dir) {
  const { selection } = getState();
  const labels = primaryLabels();
  const t = selection ? selection.start : -1;
  const lab = selection ? stepHarmony(labels, t, dir) : labels[0];
  if (!lab) return;
  selectLabel(lab).then(() => playSelection());
}

export async function playSelection(opts = {}) {
  const st = getState();
  if (!st.piece) return;
  if (audio.isPlaying() && !opts.restart) {
    audio.stop();
    return;
  }
  const sel = st.selection || { start: 0, end: st.piece.end };
  const lab = harmonyOf(sel);
  const body = {
    start: sel.start, end: sel.end,
    mode: opts.mode || st.mode,
    analysis: st.primary,
    tracks: st.tracks.length ? st.tracks : null,
    transpose: st.transpose,
    substitution: opts.substitution && lab ? { label: lab.id, figure: opts.substitution } : null,
  };
  if (sel.kind === "note" || sel.kind === "chord") {
    // a single note or vertical: hear it with its harmony's texture? Keep it literal: the selected notes.
    body.mode = "original";
  }
  let res;
  try {
    res = await api.playback(st.pieceId, body);
  } catch (e) {
    setState({ error: String(e.message || e) });
    return;
  }
  let events = res.events;
  if (sel.ids && (sel.kind === "note" || sel.kind === "chord")) {
    const want = new Set(sel.ids);
    events = events.filter((e) => e.ids.some((id) => want.has(id)));
    if (events.length) {
      // make a single note or chord audible for a moment
      events = events.map((e) => ({ ...e, onset: sel.start, duration: Math.max(e.duration, 1.5) }));
    }
  }
  const end = Math.max(sel.end, ...events.map((e) => e.onset + e.duration));
  setState({ playing: true, substitution: opts.substitution ? { label: lab?.id, figure: opts.substitution } : null });
  audio.play(events, {
    qpm: res.qpm, speed: st.speed, start: sel.start, end, loop: st.loop,
    onTick: (ids, midis) => setState({ playingIds: ids, playingMidis: midis }),
    onEnd: () => setState({ playing: false, playingIds: new Set(), playingMidis: new Set() }),
  });
}

export function stopPlayback() {
  audio.stop();
}

export const setMode = (mode) => setState({ mode });
export const setSpeed = (speed) => setState({ speed });
export const toggleLoop = () => setState((s) => ({ loop: !s.loop }));
export const setTranspose = (n) => setState({ transpose: Math.max(-6, Math.min(6, n)) });
export const setNoteColour = (noteColour) => setState({ noteColour });
export const setZoom = (zoom) => setState({ zoom: Math.max(28, Math.min(56, zoom)) });

export function toggleTrack(id) {
  setState((s) => {
    const all = s.piece.tracks.map((t) => t.id);
    let cur = s.tracks.length ? [...s.tracks] : [...all];
    cur = cur.includes(id) ? cur.filter((x) => x !== id) : [...cur, id];
    if (!cur.length || cur.length === all.length) cur = [];
    return { tracks: cur };
  });
}

export function toggleLens(id) {
  setState((s) => {
    const on = s.lenses.includes(id) ? s.lenses.filter((x) => x !== id) : [...s.lenses, id];
    return { lenses: on, primary: on.includes(s.primary) ? s.primary : on[0] || s.primary };
  });
}

export const setPrimary = (id) => setState((s) => ({ primary: id, lenses: s.lenses.includes(id) ? s.lenses : [...s.lenses, id] }));

export function notesForSelection() {
  const { piece, selection } = getState();
  if (!piece || !selection) return [];
  if (selection.ids) return piece.notes.filter((n) => selection.ids.includes(n.id));
  return notesIn(piece.notes, selection.start, selection.end);
}

function localStorageGet(k) {
  try { return window.localStorage.getItem(k); } catch { return null; }
}
function localStorageSet(k, v) {
  try { window.localStorage.setItem(k, v); } catch { /* private mode */ }
}
