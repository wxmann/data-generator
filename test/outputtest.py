import random
import unittest
from core import config, generators, output

__author__ = 'tangz'

class OutputTest(unittest.TestCase):

    def test_output(self):
        config1 = config.TabularConfig()
        config1.set_generator('Contract Reference', generators.counter(prefix='CR'))
        config1.set_generator('Netting Set', generators.as_generator(random.choice, ['A', 'B', 'C', 'D']))
        output.to_csv('first_test.csv', config1, 109)

    def test_priority(self):
        config1 = config.TabularConfig()
        config1.set_generator('Contract Reference', generators.counter(prefix='CR'), priority=1)
        config1.set_generator('Netting Set', generators.as_generator(random.choice, ['A', 'B', 'C', 'D']))

        self.assertEqual(config1.columns(), ['Contract Reference', 'Netting Set'])
        self.assertNotEqual(config1.columns(), ['Netting Set', 'Contract Reference'])
