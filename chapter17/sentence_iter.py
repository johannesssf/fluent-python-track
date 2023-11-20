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
    <sentence_iter.SentenceIterator object at 0x...>
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
        self.text = text
        self.words = RE_WORD.findall(text)

    def __getitem__(self, index):
        return self.words[index]

    def __len__(self):
        return len(self.words)

    def __repr__(self):
        return 'Sentence(%s)' % reprlib.repr(self.text)

    def __iter__(self):  # 1
        return SentenceIterator(self.words)  # 2


class SentenceIterator:
    def __init__(self, words):
        self.words = words  # 3
        self.index = 0  # 4

    def __next__(self):
        try:
            word = self.words[self.index]  # 5
        except IndexError:
            raise StopIteration()  # 6
        self.index += 1  # 7
        return word  # 8

    def __iter__(self):  # 9
        return self


if __name__ == '__main__':
    import doctest
    doctest.testmod()
