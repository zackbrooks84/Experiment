"""Compute epistemic tension ξ between two vectors."""
from ai_identity.epistemic_tension import xi
import sys


def parse_vector(text: str) -> list[float]:
    return [float(x) for x in text.split(",") if x]


if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit("usage: compute_xi.py vecA vecB")
    a = parse_vector(sys.argv[1])
    b = parse_vector(sys.argv[2])
    print(xi(a, b))
