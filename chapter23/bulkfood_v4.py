# Example 23-3
import chapter23.model_v4 as model

# class Quantity:

#     def __set_name__(self, owner, name):  # 1
#         self.storage_name = name  # 2

#     def __set__(self, instance, value):  # 3
#         if value > 0:
#             instance.__dict__[self.storage_name] = value
#         else:
#             msg = f'{self.storage_name} must be > 0'
#             raise ValueError(msg)
    
#     # no __get__ needed  # 4


class LineItem:
    weight = model.Quantity()  # 5
    price = model.Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price
    
    def subtotal(self):
        return self.weight * self.price