import random
import unittest
from core import generators

__author__ = 'tangz'

class GeneratorTest(unittest.TestCase):

    def test_counter_noargs(self):
        the_counter = generators.counter()
        for i in range(1, 3):
            self.assertEqual(next(the_counter), i)

    def test_counter_prefix(self):
        the_counter = generators.counter(prefix='CR')
        for i in range(1, 3):
            self.assertEqual(next(the_counter), 'CR{}'.format(i))

    def test_counter_prefix_sep(self):
        the_counter = generators.counter(prefix='CR', sep='-')
        for i in range(1, 3):
            self.assertEqual(next(the_counter), 'CR-{}'.format(i))

    def test_counter_start_nonzero(self):
        the_counter = generators.counter(start=10)
        for i in range(1, 3):
            self.assertEqual(next(the_counter), i+9)

    def test_repeat_with_generator(self):
        the_counter = generators.repeat(5, generators.counter, prefix='CR')
        for i in range(1, 6):
            self.assertEqual(next(the_counter), 'CR1')
        for i in range(1, 6):
            self.assertEqual(next(the_counter), 'CR2')
        for i in range(1, 6):
            self.assertEqual(next(the_counter), 'CR3')

    def test_repeat_with_function(self):
        repeater = generators.repeat(5, random.randint, 1, 10)
        first = next(repeater)
        print(first)
        for i in range(1, 5):
            self.assertEqual(next(repeater), first)
        second = next(repeater)
        print(second)
        for i in range(1, 5):
            self.assertEqual(next(repeater), second)


    def test_wrap(self):
        choices = ['A', 'B', 'C']
        wrapper = generators.wrap(random.choice, choices)
        for i in range(1, 15):
            value = next(wrapper)
            print(value)
            self.assertIn(value, choices)



