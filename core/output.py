import csv
import inspect

__author__ = 'tangz'

def to_csv(csvfile, config, n):
    with open(csvfile, 'w', newline='') as opened_file:
        writer = csv.DictWriter(opened_file, config.columns(priority_sorted=False))
        writer.writeheader()
        rowdata = RowGenerator(config)
        for i in range(n):
            rowdata.generate_row()
            writer.writerow(rowdata.output())


class DependentValueNotGeneratedError(Exception):
    pass


class RowGenerator:

    def __init__(self, generatorconfig):
        self.data = {}
        self.generatorconfig = generatorconfig

    def output(self):
        rowtoreturn = self.data
        self.data = {}
        return rowtoreturn

    def _generated_value(self, col):
        if col in self.data:
            return self.data[col]
        else:
            raise DependentValueNotGeneratedError("Column: {0} doesn't have a generated value yet.".format(col))

    def _generate_value_with_dependencies(self, funcnode):
        col_dependencies = funcnode.dependencies
        args = [self._generated_value(col_dependency) for col_dependency in col_dependencies]
        funcnode.set_dependentvalues(*args)
        return funcnode.nextvalue()

    def generate_row(self):
        columns = self.generatorconfig.columns()
        for col in columns:
            funcnode = self.generatorconfig.get_funcnode(col)
            if funcnode.dependencies is not None:
                self.data[funcnode.column] = self._generate_value_with_dependencies(funcnode)
            else:
                self.data[funcnode.column] = funcnode.nextvalue()


