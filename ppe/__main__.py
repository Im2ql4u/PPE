"""Command line: python -m ppe {fetch,convert,build,serve,doctor}."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def cmd_fetch(_args) -> None:
    """Download the corpora used by the reference pieces into data/external (git, shallow)."""
    subprocess.run([sys.executable, str(ROOT / "experiments" / "fetch_data.py")], check=True)
    from urllib.request import urlretrieve

    asap = ROOT / "data" / "external" / "asap_bwv846"
    asap.mkdir(parents=True, exist_ok=True)
    target = asap / "xml_score.musicxml"
    if not target.exists():
        print("downloading ASAP BWV 846 score …")
        urlretrieve("https://raw.githubusercontent.com/CPJKU/asap-dataset/main/Bach/Prelude/bwv_846/xml_score.musicxml", target)


def find_musescore() -> str | None:
    import os

    env = os.environ.get("MUSESCORE")
    if env and Path(env).exists():
        return env
    for c in ["mscore", "mscore4portable", "musescore", "MuseScore4", "MuseScore3",
              "/Applications/MuseScore 4.app/Contents/MacOS/mscore",
              "/Applications/MuseScore 3.app/Contents/MacOS/mscore",
              r"C:\Program Files\MuseScore 4\bin\MuseScore4.exe", r"C:\Program Files\MuseScore 3\bin\MuseScore3.exe"]:
        p = shutil.which(c) or (c if Path(c).exists() else None)
        if p:
            return p
    return None


def cmd_convert(_args) -> None:
    """Convert DCML MuseScore files to MusicXML (needs MuseScore; see docs/mac-setup.md)."""
    ms = find_musescore()
    if not ms:
        sys.exit("MuseScore not found. Install it (docs/mac-setup.md) and re-run.")
    src = ROOT / "data" / "external" / "dcml_debussy_bergamasque" / "MS3" / "l075-03_suite_clair.mscx"
    out = ROOT / "data" / "external" / "converted"
    out.mkdir(parents=True, exist_ok=True)
    target = out / "l075-03_suite_clair.musicxml"
    print(f"{ms} -o {target} {src}")
    subprocess.run([ms, "-o", str(target), str(src)], check=True)
    print("converted. Next: uv run python -m ppe build clair-de-lune")


def cmd_build(args) -> None:
    from ppe import pieces

    ids = args.pieces or pieces.available()
    missing = [p for p in pieces.SPECS if p not in pieces.available()]
    for p in missing:
        print(f"skip {p}: sources missing. {pieces.SPECS[p].requires}")
    for pid in ids:
        print(f"building {pid} …", flush=True)
        piece = pieces.build_piece(pid)
        pieces.save(piece)
        v = piece.validation
        print(f"  {len(piece.notes)} notes; cross-check with {v['crosscheck']['independent_parser']}: "
              f"{v['crosscheck']['agreement_rate']:.1%} agreement; unexplained discrepancies: {len(v['unexplained_discrepancies'])}")
        for aid, al in v["alignment"].items():
            print(f"  {aid}: chord-tone fit {al['0']:.1%} at its alignment; best at zero shift: {al['best_is_zero']}")
            for issue in v["analysis_issues"][aid]:
                print(f"    note: {issue}")


def cmd_serve(args) -> None:
    import uvicorn

    print(f"Passage Laboratory → http://{args.host}:{args.port}")
    uvicorn.run("ppe.api:app", host=args.host, port=args.port, reload=args.reload)


def cmd_doctor(_args) -> None:
    from ppe import pieces
    from ppe.render import verovio_version

    print("verovio", verovio_version())
    print("musescore", find_musescore() or "not found (only needed for Clair de lune)")
    print("sources available:", pieces.available())
    print("packs built:", pieces.built())


def main() -> None:
    ap = argparse.ArgumentParser(prog="python -m ppe")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("fetch").set_defaults(fn=cmd_fetch)
    sub.add_parser("convert").set_defaults(fn=cmd_convert)
    b = sub.add_parser("build")
    b.add_argument("pieces", nargs="*")
    b.set_defaults(fn=cmd_build)
    s = sub.add_parser("serve")
    s.add_argument("--host", default="127.0.0.1")
    s.add_argument("--port", type=int, default=8765)
    s.add_argument("--reload", action="store_true")
    s.set_defaults(fn=cmd_serve)
    sub.add_parser("doctor").set_defaults(fn=cmd_doctor)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
