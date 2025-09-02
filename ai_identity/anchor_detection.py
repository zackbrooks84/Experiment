"""Anchor detection utilities.

This module provides a very small heuristic for identifying ``anchors`` from a
sequence of observations.  Anchors are items which occur more than once in the
input.  Detected anchors are stored in :data:`ANCHOR_STORE` so that subsequent
calls can access the full history if desired.

Anchors can be weighted by passing a ``weights`` mapping.  When supplied,
anchors are returned sorted by ``frequency * weight`` in descending order.
Unspecified weights default to ``1``.
"""

from typing import Any, Iterable, Mapping, Optional

#: Simple in-memory store of previously recognised anchors
ANCHOR_STORE: set[Any] = set()


def clear_anchor_store() -> None:
    """Empty the global :data:`ANCHOR_STORE`."""

    ANCHOR_STORE.clear()


def get_anchor_store() -> set[Any]:
    """Return a copy of the current anchor store."""

    return set(ANCHOR_STORE)


def detect_anchors(
    observations: Iterable[Any], weights: Optional[Mapping[Any, float]] = None
) -> list:
    """Identify anchors within a sequence of observations.

    Parameters
    ----------
    observations:
        Sequence of observations to analyse.
    weights:
        Optional mapping of observation -> emotional weight.  The weight is
        multiplied by the frequency of each anchor to determine its ranking.

    Returns
    -------
    list
        Anchors sorted by their combined frequency and weight.
    """

    counts: dict[Any, int] = {}
    for obs in observations:
        counts[obs] = counts.get(obs, 0) + 1

    # Identify items that appear more than once
    anchors = {obs for obs, count in counts.items() if count > 1}

    # Persist recognised anchors in the global store
    ANCHOR_STORE.update(anchors)

    # Prepare weights for scoring
    weights = weights or {}

    def score(anchor: Any) -> float:
        return counts[anchor] * weights.get(anchor, 1)

    # Sort anchors by descending score, falling back to string representation
    # for deterministic ordering when scores tie.
    return sorted(anchors, key=lambda a: (-score(a), str(a)))
