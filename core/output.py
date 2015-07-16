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

    def _generate_value_with_dependencies(self, funcsetting):
        col_dependencies = funcsetting.dependencies
        args = [self._generated_value(col_dependency) for col_dependency in col_dependencies]
        return funcsetting.generatevalue(*args)

    def generate_row(self):
        columns = self.generatorconfig.columns()
        for col in columns:
            funcsetting = self.generatorconfig.get_funcsetting(col)
            if funcsetting.dependencies is not None:
                self.data[col] = self._generate_value_with_dependencies(funcsetting)
            else:
                self.data[col] = funcsetting.generatevalue()