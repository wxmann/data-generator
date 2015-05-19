import csv
import sys
from core import generate

__author__ = 'tangz'

def to_csv(csvfile, config, n):
    with _open_writer_version_dep(csvfile) as opened_file:
        writer = csv.DictWriter(opened_file, config.columns())
        writer.writeheader()
        for i in range(1, n):
            row = {col: value for col, value in generate.generate_vals(config)}
            writer.writerow(row)


def _open_writer_version_dep(file):
    if (sys.version_info > (3, 0)):
        return open(file, 'w', newline='')
    else:
        return open(file, 'wb')