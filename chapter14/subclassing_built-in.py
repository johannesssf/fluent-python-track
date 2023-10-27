import collections


class DoppelDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)  # 1


def test1():
    dd = DoppelDict(one=1)  # 2
    print(dd)
    dd['two'] = 2  # 3
    print(dd)
    dd.update(three=3)  # 4
    print(dd)


class DoppelDict2(collections.UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)

def test2():
    dd = DoppelDict2(one=1)  # 2
    print(dd)
    dd['two'] = 2  # 3
    print(dd)
    dd.update(three=3)  # 4
    print(dd)


if __name__ == '__main__':
    # test1()
    test2()
