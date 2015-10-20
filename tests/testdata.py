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