import os
import re
import yaml
from datetime import date, datetime
import pandas as pd

class PackingItem(object):

    def __init__(self, item_name, count, packed=False):
        self.item_name = str(item_name)
        self.count = int(count)
        self.packed = packed
    
    def __repr__(self):
         return (f"{self.__class__.__name__}(item_name='{self.item_name}', "
                 f"count={self.count}, packed={self.packed})")

    def __str__(self):
        return f"{self.item_name:<30}{self.count:>10}{self.packed_yesno():>10}"
    
    def __len__(self):
        return self.count
    
    def __iter__(self):
        return PackingItemIterator(self.item_name, self.count, self.packed)
    
    @property
    def packed(self):
        return self._packed

    @packed.setter
    def packed(self, i):
        if isinstance(i, bool):
            self._packed = i 
        elif isinstance(i, str):
            if i.lower() in ('yes', 'y'):
                self._packed = True
            elif i.lower() in ('no', 'n'):
                self._packed = False 
        else:
            raise ValueError("i must be True, False, 'yes', 'y', 'no' or 'n'")
        
    def packed_yesno(self):
        if self.packed:
            return 'Yes'
        return 'No'
    
    def to_dict(self):
        return {
            'item_name': self.item_name,
            'count': self.count,
            'packed': self.packed
        }


class PackingItemIterator:
    def __init__(self, item_name, count, packed=False):
        self._index = 0
        self._item_data = [item_name, count, packed]
    
    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._item_data):
            raise StopIteration
        else:
            item = self._item_data[self._index]
            self._index += 1
            return item


class PackingList(object):

    PACKING_LIST_DIR = 'packing_lists'
    os.makedirs(PACKING_LIST_DIR, exist_ok=True)

    def __init__(self, trip_name, start_date, end_date, items=None):
        self.trip_name = trip_name
        self.start_date = start_date
        self.end_date = end_date
        self._items = [PackingItem(*item) for item in items] if items else []
    
    def __repr__(self):
        start_date = self.start_date.packing_strftime()
        end_date = self.end_date.packing_strftime()
        return (f"{self.__class__.__name__}(trip_name='{self.trip_name}',"
                f" start_date='{start_date}', end_date='{end_date}')")

    def __str__(self):
        start_date = self.start_date.packing_strftime()
        end_date = self.end_date.packing_strftime()
        return f"Trip to {self.trip_name} from {start_date} to {end_date}"

    def __len__(self):
        return len(self._items)

    def __getitem__(self, s):
        return self._items[s]

    def append(self, item):
        packing_item = PackingItem(*item)
        self._items.append(packing_item)
    
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
            raise ValueError('End date must be before start date')
        self._end_date = end_date

    @property
    def filename(self):
        start_date = self.start_date.packing_strftime()
        end_date = self.end_date.packing_strftime()
        filename = f"{self.trip_name} {start_date} to {end_date}.yaml"
        return filename
    
    def print_items(self):
        print(f"{'Item':<30}{'Count':>10}{'Packed':>10}")
        for item in self._items:
            print(item)
    
    def write_yaml(self):
        filepath = os.path.join(self.__class__.PACKING_LIST_DIR, self.filename)

        data = dict(
            trip_name=self.trip_name,
            start_date=self.start_date.packing_strftime(),
            end_date=self.end_date.packing_strftime(),
            item_list=[list(item) for item in self._items]
        )

        with open(filepath, 'w') as f:
            yaml.dump(data, f)

    @classmethod
    def read_yaml(cls, filename):
        if filename[-5:] != '.yaml':
            filename = filename + '.yaml'

        filepath = os.path.join(cls.PACKING_LIST_DIR, filename)
        with open(filepath, 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        return cls(
            data['trip_name'],
            PackingListDate.packing_strptime(data['start_date']),
            PackingListDate.packing_strptime(data['end_date']),
            data['item_list']
        )
    
    @classmethod
    def list_packing_lists(cls):
        filenames = os.listdir(cls.PACKING_LIST_DIR)
        filenames_split = list(map(os.path.splitext, filenames))
        yaml_filenames = [x[0] for x in filenames_split if x[1] == '.yaml']
        return yaml_filenames


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
