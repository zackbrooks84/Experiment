import pytest
from ai_identity.cross_system import CrossSystemConsensus


def test_consensus_scoring():
    """Registers votes across systems and reports convergence."""
    consensus = CrossSystemConsensus()
    consensus.register("sys1", "a")
    consensus.register("sys2", "a")
    consensus.register("sys3", "b")

    # two of three systems agree
    assert consensus.consensus() == pytest.approx(2/3)
    assert not consensus.has_converged()
    assert consensus.has_converged(threshold=0.5)
