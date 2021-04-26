
class PackingItem(object):

    def __init__(self, item_name, count, packed=False):
        self.item_name = str(item_name).strip()
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
        return {self.item_name: {'count': self.count, 'packed': self.packed}}
    
    @classmethod
    def from_dict(cls, item_data):
        item_name = list(item_data.keys())[0]
        return cls(item_name, **item_data[item_name])


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
