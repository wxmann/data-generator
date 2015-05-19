import unittest
from core import generators

__author__ = 'tangz'

class GeneratorTest(unittest.TestCase):

    def test_counter_noargs(self):
        the_counter = generators.counter()
        self.assertEquals(next(the_counter), 1)
        self.assertEquals(next(the_counter), 2)


