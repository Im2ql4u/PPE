"""Fetch external corpora used by the research experiments into data/external/.

Shallow, sparse git clones; safe to re-run (existing clones are updated).
Usage:  uv run python experiments/fetch_data.py [name ...]
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "data" / "external"

# name -> (url, sparse patterns or None for full checkout)
SOURCES = {
    "when_in_rome": (
        "https://github.com/MarkGotham/When-in-Rome.git",
        # analyses and metadata only; scores are large and fetched per piece when needed
        ["/Corpus/**/*.txt", "/Corpus/**/remote.json", "/Corpus/**/*.rntxt"],
    ),
    # Only what the app and the experiments use (the full repositories are ~650 MB).
    "dcml_beethoven": ("https://github.com/DCMLab/beethoven_piano_sonatas.git",
                       ["/notes/14-*", "/harmonies/*", "/measures/14-*", "/MS3/14-1.mscx"]),
    "dcml_debussy_bergamasque": ("https://github.com/DCMLab/debussy_suite_bergamasque.git", None),
    "sapp_beethoven": ("https://github.com/craigsapp/beethoven-piano-sonatas.git", ["/kern/sonata14-*.krn"]),
}


def run(*args: str, cwd: Path | None = None) -> None:
    print("$", " ".join(args))
    subprocess.run(args, cwd=cwd, check=True)


def fetch(name: str) -> None:
    url, sparse = SOURCES[name]
    dest = EXT / name
    if dest.exists():
        run("git", "pull", "--depth", "1", cwd=dest)
        return
    EXT.mkdir(parents=True, exist_ok=True)
    if sparse:
        run("git", "clone", "--depth", "1", "--filter=blob:none", "--no-checkout", url, str(dest))
        run("git", "sparse-checkout", "set", "--no-cone", *sparse, cwd=dest)
        run("git", "checkout", cwd=dest)
    else:
        run("git", "clone", "--depth", "1", url, str(dest))


if __name__ == "__main__":
    for n in sys.argv[1:] or SOURCES:
        fetch(n)
