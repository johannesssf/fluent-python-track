from array import array
import reprlib
import math
import operator


class Vector:
    typecode = 'd'

    def __init__(self, components):
        self._components = array(self.typecode, components)  #1

    def __iter__(self):
        return iter(self._components)  #2

    def __repr__(self):
        components = reprlib.repr(self._components)  #3
        components = components[components.find('['):-1]  #4
        return f'Vector({components})'

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(self._components))  #5

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.hypot(*self)  #6

    def __bool__(self):
        return bool(abs(self))

    def __len__(self):
        return len(self._components)

    def __getitem__(self, key):
        if isinstance(key, slice):  #1
            cls = type(self)  #2
            return cls(self._components[key])  #3
        index = operator.index(key)  #4
        return self._components[index]  #5

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)  #7
