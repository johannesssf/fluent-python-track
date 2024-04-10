from collections import abc
from typing import Any


class FrozenJSON:
    """A read-only façade for navigating a JSON-like object
    using attribute notation
    """
    def __init__(self, mapping):
        self.__data = dict(mapping)  # 1
    
    def __getattr__(self, name: str):  # 2
        try:
            return getattr(self.__data, name)  # 3
        except AttributeError:
            return FrozenJSON.build(self.__data[name])  # 4
    
    def __dir__(self):  # 5
        return self.__data.keys()

    @classmethod
    def build(cls, obj):  # 6
        if isinstance(obj, abc.Mapping):  # 7
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):  # 8
            return [cls.build(item) for item in obj]
        else:  # 9
            return obj


if __name__ == '__main__':
    import json

    raw_feed = json.load(open('data/osconfeed.json'))
    feed = FrozenJSON(raw_feed)
    print(len(feed.Schedule.speakers))

    print(feed.keys())
    print(sorted(feed.Schedule.keys()))
    for key, value in sorted(feed.Schedule.items()):
        print(f'{len(value):3} {key}')
    
    print(feed.Schedule.speakers[-1].name)
    talk = feed.Schedule.events[40]
    print(type(talk))
    print(talk.name)
    print(talk.speakers)
    print(talk.flavor)

