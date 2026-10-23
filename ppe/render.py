"""Verovio bridge: score file -> MEI with IDs, MEI-note <-> core-note mapping, SVG rendering.

The renderer is *checked* against the core, never trusted: every MEI note must map to exactly one
core note by (measure, offset, staff, MIDI pitch), and pitches derived from the MEI must equal the
core's. Verovio 6.3.0 failed exactly this check on **kern input (see experiments/e1).
"""

from __future__ import annotations

import functools
import re
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

import verovio
from lxml import etree

from ppe.model import Label, Note, Piece

MEI_NS = "http://www.music-encoding.org/ns/mei"
NS = {"mei": MEI_NS}
XMLID = "{http://www.w3.org/XML/1998/namespace}id"
STEP = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}
ALTER = {"s": 1, "f": -1, "ss": 2, "x": 2, "ff": -2, "n": 0}

# Transposition: candidate interval spellings per semitone count, with their line-of-fifths size.
_INTERVALS = {
    1: [("m2", -5), ("A1", 7)], 2: [("M2", 2), ("d3", -10)], 3: [("m3", -3), ("A2", 9)],
    4: [("M3", 4), ("d4", -8)], 5: [("P4", -1), ("A3", 11)], 6: [("A4", 6), ("d5", -6)],
    7: [("P5", 1), ("d6", -11)], 8: [("m6", -4), ("A5", 8)], 9: [("M6", 3), ("d7", -9)],
    10: [("m7", -2), ("A6", 10)], 11: [("M7", 5), ("d8", -7)],
}


def verovio_version() -> str:
    return verovio.toolkit().getVersion()


VEROVIO_DATA = str(Path(verovio.__file__).parent / "data")


def _toolkit(options: dict | None = None) -> verovio.toolkit:
    # Set the resource path explicitly: in worker threads (FastAPI runs sync endpoints in a thread
    # pool) Verovio otherwise fails to find its fonts and silently renders nothing.
    tk = verovio.toolkit(False)
    tk.setResourcePath(VEROVIO_DATA)
    tk.resetXmlIdSeed(1)
    opts = {"breaks": "auto", "adjustPageHeight": True, "header": "none", "footer": "none"}
    opts.update(options or {})
    tk.setOptions(opts)
    return tk


def score_to_mei(path: Path) -> str:
    tk = _toolkit()
    data = path.read_text(encoding="utf-8")
    if not tk.loadData(data):
        raise ValueError(f"Verovio could not load {path}")
    return tk.getMEI()


def mei_note_addresses(mei: str) -> dict[str, tuple[int, Fraction, int, int]]:
    """MEI note id -> (measure number, offset in quarters within measure, staff, MIDI pitch).

    Offsets come from Verovio's timemap; pitches from the MEI itself (pname, oct, accid/accid.ges).
    """
    tk = _toolkit()
    tk.loadData(mei)
    tk.renderToMIDI()
    timemap = tk.renderToTimemap({"includeMeasures": True})
    root = etree.fromstring(tk.getMEI().encode())

    measure_n, staff_of, pitch_of, measure_of = {}, {}, {}, {}
    for m in root.iter(f"{{{MEI_NS}}}measure"):
        mid = m.get(XMLID)
        measure_n[mid] = int(re.sub(r"\D.*", "", m.get("n")))
        for st in m.iter(f"{{{MEI_NS}}}staff"):
            for n in st.iter(f"{{{MEI_NS}}}note"):
                if n.get("grace"):
                    continue
                nid = n.get(XMLID)
                staff_of[nid] = int(st.get("n"))
                measure_of[nid] = mid
                acc = n.get("accid.ges") or n.get("accid")
                for a in n.iter(f"{{{MEI_NS}}}accid"):
                    acc = a.get("accid") or a.get("accid.ges") or acc
                pitch_of[nid] = 12 * (int(n.get("oct")) + 1) + STEP[n.get("pname")] + ALTER.get(acc or "n", 0)

    out, m_start = {}, {}
    for entry in timemap:
        q = Fraction(entry["qstamp"]).limit_denominator(960)
        if "measureOn" in entry:
            m_start[entry["measureOn"]] = q
        for nid in entry.get("on", []):
            if nid in pitch_of:
                mid = measure_of[nid]
                out[nid] = (measure_n[mid], q - m_start[mid], staff_of[nid], pitch_of[nid])
    return out


