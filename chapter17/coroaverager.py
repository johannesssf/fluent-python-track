"""
Test for classis coroutine
    >>> coro_avg = averager()  # 1
    >>> next(coro_avg)  # 2
    0.0
    >>> coro_avg.send(10)  # 3
    10.0
    >>> coro_avg.send(30)
    20.0
    >>> coro_avg.send(5)
    15.0
    >>> coro_avg.send(20)
    16.25
    >>> coro_avg.close()
    >>> coro_avg.close()
    >>> coro_avg.send(5)
    Traceback (most recent call last):
    ...
    StopIteration
"""

from collections.abc import Generator


def averager() -> Generator[float, float, None]:  # 1
    total = 0.0
    count = 0
    average = 0.0
    while True:  # 2
        term = yield average  # 3
        total += term
        count += 1
        average = total / count


if __name__ == '__main__':
    import doctest
    doctest.testmod()
