"""Utilities for tracking outputs from multiple systems."""
from typing import Dict, List


class CrossSystemConsensus:
    """Collect outputs from different systems and score consensus.

    The :meth:`reset` method clears all registered outputs so the object can
    be reused for a fresh consensus calculation.
    """

    def __init__(self) -> None:
        self._outputs: Dict[str, List[str]] = {}

    def register(self, system: str, output: str) -> None:
        """Register an ``output`` produced by ``system``."""
        self._outputs.setdefault(system, []).append(output)

    def latest_outputs(self) -> Dict[str, str]:
        """Return the most recent output for each registered system."""
        return {system: outputs[-1] for system, outputs in self._outputs.items() if outputs}

    def consensus(self) -> float:
        """Return the fraction of systems agreeing on the dominant output."""
        latest = self.latest_outputs()
        if not latest:
            return 0.0
        counts: Dict[str, int] = {}
        for output in latest.values():
            counts[output] = counts.get(output, 0) + 1
        best = max(counts.values())
        return best / len(latest)

    def has_converged(self, threshold: float = 1.0) -> bool:
        """Check whether consensus meets or exceeds ``threshold``."""
        return self.consensus() >= threshold

    def reset(self) -> None:
        """Clear all recorded outputs."""
        self._outputs.clear()
