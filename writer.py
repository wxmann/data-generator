import csv
from parse import xmlparse

__author__ = 'tangz'

def write_csv(file, config, n):
    thewriter = CSVWriter(config)
    thewriter.write(file, n)


def write_csv_from_xml_config(file_out, xmlconfig_in, n):
    tabularconfig = xmlparse.parsexml(xmlconfig_in)
    writer = CSVWriter(tabularconfig)
    writer.write(file_out, n)


class CSVWriter(object):
    def __init__(self, tabularconfig):
        self.tabularconfig = tabularconfig

    def write(self, file, n):
        columns = self.tabularconfig.columns()
        with open(file, 'w', newline='') as opened_file:
            writer = csv.DictWriter(opened_file, columns)
            writer.writeheader()
            for i in range(n):
                row = {column: self.tabularconfig.get(column).getvalue() for column in columns}
                self.tabularconfig.resetall()
                writer.writerow(row)

