import os
import re
from datetime import date, datetime
from packing import PackingItem, PackingItemSchema
from marshmallow import Schema, fields, post_load

class PackingList(object):

    PACKING_LIST_DIR = os.path.join(os.getenv('APPDATA'), 'Packing Lists')
    os.makedirs(PACKING_LIST_DIR, exist_ok=True)

    def __init__(self, trip_name, start_date, end_date, items=[]):
        self.trip_name = trip_name
        self.start_date = start_date
        self.end_date = end_date
        self._items = [PackingItem(*item) for item in items] or []
    
    def __repr__(self):
        start_date = self.start_date.packing_strftime()
        end_date = self.end_date.packing_strftime()
        return (f"PackingList(trip_name='{self.trip_name}',"
                f" start_date='{start_date}', end_date='{end_date}')")

    def __str__(self):
        start_date = self.start_date.packing_strftime()
        end_date = self.end_date.packing_strftime()
        return f"Trip to {self.trip_name} from {start_date} to {end_date}"

    def __len__(self):
        return len(self._items)

    def __getitem__(self, s):
        return self._items[s]
    
    def __eq__(self, other):
        if not isinstance(other, PackingList):
            return False
        return (
            self.trip_name == other.trip_name and
            self.start_date == other.start_date and
            self.end_date == other.end_date and
            self.items == other.items
        )

    def append(self, item):
        packing_item = PackingItem(*item)

        # check if item is already present
        filter_func = lambda x: x.item_name == packing_item.item_name
        try:
            current_item = next(filter(filter_func, self._items))
        except StopIteration:
            self._items.append(packing_item)
        else:
            raise ValueError(f'item "{current_item.item_name}" already present in packing list')
        
    def remove(self, item):
        self._items.remove(item)
    
    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        self._start_date = PackingListDate.packing_strptime(value)

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        end_date = PackingListDate.packing_strptime(value)
        if end_date <= self.start_date:
            raise PackingDateValueError('End date must be before start date')
        self._end_date = end_date
    
    @property
    def items(self):
        return self._items

    @property
    def filename(self):
        start_date = self.start_date.packing_strftime()
        end_date = self.end_date.packing_strftime()
        filename = f"{self.trip_name} {start_date} to {end_date}.json"
        return filename
    
    def items_table(self):
        result = f"{'Item':<30}{'Count':>10}{'Packed':>10}\n"
        result += '-' * (len(result) - 1) + '\n'
        for item in self._items:
            result += str(item) + '\n'
        return result
    
    def toJSON(self):
        filepath = os.path.join(self.__class__.PACKING_LIST_DIR, self.filename)
        with open(filepath, 'w') as f:
            f.write(PackingListSchema().dumps(self))
        return filepath

    @classmethod
    def fromJSON(cls, filename):
        filepath = os.path.join(cls.PACKING_LIST_DIR, filename)
        with open(filepath, 'r') as f:
            return PackingListSchema().loads(f.read())

    @classmethod
    def get_packing_lists(cls):
        filenames = os.listdir(cls.PACKING_LIST_DIR)
        filenames_split = list(map(os.path.splitext, filenames))
        json_filenames = [x[0] for x in filenames_split if x[1] == '.json']
        return json_filenames


class PackingListDate(date):
    DATE_PAT_STR = r'\d\d\d\d-\d\d-\d\d'
    STRPTIME_PAT_STR = r'%Y-%m-%d'
    DATE_PAT = re.compile(DATE_PAT_STR)

    def packing_strftime(self):
        return self.strftime(self.__class__.STRPTIME_PAT_STR)
     
    @classmethod
    def packing_strptime(cls, value):
        if isinstance(value, (date, datetime)):
            return cls(value.year, value.month, value.day) 
        elif isinstance(value, str):
            value = datetime.strptime(value, cls.STRPTIME_PAT_STR).date()
            return cls(value.year, value.month, value.day) 
        else:
            raise ValueError(f'{type(value)} not accepted')

class PackingDateValueError(ValueError):
    """ Error raised when trip End Date is before the Start Date """

class PackingListSchema(Schema):
    class Meta:
        ordered = True

    trip_name = fields.Str()
    start_date = fields.Date()
    end_date = fields.Date()
    items = fields.Nested(PackingItemSchema, many=True)

    @post_load
    def make_packing_list(self, data, **kwargs):
        return PackingList(**data)
