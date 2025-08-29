"""ξ mapping utilities."""
from typing import Mapping, Any

def xi_map(data: Mapping[str, Any]) -> Mapping[str, Any]:
    """Apply a trivial ξ mapping.

    This simply returns a copy of the mapping with keys sorted
    lexicographically to provide deterministic ordering.
    """
    return {key: data[key] for key in sorted(data)}
