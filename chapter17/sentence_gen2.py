"""
Test Sentence class
    >>> s = Sentence('"The time has come," the Walrus said,')  # 1
    >>> s
    Sentence('"The time ha... Walrus said,')
    >>> for word in s:
    ...     print(word)
    The
    time
    has
    come
    the
    Walrus
    said
    >>> list(s)
    ['The', 'time', 'has', 'come', 'the', 'Walrus', 'said']
    >>> s[0]
    'The'
    >>> s[5]
    'Walrus'
    >>> s[-1]
    'said'

Test iter() is consumed by next()
    >>> s3 = Sentence('Life of Brian')
    >>> it = iter(s3)
    >>> it  # doctest: +ELLIPSIS
    <generator object Sentence.__iter__ at 0x...>
    >>> next(it)
    'Life'
    >>> next(it)
    'of'
    >>> next(it)
    'Brian'
    >>> next(it)
    Traceback (most recent call last):
    ...
    StopIteration
    >>> list(it)
    []
    >>> list(iter(s3))
    ['Life', 'of', 'Brian']
"""

import re
import reprlib

RE_WORD = re.compile(r'\w+')


class Sentence:
    def __init__(self, text):
        self.text = text  # 1

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):  # 1
        for match in  RE_WORD.finditer(self.text):  # 2
            yield match.group()  # 3


if __name__ == '__main__':
    import doctest
    doctest.testmod()
