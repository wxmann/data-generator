import unittest
from functions import dates

__author__ = 'tangz'

class DatesFunctionTests(unittest.TestCase):

    def test_quarters_iter(self):
        begin_date = "03/30/2015"
        gen = dates.quarters_iter(begin_date)
        self.assertEqual(next(gen), "03/31/2015")
        self.assertEqual(next(gen), "06/30/2015")
        self.assertEqual(next(gen), "09/30/2015")
        self.assertEqual(next(gen), "12/31/2015")
        self.assertEqual(next(gen), "03/31/2016")
        self.assertEqual(next(gen), "06/30/2016")

    def test_quarters_iter_begin_date(self):
        begin_date = "01/22/2015"
        gen = dates.quarters_iter(begin_date, usemonthends=False)
        self.assertEqual(next(gen), "01/01/2015")
        self.assertEqual(next(gen), "04/01/2015")
        self.assertEqual(next(gen), "07/01/2015")
        self.assertEqual(next(gen), "10/01/2015")
        self.assertEqual(next(gen), "01/01/2016")
        self.assertEqual(next(gen), "04/01/2016")

    def test_months_endday_iter(self):
        gen = dates.enddate_iter(3, 2015)
        self.assertEqual(next(gen), "03/31/2015")
        self.assertEqual(next(gen), "04/30/2015")
        self.assertEqual(next(gen), "05/31/2015")
        self.assertEqual(next(gen), "06/30/2015")
        self.assertEqual(next(gen), "07/31/2015")
        self.assertEqual(next(gen), "08/31/2015")
        self.assertEqual(next(gen), "09/30/2015")
        self.assertEqual(next(gen), "10/31/2015")
        self.assertEqual(next(gen), "11/30/2015")
        self.assertEqual(next(gen), "12/31/2015")
        self.assertEqual(next(gen), "01/31/2016")
        self.assertEqual(next(gen), "02/29/2016")

    def test_months_startday_iter(self):
        gen = dates.begindate_iter(3, 2015)
        self.assertEqual(next(gen), "03/01/2015")
        self.assertEqual(next(gen), "04/01/2015")
        self.assertEqual(next(gen), "05/01/2015")
        self.assertEqual(next(gen), "06/01/2015")
        self.assertEqual(next(gen), "07/01/2015")
        self.assertEqual(next(gen), "08/01/2015")
        self.assertEqual(next(gen), "09/01/2015")
        self.assertEqual(next(gen), "10/01/2015")
        self.assertEqual(next(gen), "11/01/2015")
        self.assertEqual(next(gen), "12/01/2015")
        self.assertEqual(next(gen), "01/01/2016")
        self.assertEqual(next(gen), "02/01/2016")