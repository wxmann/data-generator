import inspect
import functools

__author__ = 'tangz'


class ColumnNotFoundError(Exception):
    pass


class CircularDependencyError(Exception):
    pass


class ConfigurationError(Exception):
    pass


class _DependencyTracker:

    def __init__(self):
        self.all_nodes = {}

    def addroot(self, func_setting):
        self.all_nodes[func_setting.column] = func_setting

    def setdependencies(self, func_setting, *dependencies):
        if func_setting.column in self.all_nodes:
            raise CircularDependencyError('Circular dependency found for column: {}'.format(func_setting.column))
        for parent in dependencies:
            func_setting.priority = max(func_setting.priority, parent.priority + 1)


class FunctionSetting:

    def __init__(self, column, func, dependencies, *args, **kwargs):
        self.column = column
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.dependencies = dependencies
        self.priority = 1
        self.isgenerator = inspect.isgeneratorfunction(func)
        # either pre-generated or dynamically generated
        self._data_returner = None

        self._validate_inputs()
        self._preassemble_returner()

    def _validate_inputs(self):
        if self.isgenerator and self.dependencies is not None:
            raise ConfigurationError("Generators cannot be used with anything with dependencies")

    def generatevalue(self):
        if self.isgenerator:
            return next(self._data_returner)
        else:
            return self._data_returner()

    def set_dependentargs(self, *ext_args, **ext_kwargs):
        if self.dependencies is not None:
            if len(ext_args) + len(ext_kwargs) != len(self.dependencies):
                raise ConfigurationError("Number of args provided does not match number of dependencies!")
            self._data_returner = functools.partial(self.func, *ext_args, **ext_kwargs)

    def _preassemble_returner(self):
        if self.dependencies is None:
            if self.isgenerator:
                self.data_returner = self.func(*self.args, **self.kwargs)
            else:
                self.data_returner = functools.partial(self.func, *self.args, **self.kwargs)


class TabularConfig:

    def __init__(self):
        self.col_setting_mapping = {}
        self.dependencies = _DependencyTracker()

    def columns(self, priority_sorted=True):
        cols = self.col_setting_mapping.keys()
        if priority_sorted:
            prioritysortedkey = lambda col: self.col_setting_mapping[col].priority
            return sorted(cols, key=prioritysortedkey)
        return cols

    def _handle_dependency(self, setting_new):
        parentnodes = [self.col_setting_mapping[col_dependency] for col_dependency in setting_new.dependencies]
        self.dependencies.setdependencies(setting_new, parentnodes)

    def set_funcsetting(self, col, func, dependencies=None, *args, **kwargs):
        setting_new = FunctionSetting(col, func, dependencies, *args, **kwargs)
        self.col_setting_mapping[col] = setting_new
        if dependencies is None:
            self.dependencies.addroot(setting_new)
        else:
            self._handle_dependency(setting_new)

    def get_funcsetting(self, col):
        if col not in self.col_setting_mapping:
            raise ColumnNotFoundError('Column: {0} not configured'.format(col))
        return self.col_setting_mapping[col]