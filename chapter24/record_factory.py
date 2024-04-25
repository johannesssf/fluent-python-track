from typing import Union, Any
from collections.abc import Iterable, Iterator


FieldsNames = Union[str, Iterable[str]]  # 1


def record_factory(cls_name: str, field_names: FieldsNames) -> type[tuple]:  # 2

    slots = parse_identifiers(field_names)  # 3

    def __init__(self, *args, **kwargs) -> None:  # 4
        attrs = dict(zip(self.__slots__, args))
        attrs.update(kwargs)

        for name, value in attrs.items():
            setattr(self, name, value)
    
    def __iter__(self) -> Iterator[Any]:  # 5
        for name in self.__slots__:
            yield getattr(self, name)
    
    def __repr__(self):  # 6
        values = ', '.join(f'{name}={value!r}'
            for name, value in zip(self.__slots__, self))
        cls_name = self.__class__.__name__
        return f'{cls_name}({values})'
    
    cls_attrs = dict(  # 7
        __slots__=slots,
        __init__=__init__,
        __iter__=__iter__,
        __repr__=__repr__,
    )

    return type(cls_name, (object,), cls_attrs)  # 8


def parse_identifiers(names: FieldsNames) -> tuple[str, ...]:
    if isinstance(names, str):
        names = names.replace(',', ' ').split()  # 9
    
    if not all(s.isidentifier() for s in names):
        raise ValueError('names must all be valid identifiers')
    
    return tuple(names)