import inspect

__author__ = 'tangz'

def extractvalue(func, *args, **kwargs):
    if inspect.isgenerator(func):
        return next(func)
    else:
        return func(*args, **kwargs)