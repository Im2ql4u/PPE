import { h } from "preact";
import { useMemo } from "preact/hooks";
import htm from "htm";
import { playNote } from "./audio.js";
import { useStore } from "./store.js";
import { HIGHEST, LOWEST, WHITE_COUNT, isBlack, keyRect, midiName } from "./util.js";

const html = htm.bind(h);
const KW = 24; // white key width in SVG units
const KH = 132; // white key height
const BH = 84; // black key height
const ROLE = { root: "R", third: "3", fifth: "5", seventh: "7", ninth: "9", eleventh: "11", thirteenth: "13" };

export function Keyboard() {
  const piece = useStore((s) => s.piece);
  const inspect = useStore((s) => s.inspect);
  const primary = useStore((s) => s.primary);
  const transpose = useStore((s) => s.transpose);
  const playing = useStore((s) => s.playingMidis);

  const lens = piece?.analyses.find((a) => a.id === primary);
  const marks = useMemo(() => {
    const out = new Map();
    if (!inspect || inspect.empty) return out;
    const statuses = new Map((inspect.lenses.find((l) => l.analysis === primary)?.statuses || []).map((s) => [s.id, s]));
    const lowest = Math.min(...inspect.notes.map((n) => n.midi));
    for (const n of inspect.notes) {
      const midi = n.midi + transpose;
      if (out.has(midi)) continue;
      const st = statuses.get(n.id) || {};
      out.set(midi, { status: st.status, role: st.role, degree: st.degree, bass: n.midi === lowest, name: n.name });
    }
    return out;
  }, [inspect, primary, transpose]);

  const keys = [];
  const blacks = [];
  for (let m = LOWEST; m <= HIGHEST; m++) {
    const r = keyRect(m);
    const mark = marks.get(m);
    const cls = ["key", r.black ? "black" : "white"];
    if (mark) cls.push("marked", mark.status === "non-chord" ? "nct" : mark.status ? "ct" : "plain");
    if (mark?.bass) cls.push("bass");
    if (playing.has(m)) cls.push("sounding");
    const x = r.x * KW, w = r.w * KW, hgt = r.black ? BH : KH;
    const el = html`<g class=${cls.join(" ")} onClick=${() => playNote(m)}>
        <title>${mark ? `${mark.name}${mark.role ? " · " + mark.role : ""}${mark.degree ? " · degree " + mark.degree : ""}` : midiName(m)}</title>
        <rect x=${x + 0.5} y="0" width=${w - 1} height=${hgt} rx=${r.black ? 2 : 3} />
        ${mark?.role && html`<text class="role" x=${x + w / 2} y=${hgt - (r.black ? 10 : 12)}>${ROLE[mark.role] || ""}</text>`}
        ${!r.black && m % 12 === 0 && html`<text class="oct" x=${x + w / 2} y=${KH - 4}>${midiName(m)}</text>`}
      </g>`;
    (r.black ? blacks : keys).push(el);
  }
  const degrees = [...marks.entries()].filter(([, mk]) => mk.degree).map(([m, mk]) => {
    const r = keyRect(m);
    return html`<text class=${"degree" + (mk.status === "non-chord" ? " nct" : "")} x=${(r.x + r.w / 2) * KW} y=${KH + 17}>${mk.degree}</text>`;
  });
  return html`
    <div class="keyboard" style=${lens ? `--lens:${lens.colour}` : ""}>
      <svg viewBox=${`0 -2 ${WHITE_COUNT * KW} ${KH + 24}`} preserveAspectRatio="xMidYMid meet">
        ${keys}${blacks}${degrees}
      </svg>
    </div>`;
}
