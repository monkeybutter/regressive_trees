__author__ = 'SmartWombat'
from datetime import datetime
import math


def circular_distance(ang_a, ang_b):

    return 1-math.cos(ang_a-ang_b)


def yearly_distance(date_a, date_b):
    date_a = datetime(2012, date_a.month, date_a.day, date_a.hour, date_a.minute, date_a.second)
    date_b = datetime(2012, date_b.month, date_b.day, date_b.hour, date_b.minute, date_b.second)

    dist = abs((date_a-date_b).days)

    return min(dist, 366-dist)


def dayly_distance(date_a, date_b):
    date_a = datetime(2012, 1, 1, date_a.hour, date_a.minute, date_a.second)
    date_b = datetime(2012, 1, 1, date_b.hour, date_b.minute, date_b.second)

    dist = abs((date_a-date_b).seconds)

    return min(dist, 24*60*60-dist)