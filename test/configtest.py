import unittest

from core import config


__author__ = 'tangz'

class ConfigTest(unittest.TestCase):

    def setUp(self):
        self.dummyfunc = lambda x, y: x * y + 1
        self.column = 'Dummy_Column'

    def test_funcsetting_args_should_generate_value(self):
        dependencies = None
        funcsetting = config.FunctionSetting(self.column, self.dummyfunc, dependencies, 1, 2)
        self.assertEqual(funcsetting.generatevalue(), 3)

    def test_funcsetting_kwargs_should_generate_value(self):
        dependencies = None
        funcsetting = config.FunctionSetting(self.column, self.dummyfunc, dependencies, x=1, y=2)
        self.assertEqual(funcsetting.generatevalue(), 3)

    def test_funcsetting_externalargs_should_generate_value(self):
        dependencies = ['Column_A', 'Column_B']
        funcsetting = config.FunctionSetting(self.column, self.dummyfunc, dependencies)
        self.assertEqual(funcsetting.generatevalue(1, 2), 3)

    def test_funcsetting_externalkwargs_should_generate_value(self):
        dependencies = ['Column_A', 'Column_B']
        funcsetting = config.FunctionSetting(self.column, self.dummyfunc, dependencies)
        self.assertEqual(funcsetting.generatevalue(x=1, y=2), 3)

    def test_funcsetting_mixargskwargs_should_generate_value(self):
        dependencies = None
        funcsetting = config.FunctionSetting(self.column, self.dummyfunc, dependencies, 1, y=2)
        self.assertEqual(funcsetting.generatevalue(), 3)

    def test_funcsetting_someexternalargs_should_generate_value(self):
        dependencies = ['Column_A']
        funcsetting = config.FunctionSetting(self.column, self.dummyfunc, dependencies, 1)
        self.assertEqual(funcsetting.generatevalue(2), 3)

    def test_funcsetting_someexternalkwargs_should_generate_value(self):
        dependencies = ['Column_A']
        funcsetting = config.FunctionSetting(self.column, self.dummyfunc, dependencies, x=1)
        self.assertEqual(funcsetting.generatevalue(y=2), 3)

    def test_funcsetting_mix_intargsextkwargs_should_generate_value(self):
        dependencies = ['Column_A']
        funcsetting = config.FunctionSetting(self.column, self.dummyfunc, dependencies, 1)
        self.assertEqual(funcsetting.generatevalue(y=2), 3)

    def test_should_set_and_get_funcsetting_no_dependencies(self):
        dependencies = None
        funcsetting_expected = config.FunctionSetting(self.column, self.dummyfunc, dependencies, 1, 2)
        tableconfig = config.TabularConfig()
        tableconfig.set_funcsetting(self.column, self.dummyfunc, 1, 2)
        funcsetting_actual = tableconfig.get_funcsetting(self.column)

        self.assertEquals(funcsetting_actual, funcsetting_expected)


