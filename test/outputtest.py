import random
import unittest

from core import config, output
from generators import basic


__author__ = 'tangz'

class OutputTest(unittest.TestCase):

    def test_generate_row_no_dependencies(self):
        config1 = config.TabularConfig()
        config1.set_funcsetting('Contract Reference', lambda: 'CR1')
        config1.set_funcsetting('Netting Set', lambda: 'A')

        rowdata = output.RowGenerator(config1)
        rowdata.generate_row()
        rowmap = rowdata.output()

        self.assertDictEqual(rowmap, {'Contract Reference': 'CR1', 'Netting Set': 'A'})

    def test_generate_row_with_dependencies(self):
        config1 = config.TabularConfig()
        config1.set_funcsetting('Contract Reference', lambda: 'CR1')
        config1.set_funcsetting('Netting Set', lambda: 'A')
        config1.set_funcsetting('UID', lambda x, y: '{}-{}'.format(x, y), dependencies=['Contract Reference', 'Netting Set'])

        rowdata = output.RowGenerator(config1)
        rowdata.generate_row()
        rowmap = rowdata.output()

        self.assertDictEqual(rowmap, {'Contract Reference': 'CR1', 'Netting Set': 'A', 'UID': 'CR1-A'})

    def test_output(self):
        config1 = config.TabularConfig()
        config1.set_funcsetting('Contract_Reference', basic.counter, kwargs={'prefix': 'CR'})
        config1.set_funcsetting('Netting_Set', random.choice, args=[['A', 'B', 'C', 'D']])
        config1.set_funcsetting('UID', lambda x, y: '{}-{}'.format(x, y), dependencies=['Contract_Reference', "Netting_Set"])
        output.to_csv('second_test.csv', config1, 109)