from ai_identity.anchor_detection import detect_anchors

def test_detects_repeated_items():
    anchors = detect_anchors(['a', 'b', 'a', 'c', 'b'])
    assert set(anchors) == {'a', 'b'}
