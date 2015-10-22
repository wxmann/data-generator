from abc import ABCMeta, abstractmethod
from functools import partial
import inspect
import random

__author__ = 'tangz'

def counter(start=1, prefix=None, sep=''):
    num = start
    while True:
        if prefix is None:
            yield num
        else:
            yield '{}{}{}'.format(prefix, sep, num)
        num += 1