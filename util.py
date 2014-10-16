__author__ = 'SmartWombat'
from datetime import datetime
import pandas as pd
import math
import random
import copy
from datetime import date, time, timedelta
import calendar
import numpy as np


def cross_validate_splits(df, groups):

    dataframes = []

    group_size = int(round(df.shape[0]*.2))

    for i in range(groups-1):
        rows = random.sample(df.index, group_size)
        dataframes.append(df.ix[rows])
        df = df.drop(rows)

    dataframes.append(df)

    return dataframes


def cross_validate_group(test_group_pos, dataframes):
    dataframes_copy = copy.deepcopy(dataframes)

    if 0 < test_group_pos <= len(dataframes):

        test_df = dataframes_copy[test_group_pos-1]
        del dataframes_copy[test_group_pos-1]
        train_df = pd.concat(dataframes_copy)

        return train_df, test_df

    else:
        raise Exception('Group not in range!')


def evaluate_rmse(tree, ):
    data = Data(train_df, class_var, df_types, True)


"""
def circular_distance(ang_a, ang_b):

    return 1-math.cos(ang_a-ang_b)

"""
def mid_angle(ang_a, ang_b):
    #input in Degrees [0-360]

    if ang_b >= ang_a:
        return ang_a + (ang_b - ang_a)/2.0

    else:
        return (ang_a + ((360-ang_a) + ang_b)/2.0) % 360


def _bearing_average_in_arc(data, var_name):
    #input in Degrees [0-360]

    avg = _bearing_average(data.df, var_name)

    return avg


def _bearing_average(df, pred_var):
    #input in Degrees [0-360]

    x = y = 0.0
    for index, row in df.iterrows():
        x += math.cos(math.pi*row[pred_var]/180)
        y += math.sin(math.pi*row[pred_var]/180)

    avg = math.atan2(y, x)*180/math.pi

    if avg < 0.0:
        return 360+avg

    else:
        return avg

# Very cool function to calculate angular distance
def angular_distance(a, b):
    return (a-b) % 360 if (a-b) % 360 < 180 else 360 - (a-b) % 360


def circular_mean(data):

    x = np.sum(np.cos(np.radians(data.df[data.class_var])))
    y = np.sum(np.sin(np.radians(data.df[data.class_var])))

    value = math.degrees(math.atan2(y, x)) % 360

    if contained_in_arc(data.var_limits[data.class_var]['start'], data.var_limits[data.class_var]['start'], value):
        return value
    else:
        return math.degrees(math.atan2(y, x) + math.pi) % 360

def circular_mean2(data):

    x = np.sum(np.cos(np.radians(data.df[data.class_var])))
    y = np.sum(np.sin(np.radians(data.df[data.class_var])))

    return math.degrees(math.atan2(y, x)) % 360



def circular_variance(data):

    x = np.sum(np.cos(np.radians(data.df[data.class_var])))
    y = np.sum(np.sin(np.radians(data.df[data.class_var])))

    return 1 - math.sqrt(math.pow(x/data.df.shape[0], 2) + math.pow(y/data.df.shape[0], 2))


def circular_heterogeneity(data):
    #input in Degrees [0-360]

    #print('inside heterogeneity {}'.format(angles_series))

    if data != None:
        angular_mean = _bearing_average_in_arc(data, data.class_var)
        #print('angular mean {}'.format(angular_mean))

        distance_sum = 0.0

        for index, row in data.df.iterrows():
            distance_sum += 1 - math.cos(math.pi*row[data.class_var]/180-math.pi*angular_mean/180)

        return distance_sum/data.df.shape[0]

    else:
        return 0.0


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


def contained_in_arc(bearing_a, bearing_b, value):
    if bearing_a < bearing_b:
        if bearing_b >= value >= bearing_a:
            return True
        else:
            return False
    else:
        if (360 >= value > bearing_a) or (bearing_b > value >= 0):
            return True
        else:
            return False

def angle_to_date(angle):
    _date = timedelta(seconds=365 * 86400.0 * angle / 360.0)
    first_day = datetime(2012, 1, 1, 0, 0)
    return (first_day + _date).date()


def date_to_angle(a_date):
    # Limit time values to 36
    if calendar.isleap(a_date.year):
        #return 360.0*(a_date.timetuple().tm_yday-1)/366.0
        return 10*int(a_date.timetuple().tm_yday/10.0)

    else:
        #return 360.0*(a_date.timetuple().tm_yday-1)/365.0
        return 10*int(a_date.timetuple().tm_yday/10.0)



def angle_to_time(angle):

    _time = timedelta(seconds=86400.0 * angle / 360.0)
    first_day = datetime(2012, 1, 1, 0, 0)
    return (first_day + _time).time()


def time_to_angle(a_time):

    #return 360.0*(a_time.hour*3600+a_time.minute*60+a_time.second)/86400.0
    # Limit time values to 24
    return 360.0*a_time.hour/24.0