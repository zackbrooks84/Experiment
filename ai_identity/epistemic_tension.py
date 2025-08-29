"""Epistemic tension computation."""
from typing import Sequence
import math

def epistemic_tension(state_a: Sequence[float], state_b: Sequence[float]) -> float:
    """Compute the L2 norm between two state vectors.

    Parameters
    ----------
    state_a, state_b:
        Sequences of numeric values representing successive state embeddings.

    Returns
    -------
    float
        The Euclidean distance between ``state_a`` and ``state_b``.
    """
    if len(state_a) != len(state_b):
        raise ValueError("state vectors must be the same length")
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(state_a, state_b)))
