"""JSON views of the core model for the browser."""

from __future__ import annotations

from itertools import combinations

from ppe.compare import CLASS_TEXT, note_statuses, segments, summary
from ppe.explain import explain_comparison, explain_label
from ppe.model import Analysis, Label, Note, Piece
from ppe.playback import MODES
from ppe.spelling import pretty


def note_json(n: Note) -> dict:
    return {"id": n.id, "rid": n.render_id, "m": n.measure, "off": float(n.offset), "on": float(n.onset),
            "dur": float(n.duration), "staff": n.staff, "voice": n.voice, "midi": n.midi,
            "name": pretty(n.name), "tie": n.tie, "track": n.track}


def label_json(lab: Label, an: Analysis, nxt: Label | None) -> dict:
    return {
        "id": lab.id, "analysis": lab.analysis, "on": float(lab.onset), "end": float(lab.end),
        "m": lab.measure, "beat": float(lab.beat),
        "key": {"tonic": pretty(lab.key.tonic), "mode": lab.key.mode, "label": lab.key.label},
        "figure": lab.figure, "display": lab.display,
        "pitches": [pretty(p) for p in lab.pitches], "pcs": sorted(lab.pcs), "extra_pcs": sorted(lab.extra_pcs),
        "root": pretty(lab.root), "bass": pretty(lab.bass), "quality": lab.quality,
        "inversion": lab.inversion, "family": lab.family, "applied_to": lab.applied_to,
        "alternatives": list(lab.alternatives), "cadence": lab.cadence,
        "explanation": explain_label(lab, nxt, an.analyst.split(" (")[0]),
    }


def analysis_json(an: Analysis) -> dict:
    labels = an.labels
    return {
        "id": an.id, "analyst": an.analyst, "kind": an.kind, "source": an.source, "licence": an.licence,
        "colour": an.colour, "issues": an.issues,
        "notes": [{"m": x.measure, "text": x.text} for x in an.notes],
        "labels": [label_json(l, an, labels[i + 1] if i + 1 < len(labels) else None) for i, l in enumerate(labels)],
    }


def comparison_json(piece: Piece, a: Analysis, b: Analysis) -> dict:
    labs = {l.id: l for l in a.labels + b.labels}
    segs = []
    for s in segments(piece, a, b):
        la, lb = labs[s.a], labs[s.b]
        segs.append({"on": float(s.onset), "end": float(s.end), "a": s.a, "b": s.b, "cls": s.cls,
                     "text": explain_comparison(s.cls, la, lb, _short(a), _short(b))})
    return {"a": a.id, "b": b.id, "summary": summary(piece, a, b), "segments": segs,
            "classes": CLASS_TEXT}


def _short(an: Analysis) -> str:
    return an.id if an.kind != "automatic" else f"{an.id} (automatic)"


def piece_json(piece: Piece) -> dict:
    v = piece.validation
    return {
        "id": piece.id, "title": piece.title, "subtitle": piece.subtitle, "composer": piece.composer,
        "tempo_qpm": piece.tempo_qpm, "end": float(piece.end),
        "score": {"source": piece.score_source, "licence": piece.score_licence},
        "measures": [{"n": m.number, "rid": m.render_id, "on": float(m.onset), "dur": float(m.duration),
                      "ts": m.time_signature, "beat": float(m.beat), "key_fifths": m.key_fifths}
                     for m in piece.measures],
        "notes": [note_json(n) for n in piece.notes],
        "tracks": [{"id": t.id, "name": t.name, "rule": t.rule, "count": t.count} for t in piece.tracks],
        "analyses": [analysis_json(a) for a in piece.analyses],
        "comparisons": [comparison_json(piece, a, b) for a, b in combinations(piece.analyses, 2)],
        "statuses": note_statuses(piece),
        "modes": MODES,
        "validation": {
            "crosscheck_agreement": v.get("crosscheck", {}).get("agreement_rate"),
            "independent_parser": v.get("crosscheck", {}).get("independent_parser"),
            "known_discrepancy_note": v.get("known_discrepancy_note"),
            "reference": {k: (v.get("reference") or {}).get(k) for k in ("agreement_rate", "agreeing", "reference_notes", "note")}
            if v.get("reference") else None,
            "alignment": v.get("alignment"),
            "analysis_issues": v.get("analysis_issues"),
        },
    }
