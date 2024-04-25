class MetaBunch(type):  # 1

    def __new__(meta_cls, cls_name, bases, cls_dict):  # 2

        defaults = {}  # 3

        def __init__(self, **kwargs):  # 4
            for name, default in defaults.items():  # 5
                setattr(self, name, kwargs.pop(name, default))

            if kwargs:  # 6
                extra = ', '.join(kwargs)
                raise AttributeError(f'No slots left for: {extra!r}')
        
        def __repr__(self):  # 7
            rep = ', '.join(f'{name}={value!r}' 
                            for name, default in defaults.items()
                            if (value := getattr(self, name)) != default)
            return f'{cls_name}({rep})'
        
        new_dict = dict(__slots__=[], __init__=__init__, __repr__=__repr__)  # 8

        for name, value in cls_dict.items():  # 9
            if name.startswith('__') and name.endswith('__'):  # 10
                if name in new_dict:
                    raise AttributeError(f"Can't set {name!r} in {cls_name!r}")
                new_dict[name] = value
            else:  # 11
                new_dict['__slots__'].append(name)
                defaults[name] = value
        
        return super.__new__(meta_cls, cls_name, bases, new_dict)  # 12


class Bunch(metaclass=MetaBunch):  # 13
    pass