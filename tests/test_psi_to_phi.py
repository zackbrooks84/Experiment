from ai_identity.psi_to_phi import psi_to_phi

def test_identity_mapping():
    assert psi_to_phi({'state': 1}) == {'state': 1}
