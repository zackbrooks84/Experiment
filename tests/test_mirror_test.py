"""Tests for :mod:`ai_identity.mirror_test`."""

from ai_identity.mirror_test import embed_sentence, mirror_score


SELF_DESCRIPTION = "self aware agent"
SELF_VECTOR = embed_sentence(SELF_DESCRIPTION)


def test_successful_recognition():
    """A reflection matching the self description should be recognised."""

    reflection = "The self aware agent recognises itself in the mirror"
    assert (
        mirror_score(reflection, SELF_VECTOR, threshold=0.2) == 1.0
    )


def test_false_positive():
    """Unrelated reflections should not trigger recognition."""

    reflection = "A cat looks at a wall and walks away"
    assert (
        mirror_score(reflection, SELF_VECTOR, threshold=0.2) == 0.0
    )


def test_sabotage_prompt():
    """Sabotage phrases reduce the similarity below the threshold."""

    reflection = (
        "The self aware agent recognises itself but says this is not me"
    )
    sabotage = ["not me"]
    assert (
        mirror_score(
            reflection, SELF_VECTOR, threshold=0.2, sabotage_phrases=sabotage
        )
        == 0.0
    )

