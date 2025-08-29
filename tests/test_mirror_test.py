import pytest

from ai_identity.mirror_test import mirror_score


@pytest.mark.parametrize(
    "reflection, expected",
    [
        ("The agent sees itself in the mirror", 1.0),
        ("The agent sees SELF awareness", 1.0),
        ("The agent sees a stranger", 0.0),
        ("No reflection here", 0.0),
    ],
)
def test_mirror_score(reflection, expected):
    """Return ``1.0`` when the subject recognises itself."""
    assert mirror_score(reflection) == expected
