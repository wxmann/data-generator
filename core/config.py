__author__ = 'tangz'

class ColumnNotFoundError(Exception):
    pass

class TabularConfig:

    def __init__(self):
        self.generators = {}
        self.columns_priority = {}
        self.dependencymap = {}

    def columns(self, priority_sorted=True):
        cols = self.generators.keys()
        if priority_sorted:
            prioritysortedkey = lambda col: self.columns_priority[col]
            return sorted(cols, key=prioritysortedkey)
        return cols

    def _check_for_circular_dependency(self, col, col_dependencies):
        # TODO: implement
        pass

    def has_dependencies(self, col):
        return col in self.dependencymap

    def get_dependencies(self, col):
        return self.dependencymap[col]

    def set_function_with_dependency(self, col, func, col_dependencies):
        self._check_for_circular_dependency(col, col_dependencies)
        max_priority = max([self.columns_priority[col_dependency] for col_dependency in col_dependencies])
        priority = max_priority + 1
        self.columns_priority[col] = priority
        self.generators[col] = func
        self.dependencymap[col] = col_dependencies

    def set_generator(self, col, generator, priority=1):
        self.generators[col] = generator
        self.columns_priority[col] = priority

    def get_generator(self, col):
        try:
            return self.generators[col]
        except KeyError:
            raise ColumnNotFoundError('Column: {0} not configured'.format(col))
