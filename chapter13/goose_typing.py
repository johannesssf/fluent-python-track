from collections import abc


class Struggle:
    def __len__(self):
        return 23


print(isinstance(Struggle(), abc.Sized))
