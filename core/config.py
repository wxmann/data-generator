from functools import partial

__author__ = 'tangz'

class TabularConfig:

    def __init__(self):
        self.generators = {}

    def columns(self):
        # TODO: priority queue
        return self.generators.keys()

    def set_generator(self, col, func, *args, **kwargs):
        self.generators[col] = partial(func, *args, **kwargs)

    def get_generator(self, col):
        # TODO: error handling
        return self.generators[col]
