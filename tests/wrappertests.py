import unittest

from wrapper import FunctionWrapper, SingleRepeater, ClusterRepeater
from tests import testdata

__author__ = 'tangz'


class WrapperTests(unittest.TestCase):

    def test_function_wrapper_for_generator_witharg(self):
        funcwrapper = FunctionWrapper(testdata.counter)
        start = 4
        inc = 2
        for i in range(10):
            self.assertEqual(funcwrapper.eval(start, inc), start + i*inc)

    def test_function_wrapper_for_generator_withkwarg(self):
        funcwrapper = FunctionWrapper(testdata.counter)
        start = 4
        inc = 2
        for i in range(10):
            self.assertEqual(funcwrapper.eval(start=start, inc=inc), start + i*inc)

    def test_function_wrapper_for_generator_withnone(self):
        funcwrapper = FunctionWrapper(testdata.counter_none)
        for i in range(10):
            self.assertEqual(funcwrapper.eval(), i)

    def test_function_wrapper_for_generator_withboth(self):
        funcwrapper = FunctionWrapper(testdata.counter)
        start = 4
        inc = 2
        for i in range(10):
            self.assertEqual(funcwrapper.eval(start, inc=inc), start + i*inc)

    def test_function_wrapper_for_function_witharg(self):
        funcwrapper = FunctionWrapper(testdata.mult)
        self.assertEqual(funcwrapper.eval(4, 2), 8)

    def test_function_wrapper_for_function_withkwarg(self):
        funcwrapper = FunctionWrapper(testdata.mult)
        a = 4
        b = 2
        self.assertEqual(funcwrapper.eval(a=a, b=b), 8)

    def test_function_wrapper_for_function_withnone(self):
        funcwrapper = FunctionWrapper(testdata.mult_none)
        self.assertEqual(funcwrapper.eval(), 8)

    def test_function_wrapper_for_function_withboth(self):
        funcwrapper = FunctionWrapper(testdata.mult)
        a = 4
        b = 2
        self.assertEqual(funcwrapper.eval(a, b=b), 8)
        
    def test_function_setting_for_iterable(self):
        funcwrapper = FunctionWrapper(testdata.CountingIterable)
        start = 4
        inc = 2
        self.assertEqual(funcwrapper.eval(start=start, inc=inc), 4)
        self.assertEqual(funcwrapper.eval(start=start, inc=inc), 6)
        self.assertEqual(funcwrapper.eval(start=start, inc=inc), 8)

    def test_function_wrapper_for_iterable_external_iterator(self):
        funcwrapper = FunctionWrapper(testdata.CountingIterableOutsideIterator)
        start = 4
        inc = 2
        self.assertEqual(funcwrapper.eval(start=start, inc=inc), 4)
        self.assertEqual(funcwrapper.eval(start=start, inc=inc), 6)
        self.assertEqual(funcwrapper.eval(start=start, inc=inc), 8)

    def test_single_repeater(self):
        funcwrapper = FunctionWrapper(testdata.counter)
        repeated = SingleRepeater(funcwrapper, 4)
        start = 4
        inc = 2
        values = [repeated.eval(start, inc) for i in range(10)]
        self.assertEqual(values, [4, 4, 4, 4, 6, 6, 6, 6, 8, 8])

    def test_cluster_repeater(self):
        funcwrapper = FunctionWrapper(testdata.counter)
        repeated = ClusterRepeater(funcwrapper, 4)
        start = 4
        inc = 2
        values = [repeated.eval(start, inc) for i in range(10)]
        self.assertEqual(values, [4, 6, 8, 10, 4, 6, 8, 10, 4, 6])