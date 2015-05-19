from functools import partial
import inspect

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
        return _repeat_generator(count, func, *args, **kwargs)
    else:
        return _repeat_function(count, func, *args, **kwargs)

def _repeat_generator(count, func, *args, **kwargs):
    indiv_func = func(*args, **kwargs)
    while True:
        repeated_value = next(indiv_func)
        for i in range(0, count):
            yield repeated_value

def _repeat_function(count, func, *args, **kwargs):
    while True:
        value = func(*args, **kwargs)
        for i in range(0, count):
            yield value

# Func cannot be a generator or else only first value is returned.
def wrap(func, *args, **kwargs):
    wrappedfunc = partial(func, *args, **kwargs)
    while True:
        yield wrappedfunc()