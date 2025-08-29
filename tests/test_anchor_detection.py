import pytest

from ai_identity.anchor_detection import detect_anchors


@pytest.mark.parametrize(
    "observations, expected",
    [
        (['a', 'b', 'a', 'c', 'b'], {'a', 'b'}),
        ([1, 2, 3], set()),
        ([], set()),
    ],
)
def test_detect_anchors(observations, expected):
    """Detect anchors when items repeat and ignore unique items."""
    assert set(detect_anchors(observations)) == expected


def test_detect_anchors_rejects_unhashable():
    """Unhashable items should raise ``TypeError`` when counted."""
    with pytest.raises(TypeError):
        detect_anchors([[1], [1]])


def test_detect_anchors_handles_objects():
    """The detection works with arbitrary hashable objects."""
    class Item:
        pass

    obj = Item()
    assert detect_anchors([obj, obj]) == [obj]
