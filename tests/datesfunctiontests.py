import unittest
import datetime
from functions import dates

__author__ = 'tangz'


def _to_date(datestr):
    return datetime.datetime.strptime(datestr, '%m/%d/%Y')


class DatesFunctionTests(unittest.TestCase):

    def test_quarters_iter_end_date(self):
        gen = dates.quarters_iter(startyear=2015, startmonth=3, usemonthends=True)
        self.assertEqual(next(gen), _to_date("03/31/2015"))
        self.assertEqual(next(gen), _to_date("06/30/2015"))
        self.assertEqual(next(gen), _to_date("09/30/2015"))
        self.assertEqual(next(gen), _to_date("12/31/2015"))
        self.assertEqual(next(gen), _to_date("03/31/2016"))
        self.assertEqual(next(gen), _to_date("06/30/2016"))

    def test_quarters_iter_begin_date(self):
        gen = dates.quarters_iter(startyear=2015, startmonth=1, usemonthends=False)
        self.assertEqual(next(gen), _to_date("01/01/2015"))
        self.assertEqual(next(gen), _to_date("04/01/2015"))
        self.assertEqual(next(gen), _to_date("07/01/2015"))
        self.assertEqual(next(gen), _to_date("10/01/2015"))
        self.assertEqual(next(gen), _to_date("01/01/2016"))
        self.assertEqual(next(gen), _to_date("04/01/2016"))

    def test_months_endday_iter(self):
        gen = dates.months_iter(startyear=2015, startmonth=3, usemonthends=True)
        self.assertEqual(next(gen), _to_date("03/31/2015"))
        self.assertEqual(next(gen), _to_date("04/30/2015"))
        self.assertEqual(next(gen), _to_date("05/31/2015"))
        self.assertEqual(next(gen), _to_date("06/30/2015"))
        self.assertEqual(next(gen), _to_date("07/31/2015"))
        self.assertEqual(next(gen), _to_date("08/31/2015"))
        self.assertEqual(next(gen), _to_date("09/30/2015"))
        self.assertEqual(next(gen), _to_date("10/31/2015"))
        self.assertEqual(next(gen), _to_date("11/30/2015"))
        self.assertEqual(next(gen), _to_date("12/31/2015"))
        self.assertEqual(next(gen), _to_date("01/31/2016"))
        self.assertEqual(next(gen), _to_date("02/29/2016"))

    def test_months_startday_iter(self):
        gen = dates.months_iter(startyear=2015, startmonth=3, usemonthends=False)
        self.assertEqual(next(gen), _to_date("03/01/2015"))
        self.assertEqual(next(gen), _to_date("04/01/2015"))
        self.assertEqual(next(gen), _to_date("05/01/2015"))
        self.assertEqual(next(gen), _to_date("06/01/2015"))
        self.assertEqual(next(gen), _to_date("07/01/2015"))
        self.assertEqual(next(gen), _to_date("08/01/2015"))
        self.assertEqual(next(gen), _to_date("09/01/2015"))
        self.assertEqual(next(gen), _to_date("10/01/2015"))
        self.assertEqual(next(gen), _to_date("11/01/2015"))
        self.assertEqual(next(gen), _to_date("12/01/2015"))
        self.assertEqual(next(gen), _to_date("01/01/2016"))
        self.assertEqual(next(gen), _to_date("02/01/2016"))