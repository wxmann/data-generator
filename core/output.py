import csv

__author__ = 'tangz'

def to_csv(csvfile, config, n):
    with open(csvfile, 'w', newline='') as opened_file:
        writer = csv.DictWriter(opened_file, config.columns())
        writer.writeheader()
        for i in range(1, n+1):
            row = {col: generated_value for col, generated_value in generate_vals(config)}
            writer.writerow(row)

def generate_vals(config):
    for column in config.columns():
        yield column, next(config.get_generator(column))