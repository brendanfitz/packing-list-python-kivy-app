import os
import re
import yaml
import datetime as dt
import pandas as pd
from collections import OrderedDict

class PackingItem(object):

    def __init__(self, item_name, count, packed=False):
        self.item_name = item_name
        self.count = count
        self.packed = False 
    
    def pack(self):
        self.packed = True

    def unpack(self):
        self.packed = True
    
    def __str__(self):
        return f"{self.item_name:<30}{self.count:>10}{self.packed:>10}"

    def to_list(self):
        return [self.item_name, self.count, self.packed]

class PackingList(list):

    PACKING_LIST_DIR = 'packing_lists'
    DATE_PAT_STR = r'\d\d\d\d-\d\d-\d\d'
    STRPTIME_PAT_STR = r'%Y-%m-%d'
    DATE_PAT = re.compile(DATE_PAT_STR)

    CATEGORIES = []
    CSV_COLUMNS = ['Item', 'Count']

    def __init__(self, trip_name, start_date, end_date, item_list=None):
        self.trip_name = trip_name
        self.start_date = PackingList.check_date(start_date)
        self.end_date = PackingList.check_date(end_date)

        if not os.path.isdir(PackingList.PACKING_LIST_DIR):
            os.mkdir(PackingList.PACKING_LIST_DIR)

    @classmethod
    def check_date(cls, input):
        if isinstance(input, (dt.date, dt.datetime)):
            return input
        return dt.datetime.strptime(input, cls.STRPTIME_PAT_STR)

    def __getitem__(self, item_name):
        item = next(filter(lambda x: x.item_name == item_name, self))
        return item
    
    def append(self, item):
        if not isinstance(item, PackingItem):
            raise ValueError("Item must be of type PackingItem")
        list.append(self, item)
    
    def load_packing_list_csv(self, filename):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"{filename} does not exist")
        
        df = pd.read_csv(filename, dtype={'Item': str, 'Count': 'int64'})

        if df.columns.tolist() != PackingList.CSV_COLUMNS:
            raise ValueError(f"Columns must be {PackingList.CSV_COLUMNS}")

        for idx, row in df.iterrows():
            packing_item = PackingItem(row['Item'], row['Count'])
            self.append(packing_item)
    
    def print_packing_list(self):
        print(f"{'Item':<30}{'Count':>10}{'Packed':>10}")
        for item in self:
            print(item)
    
    def __str__(self):
        str_format = '%b %d, %Y'
        start_date_str = self.start_date.strftime(str_format)
        end_date_str = self.end_date.strftime(str_format)
        return f"Trip to {self.trip_name} from {start_date_str} to {end_date_str}"

    def write_yaml(self, filename):
        data = dict(
            trip_name=self.trip_name,
            start_date=self.start_date,
            end_date=self.end_date,
            item_list=[x.to_list() for x in self]
        )

        filepath = os.path.join(PackingList.PACKING_LIST_DIR, filename)
        with open(filepath, 'w') as f:
            yaml.dump(data, f)

    def read_yaml(self, filename):
        filepath = os.path.join(PackingList.PACKING_LIST_DIR, filename)
        with open(filepath, 'w') as f:
            yaml.load(data, f)



