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


def repeat(count, generator):
    while True:
        repeated_value = next(generator)
        for i in range(count):
            yield repeated_value


def repeat_cluster(count, generator):
    cluster = []
    for i in range(count):
        item = next(generator)
        cluster.append(item)
        yield item
    while True:
        for i in range(count):
            yield cluster[i]


# If func is a generator, return a generator that yields the same value in the same order as the original generator
# TODO: handle finite generator.
def as_generator(func, *args, **kwargs):
    if inspect.isgeneratorfunction(func):
        gen = func(*args, **kwargs)
        while True:
            yield next(gen)
    else:
        wrappedfunc = partial(func, *args, **kwargs)
        while True:
            yield wrappedfunc()

def const(value):
    while True:
        yield value

def choose(*args):
    return as_generator(random.choice, list(args))

def loop(items):
    while True:
        for item in items:
            yield item


# integer = IntegerGenerator()
#
#
#
#
# class NumberGenerator():
#     __metaclass__ = ABCMeta
#
#     @abstractmethod
#     def orderof(self, maglow, maghigh=None):
#         pass
#
#     @abstractmethod
#     def between(self, minval, maxval):
#         pass
#
#
# class IntegerGenerator(NumberGenerator):
#
#     def __init__(self):
#         pass
#
#     def orderof(self, maglow, maghigh=None):
#         highpow = maglow + 1 if maghigh is None else maghigh
#         lowpow = maglow
#         if highpow <= lowpow:
#             raise ValueError('High order of magnitude must be greater than low order of magnitude')
#         return wrap(random.randint, 10 ** lowpow, 10 ** highpow)
#
#     def between(self, minval, maxval):
#         if minval >= maxval:
#             raise ValueError('Min value has to be less than max value')
#         return wrap(random.randint, minval, maxval)
#
#
# class FloatGenerator(NumberGenerator):
#
#     def __init__(self):
#         pass
#
#     def orderof(self, maglow, maghigh=None):
#         highpow = maglow + 1 if maghigh is None else maghigh
#         lowpow = maglow
#         if highpow <= lowpow:
#             raise ValueError('High order of magnitude must be greater than low order of magnitude')
#         return wrap(random.uniform, 10 ** lowpow, 10 ** highpow)
#
#     def between(self, minval, maxval):
#         if minval >= maxval:
#             raise ValueError('Min value has to be less than max value')
#         return wrap(random.uniform, minval, maxval)