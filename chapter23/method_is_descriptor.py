import collections


class Text(collections.UserString):

    def __repr__(self) -> str:
        return 'Text({!r})'.format(self.data)
    
    def reverse(self):
        return self[::-1]


if __name__ == '__main__':
    word = Text('forward')
    print(word)  # 1
    print(word.reverse())  # 2
    print(Text.reverse(Text('backward')))  # 3
    print(type(Text.reverse), type(word.reverse))  # 4
    print(list(map(Text.reverse, ['repaid', (10, 20, 30), Text('stressed')])))  # 5
    print(Text.reverse.__get__(word))  # 6
    print(Text.reverse.__get__(None, Text))  # 7
    print(word.reverse)  # 8
    print(word.reverse.__self__)  # 9
    print(word.reverse.__func__ is Text.reverse)  # 10