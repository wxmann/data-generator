import functools

__author__ = 'tangz'

def dateformatter(dateformat):
    return lambda dateobj: dateobj.strftime(dateformat)


def prepend(pre):
    return lambda x: str(pre) + str(x)


def postpend(post):
    return lambda x: str(x) + str(post)


def nround(precision):
    return functools.partial(round, ndigits=precision)

def nround_to_int():
    return round