def map_render_ids(notes: list[Note], mei: str) -> tuple[list[Note], dict]:
    """Attach MEI ids to core notes. Returns (notes with render_id, validation report)."""
    addr = mei_note_addresses(mei)
    by_key: dict[tuple, list[str]] = defaultdict(list)
    for mid, (m, off, staff, midi) in addr.items():
        by_key[(m, off, staff, midi)].append(mid)
    out, unmatched_core = [], []
    used = set()
    for n in notes:
        cands = [c for c in by_key.get((n.measure, n.offset, n.staff, n.midi), []) if c not in used]
        if cands:
            used.add(cands[0])
            out.append(_with_render(n, cands[0]))
        else:
            unmatched_core.append(n.id)
            out.append(n)
    unmatched_mei = [mid for mid in addr if mid not in used]
    report = {
        "renderer": f"verovio {verovio_version()}",
        "core_notes": len(notes),
        "mei_notes": len(addr),
        "matched": len(used),
        "unmatched_core": unmatched_core,
        "unmatched_mei": [{"id": mid, "address": [addr[mid][0], str(addr[mid][1]), addr[mid][2], addr[mid][3]]} for mid in unmatched_mei],
    }
    return out, report


def _with_render(n: Note, rid: str) -> Note:
    from dataclasses import replace

    return replace(n, render_id=rid)


def transposition_interval(semitones: int, key_fifths: int) -> tuple[str, int]:
    """Interval name for Verovio's `transpose` option and its fifths size, choosing the spelling whose
    resulting key signature has the fewest accidentals (C# minor +1 -> D minor, not C## minor)."""
    if semitones == 0:
        return "P1", 0
    sign = 1 if semitones > 0 else -1
    best = min(_INTERVALS[abs(semitones) % 12 or 12], key=lambda c: abs(key_fifths + sign * c[1]))
    name = best[0] if sign > 0 else "-" + best[0]
    return name, sign * best[1]


def inject_labels(mei: str, piece: Piece, analysis_ids: list[str], colours: dict[str, str]) -> str:
    """Insert <harm> elements carrying Roman numerals for the chosen analyses below the bass staff.
    Each harm gets xml:id 'harm-<label id>' so a click on it can select the label's span."""
    root = etree.fromstring(mei.encode())
    measures = {}
    for m in root.iter(f"{{{MEI_NS}}}measure"):
        measures.setdefault(int(re.sub(r"\D.*", "", m.get("n"))), m)
    bottom_staff = str(max(n.staff for n in piece.notes))
    for aid in analysis_ids:
        an = piece.analysis(aid)
        prev_key = None
        for lab in an.labels:
            m_el = measures.get(lab.measure)
            if m_el is None:
                continue
            meas = piece.measure(lab.measure)
            tstamp = 1 + (lab.onset - meas.onset) / meas.beat
            h = etree.SubElement(m_el, f"{{{MEI_NS}}}harm")
            h.set(XMLID, f"harm-{lab.id}")
            h.set("staff", bottom_staff)
            h.set("tstamp", f"{float(tstamp):.4g}")
            h.set("place", "below")
            h.set("type", f"lens-{aid}")
            text = lab.display
            if lab.key != prev_key:
                text = f"{_key_prefix(lab)}: {text}"
                prev_key = lab.key
            r = etree.SubElement(h, f"{{{MEI_NS}}}rend")
            r.set("color", colours.get(aid, "#333333"))
            r.text = text
    return etree.tostring(root, encoding="unicode")


def _key_prefix(lab: Label) -> str:
    from ppe.spelling import pretty

    t = pretty(lab.key.tonic)
    return t if lab.key.mode == "major" else t.lower()


@functools.lru_cache(maxsize=64)
def render_svg(mei: str, width: int, transpose: str = "P1", scale: int = 40) -> tuple[str, ...]:
    """Render all pages to SVG strings. Cached per (mei, width, transposition, scale)."""
    tk = _toolkit({
        "pageWidth": max(800, int(width * 100 / scale)),
        "pageHeight": 60000,
        "scale": scale,
        "transpose": "" if transpose == "P1" else transpose,
        "svgViewBox": True,
        "svgRemoveXlink": True,
        "pageMarginLeft": 40, "pageMarginRight": 40, "pageMarginTop": 40, "pageMarginBottom": 60,
        "spacingSystem": 22,  # room for the analysis lanes drawn under each system
    })
    tk.loadData(mei)
    return tuple(tk.renderToSVG(p) for p in range(1, tk.getPageCount() + 1))


def transposed_mei_pitches(mei: str, transpose: str) -> dict[str, int]:
    """MEI id -> MIDI pitch after Verovio's transposition (for verifying the rendered transposition)."""
    tk = _toolkit({"transpose": transpose})
    tk.loadData(mei)
    root = etree.fromstring(tk.getMEI().encode())
    out = {}
    for n in root.iter(f"{{{MEI_NS}}}note"):
        if n.get("grace") or n.get("pname") is None:
            continue
        acc = n.get("accid.ges") or n.get("accid")
        for a in n.iter(f"{{{MEI_NS}}}accid"):
            acc = a.get("accid") or a.get("accid.ges") or acc
        out[n.get(XMLID)] = 12 * (int(n.get("oct")) + 1) + STEP[n.get("pname")] + ALTER.get(acc or "n", 0)
    return out
