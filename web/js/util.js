// Pure helpers (no DOM). Tested with `node --test web/tests`.

export const LOWEST = 21; // A0
export const HIGHEST = 108; // C8
const BLACK = new Set([1, 3, 6, 8, 10]);

export const isBlack = (midi) => BLACK.has(((midi % 12) + 12) % 12);

/** Number of white keys strictly below `midi` within the 88-key range. */
export function whiteIndex(midi) {
  let n = 0;
  for (let m = LOWEST; m < midi; m++) if (!isBlack(m)) n++;
  return n;
}

export const WHITE_COUNT = whiteIndex(HIGHEST + 1); // 52

/**
 * Key rectangle in "white key" units: white keys are 1 wide; black keys 0.6 wide, centred on the
 * boundary between their neighbours, nudged the way real keyboards are (C#/D# and F#/G#/A# groups).
 */
export function keyRect(midi) {
  if (!isBlack(midi)) return { x: whiteIndex(midi), w: 1, black: false };
  const pc = midi % 12;
  const nudge = { 1: -0.08, 3: 0.08, 6: -0.1, 8: 0, 10: 0.1 }[pc];
  const boundary = whiteIndex(midi); // white keys below = boundary position
  return { x: boundary - 0.3 + nudge, w: 0.6, black: true };
}

const NAMES = ["C", "C♯", "D", "E♭", "E", "F", "F♯", "G", "A♭", "A", "B♭", "B"];
export const midiName = (m) => `${NAMES[m % 12]}${Math.floor(m / 12) - 1}`;

/**
 * Interpolate an x position for score time `t` from known (onset, x) anchors within a measure.
 * anchors: sorted [{t, x}], including the measure start and end.
 */
export function xAt(anchors, t) {
  if (!anchors.length) return null;
  if (t <= anchors[0].t) return anchors[0].x;
  for (let i = 0; i < anchors.length - 1; i++) {
    const a = anchors[i], b = anchors[i + 1];
    if (t === a.t) return a.x;
    if (t > a.t && t < b.t) return a.x + ((t - a.t) / (b.t - a.t)) * (b.x - a.x);
  }
  return anchors[anchors.length - 1].x;
}

/** Collapse note positions into anchors: the leftmost x per onset, plus measure bounds. */
export function buildAnchors(measureStart, measureEnd, xLeft, xRight, notePositions) {
  const best = new Map();
  for (const { t, x } of notePositions) {
    if (!best.has(t) || x < best.get(t)) best.set(t, x);
  }
  const pts = [...best.entries()].map(([t, x]) => ({ t, x })).sort((a, b) => a.t - b.t);
  if (!pts.length || pts[0].t > measureStart) pts.unshift({ t: measureStart, x: xLeft });
  pts.push({ t: measureEnd, x: xRight });
  // enforce monotone x (grace/cross-staff glitches)
  for (let i = 1; i < pts.length; i++) if (pts[i].x < pts[i - 1].x) pts[i].x = pts[i - 1].x;
  return pts;
}

/**
 * Place labels in one lane of one system without overlap: each label sits at its time position x
 * unless that would collide with the previous one, in which case it is pushed right.
 * items: [{x, w}] in time order; returns the placed left positions.
 */
export function layoutLane(items, gap = 5) {
  const out = [];
  let right = -Infinity;
  for (const { x, w } of items) {
    const left = Math.max(x, right + gap);
    out.push(left);
    right = left + w;
  }
  return out;
}

/** Labels overlapping [start, end). */
export const labelsIn = (labels, start, end) => labels.filter((l) => l.on < end && l.end > start);

/** The label active at time t. */
export const labelAt = (labels, t) => labels.find((l) => l.on <= t && t < l.end) || null;

/** Next / previous harmony relative to time t (for arrow-key stepping). */
export function stepHarmony(labels, t, dir) {
  if (!labels.length) return null;
  if (dir > 0) return labels.find((l) => l.on > t + 1e-9) || null;
  const before = labels.filter((l) => l.on < t - 1e-9);
  return before.length ? before[before.length - 1] : null;
}

/** Selection span from a set of notes. */
export function spanOf(notes) {
  let start = Infinity, end = -Infinity;
  for (const n of notes) {
    start = Math.min(start, n.on);
    end = Math.max(end, n.on + n.dur);
  }
  return { start, end };
}

/** Notes whose onset lies within [start, end). */
export const notesIn = (notes, start, end) => notes.filter((n) => n.on >= start - 1e-9 && n.on < end - 1e-9);

/** Seconds for a duration in quarter notes at a tempo (quarters per minute) and speed factor. */
export const toSeconds = (q, qpm, speed = 1) => (q * 60) / (qpm * speed);

/** Nearest sample (Salamander set: every minor third from A0 to C8). */
export function nearestSample(midi) {
  const clamped = Math.max(LOWEST, Math.min(HIGHEST, midi));
  const idx = Math.round((clamped - LOWEST) / 3);
  const sample = Math.min(LOWEST + idx * 3, HIGHEST);
  return { sample, rate: Math.pow(2, (midi - sample) / 12) };
}

const SAMPLE_NAMES = { 0: "C", 3: "Ds", 6: "Fs", 9: "A" };
export const sampleFile = (midi) => `${SAMPLE_NAMES[midi % 12]}${Math.floor(midi / 12) - 1}.mp3`;

// Line of fifths: C = 0, G = 1, F = -1, F♯ = 6, B♭ = -2 ...
const LOF_LETTERS = ["F", "C", "G", "D", "A", "E", "B"];

export function fifthsOf(name) {
  const letter = name[0].toUpperCase();
  let acc = 0;
  for (const ch of name.slice(1)) {
    if (ch === "♯" || ch === "#") acc += 1;
    else if (ch === "♭" || ch === "b" || ch === "-") acc -= 1;
    else if (ch === "𝄪") acc += 2;
    else if (ch === "𝄫") acc -= 2;
  }
  return LOF_LETTERS.indexOf(letter) - 1 + 7 * acc;
}

export function nameOfFifths(p) {
  const idx = p + 1;
  const letter = LOF_LETTERS[((idx % 7) + 7) % 7];
  const acc = Math.floor(idx / 7);
  const sign = acc > 0 ? "♯" : "♭";
  return letter + (Math.abs(acc) === 2 ? (acc > 0 ? "𝄪" : "𝄫") : sign.repeat(Math.abs(acc)));
}

/** Transpose a tonic name by a number of fifths (the key-signature change of the transposition). */
export const transposeTonic = (name, fifths) => (fifths ? nameOfFifths(fifthsOf(name) + fifths) : name);

/** Distinct pitch classes, sorted, for comparing sets. */
export const pcSet = (midis) => [...new Set(midis.map((m) => ((m % 12) + 12) % 12))].sort((a, b) => a - b);
