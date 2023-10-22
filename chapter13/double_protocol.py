from fractions import Fraction
from typing import TypeVar, Protocol

T = TypeVar('T')  # 1


class Repeatable(Protocol):
    def __mul__(self: T, repeat_count: int) -> T: ...  # 2


RT = TypeVar('RT', bound=Repeatable)  # 3


class NotRepeatable:
    x = 5


def double(x: RT):
    return x * 2


print(double(1.5))
print(double('A'))
print(double([10, 20, 30]))
print(double(Fraction(2, 5)))
print(double(NotRepeatable()))
