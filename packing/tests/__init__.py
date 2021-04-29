from packing import PackingList
from packing.tests.test_packing_list import PackingTestCase

def load_test_list():
    PackingList.PACKING_LIST_DIR = 'packing/tests/templates'
    return PackingList.fromJSON('Hogwarts 2020-02-07 to 2020-02-17.json') 