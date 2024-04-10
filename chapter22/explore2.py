from collections import abc
import keyword


class FrozenJSON:
    """A read-only façade for navigating a JSON-like object
    using attribute notation
    """
    def __new__(cls, arg):  # 1
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)  # 2
        elif isinstance(arg, abc.MutableSequence):  # 3
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value

    
    def __getattr__(self, name: str):
        try:
            return getattr(self.__data, name)
        except AttributeError:
            return FrozenJSON(self.__data[name])  # 4
    
    def __dir__(self):
        return self.__data.keys()


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
    # print(talk.flavor)

