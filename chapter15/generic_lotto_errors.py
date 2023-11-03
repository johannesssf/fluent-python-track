from generic_lotto import LottoBlower

machine = LottoBlower[int]([1, .2])

machine = LottoBlower[int](range(1, 11))

machine.load('ABC')
