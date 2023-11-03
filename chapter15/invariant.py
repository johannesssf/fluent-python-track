from typing import TypeVar, Generic


class Beverage:  # 1
    """Any beverage."""


class Juice(Beverage):
    """Any fruit juice."""


class OrangeJuice(Juice):
    """Delicious juice from Brazilian oranges."""


T = TypeVar('T')  # 2


class BeverageDispenser(Generic[T]):  # 3
    """A dispenser parameterized on the beverage type."""
    def __init__(self, beverage: T) -> None:
        self.beverage = beverage

    def dispense(self) -> T:
        return self.beverage


def install(dispenser: BeverageDispenser[Juice]) -> None:  # 4
    """Install a fruit juice dispenser."""


if __name__ == '__main__':
    juice_dispenser = BeverageDispenser(Juice())
    install(juice_dispenser)

    beverage_dispenser = BeverageDispenser(Beverage())
    install(beverage_dispenser)

    orange_juice_dispenser = BeverageDispenser(OrangeJuice())
    install(orange_juice_dispenser)
