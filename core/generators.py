__author__ = 'tangz'

def counter(start=1, seed=None, sep=''):
    num = start
    if seed is None:
        yield num
    else:
        yield sep.join(seed, num)
    num += 1
