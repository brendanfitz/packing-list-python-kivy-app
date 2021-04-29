import unittest
from os import path, listdir, remove
import shutil
from packing import PackingList, PackingItem, PackingItemSchema, PackingListSchema, PackingDateValueError

class PackingTestCase(unittest.TestCase):

    def setUp(self):
        self.items = [
            PackingItem('Cake', 8, True),
            PackingItem('Fan', 1, False),
            PackingItem('Gloves', 2, False),
            PackingItem('Madhat', 1, False),
        ]
        self.item = self.items[0]
        self.plist = PackingList('Wonderland', '2021-04-01', '2021-04-08', items=self.items)

        templates_path = path.join('packing', 'tests', 'templates')
        self.setup_filenames = listdir(templates_path)
    
        for filename in self.setup_filenames:
            src = path.join(templates_path, filename)
            dest = path.join(PackingList.PACKING_LIST_DIR, filename)
            shutil.copy(src, dest)
    
    def tearDown(self):
        for filename in self.setup_filenames:
            filepath = path.join(PackingList.PACKING_LIST_DIR, filename)
            remove(filepath)

    def test_packing_list_toJSON(self):
        filepath = self.plist.toJSON()
        self.assertTrue(path.isfile(filepath))

        plist_copy = PackingList.fromJSON(filepath)
        self.assertEqual(self.plist, plist_copy)
        remove(filepath)
    
    def test_packing_list_fromJSON(self):
        plist = PackingList.fromJSON('Hogwarts 2020-02-07 to 2020-02-17.json')
        self.assertEqual(plist.trip_name, 'Hogwarts')
        self.assertEqual(len(plist.items), 5)

    def test_packing_item_serialization(self):
        schema = PackingItemSchema()
        item = self.items[0]

        json = schema.dumps(item)
        item_from_json = schema.loads(json)

        self.assertEqual(item, item_from_json)
    
    def test_packing_list_serialization(self):
        schema = PackingListSchema()
        json = schema.dumps(self.plist)
        plist_from_json = schema.loads(json)
        self.assertEqual(self.plist, plist_from_json)
    
    def test_packing_list_date_error(self):
        with self.assertRaises(PackingDateValueError):
            PackingList('Nowhere in particular', '2020-01-01', '2019-12-31')
    
    def test_packing_list_append_duplicate_error(self):
        with self.assertRaises(ValueError):
            self.plist.append(self.item)
    
    def test_packing_item_equality(self):
        test_items = (
            PackingItem('Cake', 8, True),
            PackingItem('Cake', 7, True),
            PackingItem('Cake', 8, False),
        )
        for item in test_items:
            self.assertEqual(self.item, item)

        item = PackingItem('Pie', 8, True)
        self.assertNotEqual(self.item, item)

    def test_packing_list_equality(self):
        plist = PackingList('Wonderland', '2021-04-01', '2021-04-08', items=self.items)
        self.assertEqual(self.plist, plist)

        test_plists = (
            PackingList('Narnia', '2021-04-01', '2021-04-08', items=self.items),
            PackingList('Wonderland', '2021-03-01', '2021-04-08', items=self.items),
            PackingList('Wonderland', '2021-04-01', '2021-04-09', items=self.items)
        )
        for plist in test_plists:
            self.assertNotEqual(self.plist, plist)
    
    def test_packing_item_packed_setter(self):
        for value in ('y', 'yes', 'YES', True):
            self.item.packed = value
            self.assertTrue(self.item.packed)

        for value in ('n', 'no', 'NO', False):
            self.item.packed = value
            self.assertFalse(self.item.packed)

        with self.assertRaises(ValueError):
            self.item.packed = 69
    
    def test_get_packing_lists(self):
        plists = PackingList.get_packing_lists()
        self.assertTrue(len(plists) >= 3)
    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(PackingTestCase)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)