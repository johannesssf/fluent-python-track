# simple decorator to show the running time of functions
import time
import functools


def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):  #1
        t0 = time.perf_counter()
        result = func(*args, **kwargs)  #2
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_lst = [repr(arg) for arg in args]
        arg_lst.extend(f'{k}={v!r}' for k, v in kwargs.items())
        args_str = ', '.join(arg_lst)
        print(f'[{elapsed:0.8f}s] {name}({args_str}) -> {result!r}')
        return result
    return clocked  #3
