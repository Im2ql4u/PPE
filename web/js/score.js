import { h } from "preact";
import { useEffect, useLayoutEffect, useMemo, useRef, useState } from "preact/hooks";
import htm from "htm";
import * as api from "./api.js";
import { selectChordAt, selectLabel, selectMeasure, selectNote } from "./actions.js";
import { setState, useStore } from "./store.js";
import { buildAnchors, layoutLane, xAt } from "./util.js";

const html = htm.bind(h);

/** Disputed notes between the first two shown lenses: chord-tone status differs. */
function disputedSet(piece, lenses) {
  if (!piece || lenses.length < 2) return new Set();
  const [a, b] = lenses;
  const out = new Set();
  for (const [id, st] of Object.entries(piece.statuses)) {
    const sa = st[a], sb = st[b];
    if (sa != null && sb != null && (sa === "non-chord") !== (sb === "non-chord")) out.add(id);
  }
  return out;
}

export function Score() {
  const piece = useStore((s) => s.piece);
  const transpose = useStore((s) => s.transpose);
  const zoom = useStore((s) => s.zoom);
  const lenses = useStore((s) => s.lenses);
  const selection = useStore((s) => s.selection);
  const playingIds = useStore((s) => s.playingIds);
  const noteColour = useStore((s) => s.noteColour);
  const primary = useStore((s) => s.primary);

  const wrap = useRef(null);
  const paper = useRef(null);
  const host = useRef(null);
  const [width, setWidth] = useState(0);
  const [svgVersion, setSvgVersion] = useState(0);
  const [geom, setGeom] = useState(null);
  const [busy, setBusy] = useState(false);

  // width tracking (debounced)
  useEffect(() => {
    if (!wrap.current) return;
    let t;
    const ro = new ResizeObserver((entries) => {
      clearTimeout(t);
      const w = entries[0].contentRect.width;
      t = setTimeout(() => setWidth((old) => (Math.abs(old - w) > 24 ? w : old)), 180);
    });
    ro.observe(wrap.current);
    setWidth(wrap.current.clientWidth);
    return () => { ro.disconnect(); clearTimeout(t); };
  }, []);

  // fetch and insert the SVG
  useEffect(() => {
    if (!piece || !width) return;
    let cancelled = false;
    setBusy(true);
    api.getScore(piece.id, { width: width - 32, transpose, zoom }).then((res) => {
      if (cancelled) return;
      host.current.innerHTML = res.pages.join("");
      setState({ transposeInfo: res.transpose });
      setSvgVersion((v) => v + 1);
      setBusy(false);
    }).catch((e) => { if (!cancelled) { setBusy(false); setState({ error: String(e.message || e) }); } });
    return () => { cancelled = true; };
  }, [piece?.id, width, transpose, zoom]);

  const maps = useMemo(() => {
    if (!piece) return null;
    const ridToNote = new Map(piece.notes.filter((n) => n.rid).map((n) => [n.rid, n]));
    const ridToMeasure = new Map(piece.measures.map((m) => [m.rid, m]));
    return { ridToNote, ridToMeasure };
  }, [piece]);

  // geometry: note elements, per-measure anchors, systems
  useLayoutEffect(() => {
    if (!piece || !host.current || !svgVersion) return;
    // Positions relative to the paper (the lanes' positioning context); both scroll together.
    const base = paper.current.getBoundingClientRect();
    const rel = (r) => ({ left: r.left - base.left, right: r.right - base.left, top: r.top - base.top, bottom: r.bottom - base.top });
    const noteEl = new Map();
    const perMeasure = new Map();
    for (const el of host.current.querySelectorAll("g.note")) {
      const n = maps.ridToNote.get(el.id);
      if (!n) continue;
      noteEl.set(n.id, el);
      const head = el.querySelector(".notehead") || el;
      const r = rel(head.getBoundingClientRect());
      if (!perMeasure.has(n.m)) perMeasure.set(n.m, []);
      perMeasure.get(n.m).push({ t: n.on, x: r.left });
    }
    const systems = [];
    const measureSystem = new Map();
    const anchors = new Map();
    host.current.querySelectorAll("g.system").forEach((sys, i) => {
      const r = rel(sys.getBoundingClientRect());
      const staves = [...sys.querySelectorAll("g.staff")].map((s) => rel(s.getBoundingClientRect()));
      const staffBottom = Math.max(...staves.map((s) => s.bottom), r.top);
      systems.push({ i, left: r.left, right: r.right, top: r.top, bottom: Math.max(staffBottom, r.bottom) });
      for (const mEl of sys.querySelectorAll("g.measure")) {
        const m = maps.ridToMeasure.get(mEl.id);
        if (!m) continue;
        measureSystem.set(m.n, i);
        const mr = rel((mEl.querySelector("g.staff") || mEl).getBoundingClientRect());
        anchors.set(m.n, buildAnchors(m.on, m.on + m.dur, mr.left + 2, mr.right - 4, perMeasure.get(m.n) || []));
      }
    });
    setGeom({ noteEl, systems, measureSystem, anchors });
  }, [svgVersion, maps]);

  // note colouring: selection, playback, lens state
  const disputed = useMemo(() => disputedSet(piece, lenses), [piece, lenses]);
  useEffect(() => {
    if (!geom || !piece) return;
    const selIds = selection?.ids ? new Set(selection.ids) : null;
    for (const n of piece.notes) {
      const el = geom.noteEl.get(n.id);
      if (!el) continue;
      const inSel = selection && (selIds ? selIds.has(n.id) : n.on >= selection.start - 1e-9 && n.on < selection.end - 1e-9);
      el.classList.toggle("sel", !!inSel);
      el.classList.toggle("playing", playingIds.has(n.id));
      const st = piece.statuses[n.id]?.[primary];
      el.classList.toggle("nct", noteColour === "chordtones" && st === "non-chord");
      el.classList.toggle("disputed", noteColour === "disagreement" && disputed.has(n.id));
    }
  }, [geom, selection, playingIds, noteColour, primary, disputed]);

  // keep the selection in view when it changes by keyboard stepping
  useEffect(() => {
    if (!geom || !selection) return;
    const first = piece.notes.find((n) => n.on >= selection.start - 1e-9 && geom.noteEl.has(n.id));
    const el = first && geom.noteEl.get(first.id);
    if (!el) return;
    const r = el.getBoundingClientRect(), w = wrap.current.getBoundingClientRect();
    if (r.top < w.top + 40 || r.bottom > w.bottom - 120) el.scrollIntoView({ block: "center", behavior: "smooth" });
  }, [selection?.start, geom]);

  // follow playback
  useEffect(() => {
    if (!geom || !playingIds.size) return;
    const id = playingIds.values().next().value;
    const el = geom.noteEl.get(id);
    if (!el) return;
    const r = el.getBoundingClientRect(), w = wrap.current.getBoundingClientRect();
    if (r.bottom > w.bottom - 60 || r.top < w.top) el.scrollIntoView({ block: "center", behavior: "smooth" });
  }, [playingIds, geom]);

  const onClick = (e) => {
    const label = e.target.closest("[data-label]");
    if (label) {
      const lab = piece.analyses.flatMap((a) => a.labels).find((l) => l.id === label.dataset.label);
      if (lab) selectLabel(lab);
      return;
    }
    const noteG = e.target.closest("g.note");
    if (noteG && maps.ridToNote.has(noteG.id)) {
      selectNote(maps.ridToNote.get(noteG.id).id, e.shiftKey);
      return;
    }
    const mG = e.target.closest("g.measure");
    if (mG && maps.ridToMeasure.has(mG.id)) {
      selectMeasure(maps.ridToMeasure.get(mG.id).n, e.shiftKey);
      return;
    }
  };
  const onDblClick = (e) => {
    const noteG = e.target.closest("g.note");
    if (noteG && maps.ridToNote.has(noteG.id)) selectChordAt(maps.ridToNote.get(noteG.id).id);
  };

  return html`
    <div class="score-wrap" ref=${wrap} onClick=${onClick} onDblClick=${onDblClick}>
      <div class=${"paper" + (busy ? " busy" : "")} ref=${paper}>
        <div class="svg-host" ref=${host}></div>
        ${geom && html`<${Lanes} piece=${piece} geom=${geom} lenses=${lenses} selection=${selection} />`}
      </div>
    </div>`;
}

