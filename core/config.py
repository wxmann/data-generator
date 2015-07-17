import inspect
import functools
from core import repeat, common

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

    def addroot(self, col, func_setting):
        self.all_nodes[col] = func_setting

    def setdependencies(self, col, func_setting, *dependencies):
        if col in self.all_nodes:
            raise CircularDependencyError('Circular dependency found for column: {}'.format(col))
        for parent in dependencies:
            func_setting.priority = max(func_setting.priority, parent.priority + 1)


class FunctionSetting:

    def __init__(self, func, args=None, kwargs=None, dependencies=None, groupmode=None, groupcount=1):
        self.func = func
        self.args = [] if args is None else args
        self.kwargs = {} if kwargs is None else kwargs
        self.dependencies = dependencies
        self.groupmode = groupmode
        self.groupcount = groupcount
        self.priority = 1
        self.isgenerator = inspect.isgeneratorfunction(func)
        # either pre-generated or dynamically generated
        self._data_returner = None

        self._validate_inputs()
        self._preassemble_returner()

    def _validate_inputs(self):
        if self.isgenerator and self.dependencies is not None:
            raise ConfigurationError("Generators cannot be used with anything with dependencies")

    def generatevalue(self, *ext_args, **ext_kwargs):
        # TODO: figure out if this condition is needed
        #    if len(ext_args) + len(ext_kwargs) != len(self.dependencies):
        #     raise ConfigurationError("Number of args provided does not match number of dependencies!")
        # TODO: test dependencies with groups
        if self.groupmode is not None:
            self._data_returner.ext_args = ext_args
            self._data_returner.ext_kwargs = ext_kwargs
        return common.extractvalue(self._data_returner, *ext_args, **ext_kwargs)

    def _preassemble_returner(self):
        if self.isgenerator:
            data_returner = self.func(*self.args, **self.kwargs)
        else:
            data_returner = functools.partial(self.func, *self.args, **self.kwargs)

        if self.groupmode is None:
            self._data_returner = data_returner
        elif self.groupmode == 'single':
            self._data_returner = repeat.repeatsingle(self.groupcount, data_returner)
        elif self.groupmode == 'cluster':
            self._data_returner = repeat.repeatcluster(self.groupcount, data_returner)
        else:
            raise ValueError('Invalid group mode: {0}'.format(self.groupmode))

    def __eq__(self, other):
        if isinstance(other, FunctionSetting):
            return self.func == other.func \
                and self.args == other.args \
                and self.kwargs == other.kwargs \
                and self.dependencies == other.dependencies \
                and self.groupmode == other.groupmode \
                and self.groupcount == other.groupcount \
                and self.priority == other.priority
        else:
            return NotImplemented

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result


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

    def _handle_dependency(self, col, setting):
        dependencies = [self.col_setting_mapping[col_dependency] for col_dependency in setting.dependencies]
        self.dependencies.setdependencies(col, setting, *dependencies)

    def set_funcsetting(self, col, func, args=None, kwargs=None, dependencies=None, groupmode=None, groupcount=1):
        setting_new = FunctionSetting(func, args=args, kwargs=kwargs, dependencies=dependencies, groupmode=groupmode, groupcount=groupcount)
        self.col_setting_mapping[col] = setting_new
        if dependencies is None:
            self.dependencies.addroot(col, setting_new)
        else:
            self._handle_dependency(col, setting_new)

    def get_funcsetting(self, col):
        if col not in self.col_setting_mapping:
            raise ColumnNotFoundError('Column: {0} not configured'.format(col))
        return self.col_setting_mapping[col]