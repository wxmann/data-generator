import unittest

from core import config


__author__ = 'tangz'

def dummygenerator(x, y):
    i = 1
    while True:
        yield x * y + i
        i += 1

class ConfigTest(unittest.TestCase):

    def setUp(self):
        self.dummyfunc = lambda x, y: x * y + 1
        self.dummygen = dummygenerator
        self.column = 'TestColumn'

    def test_funcsetting_args_should_generate_value(self):
        funcsetting = config.FunctionSetting(self.dummyfunc, args=[1, 2])
        self.assertEqual(funcsetting.generatevalue(), 3)

    def test_funcsetting_args_should_generate_value_withgenerator(self):
        funcsetting = config.FunctionSetting(self.dummygen, args=[1, 2])
        self.assertEqual(funcsetting.generatevalue(), 3)
        self.assertEqual(funcsetting.generatevalue(), 4)
        self.assertEqual(funcsetting.generatevalue(), 5)

    def test_funcsetting_kwargs_should_generate_value(self):
        funcsetting = config.FunctionSetting(self.dummyfunc, kwargs={'x': 1, 'y': 2})
        self.assertEqual(funcsetting.generatevalue(), 3)

    def test_funcsetting_kwargs_should_generate_value_withgenerator(self):
        funcsetting = config.FunctionSetting(self.dummygen, kwargs={'x': 1, 'y': 2})
        self.assertEqual(funcsetting.generatevalue(), 3)
        self.assertEqual(funcsetting.generatevalue(), 4)
        self.assertEqual(funcsetting.generatevalue(), 5)

    def test_funcsetting_externalargs_should_generate_value(self):
        funcsetting = config.FunctionSetting(self.dummyfunc, dependencies=['Column_A', 'Column_B'])
        self.assertEqual(funcsetting.generatevalue(1, 2), 3)

    def test_funcsetting_externalkwargs_should_generate_value(self):
        funcsetting = config.FunctionSetting(self.dummyfunc, dependencies=['Column_A', 'Column_B'])
        self.assertEqual(funcsetting.generatevalue(x=1, y=2), 3)

    def test_funcsetting_mixargskwargs_should_generate_value(self):
        funcsetting = config.FunctionSetting(self.dummyfunc, args=[1], kwargs={'y': 2})
        self.assertEqual(funcsetting.generatevalue(), 3)

    def test_funcsetting_someexternalargs_should_generate_value(self):
        funcsetting = config.FunctionSetting(self.dummyfunc, dependencies=['Column_A'], args={1})
        self.assertEqual(funcsetting.generatevalue(2), 3)

    def test_funcsetting_someexternalkwargs_should_generate_value(self):
        funcsetting = config.FunctionSetting(self.dummyfunc, dependencies=['Column_A'], kwargs={'x': 1})
        self.assertEqual(funcsetting.generatevalue(y=2), 3)

    def test_funcsetting_mix_intargsextkwargs_should_generate_value(self):
        funcsetting = config.FunctionSetting(self.dummyfunc, dependencies=['Column_A'], args=[1])
        self.assertEqual(funcsetting.generatevalue(y=2), 3)

    def test_funcsetting_same_attributes_eq(self):
        dependencies = ['A']
        setting1 = config.FunctionSetting(self.dummyfunc, dependencies=dependencies, args=[1, 2])
        setting2 = config.FunctionSetting(self.dummyfunc, dependencies=dependencies, args=[1, 2])
        self.assertEqual(setting1, setting2)

    def test_funcsetting_diff_attributes_noteq(self):
        dependencies = ['A']
        setting1 = config.FunctionSetting(self.dummyfunc, dependencies=dependencies, args=[1, 2])
        setting2 = config.FunctionSetting(self.dummyfunc, dependencies=dependencies, args=[2, 3])
        self.assertNotEqual(setting1, setting2)

    def test_should_set_and_get_funcsetting_no_dependencies(self):
        funcsetting_expected = config.FunctionSetting(self.dummyfunc, args=[1, 2])
        tableconfig = config.TabularConfig()
        tableconfig.set_funcsetting(self.column, self.dummyfunc, args=[1, 2])
        funcsetting_actual = tableconfig.get_funcsetting(self.column)

        self.assertEquals(funcsetting_actual, funcsetting_expected)


