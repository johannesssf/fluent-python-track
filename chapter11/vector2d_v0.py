from array import array
import math


class Vector2d:
    typecode = 'd'  #1

    def __init__(self, x, y):
        self.x = float(x)  #2
        self.y = float(y)

    def __iter__(self):
        return (i for i in (self.x, self.y))  #3

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self)  #4

    def __str__(self):
        return str(tuple(self))  #5

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) +  #6
            bytes(array(self.typecode, self)))  #7

    def __eq__(self, other):
        return tuple(self) == tuple(other)  #8

    def __abs__(self):
        return math.hypot(self.x, self.y)  #9

    def __bool__(self):
        return bool(abs(self))  #10

    # vector2d_v1 complement
    @classmethod  #1
    def frombytes(cls, octets):  #2
        typecode = chr(octets[0])  #3
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)  #5

    def angle(self):
        return math.atan2(self.y, self.x)

    # Vector2d.__format__ method, take #1
    # def __format__(self, fmt_spec=''):
    #     components = (format(c, fmt_spec) for c in self)  #1
    #     return '({}, {})'.format(*components)

    # Vector2d.__format__ method, take #2
    def __format__(self, fmt_spec=''):
        if fmt_spec.endswith('p'):  #1
            fmt_spec = fmt_spec[:-1]  #2
            coords = (abs(self), self.angle())  #3
            outer_fmt = '<{}, {}>'  #4
        else:
            coords = self  #5
            outer_fmt = '({}, {})'  #6
        components = (format(c, fmt_spec) for c in coords)  #7
        return outer_fmt.format(*components)



if __name__ == '__main__':
    v = Vector2d(3, 4)
    print(format(v, '.3e'))
    print([c for c in v])
