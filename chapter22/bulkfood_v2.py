"""
>>> raisins = LineItem('Golden raisins', 10, 6.95)
>>> raisins.subtotal()
69.5
>>> raisins.weight = -20  # garbage in
Traceback (most recent call last):
...
ValueError: value must be > 0

>>> raisins2 = LineItem('Golden raisins', 0, 6.95)
Traceback (most recent call last):
...
ValueError: value must be > 0
"""


class LineItem:

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight  # 1
        self.price = price
    
    def subtotal(self):
        return self.weight * self.price
    
    @property  # 2
    def weight(self):  # 3
        return self.__weight  # 4

    @weight.setter  # 5
    def weight(self, value):
        if value > 0:
            self.__weight = value  # 6
        else:
            raise ValueError('value must be > 0')  # 7


if __name__ == '__main__':
    import doctest
    doctest.testmod()