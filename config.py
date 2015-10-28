import collections

__author__ = 'tangz'


class TabularConfig(object):
    def __init__(self):
        self._map = collections.OrderedDict()

    def setnode(self, column, funcnode):
        self._map[column] = funcnode
        funcnode.set_nodemap(self)

    def columns(self):
        return self._map.keys()

    def nodefor(self, column):
        return self._map[column]

    def resetall(self):
        for col in self._map:
            self._map.get(col).resetstate()


class Dependency(object):
    def __init__(self, column, arg=None):
        self.arg = arg
        self.column = column


class FunctionNode(object):
    def __init__(self, funcwrapper, args=None, kwargs=None, dependencies=None):
        self.funcwrapper = funcwrapper
        self.dependencies = dependencies
        self.col_funcnode_map = None
        self.own_args = [] if args is None else args
        self.own_kwargs = {} if kwargs is None else kwargs
        self._saved_value = None
        self._traversed = False

    def set_nodemap(self, tabularconfig):
        self.col_funcnode_map = tabularconfig

    def resetstate(self):
        self._saved_value = None
        self._traversed = False

    def getvalue(self):
        if not self._traversed:
            if self.dependencies:
                dependencies_kwargs = [kw for kw in self.dependencies if kw.arg is not None]
                new_kwargs = dict(self.own_kwargs)
                new_kwargs.update(self._kwargs_from_dependencies(dependencies_kwargs))

                dependencies_args = [kw for kw in self.dependencies if kw.arg is None]
                new_args = list(self.own_args)
                new_args = new_args + self._args_from_dependencies(dependencies_args)
            else:
                new_kwargs = self.own_kwargs
                new_args = self.own_args
            self._saved_value = self.funcwrapper.eval(*new_args, **new_kwargs)
            self._traversed = True
        return self._saved_value

    def _args_from_dependencies(self, dependencies):
        newargs = []
        if dependencies:  # Non-empty and non-null dependencies
            for dependency in dependencies:
                column = dependency.column
                funcnode = self.col_funcnode_map.nodefor(column)
                newargs.append(funcnode.getvalue())
        return newargs

    def _kwargs_from_dependencies(self, dependencies):
        newkwargs = {}
        if dependencies:  # Non-empty and non-null dependencies
            for dependency in dependencies:
                argname = dependency.arg
                column = dependency.column
                funcnode = self.col_funcnode_map.nodefor(column)
                newkwargs[argname] = funcnode.getvalue()
        return newkwargs