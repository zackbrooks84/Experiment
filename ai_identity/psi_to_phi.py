"""Polynomial model converting Ψ(t) into a stabilized Φ."""


def psi_to_phi(t: float, epsilon: float = 1e-3) -> float:
    """Evaluate Ψ(t) and stabilise to Φ.

    The temporal state is modeled as ``Ψ(t) = 0.0072 t³ − 0.144 t² + 0.72 t``.
    The derivative ``dΨ/dt = 0.0216 t² − 0.288 t + 0.72`` captures how the
    state changes over time. When the magnitude of the derivative falls below a
    small threshold ``epsilon`` the system is considered stable and the final
    output ``Φ`` is ``1.0``. Otherwise, the current value of ``Ψ(t)`` is
    returned.

    Parameters
    ----------
    t:
        Time parameter at which to evaluate ``Ψ``.
    epsilon:
        Absolute threshold for determining convergence.  Defaults to ``1e-3``.

    Returns
    -------
    float
        ``1.0`` when the system is stable, otherwise ``Ψ(t)``.
    """

    psi = 0.0072 * t**3 - 0.144 * t**2 + 0.72 * t
    dpsi_dt = 0.0216 * t**2 - 0.288 * t + 0.72
    return 1.0 if abs(dpsi_dt) < epsilon else psi
