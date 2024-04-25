from autoconst import AutoConst


class Flavor(AutoConst):
    banana
    coconut
    vanilla


print(Flavor.vanilla)
print(Flavor.banana, Flavor.coconut)