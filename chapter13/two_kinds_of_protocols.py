class Vowels:
    def __getitem__(self, i):
        return 'AEIOU'[i]


def main1():
    v = Vowels()
    print(v[0])
    print(v[-1])

    for c in v: print(c)

    print('E' in v)
    print('Z' in v)


def main2():
    from random import shuffle
    l = list(range(10))
    shuffle(l)
    print(l)


def _set_card(deck, position, card):  # 1
    deck._cards[position] = card


def main3():
    from random import shuffle
    from chapter01.card_deck import FrenchDeck

    deck = FrenchDeck()
    FrenchDeck.__setitem__ = _set_card  # 2
    shuffle(deck)
    print(deck[:5])


if __name__ == '__main__':
    main3()
