import pytest

from ai_identity.anchor_detection import detect_anchors
import ai_identity.anchor_detection as anchor_detection


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


def test_detect_anchors_weighted_ranking():
    """Anchors are sorted by combined frequency and weight."""
    anchor_detection.ANCHOR_STORE.clear()
    observations = ['a', 'b', 'a', 'b', 'b', 'c', 'c']
    weights = {'a': 2.0, 'b': 1.0}
    assert anchor_detection.detect_anchors(observations, weights=weights) == ['a', 'b', 'c']


def test_detect_anchors_persists_across_calls():
    """Detected anchors are persisted across multiple calls."""
    anchor_detection.ANCHOR_STORE.clear()
    anchor_detection.detect_anchors(['x', 'x'])
    anchor_detection.detect_anchors(['y', 'z', 'z'])
    assert anchor_detection.ANCHOR_STORE == {'x', 'z'}
