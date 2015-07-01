import random
import unittest

from core import config, output
from generators import basic


__author__ = 'tangz'

class OutputTest(unittest.TestCase):

    def test_generate_row_no_dependencies(self):
        config1 = config.TabularConfig()
        config1.set_generator('Contract Reference', basic.const('CR1'))
        config1.set_generator('Netting Set', basic.const('A'))

        rowdata = output.RowGenerator(config1)
        rowdata.generate_row()
        rowmap = rowdata.output()

        self.assertDictEqual(rowmap, {'Contract Reference': 'CR1', 'Netting Set': 'A'})

    def test_generate_row_with_dependencies(self):
        config1 = config.TabularConfig()
        config1.set_generator('Contract Reference', basic.const('CR1'))
        config1.set_generator('Netting Set', basic.const('A'))
        config1.set_function_with_dependency('UID', lambda x, y: '{}-{}'.format(x, y), ['Contract Reference', 'Netting Set'])

        rowdata = output.RowGenerator(config1)
        rowdata.generate_row()
        rowmap = rowdata.output()

        self.assertDictEqual(rowmap, {'Contract Reference': 'CR1', 'Netting Set': 'A', 'UID': 'CR1-A'})

    def test_output(self):
        config1 = config.TabularConfig()
        config1.set_generator('Contract Reference', basic.counter(prefix='CR'))
        config1.set_generator('Netting Set', basic.as_generator(random.choice, ['A', 'B', 'C', 'D']))
        config1.set_function_with_dependency('UID', lambda x, y: '{}-{}'.format(x, y), ['Contract Reference', 'Netting Set'])
        output.to_csv('first_test.csv', config1, 109)
