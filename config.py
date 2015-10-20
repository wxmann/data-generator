__author__ = 'tangz'


class TabularConfig(object):
    def __init__(self):
        self._map = {}

    def set(self, column, funcnode):
        self._map[column] = funcnode
        funcnode.set_nodemap(self)

    def get(self, column):
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
        self.saved_value = None

    def set_nodemap(self, tabularconfig):
        self.col_funcnode_map = tabularconfig

    def resetstate(self):
        self.saved_value = None

    def getvalue(self):
        if self.saved_value is not None:
            return self.saved_value

        if self.dependencies is not None:
            dependencies_kwargs = [kw for kw in self.dependencies if kw.arg is not None]
            new_kwargs = dict(self.own_kwargs)
            new_kwargs.update(self._kwargs_from_dependencies(dependencies_kwargs))

            dependencies_args = [kw for kw in self.dependencies if kw.arg is None]
            new_args = list(self.own_args)
            new_args = new_args + self._args_from_dependencies(dependencies_args)
        else:
            new_kwargs = self.own_kwargs
            new_args = self.own_args

        return self.funcwrapper.get(*new_args, **new_kwargs)

    def _args_from_dependencies(self, dependencies):
        newargs = []
        if dependencies: # Non-empty and non-null dependencies
            for dependency in dependencies:
                column = dependency.column
                funcnode = self.col_funcnode_map.get(column)
                newargs.append(funcnode.getvalue())
        return newargs


    def _kwargs_from_dependencies(self, dependencies):
        newkwargs = {}
        if dependencies: # Non-empty and non-null dependencies
            for dependency in dependencies:
                argname = dependency.arg
                column = dependency.column
                funcnode = self.col_funcnode_map.get(column)
                newkwargs[argname] = funcnode.getvalue()
        return newkwargs