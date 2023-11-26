from collections.abc import Generator
from typing import Union, NamedTuple


class Result(NamedTuple):  # 1
    count: int  # type: ignore  #2
    average: float


class Sentinel:  # 3
    def __repr__(self):
        return '<Sentinel>'


STOP = Sentinel()  # 4
SendType = Union[float, Sentinel]  # 5


def averager2(verbose: bool = False) -> Generator[None, SendType, Result]:  # 1
    total = 0.0
    count = 0
    average = 0.0
    while True:
        term = yield  # 2
        if verbose:
            print('received:', term)
        if isinstance(term, Sentinel):  # 3
            break
        total += term  # 4
        count += 1
        average = total / count

    return Result(count, average)  # 5


def compute():
    res = yield from averager2(True)  # 1
    print('computed:', res)  # 2
    return res  # 3


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()
    # coro_avg = averager2()
    # next(coro_avg)
    # coro_avg.send(10)  # 1
    # coro_avg.send(30)
    # coro_avg.send(6.5)
    # # coro_avg.close()  # 2
    # try:
    #     coro_avg.send(STOP)  # 1
    # except StopIteration as exc:
    #     result = exc.value  # 2
    # print(result)  # 3
    comp = compute()  # 4
    for v in [None, 10, 20, 30, STOP]:  # 5
        try:
            comp.send(v)  # 6
        except StopIteration as exc:  # 7
            result = exc.value
    print(result)  # 8
