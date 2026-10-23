# Passage Laboratory: research repository

Research for a personal, local-first environment for learning piano: to perceive music as a system of relationships between notation, sound, keyboard geometry, harmony, performance and imagination.

**Status:** research phase. No application code yet.

- Start with [docs/synthesis.md](docs/synthesis.md), then [docs/product-concepts.md](docs/product-concepts.md).
- Working state and resume point: [docs/research-plan.md](docs/research-plan.md).
- Experiments: [experiments/](experiments/) (each folder has a README with question, method, results and limits).

## Setup

```sh
uv sync                                   # Python 3.12 environment in .venv
uv run python experiments/fetch_data.py   # corpora → data/external/ (gitignored)
uv run python experiments/e1_render_and_address/render_address.py
```

Runs on macOS and Windows. The future app targets macOS + Chrome.

## Data licences

The fetched corpora keep their own licences: DCML (CC BY-NC-SA 4.0), When in Rome (CC BY-SA 4.0 / per source), (n)ASAP (CC BY-NC-SA 4.0), Sapp Beethoven kern (no licence file; private use). Nothing from them is committed here.
