"""Epistemic tension computation utilities.

This module exposes a generic :func:`xi` function for measuring the
"epistemic tension" between successive state embeddings.  Two distance
metrics are provided:

``l2``
    Standard Euclidean distance between vectors.

``cosine``
    Cosine distance ``1 - cos(θ)`` where ``θ`` is the angle between the
    vectors.

Additionally, :func:`xi_series_to_coherence` converts a series of ξ values
into coherence (§) scores as described in Appendix A of the specification.
The coherence after each step is ``1 / (1 + Σ ξ)``.
"""

from __future__ import annotations

from typing import Iterable, Sequence, List
import math


def xi(
    state_a: Sequence[float],
    state_b: Sequence[float],
    *,
    metric: str = "l2",
) -> float:
    """Compute epistemic tension between two state vectors.

    Parameters
    ----------
    state_a, state_b:
        Sequences of numeric values representing successive state
        embeddings.  Both sequences must be of equal length.
    metric:
        The distance metric to use.  Supported values are ``"l2"`` for
        Euclidean distance and ``"cosine"`` for cosine distance.

    Returns
    -------
    float
        The distance between ``state_a`` and ``state_b`` under the
        requested metric.
    """

    if len(state_a) != len(state_b):
        raise ValueError("state vectors must be the same length")

    if metric == "l2":
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(state_a, state_b)))

    if metric == "cosine":
        dot = sum(a * b for a, b in zip(state_a, state_b))
        norm_a = math.sqrt(sum(a * a for a in state_a))
        norm_b = math.sqrt(sum(b * b for b in state_b))
        if norm_a == 0 or norm_b == 0:
            raise ValueError("state vectors must be non-zero for cosine metric")
        return 1 - (dot / (norm_a * norm_b))

    raise ValueError(f"unsupported metric '{metric}'")


def epistemic_tension(
    state_a: Sequence[float], state_b: Sequence[float], *, metric: str = "l2"
) -> float:
    """Backward compatible wrapper around :func:`xi`.

    ``epistemic_tension(a, b)`` is equivalent to ``xi(a, b, metric="l2")`` by
    default, but the ``metric`` parameter is exposed for completeness.
    """

    return xi(state_a, state_b, metric=metric)


def xi_series_to_coherence(xi_series: Iterable[float]) -> List[float]:
    """Convert a series of ξ values into coherence (§) scores.

    The coherence after each step ``k`` is defined as::

        §_k = 1 / (1 + Σ_{i=1..k} ξ_i)

    Parameters
    ----------
    xi_series:
        Iterable of non-negative ξ values.

    Returns
    -------
    list of float
        Coherence score after each successive ξ.
    """

    coherence: List[float] = []
    cumulative = 0.0
    for xi_value in xi_series:
        if xi_value < 0:
            raise ValueError("ξ values must be non-negative")
        cumulative += xi_value
        coherence.append(1.0 / (1.0 + cumulative))
    return coherence


__all__ = ["xi", "epistemic_tension", "xi_series_to_coherence"]

