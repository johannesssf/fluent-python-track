from array import array
import reprlib
import math
import operator
from typing import Any


class Vector:
    typecode = 'd'
    __match_args__ = ('x', 'y', 'z', 't')  #1

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return f'Vector({components})'

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(self._components))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.hypot(*self)

    def __bool__(self):
        return bool(abs(self))

    def __len__(self):
        return len(self._components)

    def __getitem__(self, key):
        if isinstance(key, slice):
            cls = type(self)
            return cls(self._components[key])
        index = operator.index(key)
        return self._components[index]

    def __getattr__(self, name):
        cls = type(self)  #2
        try:
            pos = cls.__match_args__.index(name)  #3
        except ValueError:  #4
            pos = -1

        if 0 <= pos < len(self._components):  #5
            return self._components[pos]

        msg = f'{cls.__name__!r} object has no attribute {name!r}'  #6

        raise AttributeError(msg)

    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:  #1
            if name in cls.__match_args__:  #2
                error = 'readonly attribute {attr_name!r}'
            elif name.islower():  #3
                error = "can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''  #4

            if error:  #5
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        super().__setattr__(name, value)  #6


    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)
