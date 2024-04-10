# Example 23-8

### auxiliary functions for display only ###

def cls_name(obj_or_cls):
    cls = type(obj_or_cls)
    if cls is type:
        cls = obj_or_cls
    return cls.__name__.split('.')[-1]


def display(obj):
    cls = type(obj)
    if cls is type:
        return f'<class {obj.__name__}>'
    elif cls in [type(None), int]:
        return repr(obj)
    else:
        return f'<{cls_name(obj)} object>'


def print_args(name, *args):
    pseudo_args = ', '.join(display(x) for x in args)
    print(f'-> {cls_name(args[0])}.__{name}__({pseudo_args})')

### essential classes for this example ###

class Overriding:  # 1
    """a.k.a. data descriptor or enforced descriptor"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)  # 2

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class OverridingNoGet:  # 3
    """a.k.a. overriding descriptor withou ``__get__``"""

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


class NonOverriding:  # 4
    """a.k.a. non-data or shadowable descriptor"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)


class Managed:  # 5
    over = Overriding()
    over_no_get = OverridingNoGet()
    non_over = NonOverriding()

    def spam(self):  # 6
        print(f'-> Managed.spam({display(self)})')


def overriding():
    obj = Managed()  # 1
    obj.over  # 2
    Managed.over  # 3
    obj.over = 7  # 4
    obj.over  # 5
    obj.__dict__['over'] = 8  # 6
    print(vars(obj))  # 7
    obj.over  # 8


def overriding_no_get():
    obj = Managed()
    print(obj.over_no_get)  # 1
    print(Managed.over_no_get)  # 2
    obj.over_no_get = 7  # 3
    print(obj.over_no_get)  # 4
    obj.__dict__['over_no_get'] = 9  # 5
    print(obj.over_no_get)  # 6
    obj.over_no_get = 7  # 7
    print(obj.over_no_get)  # 8


def nonoverriding():
    obj = Managed()
    obj.non_over  # 1
    obj.non_over = 7  # 2
    print(obj.non_over)  # 3
    Managed.non_over  # 4
    del obj.non_over  # 5
    obj.non_over  # 6


def overwriting():
    obj = Managed()  # 1
    Managed.over = 1  # 2
    Managed.over_no_get = 2
    Managed.non_over = 3
    print(obj.over, obj.over_no_get, obj.non_over)


def method_nonoverriding():
    obj = Managed()
    print(obj.spam)  # 1
    print(Managed.spam)  # 2
    obj.spam = 7  # 3
    print(obj.spam)


if __name__ == '__main__':
    method_nonoverriding()