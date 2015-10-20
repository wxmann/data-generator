import unittest

from wrapper import FunctionWrapper, SingleRepeater, ClusterRepeater
from tests import testdata

__author__ = 'tangz'


class WrapperTests(unittest.TestCase):

    def test_basic_function_setting_for_generator_witharg(self):
        funcwrapper = FunctionWrapper(testdata.counter)
        start = 4
        inc = 2
        for i in range(10):
            self.assertEqual(funcwrapper.get(start, inc), start + i*inc)

    def test_basic_function_setting_for_generator_withkwarg(self):
        funcwrapper = FunctionWrapper(testdata.counter)
        start = 4
        inc = 2
        for i in range(10):
            self.assertEqual(funcwrapper.get(start=start, inc=inc), start + i*inc)

    def test_basic_function_setting_for_generator_withnone(self):
        funcwrapper = FunctionWrapper(testdata.counter_none)
        for i in range(10):
            self.assertEqual(funcwrapper.get(), i)

    def test_basic_function_setting_for_generator_withboth(self):
        funcwrapper = FunctionWrapper(testdata.counter)
        start = 4
        inc = 2
        for i in range(10):
            self.assertEqual(funcwrapper.get(start, inc=inc), start + i*inc)

    def test_basic_function_setting_for_function_witharg(self):
        funcwrapper = FunctionWrapper(testdata.mult)
        self.assertEqual(funcwrapper.get(4, 2), 8)

    def test_basic_function_setting_for_function_withkwarg(self):
        funcwrapper = FunctionWrapper(testdata.mult)
        a = 4
        b = 2
        self.assertEqual(funcwrapper.get(a=a, b=b), 8)

    def test_basic_function_setting_for_function_withnone(self):
        funcwrapper = FunctionWrapper(testdata.mult_none)
        self.assertEqual(funcwrapper.get(), 8)

    def test_basic_function_setting_for_function_withboth(self):
        funcwrapper = FunctionWrapper(testdata.mult)
        a = 4
        b = 2
        self.assertEqual(funcwrapper.get(a, b=b), 8)

    def test_single_repeater(self):
        funcwrapper = FunctionWrapper(testdata.counter)
        repeated = SingleRepeater(funcwrapper, 4)
        start = 4
        inc = 2
        values = [repeated.get(start, inc) for i in range(10)]
        self.assertEqual(values, [4, 4, 4, 4, 6, 6, 6, 6, 8, 8])

    def test_cluster_repeater(self):
        funcwrapper = FunctionWrapper(testdata.counter)
        repeated = ClusterRepeater(funcwrapper, 4)
        start = 4
        inc = 2
        values = [repeated.get(start, inc) for i in range(10)]
        self.assertEqual(values, [4, 6, 8, 10, 4, 6, 8, 10, 4, 6])