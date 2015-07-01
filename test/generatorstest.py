import random
import unittest
import logging

from generators import basic


__author__ = 'tangz'

class GeneratorTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.INFO)

    def test_counter_noargs(self):
        the_counter = basic.counter()
        for i in range(1, 3):
            self.assertEqual(next(the_counter), i)

    def test_counter_prefix(self):
        the_counter = basic.counter(prefix='CR')
        for i in range(1, 3):
            self.assertEqual(next(the_counter), 'CR{}'.format(i))

    def test_counter_prefix_sep(self):
        the_counter = basic.counter(prefix='CR', sep='-')
        for i in range(1, 3):
            self.assertEqual(next(the_counter), 'CR-{}'.format(i))

    def test_counter_start_nonzero(self):
        the_counter = basic.counter(start=10)
        for i in range(1, 3):
            self.assertEqual(next(the_counter), i+9)

    def test_repeat_with_generator(self):
        generator = basic.as_generator(basic.counter, prefix='CR')
        the_counter = basic.repeat(5, generator)
        for i in range(1, 6):
            self.assertEqual(next(the_counter), 'CR1')
        for i in range(1, 6):
            self.assertEqual(next(the_counter), 'CR2')
        for i in range(1, 6):
            self.assertEqual(next(the_counter), 'CR3')

    def test_repeat_with_function(self):
        generator = basic.as_generator(random.randint, 1, 10)
        repeater = basic.repeat(5, generator)
        first = next(repeater)
        logging.info('First repeated value: {}'.format(first))
        for i in range(1, 5):
            self.assertEqual(next(repeater), first)
        second = next(repeater)
        logging.info('Second repeated value: {}'.format(second))
        for i in range(1, 5):
            self.assertEqual(next(repeater), second)

    def test_asgenerator_function(self):
        choices = ['A', 'B', 'C']
        wrapper = basic.as_generator(random.choice, choices)
        for i in range(1, 15):
            value = next(wrapper)
            logging.info('Chose: {}'.format(value))
            self.assertIn(value, choices)

    def test_asgenerator_generator(self):
        thegen = basic.as_generator(basic.counter, start=1)
        self.assertEqual(next(thegen), 1)
        self.assertEqual(next(thegen), 2)

    def test_repeat_cluster(self):
        thegen = basic.choose('A', 'B', 'C', 'D', 'E', 'F')
        clustergen = basic.repeat_cluster(2, thegen)

        result = [next(clustergen) for i in range(10)]
        logging.info('Result list: {}'.format(result))
        result0 = result[0]
        result1 = result[1]
        for i in range(10):
            result_to_compare = result0 if i % 2 == 0 else result1
            self.assertEqual(result[i], result_to_compare)




