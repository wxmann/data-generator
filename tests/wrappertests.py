import unittest

from wrapper import FunctionWrapper, SingleRepeater, ClusterRepeater, FormatWrapper
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
        
    def test_function_wrapper_for_iterable(self):
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

    # TODO: add tests for formatters

    def test_function_wrappers_eq(self):
        fn1 = lambda x: x
        fn2 = lambda x, y: x + y
        wrapper1 = FunctionWrapper(fn1)
        wrapper2 = FunctionWrapper(fn1)
        wrapper3 = FunctionWrapper(fn2)

        self.assertTrue(wrapper1 == wrapper2)
        self.assertTrue(wrapper1 != wrapper3)

    def test_format_wrappers_eq(self):
        fn1 = lambda x: x
        fn2 = lambda x, y: x + y
        formatter1 = lambda x: 'Ref_' + str(x)
        formatter2 = lambda x: 'Bref_' + str(x)
        wrapper1 = FormatWrapper(FunctionWrapper(fn1), formatter1)
        wrapper2 = FormatWrapper(FunctionWrapper(fn1), formatter1)
        wrapper3 = FormatWrapper(FunctionWrapper(fn2), formatter1)
        wrapper4 = FormatWrapper(FunctionWrapper(fn1), formatter2)

        self.assertTrue(wrapper1 == wrapper2)
        self.assertTrue(wrapper1 != wrapper3, 'Wrappers using different function, same formatter should not be equal.')
        self.assertTrue(wrapper1 != wrapper4, 'Wrappers using same function, different formatter should not be equal.')

    def test_single_repeater_wrappers_eq(self):
        fn1 = lambda x: x
        fn2 = lambda x, y: x + y
        wrapper1 = SingleRepeater(FunctionWrapper(fn1), 5)
        wrapper2 = SingleRepeater(FunctionWrapper(fn1), 5)
        wrapper3 = SingleRepeater(FunctionWrapper(fn1), 4)
        wrapper4 = SingleRepeater(FunctionWrapper(fn2), 5)

        self.assertTrue(wrapper1 == wrapper2)
        self.assertTrue(wrapper1 != wrapper3, 'Wrappers using same function, different n should not be equal.')
        self.assertTrue(wrapper1 != wrapper4, 'Wrappers using different function, same n should not be equal.')

    def test_cluster_repeater_wrappers_eq(self):
        fn1 = lambda x: x
        fn2 = lambda x, y: x + y
        wrapper1 = ClusterRepeater(FunctionWrapper(fn1), 5)
        wrapper2 = ClusterRepeater(FunctionWrapper(fn1), 5)
        wrapper3 = ClusterRepeater(FunctionWrapper(fn1), 4)
        wrapper4 = ClusterRepeater(FunctionWrapper(fn2), 5)

        self.assertTrue(wrapper1 == wrapper2)
        self.assertTrue(wrapper1 != wrapper3, 'Wrappers using same function, different n should not be equal.')
        self.assertTrue(wrapper1 != wrapper4, 'Wrappers using different function, same n should not be equal.')