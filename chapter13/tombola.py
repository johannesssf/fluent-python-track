import abc


class Tombola(abc.ABC):

    @abc.abstractmethod
    def load(self, iterable):  # 2
        """Add items from an iterable."""

    @abc.abstractmethod
    def pick(self):  # #
        """Remove item at random, returning it.

        This method should raise `LookupError` when the instance is empty.
        """

    def loaded(self):  # 4
        """Return `True` if there's at least ' item, `False` otherwise."""
        return bool(self.inspect())  # 5

    def inspect(self):
        """Return a sorted tuple with the items currently inside."""
        items = []
        while True:  # 6
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)  # 7
        return tuple(items)


class Fake(Tombola):
    def pick(self):  # 1
        return 13


# print(Fake)  # 2
# f = Fake()  # 3
