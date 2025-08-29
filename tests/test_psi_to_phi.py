import pytest

from ai_identity.psi_to_phi import psi_to_phi


def test_returns_psi_before_convergence():
    t = 0.0
    expected = 0.0
    phi = psi_to_phi(t)
    assert phi == expected
    assert phi != 1.0


def test_converges_to_phi_when_derivative_small():
    t = 10.0
    phi = psi_to_phi(t, epsilon=1e-3)
    assert phi == 1.0


def test_derivative_decays_towards_root():
    def dpsi_dt(time: float) -> float:
        return 0.0216 * time ** 2 - 0.288 * time + 0.72

    derivatives = [abs(dpsi_dt(t)) for t in [0, 1, 2, 3]]
    for earlier, later in zip(derivatives, derivatives[1:]):
        assert earlier > later
