__author__ = 'SmartWombat'

import numpy as np
from criteria_factory import CriteriaFactory


def linear_generic_splitter(df, class_var, pred_var):

    criteria = CriteriaFactory('basic_regression')

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

        if next_pred_value > df[pred_var][index]:
            new_split_value = criteria.get_value(left_df, right_df, class_var)
            if new_split_value > best_till_now:
                best_till_now = new_split_value
                best_cut_point = (next_pred_value + df[pred_var][index])/2
                best_index = index

    return best_cut_point, best_till_now, df[:best_index], df[best_index:]