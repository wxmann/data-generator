import csv

__author__ = 'tangz'

def to_csv(csvfile, config, n):
    with open(csvfile, 'w', newline='') as opened_file:
        writer = csv.DictWriter(opened_file, config.columns(priority_sorted=False))
        writer.writeheader()
        rowdata = RowGenerator(config)
        for i in range(1, n+1):
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
        try:
            return self.data[col]
        except KeyError:
            raise DependentValueNotGeneratedError("Column: {0} doesn't have a generated value yet.".format(col))

    def _generate_value_with_dependencies(self, funcforcol, col_dependencies):
        args = (self._generated_value(col_dependency) for col_dependency in col_dependencies)
        return funcforcol(*args)

    def generate_row(self):
        columns = self.generatorconfig.columns()
        for col in columns:
            genforcol = self.generatorconfig.get_generator(col)
            if self.generatorconfig.has_dependencies(col):
                funcforcol = genforcol
                self.data[col] = self._generate_value_with_dependencies(funcforcol, self.generatorconfig.get_dependencies(col))
            else:
                self.data[col] = next(genforcol)


