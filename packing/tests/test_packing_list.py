import unittest
from packing import PackingList, PackingItem
from packing.tests import setup
from packing.tests import teardown

class PackingListTestCase(unittest.TestCase):

    def setUp(self):
        setup.main()
    
    def test_packing_list_load(self):
        filename = 'Austin 2020-08-28 to 2020-09-07.yaml'
        pl = PackingList.read_yaml(filename)
        pl_len = len(pl)
        self.assertEqual(pl_len, 5)
    
    def tearDown(self):
        teardown.main()

if __name__ == '__main__':
    unittest.main()