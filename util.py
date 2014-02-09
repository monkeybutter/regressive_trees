__author__ = 'SmartWombat'
from datetime import datetime
import math
import pandas


def circular_distance(ang_a, ang_b):

    return 1-math.cos(ang_a-ang_b)


def yearly_distance(date_a, date_b):
    date_a = datetime(2012, date_a.month, date_a.day, date_a.hour, date_a.minute, date_a.second)
    date_b = datetime(2012, date_b.month, date_b.day, date_b.hour, date_b.minute, date_b.second)

    dist = abs((date_a-date_b).days)

    return min(dist, 366-dist)


def daily_distance(date_a, date_b):
    date_a = datetime(2012, 1, 1, date_a.hour, date_a.minute, date_a.second)
    date_b = datetime(2012, 1, 1, date_b.hour, date_b.minute, date_b.second)

    dist = abs((date_a-date_b).seconds)

    return min(dist, 24*60*60-dist)


def bearing_average(angles_series):
    #input in Degrees [0-360]

    x = y = 0.0
    for angle in angles_series.iteritems():
        x += math.cos(math.pi*angle[1]/180)
        y += math.sin(math.pi*angle[1]/180)

    avg = math.atan2(y, x)*180/math.pi

    if avg < 0.0:
        return 360+avg
    else:
        return avg


def circular_heterogeneity(angles_series):
    #input in Degrees [0-360]

    angular_mean = bearing_average(angles_series)

    distance_sum = 0.0

    for angle in angles_series.iteritems():
        distance_sum += 1 - math.cos(math.pi*angle[1]/180-math.pi*angular_mean/180)

    return distance_sum/angles_series.shape[0]


def sort_in_arc(df, bearing_a, bearing_b, pred_var):
    #

    if bearing_b > bearing_a:
        df= df.sort([pred_var])
        df.index = range(0,len(df))
        return df[(df[pred_var] > bearing_a) & (df[pred_var] < bearing_b)]

    elif bearing_b < bearing_a:
        df= df.sort([pred_var])
        first_part = df[(df[pred_var] > bearing_a) & (df[pred_var] <= 360.0)]
        second_part = df[(df[pred_var] >= 0.0) & (df[pred_var] < bearing_b)]
        df = first_part.append(second_part)
        df.index = range(0,len(df))
        return df

    else:
        raise Exception('This call should not happen!')
