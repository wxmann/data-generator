import inspect
import functools

__author__ = 'tangz'


class ColumnNotFoundError(Exception):
    pass


class CircularDependencyError(Exception):
    pass


class ConfigurationError(Exception):
    pass

# TODO: rename to dependency tracker
class DependencyForest:

    def __init__(self):
        self.all_nodes = {}

    def addroot(self, node):
        self.all_nodes[node.column] = node

    def setparents(self, node, *parents):
        if node.column in self.all_nodes:
            raise CircularDependencyError('Circular dependency found for column: {}'.format(node.column))
        for parent in parents:
            node.priority = max(node.priority, parent.priority + 1)

# TODO: rename to column-configuration
class FunctionNode:

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

    def nextvalue(self):
        if self.isgenerator:
            return next(self._data_returner)
        else:
            return self._data_returner()

    def set_dependentvalues(self, *ext_args, **ext_kwargs):
        if self.dependencies is not None:
            if len(ext_args) + len(ext_kwargs) != len(self.dependencies):
                raise ConfigurationError("Number of args provided does not match number of dependencies!")
            self._data_returner = functools.partial(self.func, *self.args, **self.kwargs)

    def _preassemble_returner(self):
        if self.dependencies is None:
            if self.isgenerator:
                self.data_returner = self.func(*self.args, **self.kwargs)
            else:
                self.data_returner = functools.partial(self.func, *self.args, **self.kwargs)


class TabularConfig:

    def __init__(self):
        self.column_node_mapping = {}
        self.dependencies = DependencyForest()

    # TODO: rename to sorted-columns
    def columns(self, priority_sorted=True):
        cols = self.column_node_mapping.keys()
        if priority_sorted:
            prioritysortedkey = lambda col: self.column_node_mapping[col].priority
            return sorted(cols, key=prioritysortedkey)
        return cols

    # def has_dependencies(self, col):
    #     if col in self.column_node_mapping:
    #         return len(self.column_node_mapping[col].dependencies) > 0
    #     return False

    # def get_dependencies(self, col):
    #     if col not in self.column_node_mapping:
    #         raise ColumnNotFoundError('Column: {0} not configured'.format(col))
    #     return self.column_node_mapping[col].dependencies

    def _handle_dependency(self, node_new):
        parentnodes = [self.column_node_mapping[col_dependency] for col_dependency in node_new.dependencies]
        self.dependencies.setparents(node_new, parentnodes)

    def set_funcnode(self, col, func, dependencies=None, *args, **kwargs):
        node_new = FunctionNode(col, func, dependencies, *args, **kwargs)
        self.column_node_mapping[col] = node_new
        if dependencies is None:
            self.dependencies.addroot(node_new)
        else:
            self._handle_dependency(node_new)

    def get_funcnode(self, col):
        if col not in self.column_node_mapping:
            raise ColumnNotFoundError('Column: {0} not configured'.format(col))
        return self.column_node_mapping[col]

