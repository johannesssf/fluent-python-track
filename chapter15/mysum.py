import functools
import operator
from collections.abc import Iterable
from typing import overload, Union, TypeVar


T = TypeVar('T')
S = TypeVar('S')  # 1


@overload
def sum(it: Iterable[T]) -> Union[T, int]: ...  # 2


@overload
def sum(it: Iterable[T], /, start: S) -> Union[T, S]: ...  # 3


def sum(it, /, start=0):  # 4
    return functools.reduce(operator.add, it, start)

if __name__ == '__main__':
    n = [1, 2, 3]
    print(sum(n, 1))
