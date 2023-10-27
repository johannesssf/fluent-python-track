from diamond import A  # 1


class U:  # 2
    def ping(self):
        print(f'{self}.ping() in U')
        super().ping()  # 3


# class LeafUA(U, A):  # 4
class LeafUA(A, U):  # 4
    def ping(self):
        print(f'{self}.ping() in LeafUA')
        super().ping()


if __name__ == '__main__':
    l = LeafUA()
    l.ping()
    print(LeafUA.__mro__)
