import time

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'


def clock(fmt=DEFAULT_FMT):  #1
    def decorate(func):  #2
        def clocked(*_args):  #3
            t0 = time.perf_counter()
            _result = func(*_args)  #4
            elapsed = time.perf_counter() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)  #5
            result = repr(_result)  #6
            print(fmt.format(**locals()))  #7
            return _result  #8
        return clocked  #9
    return decorate  #10


if __name__ == '__main__':
    @clock()  #11
    def snooze(seconds):
        time.sleep(seconds)

    for i in range(3):
        snooze(.123)
