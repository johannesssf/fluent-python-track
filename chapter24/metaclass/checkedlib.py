from typing import Any, Callable, get_type_hints, NoReturn

class Field:
    def __init__(self, name: str, constructor: Callable) -> None:
        if not callable(constructor) or constructor is type(None):
            raise TypeError(f'{name!r} type hint must be callable')
        self.name = name
        self.storage_name = '_' + name  # 1
        self.constructor = constructor
    
    def __get__(self, instance, owner=None):
        if instance is None:  # 2
            return self
        return getattr(instance, self.storage_name)  # 3
    
    def __set__(self, instance: Any, value: Any) -> None:
        if value is ...:
            value = self.constructor()
        else:
            try:
                value = self.constructor(value)
            except (TypeError, ValueError) as e:
                type_name = self.constructor.__name__
                msg = f'{value!r} is not compatible with {self.name}:{type_name}'
                raise TypeError(msg) from e
        setattr(instance, self.storage_name, value)  # 4


class CheckedMeta(type):

    def __new__(meta_cls, cls_name, bases, cls_dict):  # 1
        if '__slots__' not in cls_dict:  # 2
            slots = []
            type_hints = cls_dict.get('__annotations__', {})  # 3

            for name, constructor in type_hints.items():  # 4
                field = Field(name, constructor)  # 5
                cls_dict[name] = field  # 6
                slots.append(field.storage_name)  # 7
            
            cls_dict['__slots__'] = slots  # 8
        
        return super().__new__(meta_cls, cls_name, bases, cls_dict)  # 9


class Checked(metaclass=CheckedMeta):
    __slots__ = ()  # skip CheckedMeta.__new__ processing

    @classmethod
    def _fields(cls) -> dict[str, type]:
        return get_type_hints(cls)
    
    def __init__(self, **kwargs: Any) -> None:
        for name in self._fields():
            value = kwargs.pop(name, ...)
            setattr(self, name, value)
        
        if kwargs:
            self.__flag_unknown_attrs(*kwargs)
    
    def __flag_unknown_attrs(self, *names: str) -> NoReturn:
        plural = 's' if len(names) > 1 else ''
        extra = ', '.join(f'{name!r}' for name in names)
        cls_name = repr(self.__class__.__name__)
        raise AttributeError(f'{cls_name} object has no attribute{plural} {extra}')

    def _asdict(self) -> dict[str, Any]:
        return {
            name: getattr(self, name)
            for name, attr in self.__class__.__dict__.items()
            if isinstance(attr, Field)
        }
    
    def __repr__(self) -> str:
        kwargs = ', '.join(
            f'{key}={value!r}' for key, value in self._asdict().items()
        )
        return f'{self.__class__.__name__}({kwargs})'