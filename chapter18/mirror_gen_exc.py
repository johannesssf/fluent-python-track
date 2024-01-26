"""
Example 18-8
>>> @looking_glass()
... def verse():
...     print('The time has come')

>>> verse()  # 1
emoc sah emit ehT
>>> print('back to normal')  # 2
back to normal
"""

# Example 18-7
import contextlib
import sys


@contextlib.contextmanager
def looking_glass():
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    msg = ''  # 1
    try:
        yield 'JABBERWOCKY'
    except ZeroDivisionError:  # 2
        msg = 'Please DO NOT divide by zero!'
    finally:
        sys.stdout.write = original_write  # 3
        if msg:
            print(msg)  # 4
