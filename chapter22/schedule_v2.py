import inspect  # 1
import json


JSON_PATH = 'data/osconfeed.json'


class Record:
    __index = None  # 2

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
    
    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} serial={self.serial!r}>'

    @staticmethod  # 3
    def fetch(key):
        if Record.__index is None:  # 4
            Record.__index = load()
        
        return Record.__index[key]  # 5

def load(path=JSON_PATH):
    records = {}

    with open(path) as fp:
        raw_data = json .load(fp)
    
    for collection, raw_records in raw_data['Schedule'].items():
        record_type = collection[:-1]  # 1
        cls_name = record_type.capitalize()  # 2
        cls = globals().get(cls_name, Record)  # 3

        if inspect.isclass(cls) and issubclass(cls, Record):  # 4
            factory = cls  # 5
        else:
            factory = Record  # 6
        
        for raw_record in raw_records:  # 7
            key = f'{record_type}.{raw_record["serial"]}'
            records[key] = factory(**raw_record)  # 8
    
    return records


class Event(Record):  # 1

    def __repr__(self):
        try:
            return f'<{self.__class__.__name__} {self.name!r}>'  # 2
        except AttributeError:
            return super().__repr__()
    
    @property
    def venue(self):
        key = f'venue.{self.venue_serial}'
        return self.__class__.fetch(key)  # 3
