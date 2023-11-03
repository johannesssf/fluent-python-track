from typing import TypeVar, Generic


class Beverage:
    """Any beverage."""


class Juice(Beverage):
    """Any fruit juice."""


class OrangeJuice(Juice):
    """Delicious juice from Brazilian oranges."""


T_co = TypeVar('T_co', covariant=True)  # 1


class BeverageDispenser(Generic[T_co]):  # 2
    """A dispenser parameterized on the beverage type."""
    def __init__(self, beverage: T_co) -> None:
        self.beverage = beverage

    def dispense(self) -> T_co:
        return self.beverage


def install(dispenser: BeverageDispenser[Juice]) -> None:  # 3
    """Install a fruit juice dispenser."""


if __name__ == '__main__':
    juice_dispenser = BeverageDispenser(Juice())
    install(juice_dispenser)

    beverage_dispenser = BeverageDispenser(Beverage())
    install(beverage_dispenser)

    orange_juice_dispenser = BeverageDispenser(OrangeJuice())
    install(orange_juice_dispenser)
