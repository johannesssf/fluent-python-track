from collections.abc import Callable
from typing import Any, NoReturn, get_type_hints

from initsub.checkdlib import Field


def checked(cls: type) -> type:  # 1
    for name, constructor in _fields(cls).items():  # 2
        setattr(cls, name, Field(name, constructor))  # 3
    
    cls._fields = classmethod(_fields)  # type: ignore  # 4

    instance_methods = (  # 5
        __init__,
        __repr__,
        __setattr__,
        _asdict,
        __flag_unknown_attrs,
    )
    for method in instance_methods:  # 6
        setattr(cls, method.__name__, method)
    
    return cls  # 7


def _fields(cls: type) -> dict[str, type]:
    return get_type_hints(cls)


def __init__(self: Any, **kwargs: Any) -> None:
    for name in self._fields():
        value = kwargs.pop(name, ...)
        setattr(self, name, value)
    if kwargs:
        self.__flag_unknown_attrs(*kwargs)


def __setattr__(self: Any, name: str, value: Any) -> None:
    if name in self._fields():
        cls = self.__class__
        descriptor = getattr(cls, name)
        descriptor.__set__(self, value)
    else:
        self.__flag_unknown_attrs(name)


def __flag_unknown_attrs(self, *names: str) -> NoReturn:  # 5
    plural = 's' if len(names) > 1 else ''
    extra = ', '.join(f'{name!r}' for name in names)
    cls_name = repr(self.__class__.__name__)
    raise AttributeError(f'{cls_name} object has no attribute{plural} {extra}')


def _asdict(self) -> dict[str, Any]:  # 6
    return {
        name: getattr(self, name)
        for name, attr in self.__class__.__dict__.items()
        if isinstance(attr, Field)
    }
    
def __repr__(self) -> str:  # 7
    kwargs = ', '.join(f'{key}={value!r}' for key, value in self._asdict().items())
    return f'{self.__class__.__name__}({kwargs})'