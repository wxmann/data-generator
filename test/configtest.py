import unittest
from core import generators, config

__author__ = 'tangz'

class ConfigTest(unittest.TestCase):

    def test_set_generator_simple(self):
        dummyconfig = config.TabularConfig()
        dummygenerator = generators.const('ABC')
        column = 'Name'
        dummyconfig.set_generator(column, dummygenerator)
        self.assertIs(dummyconfig.get_generator(column), dummygenerator)

    def test_set_multiple_generators(self):
        dummyconfig = config.TabularConfig()
        column1 = 'Name'
        column2 = 'Birthday'
        column3 = 'SSN'
        dummygenerator1 = generators.const('Jim')
        dummygenerator2 = generators.choose('08/05/1991', '09/01/1992')
        dummygenerator3 = generators.const('11111111')
        dummyconfig.set_generator(column1, dummygenerator1)
        dummyconfig.set_generator(column2, dummygenerator2)
        dummyconfig.set_generator(column3, dummygenerator3)
        self.assertIs(dummyconfig.get_generator(column1), dummygenerator1)
        self.assertIs(dummyconfig.get_generator(column2), dummygenerator2)
        self.assertIs(dummyconfig.get_generator(column3), dummygenerator3)

    def test_get_columns(self):
        dummyconfig = config.TabularConfig()
        column1 = 'Name'
        column2 = 'Birthday'
        column3 = 'SSN'
        dummygenerator1 = generators.const('Jim')
        dummygenerator2 = generators.choose('08/05/1991', '09/01/1992')
        dummygenerator3 = generators.const('11111111')
        dummyconfig.set_generator(column1, dummygenerator1)
        dummyconfig.set_generator(column2, dummygenerator2)
        dummyconfig.set_generator(column3, dummygenerator3)
        self.assertCountEqual(dummyconfig.columns(), [column1, column2, column3])

    def test_set_with_priority(self):
        dummyconfig = config.TabularConfig()
        column1 = 'Name'
        column2 = 'Birthday'
        dummygenerator1 = generators.const('Jim')
        dummygenerator2 = generators.choose('08/05/1991', '09/01/1992')
        dummyconfig.set_generator(column1, dummygenerator1)
        dummyconfig.set_generator(column2, dummygenerator2, priority=5)

        self.assertEquals(dummyconfig.columns(), [column1, column2])

    def test_set_with_dependency(self):
        dummyconfig = config.TabularConfig()
        column1 = 'Name'
        column2 = 'Birthday'
        column3 = 'UID'
        dummygenerator1 = generators.const('Jim')
        dummygenerator2 = generators.choose('08/05/1991', '09/01/1992')
        dummyfunc3 = lambda x, y: '{}-{}'.format(x, y)
        dummyconfig.set_generator(column1, dummygenerator1)
        dummyconfig.set_generator(column2, dummygenerator2)
        dummyconfig.set_function_with_dependency(column3, dummyfunc3, [column1, column2])

        self.assertTrue(dummyconfig.has_dependencies(column3))
        self.assertCountEqual(dummyconfig.get_dependencies(column3), [column1, column2])
