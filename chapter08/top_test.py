from collections.abc import Iterator
from typing import TYPE_CHECKING  #1

import pytest

from top import top


def test_top_tuples() -> None:
    fruit = 'mango pear apple kiwi banana'.split()
    series: Iterator[tuple[int, str]] = ((len(s), s) for s in fruit)  #2
    length = 3
    expected = [(6, 'banana'), (5, 'mango'), (5, 'apple')]
    result = top(series, length)

    if TYPE_CHECKING:  #3
        reveal_type(series)  #4
        reveal_type(expected)
        reveal_type(result)

    assert result == expected


def test_top_objects_error() -> None:
    series = [object() for _ in range(4)]
    if TYPE_CHECKING:
        reveal_type(series)
    
    with pytest.raises(TypeError) as excinfo:
        top(series, 3)  #5
    
    assert "'<' not supported" in str(excinfo.value)