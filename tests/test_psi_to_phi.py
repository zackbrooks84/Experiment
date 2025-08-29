import pytest

from ai_identity.psi_to_phi import psi_to_phi


@pytest.mark.parametrize("psi", [
    {"state": 1},
    [1, 2, 3],
    "text",
])
def test_identity_mapping_returns_same_object(psi):
    """The transformation should return the same object instance."""
    phi = psi_to_phi(psi)
    assert phi == psi
    assert phi is psi
