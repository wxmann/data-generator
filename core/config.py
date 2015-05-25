from functools import partial

INITIAL_PRIORITY = 999

__author__ = 'tangz'

class TabularConfig:

    def __init__(self):
        self.generators = {}
        self.columns_priority = {}
        self.priority = INITIAL_PRIORITY

    def columns(self, priority_sorted=True):
        cols = self.generators.keys()
        if priority_sorted:
            prioritysortedkey = lambda col: self.columns_priority[col]
            return sorted(cols, key=prioritysortedkey)
        return cols

    def set_generator(self, col, generator, priority=None):
        self.generators[col] = generator
        priority = self._priority() if priority is None else priority
        self.columns_priority[col] = priority

    def get_generator(self, col):
        # TODO: error handling
        return self.generators[col]

    def _priority(self):
        self.priority += 1
        return self.priority
