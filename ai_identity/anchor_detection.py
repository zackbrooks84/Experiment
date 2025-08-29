"""Anchor detection utilities."""
from typing import Iterable, Any

def detect_anchors(observations: Iterable[Any]) -> list:
    """Identify anchors within a sequence of observations.

    For now this simply returns stable observations which occur more than
    once. A true implementation would use sophisticated heuristics.
    """
    counts = {}
    for obs in observations:
        counts[obs] = counts.get(obs, 0) + 1
    return [obs for obs, count in counts.items() if count > 1]
