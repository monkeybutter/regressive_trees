__author__ = 'SmartWombat'

from util import time_to_angle, date_to_angle, contained_in_arc
from math import sqrt
from datetime import datetime


def evaluate_dataset(class_var, tree, df):
    acum_sq_error = 0
    total_values = df.shape[0]
    for index, row in df.iterrows():
        real_val = row[class_var]
        pred_val = _evaluate_value(tree, row)
        acum_sq_error += (real_val - pred_val)**2
    return sqrt(acum_sq_error/total_values)


def _evaluate_value(tree, data_row):
    if tree.get_name() == 'Node':
        if tree.var_type == 'linear':
            if data_row[tree.split_var] < tree.split_values[1]:
                return _evaluate_value(tree.left_child, data_row)
            else:
                return _evaluate_value(tree.right_child, data_row)

        elif tree.var_type == 'circular':
            if contained_in_arc(tree.split_values[0], tree.split_values[1], data_row[tree.split_var]):
                return _evaluate_value(tree.left_child, data_row)
            elif contained_in_arc(tree.split_values[2], tree.split_values[3], data_row[tree.split_var]):
                return _evaluate_value(tree.right_child, data_row)
            else:
                raise Exception

        elif tree.var_type == 'date':
            value = date_to_angle(datetime.strptime(data_row[tree.split_var], "%Y-%m-%d").date())
            if contained_in_arc(tree.split_values[0], tree.split_values[1], value):
                return _evaluate_value(tree.left_child, data_row)
            elif contained_in_arc(tree.split_values[2], tree.split_values[3], value):
                return _evaluate_value(tree.right_child, data_row)
            else:
                raise Exception

        elif tree.var_type == 'time':
            value = time_to_angle(datetime.strptime(data_row[tree.split_var], "%H:%M").time())
            if contained_in_arc(tree.split_values[0], tree.split_values[1], value):
                return _evaluate_value(tree.left_child, data_row)
            elif contained_in_arc(tree.split_values[2], tree.split_values[3], value):
                return _evaluate_value(tree.right_child, data_row)
            else:
                raise Exception

        else:
            raise Exception

    if tree.get_name() == 'Leaf':
        return tree.value