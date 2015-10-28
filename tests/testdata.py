__author__ = 'tangz'

def counter_none():
    count = 0
    while True:
        yield count
        count += 1

def counter(start, inc):
    count = start
    while True:
        yield count
        count += inc

def mult(a, b):
    return a*b

def mult_none():
    return mult(4, 2)


class CountingIterable(object):
    def __init__(self, start=0, inc=1):
        self.num = start
        self.inc = inc

    def __iter__(self):
        return self

    def __next__(self):
        num_to_return = self.num
        self.num += self.inc
        return num_to_return


class CountingIterableOutsideIterator(object):
    def __init__(self, start=0, inc=1):
        self.num = start
        self.inc = inc

    def __iter__(self):
        return _ActualIterator(self.num, self.inc)


class _ActualIterator(object):
    def __init__(self, start, inc):
        self.num = start
        self.inc = inc

    def __iter__(self):
        return self

    def __next__(self):
        num_to_return = self.num
        self.num += self.inc
        return num_to_return