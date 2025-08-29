import pytest

from ai_identity.epistemic_tension import epistemic_tension


def test_epistemic_tension_zero():
    """Zero distance for identical states."""
    assert epistemic_tension([0, 0], [0, 0]) == 0.0


def test_epistemic_tension_known_values():
    """Distance matches known Euclidean value."""
    assert epistemic_tension([0, 0], [3, 4]) == 5.0


def test_epistemic_tension_mismatched_length():
    """Mismatched vector lengths raise ``ValueError``."""
    with pytest.raises(ValueError):
        epistemic_tension([1, 2], [1])
