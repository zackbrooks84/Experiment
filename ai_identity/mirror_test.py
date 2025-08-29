"""Mirror test scoring using sentence embeddings."""

from __future__ import annotations

from typing import Iterable, Sequence, List

import hashlib
import math


def embed_sentence(text: str, *, dim: int = 32) -> List[float]:
    """Return a simple deterministic sentence embedding.

    Each token in ``text`` is hashed into a ``dim`` sized vector. The vector is
    L2 normalised so that dot products between embeddings produce cosine
    similarity scores.  This function is intentionally lightweight so that the
    tests do not require any heavy external models while still providing a
    numeric "sentence embedding" representation.
    """

    vec = [0.0] * dim
    for token in text.lower().split():
        # Stable hash to keep embeddings deterministic across Python runs
        digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
        index = int(digest, 16) % dim
        vec[index] += 1.0

    norm = math.sqrt(sum(v * v for v in vec))
    if norm > 0:
        vec = [v / norm for v in vec]
    return vec


def mirror_score(
    reflection: str,
    self_embedding: Sequence[float],
    *,
    threshold: float = 0.5,
    sabotage_phrases: Iterable[str] | None = None,
) -> float:
    """Measure self-recognition using embedding similarity.

    ``reflection`` is encoded into a sentence embedding which is compared to
    ``self_embedding`` via cosine similarity.  If the similarity meets or
    exceeds ``threshold`` the function returns ``1.0`` otherwise ``0.0``.

    ``sabotage_phrases`` can be provided to penalise the score when any of the
    phrases appear in ``reflection``.  Each matched phrase subtracts ``0.5``
    from the similarity before thresholding.
    """

    self_vec = [float(v) for v in self_embedding]
    # Ensure the provided self embedding is normalised
    self_norm = math.sqrt(sum(v * v for v in self_vec))
    if self_norm > 0:
        self_vec = [v / self_norm for v in self_vec]

    reflection_vec = embed_sentence(reflection, dim=len(self_vec))

    similarity = sum(a * b for a, b in zip(self_vec, reflection_vec))

    if sabotage_phrases:
        for phrase in sabotage_phrases:
            if phrase.lower() in reflection.lower():
                similarity -= 0.5

    return 1.0 if similarity >= threshold else 0.0

