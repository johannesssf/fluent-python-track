"""
Example 18-6
>>> with looking_glass() as what:  # 1
...     print('Alice, Kitty and Snowdrop')
...     print(what)
pordwonS dna yttiK ,ecilA
YKCOWREBBAJ
>>> what
'JABBERWOCKY'
>>> print('back to normal')
back to normal
"""

# Example 18-5
import contextlib
import sys


@contextlib.contextmanager  # 1
def looking_glass():
    original_write = sys.stdout.write  # 2

    def reverse_write(text):  # 3
        original_write(text[::-1])

    sys.stdout.write = reverse_write  # 4
    yield 'JABBERWOCKY'  # 5
    sys.stdout.write = original_write  # 6
