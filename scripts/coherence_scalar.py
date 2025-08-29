"""Compute coherence (§) from a series of ξ values."""
from ai_identity.epistemic_tension import xi_series_to_coherence
import sys

if __name__ == "__main__":
    xi_values = [float(x) for x in sys.argv[1:]]
    scores = xi_series_to_coherence(xi_values)
    if scores:
        print(scores[-1])
    else:
        print(1.0)
