from generic_lotto import LottoBlower


machine = LottoBlower[int](range(1, 11))  # 1

first = machine.pick()  # 2
remain = machine.inspect()  # 3
