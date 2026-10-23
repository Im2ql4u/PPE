// A tiny observable store with a Preact hook. State is replaced immutably on every update.
import { useEffect, useRef, useState } from "preact/hooks";

let state = {
  pieces: [],
  pieceId: null,
  piece: null, // full piece JSON
  loading: false,
  error: null,
  lenses: [], // analysis ids shown as lanes
  primary: null, // analysis used for keyboard roles, chord-tone colouring and stepping
  noteColour: "plain", // plain | chordtones | disagreement
  selection: null, // { kind, ids?, start, end, label? }
  inspect: null,
  transpose: 0,
  transposeInfo: null,
  mode: "original",
  tracks: [], // empty = all
  speed: 1,
  loop: false,
  pedal: true, // sustain pedal changed at each harmony of the primary analysis
  playing: false,
  playingIds: new Set(),
  playingMidis: new Set(),
  substitution: null, // { label, figure }
  alternatives: null,
  zoom: 40,
  panel: { more: {} },
};

const listeners = new Set();

export const getState = () => state;

export function setState(patch) {
  const next = typeof patch === "function" ? patch(state) : patch;
  state = { ...state, ...next };
  for (const l of listeners) l();
}

export function useStore(selector) {
  const [, force] = useState(0);
  const sel = useRef(selector);
  sel.current = selector;
  const value = selector(state);
  const last = useRef(value);
  last.current = value;
  useEffect(() => {
    const l = () => {
      const v = sel.current(state);
      if (!Object.is(v, last.current)) force((x) => x + 1);
    };
    listeners.add(l);
    return () => listeners.delete(l);
  }, []);
  return value;
}
