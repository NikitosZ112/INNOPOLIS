import pytest
from lesson_two.src.main import search_array

@pytest.mark.parametrize(
    'arr, x, expected',
    [
        ([1, 2, None, None, 5, 6, 7, None, 10, 11], 5, 4),   # Элемент присутствует
        ([1, 2, None, None, 5, 6, 7, None, 10, 11], 11, 9),  # Элемент присутствует
        ([1, 2, None, None, 5, 6, 7, None, 10, 11], None, 2), # Элемент None присутствует
        ([1, 2, None, None, 5, 6, 7, None, 10, 11], 8, -1),   # Элемент отсутствует
    ]
)
def test_search(arr, x, expected):
    if isinstance(expected, type) and expected is TypeError:
        with pytest.raises(TypeError):
            search_array(arr, x)
    else:
        assert search_array(arr, x) == expected