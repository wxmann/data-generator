import calendar
import datetime

__author__ = 'tangz'

JANUARY = 1
FEBRUARY = 2
DECEMBER = 12


def begindate_iter(startmonth, year, month_inc=1):
    theyear = year
    themonth = startmonth
    while True:
        dateobj = datetime.datetime(year=theyear, month=themonth, day=1)
        yield dateobj
         # calculate the next month
        themonth += month_inc
        if themonth > DECEMBER:
            themonth = JANUARY
            theyear += 1


def enddate_iter(startmonth, year, month_inc=1):
    theyear = year
    themonth = startmonth
    while True:
        dateobj = datetime.datetime(year=theyear, month=themonth, day=_endday(themonth, theyear))
        yield dateobj
         # calculate the next month
        themonth += month_inc
        if themonth > DECEMBER:
            themonth -= DECEMBER
            theyear += 1


def _endday(month, year):
    if month == FEBRUARY and calendar.isleap(year):
        return 29
    return calendar.mdays[month]


def quarters_iter(startyear, startmonth, usemonthends=True):
    if usemonthends:
        itr = enddate_iter(startmonth, startyear, month_inc=3)
    else:
        itr = begindate_iter(startmonth, startyear, month_inc=3)
    while True:
        yield next(itr)
