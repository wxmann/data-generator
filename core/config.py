from functools import partial

__author__ = 'tangz'

class TabularConfig:

    # TODO: use OrderedDict
    def __init__(self):
        self.generators = {}

    def columns(self):
        # TODO: priority queue
        return self.generators.keys()

    def set_generator(self, col, generator):
        self.generators[col] = generator

    def get_generator(self, col):
        # TODO: error handling
        return self.generators[col]
