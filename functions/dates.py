import calendar
import datetime

__author__ = 'tangz'

DEFAULT_DATEFORMAT = '%m/%d/%Y'

JANUARY = 1
FEBRUARY = 2
DECEMBER = 12


def begindate_iter(startmonth, year, month_inc=1, dateformat=DEFAULT_DATEFORMAT):
    theyear = year
    themonth = startmonth
    while True:
        dateobj = datetime.datetime(year=theyear, month=themonth, day=1)
        yield dateobj.strftime(dateformat)
         # calculate the next month
        themonth += month_inc
        if themonth > DECEMBER:
            themonth = JANUARY
            theyear += 1


def enddate_iter(startmonth, year, month_inc=1, dateformat=DEFAULT_DATEFORMAT):
    theyear = year
    themonth = startmonth
    while True:
        dateobj = datetime.datetime(year=theyear, month=themonth, day=_endday(themonth, theyear))
        yield dateobj.strftime(dateformat)
         # calculate the next month
        themonth += month_inc
        if themonth > DECEMBER:
            themonth -= DECEMBER
            theyear += 1


def _endday(month, year):
    if month == FEBRUARY and calendar.isleap(year):
        return 29
    return calendar.mdays[month]


def quarters_iter(startdate=None, usemonthends=True, dateformat=DEFAULT_DATEFORMAT):
    begin_date = datetime.now() if startdate is None else datetime.datetime.strptime(startdate, dateformat).date()
    if usemonthends:
        iter = enddate_iter(begin_date.month, begin_date.year, month_inc=3, dateformat=dateformat)
    else:
        iter = begindate_iter(begin_date.month, begin_date.year, month_inc=3, dateformat=dateformat)
    while True:
        yield next(iter)
