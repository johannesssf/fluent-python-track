# Example 23-1

class Quantity:  # 1

    def __init__(self, storage_name):
        self.storage_name = storage_name  # 2

    def __set__(self, instance, value):  # 3
        if value > 0:
            instance.__dict__[self.storage_name] = value  # 4
        else:
            msg = f'{self.storage_name} must be > 0'
            raise ValueError(msg)
    
    def __get__(self, instance, owner):  # 5
        if instance is None:
            return self
        else:
            return instance.__dict__[self.storage_name]


class LineItem:
    weight = Quantity('weight')  # 1
    price = Quantity('price')  # 2

    def __init__(self, description, weight, price):  # 3
        self.description = description
        self.weight = weight
        self.price = price
    
    def subtotal(self):
        return self.weight * self.price