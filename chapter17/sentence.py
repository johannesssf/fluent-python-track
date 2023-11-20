"""
Test Sentence class
    >>> s = Sentence('"The time has come," the Walrus said,')  # 1
    >>> s
    Sentence('"The time ha... Walrus said,')
    >>> for word in s:  # 3
    ...     print(word)
    The
    time
    has
    come
    the
    Walrus
    said
    >>> list(s)  # 4
    ['The', 'time', 'has', 'come', 'the', 'Walrus', 'said']
    >>> s[0]
    'The'
    >>> s[5]
    'Walrus'
    >>> s[-1]
    'said'

Test iter() is consumed by next()
    >>> s3 = Sentence('Life of Brian')  # 1
    >>> it = iter(s3)  # 2
    >>> it  # doctest: +ELLIPSIS
    <iterator object at 0x...>
    >>> next(it)  # 3
    'Life'
    >>> next(it)
    'of'
    >>> next(it)
    'Brian'
    >>> next(it)  # 4
    Traceback (most recent call last):
    ...
    StopIteration
    >>> list(it)  # 5
    []
    >>> list(iter(s3))  # 6
    ['Life', 'of', 'Brian']
"""

import re
import reprlib

RE_WORD = re.compile(r'\w+')


class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)  # 1

    def __getitem__(self, index):
        return self.words[index]  # 2

    def __len__(self):  # 3
        return len(self.words)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)  # 4


if __name__ == '__main__':
    import doctest
    doctest.testmod()
