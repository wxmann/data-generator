import random
import unittest
from core import config, repeat

__author__ = 'tangz'

def incrementer(x):
    i = 0
    while True:
        yield x + i
        i += 1

class RepeatTest(unittest.TestCase):

    def test_should_repeat_cluster(self):
        funcsetting = config.FunctionSetting('ABC', incrementer, None, 3)
        count = 3
        cluster = repeat.repeatcluster(count, funcsetting).series()

        self.assertEquals(next(cluster), 3)
        self.assertEquals(next(cluster), 4)
        self.assertEquals(next(cluster), 5)
        self.assertEquals(next(cluster), 3)
        self.assertEquals(next(cluster), 4)
        self.assertEquals(next(cluster), 5)