from collections.abc import Callable  # 1
from typing import Any, NoReturn, get_type_hints


class Field:
    def __init__(self, name: str, constructor: Callable) -> None:  # 2
        if not callable(constructor) or constructor is type(None):  # 3
            raise TypeError(f'{name!r} type hint must be callable')
        self.name = name
        self.constructor = constructor
    
    def __set__(self, instance: Any, value: Any) -> None:
        if value is ...:  # 4
            value = self.constructor()
        else:
            try:
                value = self.constructor(value)  # 5
            except (TypeError, ValueError) as e:  # 6
                type_name = self.constructor.__name__
                msg = f'{value!r} is not compatible with {self.name}:{type_name}'
                raise TypeError(msg) from e
        instance.__dict__[self.name] = value  # 7


class Checked:
    @classmethod
    def _fields(cls) -> dict[str, type]:  # 1
        return get_type_hints(cls)
    
    def __init_subclass__(subclass) -> None:  # 2
        super().__init_subclass__()  # 3
        for name, constructor in subclass._fields().items():  # 4
            setattr(subclass, name, Field(name, constructor))  # 5
    
    def __init__(self, **kwargs: Any) -> None:
        for name in self._fields():  # 6
            value = kwargs.pop(name, ...)  # 7
            setattr(self, name, value)  # 8
        if kwargs:  # 9
            self.__flag_unknown_attrs(*kwargs)  # 10
    
    def __setattr__(self, name: str, value: Any) -> None:  # 1
        if name in self._fields():  # 2
            cls = self.__class__
            descriptor = getattr(cls, name)
            descriptor.__set__(self, value)  # 3
        else:  # 4
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