import random
import itertools

__author__ = 'tangz'

FUNCTIONS = {
    'const': lambda value: value,
    'loop': itertools.cycle,
    'choice': random.choice,
    'range': random.uniform,
    'range-int': random.randint,
    'decimal': random.random
}


class InvalidFunctionError(Exception):
    pass


def lookup(funcid):
    if funcid not in FUNCTIONS:
        raise InvalidFunctionError('Invalid function provided: {}'.format(funcid))
    return FUNCTIONS[funcid]
