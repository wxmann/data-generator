import datetime
import unittest
from functions import formatters

__author__ = 'tangz'

class FormatterTests(unittest.TestCase):

    def test_rounding_formatter_rounds_float_positive(self):
        x = 31.983252525536530
        frmttr = formatters.nround(2)
        rounded_x = frmttr(x)
        self.assertEqual(str(rounded_x), '31.98')

    def test_rounding_formatter_rounds_float_negative(self):
        x = -31.983252525536530
        frmttr = formatters.nround(2)
        rounded_x = frmttr(x)
        self.assertEqual(str(rounded_x), '-31.98')

    def test_rounding_formatter_rounds_zero(self):
        x = 0.00000123
        frmttr = formatters.nround(2)
        rounded_x = frmttr(x)
        self.assertEqual(str(rounded_x), '0.0')

    def test_round_to_integer(self):
        x = 31.983252525536530
        frmttr = formatters.nround_to_int()
        rounded_x = frmttr(x)
        self.assertEqual(str(rounded_x), '32')

    def test_round_to_integer_midpoint(self):
        x = 31.5
        frmttr = formatters.nround_to_int()
        rounded_x = frmttr(x)
        self.assertEqual(str(rounded_x), '32')

    def test_prepend_to_str(self):
        x = 'Test'
        prefix = 'The-'
        self.assertEqual(formatters.prepend(prefix)(x), 'The-Test')

    def test_postpend_to_str(self):
        x = 'The'
        post = '_Test'
        self.assertEqual(formatters.postpend(post)(x), 'The_Test')

    def test_timeformatter_on_date(self):
        thedate = datetime.date(2015, 9, 24)
        self.assertEqual(formatters.dateformatter('%m/%d/%Y')(thedate), '09/24/2015')
        self.assertEqual(formatters.dateformatter('%b-%d-%y')(thedate), 'Sep-24-15')