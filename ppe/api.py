"""Local web service: JSON API + the static browser app."""

from __future__ import annotations

import functools
from fractions import Fraction
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from ppe import pieces
from ppe.playback import build as build_playback
from ppe.render import inject_labels, render_svg, transposition_interval
from ppe.selection import inspect
from ppe.serialize import piece_json
from ppe.spelling import pretty
from ppe.transform import candidates, transpose_label

WEB = Path(__file__).resolve().parents[1] / "web"
FIFTHS_MAJOR = ["C♭", "G♭", "D♭", "A♭", "E♭", "B♭", "F", "C", "G", "D", "A", "E", "B", "F♯", "C♯"]
FIFTHS_MINOR = ["A♭", "E♭", "B♭", "F", "C", "G", "D", "A", "E", "B", "F♯", "C♯", "G♯", "D♯", "A♯"]

app = FastAPI(title="Passage Laboratory")


def _pack_mtime(pid: str) -> float:
    if pid not in pieces.built():
        raise HTTPException(404, f"piece '{pid}' is not built; run `python -m ppe build`")
    return (pieces.pack_dir(pid) / "piece.pkl").stat().st_mtime


@functools.lru_cache(maxsize=8)
def _load(pid: str, mtime: float):
    return pieces.load(pid)


@functools.lru_cache(maxsize=8)
def _load_json(pid: str, mtime: float) -> dict:
    return piece_json(_load(pid, mtime))


def get_piece(pid: str):
    """The built piece; reloaded automatically when its pack is rebuilt."""
    return _load(pid, _pack_mtime(pid))


def get_piece_json(pid: str) -> dict:
    return _load_json(pid, _pack_mtime(pid))


@app.get("/api/pieces")
def list_pieces():
    built = set(pieces.built())
    return [{"id": pid, "title": s.title, "subtitle": s.subtitle, "composer": s.composer,
             "built": pid in built, "requires": s.requires} for pid, s in pieces.SPECS.items()]


@app.get("/api/pieces/{pid}")
def piece(pid: str):
    return get_piece_json(pid)


@app.get("/api/pieces/{pid}/score")
def score(pid: str, width: int = 1100, transpose: int = 0, lenses: str = "", scale: int = 40):
    p = get_piece(pid)
    ids = [a for a in lenses.split(",") if a]
    known = {a.id for a in p.analyses}
    if any(a not in known for a in ids):
        raise HTTPException(400, f"unknown analysis in {ids}")
    mei = inject_labels(p.mei, p, ids, {a.id: a.colour for a in p.analyses}) if ids else p.mei
    key_fifths = p.measures[0].key_fifths
    interval, fifths = transposition_interval(transpose, key_fifths)
    pages = render_svg(mei, max(600, min(width, 2400)), interval, max(25, min(scale, 60)))
    new_fifths = key_fifths + fifths
    return {"pages": list(pages),
            "transpose": {"semitones": transpose, "interval": interval, "key_fifths": new_fifths,
                          "key_names": _key_names(new_fifths)}}


def _key_names(fifths: int) -> dict:
    i = fifths + 7
    ok = 0 <= i < 15
    return {"major": FIFTHS_MAJOR[i] if ok else None, "minor": FIFTHS_MINOR[i] if ok else None}


class InspectReq(BaseModel):
    ids: list[str] | None = None
    start: float | None = None
    end: float | None = None
    transpose: int = 0


def _frac(x: float | None) -> Fraction | None:
    return None if x is None else Fraction(x).limit_denominator(960)


@app.post("/api/pieces/{pid}/inspect")
def inspect_selection(pid: str, req: InspectReq):
    p = get_piece(pid)
    if not req.ids and (req.start is None or req.end is None):
        raise HTTPException(400, "give ids or start/end")
    return inspect(p, req.ids, _frac(req.start), _frac(req.end), transpose=max(-11, min(11, req.transpose)))


class Substitution(BaseModel):
    label: str
    figure: str


class PlaybackReq(BaseModel):
    start: float
    end: float
    mode: str = "original"
    analysis: str | None = None
    tracks: list[str] | None = None
    transpose: int = 0
    substitution: Substitution | None = None
    pedal: bool = False


@app.post("/api/pieces/{pid}/playback")
def playback(pid: str, req: PlaybackReq):
    p = get_piece(pid)
    sub = None
    if req.substitution:
        lab = next((l for a in p.analyses for l in a.labels if l.id == req.substitution.label), None)
        if lab is None:
            raise HTTPException(404, "label not found")
        cand = next((c for c in candidates(lab, limit=40) if c["figure"] == req.substitution.figure), None)
        if cand is None:
            raise HTTPException(400, "unknown substitute")
        sub = (lab, cand["pitches"])
    try:
        events, info = build_playback(p, start=_frac(req.start), end=_frac(req.end), mode=req.mode,
                                      analysis=req.analysis, tracks=set(req.tracks) if req.tracks else None,
                                      transpose=req.transpose, substitution=sub,
                                      pedal=req.pedal and bool(req.analysis))
    except ValueError as e:
        raise HTTPException(400, str(e)) from e
    return {"events": [e.to_json() for e in events], "info": info, "qpm": p.tempo_qpm}


@app.get("/api/pieces/{pid}/labels/{label_id}/alternatives")
def alternatives(pid: str, label_id: str, transpose: int = 0):
    p = get_piece(pid)
    lab = next((l for a in p.analyses for l in a.labels if l.id == label_id), None)
    if lab is None:
        raise HTTPException(404, "label not found")
    interval, _ = transposition_interval(transpose, p.measures[0].key_fifths)
    shown = transpose_label(lab, interval, transpose)  # figures and distances are transposition-invariant
    return {"label": label_id, "original": {"display": shown.display, "pitches": [pretty(x) for x in shown.pitches]},
            "candidates": candidates(shown)}


@app.get("/")
def index():
    return FileResponse(WEB / "index.html")


app.mount("/", StaticFiles(directory=WEB), name="web")
