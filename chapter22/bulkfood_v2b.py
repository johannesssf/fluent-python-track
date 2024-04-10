class LineItem:

    def __init__(self, description, weight, price) -> None:
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    def get_weight(self):  # 1
        return self.__weight

    def set_weight(self, value):  # 2
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')
    
    weight = property(get_weight, set_weight)  # 3