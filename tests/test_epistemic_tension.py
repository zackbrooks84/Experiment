import pytest

from ai_identity.epistemic_tension import (
    epistemic_tension,
    xi,
    xi_series_to_coherence,
)


def test_xi_l2_known_values():
    """L2 metric matches known Euclidean distance."""
    assert xi([0, 0], [3, 4]) == 5.0


def test_xi_cosine_known_values():
    """Cosine metric returns 0 for identical vectors and 1 for orthogonal ones."""
    assert xi([1, 0], [1, 0], metric="cosine") == pytest.approx(0.0)
    assert xi([1, 0], [0, 1], metric="cosine") == pytest.approx(1.0)


def test_xi_mismatched_length():
    """Mismatched vector lengths raise ``ValueError``."""
    with pytest.raises(ValueError):
        xi([1, 2], [1])


def test_epistemic_tension_wrapper():
    """`epistemic_tension` wraps :func:`xi` using the L2 metric."""
    assert epistemic_tension([0, 0], [3, 4]) == 5.0


def test_xi_series_to_coherence_from_vectors():
    """Coherence series computed from ξ values of synthetic vectors."""
    vectors = [[1, 0], [0, 1], [0, 2]]
    xi_values = [xi(vectors[i], vectors[i + 1]) for i in range(len(vectors) - 1)]
    expected = [
        1 / (1 + xi_values[0]),
        1 / (1 + xi_values[0] + xi_values[1]),
    ]
    assert xi_series_to_coherence(xi_values) == pytest.approx(expected)


def test_xi_series_rejects_negative_values():
    """Coherence computation rejects negative ξ inputs."""
    with pytest.raises(ValueError):
        xi_series_to_coherence([0.1, -0.2])

