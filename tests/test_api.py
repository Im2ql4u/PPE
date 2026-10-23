"""End-to-end through the HTTP API (uses the built packs in data/packs)."""

import pytest
from fastapi.testclient import TestClient

from ppe import pieces
from ppe.api import app


@pytest.fixture(scope="module")
def client():
    if "moonlight" not in pieces.built():
        pytest.skip("packs not built (python -m ppe build)")
    return TestClient(app)


def test_piece_list_and_payload(client):
    lst = client.get("/api/pieces").json()
    assert {p["id"] for p in lst} >= {"moonlight", "bach-prelude-c", "clair-de-lune"}
    p = client.get("/api/pieces/moonlight").json()
    assert [a["id"] for a in p["analyses"]] == ["BPS", "DT"]
    assert p["comparisons"][0]["summary"]["strict_agreement"] > 0.6


def test_score_svg_contains_every_note(client):
    p = client.get("/api/pieces/moonlight").json()
    s = client.get("/api/pieces/moonlight/score", params={"width": 1200}).json()
    svg = "".join(s["pages"])
    missing = [n["rid"] for n in p["notes"] if f'id="{n["rid"]}"' not in svg]
    assert not missing, missing[:5]


def test_inspect_harmony_selection(client):
    p = client.get("/api/pieces/moonlight").json()
    m16 = next(m for m in p["measures"] if m["n"] == 16)
    r = client.post("/api/pieces/moonlight/inspect", json={"start": m16["on"], "end": m16["on"] + m16["dur"]}).json()
    assert r["span"]["text"] == "m. 16"
    assert {c["cls"] for c in r["comparisons"]} == {"key_frame"}
    readings = {l["analysis"]: l for l in r["lenses"]}
    assert readings["BPS"]["primary"] and readings["DT"]["primary"]


def test_playback_and_alternatives(client):
    r = client.post("/api/pieces/moonlight/playback", json={"start": 0, "end": 4, "mode": "blocked"}).json()
    assert r["events"] and r["qpm"] > 0
    alt = client.get("/api/pieces/moonlight/labels/BPS-3/alternatives").json()
    assert alt["candidates"]
    fig = alt["candidates"][0]["figure"]
    r2 = client.post("/api/pieces/moonlight/playback",
                     json={"start": 10, "end": 12, "substitution": {"label": "BPS-3", "figure": fig}}).json()
    assert "moves" in r2["info"]


def test_bad_requests_are_rejected(client):
    assert client.get("/api/pieces/nope").status_code == 404
    assert client.post("/api/pieces/moonlight/playback", json={"start": 0, "end": 4, "mode": "chord_tones"}).status_code == 400
