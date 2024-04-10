import inspect
import json

from functools import cache, cached_property


JSON_PATH = 'data/osconfeed.json'


class Record:
    __index = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    
    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} serial={self.serial!r}>'

    @staticmethod
    def fetch(key):
        if Record.__index is None:
            Record.__index = load()
        
        return Record.__index[key]


def load(path=JSON_PATH):
    records = {}

    with open(path) as fp:
        raw_data = json .load(fp)
    
    for collection, raw_records in raw_data['Schedule'].items():
        record_type = collection[:-1]
        cls_name = record_type.capitalize()
        cls = globals().get(cls_name, Record)

        if inspect.isclass(cls) and issubclass(cls, Record):
            factory = cls
        else:
            factory = Record
        
        for raw_record in raw_records:
            key = f'{record_type}.{raw_record["serial"]}'
            records[key] = factory(**raw_record)
    
    return records


class Event(Record):
    def __init__(self, **kwargs):
        self.__speakers_obj = None
        super().__init__(**kwargs)

    def __repr__(self):
        try:
            return f'<{self.__class__.__name__} {self.name!r}>'
        except AttributeError:
            return super().__repr__()
    
    @cached_property
    def venue(self):
        key = f'venue.{self.venue_serial}'
        return self.__class__.fetch(key)
    
    @property
    @cache
    def speakers(self):
        if self.__speakers_obj is None:
            spkr_serials = self.__dict__['speakers']  # 1
            fetch = self.__class__.fetch
            self.__speakers_obj = [fetch(f'speaker.{key}') for key in spkr_serials]
        return self.__speakers_obj
