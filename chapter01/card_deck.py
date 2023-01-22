import collections

from random import choice


Card = collections.namedtuple("Card", ["rank", "suit"])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")
    suits = "spades diamonds clubs hearts".split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
    
    def __len__(self):
        return len(self._cards)
    
    # benefits of implementing this
    def __getitem__(self, position):
        return self._cards[position]


def spades_high(card):
    suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)
    rank_value = FrenchDeck.ranks.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]


if __name__ == "__main__":
    french_deck = FrenchDeck()
    print(len(french_deck))
    print(french_deck[0])
    print(french_deck[-1])

    # random access
    print(choice(french_deck))
    print(choice(french_deck))
    print(choice(french_deck))

    # slicing
    print(french_deck[:3])
    print(french_deck[12::13])

    # iterable
    for card in french_deck:
        print(card)
    
    for card in reversed(french_deck):
        print(card)
    
    # working with: in
    print(Card("Q", "hearts") in french_deck)
    print(Card("7", "beasts") in french_deck)

    # sorting
    for card in sorted(french_deck, key=spades_high):
        print(card)
    