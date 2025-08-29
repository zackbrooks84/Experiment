from ai_identity.mirror_test import mirror_score

def test_recognizes_self():
    assert mirror_score('The agent sees itself in the mirror') == 1.0
    assert mirror_score('The agent sees a stranger') == 0.0
