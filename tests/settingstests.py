import unittest

from settings import FunctionSetting, SingleRepeater, ClusterRepeater
from tests import testdata

__author__ = 'tangz'


class SettingsTests(unittest.TestCase):

    def test_basic_function_setting_for_generator_witharg(self):
        funcsetting = FunctionSetting(testdata.counter)
        start = 4
        inc = 2
        for i in range(10):
            self.assertEqual(funcsetting.get(start, inc), start + i*inc)

    def test_basic_function_setting_for_generator_withkwarg(self):
        funcsetting = FunctionSetting(testdata.counter)
        start = 4
        inc = 2
        for i in range(10):
            self.assertEqual(funcsetting.get(start=start, inc=inc), start + i*inc)

    def test_basic_function_setting_for_generator_withnone(self):
        funcsetting = FunctionSetting(testdata.counter_none)
        for i in range(10):
            self.assertEqual(funcsetting.get(), i)

    def test_basic_function_setting_for_generator_withboth(self):
        funcsetting = FunctionSetting(testdata.counter)
        start = 4
        inc = 2
        for i in range(10):
            self.assertEqual(funcsetting.get(start, inc=inc), start + i*inc)

    def test_basic_function_setting_for_function_witharg(self):
        funcsetting = FunctionSetting(testdata.mult)
        self.assertEqual(funcsetting.get(4, 2), 8)

    def test_basic_function_setting_for_function_withkwarg(self):
        funcsetting = FunctionSetting(testdata.mult)
        a = 4
        b = 2
        self.assertEqual(funcsetting.get(a=a, b=b), 8)

    def test_basic_function_setting_for_function_withnone(self):
        funcsetting = FunctionSetting(testdata.mult_none)
        self.assertEqual(funcsetting.get(), 8)

    def test_basic_function_setting_for_function_withboth(self):
        funcsetting = FunctionSetting(testdata.mult)
        a = 4
        b = 2
        self.assertEqual(funcsetting.get(a, b=b), 8)

    def test_single_repeater(self):
        funcsetting = FunctionSetting(testdata.counter)
        repeated = SingleRepeater(funcsetting, 4)
        start = 4
        inc = 2
        values = [repeated.get(start, inc) for i in range(10)]
        self.assertEqual(values, [4, 4, 4, 4, 6, 6, 6, 6, 8, 8])

    def test_cluster_repeater(self):
        funcsetting = FunctionSetting(testdata.counter)
        repeated = ClusterRepeater(funcsetting, 4)
        start = 4
        inc = 2
        values = [repeated.get(start, inc) for i in range(10)]
        self.assertEqual(values, [4, 6, 8, 10, 4, 6, 8, 10, 4, 6])