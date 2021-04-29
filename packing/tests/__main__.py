import unittest
from packing.tests import PackingTestCase

suite = unittest.TestLoader().loadTestsFromTestCase(PackingTestCase)
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)