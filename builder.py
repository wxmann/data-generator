from config import Dependency, FunctionNode, TabularConfig
from wrapper import FunctionWrapper, ClusterRepeater, SingleRepeater, FormatWrapper

__author__ = 'tangz'

REPEATER_SINGLE = 'single'
REPEATER_CLUSTER = 'cluster'


def _to_wrapper(func, repeater=None, formatter=None):
    wrapper = FunctionWrapper(func)
    if formatter is not None:
        wrapper = FormatWrapper(wrapper, formatter)

    if repeater is None:
        return wrapper
    elif repeater.repeatername == REPEATER_SINGLE:
        return SingleRepeater(wrapper, repeater.n)
    elif repeater.repeatername == REPEATER_CLUSTER:
        return ClusterRepeater(wrapper, repeater.n)
    else:
        return wrapper


class _RepeaterRepr(object):
    def __init__(self, repeatername, n):
        if repeatername != REPEATER_CLUSTER and repeatername != REPEATER_SINGLE:
            raise ValueError(
                "Invalid repeater flag: {0}, require {1} or {2}".format(repeatername, REPEATER_SINGLE, REPEATER_CLUSTER))
        self.repeatername = repeatername
        self.n = n


class GlobalSettingBuilder(object):
    def __init__(self, root_builder):
        self.repeater = None
        self.root_builder = root_builder

    def userepeater(self, repeatername, n):
        self.repeater = _RepeaterRepr(repeatername, n)
        return self

    def build(self):
        self.root_builder.globalsetting = GlobalSetting(self.repeater)


class GlobalSetting(object):
    def __init__(self, repeater=None):
        self.repeater = repeater


class ColumnSettingBuilder(object):
    def __init__(self, column, root_builder):
        self.column = column
        self.func = None
        self.args = []
        self.kwargs = {}
        self.dependencies = []
        self.root_builder = root_builder
        self.globalsetting = root_builder.globalsetting
        self.repeater = None if self.globalsetting is None else self.globalsetting.repeater
        self.formatter = None

    def usefunc(self, func):
        self.func = func
        return self

    def useargs(self, *args):
        self.args = args
        return self

    def usekwargs(self, **kwargs):
        self.kwargs = kwargs
        return self

    def add_dependency(self, column_dep):
        self.dependencies.append(Dependency(column_dep))
        return self

    def add_named_dependency(self, column_dep, argname):
        self.dependencies.append(Dependency(column_dep, argname))
        return self

    def norepeater(self):
        self.repeater = None
        return self

    def userepeater(self, repeater_name, n):
        self.repeater = _RepeaterRepr(repeater_name, n)
        return self

    def useformatter(self, formatter):
        self.formatter = formatter
        return self

    def build(self):
        if self.column is None or self.column == "":
            raise ValueError("Column cannot be empty!")
        if self.func is None:
            raise ValueError("Function cannot be empty!")

        self.root_builder.tabularconfig\
            .setnode(self.column,
                     FunctionNode(_to_wrapper(self.func, self.repeater, self.formatter),
                                  self.args, self.kwargs, self.dependencies))


# All config builder must have a globalsetting attribute, otherwise, this breaks above classes which reference
# the attribute.
class ConfigBuilder(object):
    def __init__(self):
        self.tabularconfig = TabularConfig()
        self.globalsetting = None

    def newglobalsetting(self):
        return GlobalSettingBuilder(self)

    def newcolumn(self, column):
        self.columnbuilder_current = ColumnSettingBuilder(column, self)
        return self.columnbuilder_current

    def output_config(self):
        # TODO: some validation with column dependencies.
        # We want to make sure dependency is there.
        return self.tabularconfig


