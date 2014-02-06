__author__ = 'SmartWombat'

import numpy as np


def best_numeric_splitter(df, class_var, pred_var):

    # Drop NaNs and order under pred_var values
    df = df[np.isfinite(df[class_var])]
    df = df[np.isfinite(df[pred_var])]
    df = df.sort([pred_var])
    df.index = range(0,len(df))
    #print(df.shape)

    total_cases = df.shape[0]
    y_sum = np.sum(df[class_var])

    right_cases = total_cases
    right_sum = y_sum
    left_cases = 0
    left_sum = 0

    best_till_now = 0
    best_cut_point = None

    for index, row in df.iterrows():

        left_cases += 1
        left_sum += row[class_var]
        right_cases -=1
        right_sum -= row[class_var]

        # TODO REVIEW this -1
        if index < total_cases-1:
            next_pred_value = df[pred_var][index+1]
        else:
            next_pred_value = row[pred_var]

        if next_pred_value > row[pred_var]:
            new_split_value = (left_sum*left_sum/left_cases) + (right_sum*right_sum/right_cases)
            if new_split_value > best_till_now:
                best_till_now = new_split_value
                best_cut_point = (next_pred_value + row[pred_var])/2
                left_df = df[:index]
                right_df = df[index:]

    return best_cut_point, best_till_now, left_df, right_df


def best_general_splitter(df, class_var, pred_var, measure):

    measure_inst = measureFactory(measure)
    # Drop NaNs and order under pred_var values
    df = df[np.isfinite(df[class_var])]
    df = df[np.isfinite(df[pred_var])]
    df = df.sort([pred_var])
    df.index = range(0,len(df))

    left = []
    right = [df[:]]

    total_cases = df.shape[0]
    y_sum = np.sum(df[class_var])

    right_cases = total_cases
    right_sum = y_sum
    left_cases = 0
    left_sum = 0

    best_till_now =
    best_cut_point = 0

    for value in right:

        left_cases += 1
        left_sum += row[class_var]
        right_cases -=1
        right_sum -= row[class_var]

        # TODO REVIEW this -1
        if index < total_cases-1:
            next_pred_value = df[pred_var][index+1]
        else:
            next_pred_value = row[pred_var]

        if next_pred_value > row[pred_var]:
            new_split_value = (left_sum*left_sum/left_cases) + (right_sum*right_sum/right_cases)
            if new_split_value > best_till_now:
                best_till_now = new_split_value
                best_cut_point = (next_pred_value + row[pred_var])/2
                left_df = df[:index]
                right_df = df[index:]

    return best_cut_point, best_till_now, left_df, right_df