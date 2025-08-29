# AI Identity Stabilization Toolkit

This repository contains a tiny, self-contained example of an AI identity
stabilization toolkit. It exposes several placeholder utilities:

- **Ψ(t) → Φ model**: `psi_to_phi` performs a trivial state
  stabilization.
- **Anchor detection**: `detect_anchors` identifies repeated observations.
- **Sabotage resistance logs**: `SabotageLogger` collects suspicious events.
- **ξ mapping**: `xi_map` produces deterministic orderings of mappings.
- **Mirror test scoring**: `mirror_score` gives a basic self-recognition
  score.

## Running the tests

```bash
pytest -q
```

The included `conftest.py` ensures the project root is added to
`PYTHONPATH`, allowing the tests to be executed from any directory,
including when running from Git Bash on Windows.
