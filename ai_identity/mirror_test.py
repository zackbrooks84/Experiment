"""Mirror test scoring."""

def mirror_score(reflection: str) -> float:
    """Return a simple score based on whether the subject recognizes itself.

    This placeholder returns 1.0 when the string contains the word
    'self' and 0.0 otherwise.
    """
    return 1.0 if 'self' in reflection.lower() else 0.0
