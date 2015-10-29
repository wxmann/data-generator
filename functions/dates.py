import calendar
import datetime

__author__ = 'tangz'

JANUARY = 1
FEBRUARY = 2
DECEMBER = 12

def _endday(month, year):
    if month == FEBRUARY and calendar.isleap(year):
        return 29
    return calendar.mdays[month]

def months_iter(startyear, startmonth, month_inc=1, usemonthends=False):
    theyear = startyear
    themonth = startmonth
    while True:
        theday = 1 if usemonthends is False else _endday(themonth, theyear)
        dateobj = datetime.datetime(year=theyear, month=themonth, day=theday)
        yield dateobj
         # calculate the next month
        themonth += month_inc
        if themonth > DECEMBER:
            themonth -= DECEMBER
            theyear += 1

def quarters_iter(startyear, startmonth, usemonthends=False):
    itr = months_iter(startyear, startmonth, month_inc=3, usemonthends=usemonthends)
    while True:
        yield next(itr)
