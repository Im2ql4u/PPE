// A small sampled piano (Salamander Grand, CC-BY 3.0) on the Web Audio API, with a scheduler that
// reports which notes are sounding so score and keyboard can light up in sync.
import { nearestSample, sampleFile, toSeconds } from "./util.js";

let ctx = null;
let master = null;
const buffers = new Map(); // sample midi -> AudioBuffer
let loading = null;

function audio() {
  if (!ctx) {
    ctx = new (window.AudioContext || window.webkitAudioContext)({ latencyHint: "interactive" });
    master = ctx.createGain();
    master.gain.value = 0.8;
    const comp = ctx.createDynamicsCompressor();
    comp.threshold.value = -14;
    comp.ratio.value = 3;
    master.connect(comp).connect(ctx.destination);
  }
  if (ctx.state === "suspended") ctx.resume();
  return ctx;
}

export function loadSamples() {
  if (loading) return loading;
  const a = audio();
  const jobs = [];
  for (let m = 21; m <= 108; m += 3) {
    jobs.push(
      fetch(`/samples/salamander/${sampleFile(m)}`)
        .then((r) => r.arrayBuffer())
        .then((b) => a.decodeAudioData(b))
        .then((buf) => buffers.set(m, buf))
        .catch(() => {}),
    );
  }
  loading = Promise.all(jobs);
  return loading;
}

const voices = new Set();

function voice(midi, when, dur, velocity) {
  const a = audio();
  const { sample, rate } = nearestSample(midi);
  const buf = buffers.get(sample);
  const g = a.createGain();
  const peak = 0.12 + 0.78 * velocity * velocity;
  g.gain.setValueAtTime(0, when);
  g.gain.linearRampToValueAtTime(peak, when + 0.004);
  const release = Math.max(when + 0.05, when + dur);
  g.gain.setValueAtTime(peak, release);
  g.gain.exponentialRampToValueAtTime(0.0008, release + 0.35);
  g.connect(master);
  let src;
  if (buf) {
    src = a.createBufferSource();
    src.buffer = buf;
    src.playbackRate.value = rate;
  } else {
    // fallback while samples load: a soft triangle tone
    src = a.createOscillator();
    src.type = "triangle";
    src.frequency.value = 440 * Math.pow(2, (midi - 69) / 12);
    g.gain.value *= 0.4;
  }
  src.connect(g);
  src.start(when);
  src.stop(release + 0.4);
  const v = { src, g };
  voices.add(v);
  src.onended = () => voices.delete(v);
  return v;
}

/** Play one note now (keyboard clicks). */
export function playNote(midi, dur = 0.9, velocity = 0.6) {
  loadSamples();
  voice(midi, audio().currentTime + 0.01, dur, velocity);
}

let session = null;

export function stop() {
  if (session) {
    cancelAnimationFrame(session.raf);
    session.onTick(new Set(), new Set());
    session.onEnd?.();
    session = null;
  }
  const now = ctx ? ctx.currentTime : 0;
  for (const v of voices) {
    try {
      v.g.gain.cancelScheduledValues(now);
      v.g.gain.setTargetAtTime(0, now, 0.03);
      v.src.stop(now + 0.15);
    } catch { /* already stopped */ }
  }
  voices.clear();
}

export const isPlaying = () => session !== null;

/**
 * Play events [{onset, duration, midi, ids, velocity}] (onset in quarters, absolute score time).
 * onTick(ids:Set, midis:Set) is called whenever the set of sounding notes changes.
 */
export async function play(events, { qpm, speed = 1, start, end, loop = false, onTick, onEnd }) {
  stop();
  await loadSamples();
  const a = audio();
  const t0 = a.currentTime + 0.08;
  const span = end - start;
  const sec = (q) => toSeconds(q, qpm, speed);
  const schedule = (offset) => {
    for (const e of events) voice(e.midi, offset + sec(e.onset - start), sec(e.duration), e.velocity);
  };
  schedule(t0);
  const s = { raf: 0, onTick, onEnd, t0, lastKey: "", queued: false };
  session = s;
  const tick = () => {
    if (session !== s) return;
    let q = start + ((a.currentTime - s.t0) * qpm * speed) / 60;
    if (loop && !s.queued && a.currentTime > s.t0 + sec(span) - 0.3) {
      schedule(s.t0 + sec(span)); // queue the next pass slightly ahead so the loop is seamless
      s.queued = true;
    }
    if (q >= end) {
      if (loop) {
        s.t0 += sec(span);
        s.queued = false;
        q = start + ((a.currentTime - s.t0) * qpm * speed) / 60;
      } else {
        stop();
        return;
      }
    }
    const ids = new Set(), midis = new Set();
    for (const e of events) {
      if (e.onset <= q && q < e.onset + e.duration) {
        for (const id of e.ids) ids.add(id);
        midis.add(e.midi);
      }
    }
    const key = [...midis].sort().join(",") + "|" + ids.size;
    if (key !== s.lastKey) {
      s.lastKey = key;
      onTick(ids, midis, q);
    }
    s.raf = requestAnimationFrame(tick);
  };
  s.raf = requestAnimationFrame(tick);
}
