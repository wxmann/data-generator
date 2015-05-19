__author__ = 'tangz'

def generate_vals(config):
    for column in config.columns():
        yield column, config.get_generator(column)()