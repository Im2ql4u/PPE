"""Build the core note model from Verovio's MEI.

Why MEI rather than music21 directly: music21's Humdrum importer silently drops and shifts notes
where a spine splits into several sub-spines (Moonlight mm. 60-63; see docs/validation.md), while
Verovio's Humdrum importer (humlib) reads them correctly. Neither parser is trusted alone: the core
built here is cross-checked against an independent music21 parse (ppe.validate).
"""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

import verovio
from lxml import etree

from ppe.model import Measure, Note

MEI = "http://www.music-encoding.org/ns/mei"
XMLID = "{http://www.w3.org/XML/1998/namespace}id"
STEP = {"c": 0, "d": 2, "e": 4, "f": 5, "g": 7, "a": 9, "b": 11}
ALTER = {"s": 1, "f": -1, "ss": 2, "x": 2, "ff": -2, "n": 0}


def _q(x) -> Fraction:
    return Fraction(x).limit_denominator(960)


def _offset_id(x: Fraction) -> str:
    return f"{x.numerator}" if x.denominator == 1 else f"{x.numerator}_{x.denominator}"


def _tag(el) -> str:
    return etree.QName(el).localname


def load_mei(path: Path) -> str:
    """Score file (MusicXML, **kern, MEI) -> MEI string with stable xml:ids."""
    tk = verovio.toolkit()
    tk.resetXmlIdSeed(1)
    if not tk.loadData(path.read_text(encoding="utf-8")):
        raise ValueError(f"Verovio could not load {path}")
    return tk.getMEI()


def _accidental(note_el) -> int:
    acc = note_el.get("accid.ges") or note_el.get("accid")
    for a in note_el.iter(f"{{{MEI}}}accid"):
        acc = a.get("accid") or a.get("accid.ges") or acc
    return ALTER.get(acc or "n", 0)


def _key_fifths(sig: str | None) -> int | None:
    if not sig:
        return None
    if sig == "0":
        return 0
    m = re.fullmatch(r"(\d+)([sf])", sig)
    return None if not m else int(m.group(1)) * (1 if m.group(2) == "s" else -1)


def mei_to_core(mei: str) -> tuple[list[Measure], list[Note], dict]:
    tk = verovio.toolkit()
    tk.resetXmlIdSeed(1)
    tk.loadData(mei)
    tk.renderToMIDI()
    timemap = tk.renderToTimemap({"includeMeasures": True})
    root = etree.fromstring(mei.encode())

    on_q: dict[str, Fraction] = {}
    off_q: dict[str, Fraction] = {}
    m_start: dict[str, Fraction] = {}
    for e in timemap:
        q = _q(e["qstamp"])
        if "measureOn" in e:
            m_start[e["measureOn"]] = q
        for nid in e.get("on", []):
            on_q.setdefault(nid, q)
        for nid in e.get("off", []):
            off_q[nid] = q

    # Ties: <tie startid endid> elements and @tie="i|m|t" attributes.
    tie_kind: dict[str, str] = {}
    for t in root.iter(f"{{{MEI}}}tie"):
        s, e = (t.get("startid") or "").lstrip("#"), (t.get("endid") or "").lstrip("#")
        if s:
            tie_kind[s] = "continue" if tie_kind.get(s) == "stop" else "start"
        if e:
            tie_kind[e] = "continue" if tie_kind.get(e) == "start" else "stop"
    for n in root.iter(f"{{{MEI}}}note"):
        t = n.get("tie")
        if t:
            tie_kind[n.get(XMLID)] = {"i": "start", "m": "continue", "t": "stop"}[t]

    measures: list[Measure] = []
    notes: list[Note] = []
    meter = (4, 4)
    key = 0
    seen: dict[tuple, int] = {}
    issues: list[str] = []
    m_index = 0
    for el in root.iter():
        tag = _tag(el) if isinstance(el.tag, str) else ""
        if tag in ("scoreDef", "staffDef"):
            if el.get("meter.count"):
                meter = (int(el.get("meter.count")), int(el.get("meter.unit")))
            k = _key_fifths(el.get("key.sig") or el.get("keysig"))
            if k is not None:
                key = k
        elif tag == "meterSig" and el.get("count"):
            meter = (int(el.get("count")), int(el.get("unit")))
        elif tag == "keySig":
            k = _key_fifths(el.get("sig"))
            if k is not None:
                key = k
        elif tag == "measure":
            mid = el.get(XMLID)
            number = int(re.sub(r"\D.*", "", el.get("n")))
            count, unit = meter
            beat = Fraction(4, unit) * (3 if unit == 8 and count % 3 == 0 and count > 3 else 1)
            measures.append(Measure(number=number, index=m_index, onset=m_start.get(mid, Fraction(0)),
                                    duration=Fraction(0), time_signature=f"{count}/{unit}",
                                    beat=beat, key_fifths=key, render_id=mid))
            m_index += 1
            for staff in el.iter(f"{{{MEI}}}staff"):
                staff_n = int(staff.get("n"))
                for layer in staff.iter(f"{{{MEI}}}layer"):
                    voice = int(layer.get("n") or 1)
                    for n in layer.iter(f"{{{MEI}}}note"):
                        nid = n.get(XMLID)
                        if n.get("grace") or nid not in on_q:
                            continue
                        alter = _accidental(n)
                        step = n.get("pname").upper()
                        octave = int(n.get("oct"))
                        midi = 12 * (octave + 1) + STEP[n.get("pname")] + alter
                        onset = on_q[nid]
                        offset = onset - measures[-1].onset
                        dur = off_q.get(nid, onset) - onset
                        if dur <= 0:
                            issues.append(f"non-positive duration for {nid}")
                        k = (number, staff_n, voice, offset, midi)
                        seen[k] = seen.get(k, 0) + 1
                        suffix = "" if seen[k] == 1 else f".{seen[k]}"
                        notes.append(Note(
                            id=f"m{number}.s{staff_n}.v{voice}.o{_offset_id(offset)}.p{midi}{suffix}",
                            measure=number, offset=offset, onset=onset, duration=dur,
                            staff=staff_n, voice=voice, midi=midi,
                            name=step + ("#" * alter if alter > 0 else "-" * -alter) + str(octave),
                            step=step, alter=alter, octave=octave,
                            tie=tie_kind.get(nid), render_id=nid,
                        ))

    # measure durations from successive onsets; last from its notes / metre
    total_end = max((n.onset + n.duration for n in notes), default=Fraction(0))
    fixed = []
    for i, m in enumerate(measures):
        nxt = measures[i + 1].onset if i + 1 < len(measures) else None
        count, unit = (int(x) for x in m.time_signature.split("/"))
        nominal = Fraction(4 * count, unit)
        dur = (nxt - m.onset) if nxt is not None else max(nominal, total_end - m.onset)
        fixed.append(Measure(m.number, m.index, m.onset, dur, m.time_signature, m.beat, m.key_fifths, m.render_id))
    notes.sort(key=lambda n: (n.onset, -n.midi, n.staff, n.voice))

    # Verovio's own MIDI pitch for each note, as a second reading of the same MEI.
    midi_mismatch = []
    for n in notes:
        v = tk.getMIDIValuesForElement(n.render_id).get("pitch")
        if v is not None and v != n.midi:
            midi_mismatch.append({"id": n.id, "mei_pitch": n.midi, "verovio_midi": v})
    report = {"notes": len(notes), "measures": len(fixed), "issues": issues,
              "verovio_midi_vs_mei_pitch_mismatches": midi_mismatch}
    return fixed, notes, report
