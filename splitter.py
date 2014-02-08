__author__ = 'SmartWombat'

import numpy as np
from criteria_factory import CriteriaFactory
from util import *


def linear_generic_splitter(df, class_var, pred_var):

    criteria = CriteriaFactory('circular_regression')

    # Drop NaNs and order under pred_var values
    df = df[np.isfinite(df[class_var])]
    df = df[np.isfinite(df[pred_var])]
    df = df.sort([pred_var])
    df.index = range(0,len(df))

    total_cases = df.shape[0]

    best_till_now = 0
    best_cut_point = None
    best_index = None

    for index in range(1, df.shape[0]):

    #for index, row in df.iterrows():

        left_df = df[:index]
        right_df = df[index:]

        if index < total_cases-1:
            next_pred_value = df[pred_var][index+1]
        else:
            next_pred_value = df[pred_var][index]

        if next_pred_value != df[pred_var][index]:
            new_split_value = criteria.get_value(left_df, right_df, class_var)
            print(new_split_value)
            if new_split_value > best_till_now:
                best_till_now = new_split_value
                best_cut_point = (next_pred_value + df[pred_var][index])/2
                best_index = index

    return best_cut_point, best_till_now, df[:best_index], df[best_index:]


def circular_generic_splitter(df, bearing_a, bearing_b, class_var, pred_var):
    #input in Degrees [0-360]
    #as two bearings can define two arcs depending on the clockwise or anti-clockwise direction
    #we assume the convention that the arc is defined going from bearing_a to bearing_b clockwise


    criteria = CriteriaFactory('basic_regression')
    #class_var is linear
    #pred_var is circular

    # Drop NaNs and order under pred_var values
    df = df[np.isfinite(df[class_var])]
    df = df[np.isfinite(df[pred_var])]

    if bearing_a == bearing_b:
        #This is the first call to the circular splitter
        #We need to check every split!
        df = df.sort([pred_var])
        df.index = range(0,len(df))
        pass

    else:
        best_till_now = 0
        best_cut_point = None
        best_index = None
        df = sort_in_arc(df, bearing_a, bearing_b, pred_var)
        total_cases = df.shape[0]
        for index in range(1, total_cases):
            left_df = df[:index]
            right_df = df[index:]
            if index < total_cases-1:
                next_pred_value = df[pred_var][index+1]
            else:
                next_pred_value = df[pred_var][index]

            if next_pred_value != df[pred_var][index]:
                new_split_value = criteria.get_value(left_df, right_df, class_var)
                if new_split_value > best_till_now:
                    best_till_now = new_split_value
                    best_cut_point = (next_pred_value + df[pred_var][index])/2
                    best_index = index

    return best_cut_point, best_till_now, df[:best_index], df[best_index:]