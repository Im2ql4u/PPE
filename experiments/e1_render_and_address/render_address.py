"""E1 (lite): render a score with Verovio, map SVG note IDs to musical addresses,
cross-check against music21, test ID stability, and colour notes by whether two
expert analyses agree that they are chord tones.

Usage:  uv run python experiments/e1_render_and_address/render_address.py
"""

import json
import re
from collections import Counter
from fractions import Fraction
from pathlib import Path

import verovio
from lxml import etree
from music21 import converter, roman

ROOT = Path(__file__).resolve().parents[2]
KERN = ROOT / "data/external/sapp_beethoven/kern/sonata14-1.krn"
WIR = ROOT / "data/external/when_in_rome/Corpus/Piano_Sonatas/Beethoven,_Ludwig_van/Op027_No2(Moonlight)/1"
OUT = Path(__file__).parent / "out"
MEI_NS = {"mei": "http://www.music-encoding.org/ns/mei"}
XMLID = "{http://www.w3.org/XML/1998/namespace}id"


def toolkit(data: str, seed: int = 1) -> verovio.toolkit:
    tk = verovio.toolkit()
    tk.setOptions({"scale": 35, "pageWidth": 2400, "adjustPageHeight": True, "breaks": "auto"})
    tk.resetXmlIdSeed(seed)
    tk.loadData(data)
    return tk


def verovio_addresses(tk: verovio.toolkit) -> dict[str, tuple[int, Fraction, int]]:
    """note xml:id -> (measure number, onset in quarters within measure, MIDI pitch)."""
    tk.renderToMIDI()  # required for timing queries
    timemap = tk.renderToTimemap({"includeMeasures": True})
    mei = etree.fromstring(tk.getMEI().encode())
    measure_n = {m.get(XMLID): int(m.get("n")) for m in mei.iterfind(".//mei:measure", MEI_NS)}
    # getMIDIValuesForElement ignored key-signature accidentals in our test (G for G#),
    # so compute pitch from the MEI note: pname + oct + written or gestural accidental.
    step = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}
    alter = {"s": 1, "f": -1, "ss": 2, "x": 2, "ff": -2, "n": 0}
    pitch_of = {}
    for n in mei.iterfind(".//mei:note", MEI_NS):
        acc = n.get("accid") or n.get("accid.ges")
        for a in n.iterfind("mei:accid", MEI_NS):
            acc = a.get("accid") or a.get("accid.ges") or acc
        pitch_of[n.get(XMLID)] = 12 * (int(n.get("oct")) + 1) + step[n.get("pname")] + alter.get(acc or "n", 0)

    addr, measure_start, current = {}, {}, None
    for entry in timemap:
        q = Fraction(entry["qstamp"]).limit_denominator(96)
        if "measureOn" in entry:
            current = entry["measureOn"]
            measure_start[current] = q
        for nid in entry.get("on", []):
            if nid not in pitch_of:
                continue  # rests etc.
            addr[nid] = (measure_n[current], q - measure_start[current], pitch_of[nid])
    return addr


def music21_addresses(path: Path) -> Counter:
    s = converter.parse(str(path))
    c = Counter()
    for n in s.recurse().notes:
        m = n.getContextByClass("Measure")
        off = Fraction(n.getOffsetInHierarchy(m)).limit_denominator(96)
        for p in n.pitches:
            if n.tie is None or n.tie.type == "start":
                c[(m.number, off, p.midi)] += 1
    return c


def rn_timeline(path: Path):
    s = converter.parse(str(path), format="romantext")
    return [(float(r.offset), float(r.offset + r.quarterLength), r) for r in s.flatten().getElementsByClass(roman.RomanNumeral)]


def active(tl, t: float):
    for a, b, r in tl:
        if a <= t < b:
            return r
    return None


def main() -> None:
    OUT.mkdir(exist_ok=True)
    data = KERN.read_text(encoding="utf-8")
    tk = toolkit(data)
    va = verovio_addresses(tk)

    # 1. cross-check against music21's independent parse of the same file
    v_counts = Counter(va.values())
    m_counts = music21_addresses(KERN)
    matched = sum((v_counts & m_counts).values())
    report = {
        "verovio_notes": sum(v_counts.values()),
        "music21_notes": sum(m_counts.values()),
        "matched_addresses": matched,
        "only_verovio_examples": [str(k) for k in list((v_counts - m_counts).elements())[:5]],
        "only_music21_examples": [str(k) for k in list((m_counts - v_counts).elements())[:5]],
    }

    # 2. ID stability: same input + same seed; and a one-note edit
    ids_again = verovio_addresses(toolkit(data))
    report["ids_identical_same_seed"] = ids_again == va
    edited = data.replace("12eJ", "12dJ", 1)  # change one note early in m. 1
    ids_edit = verovio_addresses(toolkit(edited))
    same_id_same_addr = sum(1 for k, v in va.items() if ids_edit.get(k) == v)
    report["after_one_note_edit_ids_still_pointing_to_same_address"] = f"{same_id_same_addr}/{len(va)}"
    addr_to_id_before = {v: k for k, v in va.items()}
    addr_to_id_after = {v: k for k, v in ids_edit.items()}
    common = set(addr_to_id_before) & set(addr_to_id_after)
    report["after_edit_addresses_keeping_same_id"] = f"{sum(addr_to_id_before[a] == addr_to_id_after[a] for a in common)}/{len(common)}"

    # 3. chord-tone status of each note under each expert analysis
    analyses = {"BPS": rn_timeline(WIR / "analysis.txt"), "DT": rn_timeline(WIR / "analysis_DT.txt")}
    status, colours = {}, {}
    for nid, (m, onset, pitch) in va.items():
        t = (m - 1) * 4 + float(onset)  # 2/2 throughout, no anacrusis
        verdict = {}
        for name, tl in analyses.items():
            rn = active(tl, t)
            verdict[name] = None if rn is None else (pitch % 12) in set(rn.pitchClasses)
        status[nid] = verdict
        a, b = verdict["BPS"], verdict["DT"]
        colours[nid] = (
            "#9aa0a6" if a is None or b is None else
            "#1a73e8" if a and b else
            "#e8710a" if a != b else
            "#5f6368"
        )
    summary = Counter(
        "both chord tone" if v["BPS"] and v["DT"] else
        "both non-chord tone" if v["BPS"] is False and v["DT"] is False else
        "analysts disagree" if None not in v.values() else "unlabelled"
        for v in status.values()
    )
    report["chord_tone_status"] = dict(summary)
    disputed = sorted({va[n][0] for n, v in status.items() if None not in v.values() and v["BPS"] != v["DT"]})
    report["measures_with_disputed_notes"] = disputed

    # 4. render all pages with notes coloured by agreement status
    pages = []
    for p in range(1, tk.getPageCount() + 1):
        svg = tk.renderToSVG(p)
        for nid, col in colours.items():
            svg = re.sub(rf'(<g id="{nid}" class="note")', rf'\1 fill="{col}" color="{col}"', svg)
        pages.append(svg)
    legend = (
        '<p style="font-family:sans-serif">Notes coloured by two expert analyses (BPS = Chen &amp; Su; DT = Tymoczko): '
        '<b style="color:#1a73e8">chord tone for both</b> · <b style="color:#5f6368">non-chord tone for both</b> · '
        '<b style="color:#e8710a">analysts disagree</b></p>'
    )
    (OUT / "moonlight_agreement.html").write_text(
        "<!doctype html><meta charset=utf-8><title>Moonlight: chord-tone agreement</title>" + legend + "".join(pages),
        encoding="utf-8",
    )
    (OUT / "report.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()
