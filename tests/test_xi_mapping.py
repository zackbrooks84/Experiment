from ai_identity.xi_mapping import xi_map

def test_sorting():
    result = xi_map({'b': 2, 'a': 1})
    assert list(result.keys()) == ['a', 'b']
