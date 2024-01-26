"""
Example 18-1
>>> with open('mirror.py') as fp:  # 1
...     src = fp.read(60)  # 2
...
>>> len(src)
60
>>> fp  # 3
<_io.TextIOWrapper name='mirror.py' mode='r' encoding='UTF-8'>
>>> fp.closed, fp.encoding  # 4 and 5
(True, 'UTF-8')
>>> fp.read(60)  # 6
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: I/O operation on closed file.

Example 18-2
>>> with LookingGlass() as what:  # 1
...     print('Alice, Kitty and Snowdrop')  # 2
...     print(what)
...
pordwonS dna yttiK ,ecilA
YKCOWREBBAJ
>>> what  # 3
'JABBERWOCKY'
>>> print('Back to normal.')  # 4
Back to normal.

Example 18-4
>>> manager = LookingGlass()  # 1
>>> manager  # doctest: +ELLIPSIS
<mirror.LookingGlass object at 0x...>
>>> monster = manager.__enter__()  # 2
>>> monster == 'JABBERWOCKY'
eurT
>>> monster
'YKCOWREBBAJ'
>>> manager  # doctest: +ELLIPSIS
>... ta tcejbo ssalGgnikooL.rorrim<
>>> manager.__exit__(None, None, None)  # 4
>>> monster
'JABBERWOCKY'
"""

# Example 18-3
import sys


class LookingGlass:
    def __enter__(self):  # 1
        self.original_write = sys.stdout.write  # 2
        sys.stdout.write = self.reverse_write  # 3
        return 'JABBERWOCKY'  # 4

    def reverse_write(self, text):  # 5
        self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_val, exc_tb):  # 6
        sys.stdout.write = self.original_write  # 7
        if exc_type is ZeroDivisionError:  # 8
            print('Please DO NOT divide by zero!')
            return True  # 9
        # 10