function Lanes({ piece, geom, lenses, selection }) {
  const shown = lenses.map((id) => piece.analyses.find((a) => a.id === id)).filter(Boolean);
  if (!shown.length) return null;
  const LANE = 19;
  const items = [];
  // analysis labels: positioned at their onset, pushed right where they would collide
  shown.forEach((an, li) => {
    let prevKey = null;
    const perSystem = new Map();
    for (const lab of an.labels) {
      const sysI = geom.measureSystem.get(lab.m);
      const anchors = geom.anchors.get(lab.m);
      if (sysI == null || !anchors) continue;
      const keyText = lab.key.label !== prevKey ? keyPrefix(lab.key) : "";
      prevKey = lab.key.label;
      const x = xAt(anchors, lab.on);
      if (!perSystem.has(sysI)) perSystem.set(sysI, []);
      perSystem.get(sysI).push({ lab, keyText, x, w: textWidth(keyText + lab.display) + 6 });
    }
    for (const [sysI, row] of perSystem) {
      const sys = geom.systems[sysI];
      const lefts = layoutLane(row);
      row.forEach(({ lab, keyText }, i) => {
        const selected = selection && lab.on < selection.end - 1e-9 && lab.end > selection.start + 1e-9;
        items.push(html`<span
          class=${"lane-label" + (selected ? " on" : "")}
          data-label=${lab.id}
          title=${`${an.id}: ${lab.display} in ${lab.key.label}${lab.explanation.gist ? " — " + lab.explanation.gist : ""}`}
          style=${`left:${lefts[i]}px;top:${sys.bottom + 8 + li * LANE}px;--lens:${an.colour}`}>${keyText && html`<i>${keyText}</i>`}${lab.display}</span>`);
      });
    }
  });
  // disagreement marks between the first two lanes
  const cmp = shown.length > 1 && piece.comparisons.find((c) => c.a === shown[0].id && c.b === shown[1].id || c.a === shown[1].id && c.b === shown[0].id);
  if (cmp) {
    for (const seg of cmp.segments) {
      if (seg.cls === "same") continue;
      for (const part of splitBySystem(piece, geom, seg.on, seg.end)) {
        items.push(html`<span class=${"lane-diff " + seg.cls} title=${seg.text}
          style=${`left:${part.x0}px;width:${Math.max(6, part.x1 - part.x0)}px;top:${part.top + 8 + LANE - 3}px`}></span>`);
      }
    }
  }
  // lane names at the left of every system
  geom.systems.forEach((sys) => {
    shown.forEach((an, li) => items.push(html`<span class="lane-name" style=${`left:${sys.left - 4}px;top:${sys.bottom + 8 + li * LANE}px;--lens:${an.colour}`}>${an.id}</span>`));
  });
  return html`<div class="lanes">${items}</div>`;
}

let measureCtx = null;
function textWidth(text) {
  if (!measureCtx) {
    measureCtx = document.createElement("canvas").getContext("2d");
    measureCtx.font = `14px ${getComputedStyle(document.documentElement).getPropertyValue("--serif") || "serif"}`;
  }
  return measureCtx.measureText(text).width;
}

function keyPrefix(key) {
  const t = key.tonic;
  return (key.mode === "minor" ? t.charAt(0).toLowerCase() + t.slice(1) : t) + ": ";
}

function splitBySystem(piece, geom, on, end) {
  const out = [];
  const ms = piece.measures.filter((m) => m.on < end && m.on + m.dur > on);
  let cur = null;
  for (const m of ms) {
    const sysI = geom.measureSystem.get(m.n);
    const a = geom.anchors.get(m.n);
    if (sysI == null || !a) continue;
    const x0 = xAt(a, Math.max(on, m.on));
    const x1 = xAt(a, Math.min(end, m.on + m.dur));
    if (cur && cur.sys === sysI) cur.x1 = x1;
    else {
      cur = { sys: sysI, x0, x1, top: geom.systems[sysI].bottom };
      out.push(cur);
    }
  }
  return out;
}
