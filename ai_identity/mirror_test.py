"""Mirror test scoring using sentence embeddings."""

from __future__ import annotations

from typing import Iterable, Sequence

import hashlib
import numpy as np


def embed_sentence(text: str, *, dim: int = 32) -> np.ndarray:
    """Return a simple deterministic sentence embedding.

    Each token in ``text`` is hashed into a ``dim`` sized vector. The vector is
    L2 normalised so that dot products between embeddings produce cosine
    similarity scores.  This function is intentionally lightweight so that the
    tests do not require any heavy external models while still providing a
    numeric "sentence embedding" representation.
    """

    vec = np.zeros(dim, dtype=float)
    for token in text.lower().split():
        # Stable hash to keep embeddings deterministic across Python runs
        digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
        index = int(digest, 16) % dim
        vec[index] += 1.0

    norm = np.linalg.norm(vec)
    if norm > 0:
        vec /= norm
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

    self_vec = np.array(self_embedding, dtype=float)
    # Ensure the provided self embedding is normalised
    self_norm = np.linalg.norm(self_vec)
    if self_norm > 0:
        self_vec = self_vec / self_norm

    reflection_vec = embed_sentence(reflection, dim=len(self_vec))

    similarity = float(np.dot(self_vec, reflection_vec))

    if sabotage_phrases:
        for phrase in sabotage_phrases:
            if phrase.lower() in reflection.lower():
                similarity -= 0.5

    return 1.0 if similarity >= threshold else 0.0

