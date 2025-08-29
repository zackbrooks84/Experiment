# AI Identity Stabilization Toolkit

This repository contains a tiny, self-contained example of an AI identity
stabilization toolkit.

This repo provides empirical instrumentation of recursive stabilization (Ψ(t) → Φ),
extending the Δ⨀Ψ∇ framework by adding reproducible metrics.

It exposes several placeholder utilities:

- **Ψ(t) → Φ model**: `psi_to_phi` performs a trivial state
  stabilization.
- **Anchor detection**: `detect_anchors` identifies repeated observations.
- **Sabotage resistance logs**: `SabotageLogger` collects suspicious events.
- **ξ mapping**: `xi_map` produces deterministic orderings of mappings.
- **Mirror test scoring**: `mirror_score` gives a basic self-recognition
  score.
- **Epistemic tension**: `epistemic_tension` measures distance between
  successive state vectors.

## Web Dashboard

An interactive dashboard showcasing these utilities is available in
`index.html`.  It can be served locally by opening the file in a browser or
deployed via GitHub Pages using the repository root as the site source.  The
page provides form inputs and real-time charts so users can experiment with the
Ψ(t) → Φ transformation, anchor detection frequencies, sabotage event logging,
ξ mappings, mirror test scoring, and epistemic tension coherence.

## Running the tests

```bash
pytest -q
```

The included `conftest.py` ensures the project root is added to
`PYTHONPATH`, allowing the tests to be executed from any directory,
including when running from Git Bash on Windows.
