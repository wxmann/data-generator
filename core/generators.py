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

def repeat(count, func, *args, **kwargs):
    if inspect.isgeneratorfunction(func):
        func_callable = func(*args, **kwargs)
    else:
        func_callable = wrap(func, *args, **kwargs)
    return _repeat_generator(count, func_callable)

def _repeat_generator(count, func):
    while True:
        repeated_value = next(func)
        for i in range(0, count):
            yield repeated_value

# Func cannot be a generator or else only first value is returned.
def wrap(func, *args, **kwargs):
    wrappedfunc = partial(func, *args, **kwargs)
    while True:
        yield wrappedfunc()

def const(value):
    while True:
        yield value

def choose(*args):
    return wrap(random.choice, list(args))

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