import pytest

from ai_identity.xi_mapping import xi_map


@pytest.mark.parametrize(
    "data, expected_order",
    [
        ({'b': 2, 'a': 1}, ['a', 'b']),
        ({'c': 3, 'b': 2, 'a': 1}, ['a', 'b', 'c']),
    ],
)
def test_sorting(data, expected_order):
    """Keys are sorted lexicographically in the returned mapping."""
    result = xi_map(data)
    assert list(result.keys()) == expected_order


def test_returns_new_mapping():
    """The original mapping is not modified in-place."""
    original = {'b': 2, 'a': 1}
    result = xi_map(original)
    assert result is not original
