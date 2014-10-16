__author__ = 'SmartWombat'

from util import time_to_angle, date_to_angle, contained_in_arc, angular_distance
from math import sqrt
from datetime import datetime


def evaluate_dataset_rmse(class_var, type, tree, df):

    if type == 'linear':
        acum_sq_error = 0
        total_values = df.shape[0]
        for index, row in df.iterrows():
            real_val = row[class_var]
            pred_val = _evaluate_value(tree, row)
            acum_sq_error += (pred_val - real_val)**2
        return sqrt(acum_sq_error/total_values)

    elif type == 'circular':
        acum_sq_error = 0
        total_values = df.shape[0]
        for index, row in df.iterrows():
            real_val = row[class_var]
            pred_val = _evaluate_value(tree, row)
            acum_sq_error += angular_distance(pred_val, real_val)**2
        return sqrt(acum_sq_error/total_values)

def evaluate_dataset_mae(class_var, tree, df):
    acum_error = 0
    total_values = df.shape[0]
    for index, row in df.iterrows():
        real_val = row[class_var]
        pred_val = _evaluate_value(tree, row)
        acum_error += (pred_val - real_val)
    return acum_error/total_values

# Error: metar - tree(gfs)
def evaluate_dataset_raw(class_var, tree, df):
    result = []
    for index, row in df.iterrows():
        result.append(row[class_var] - _evaluate_value(tree, row))
    return result

# Error: metar - gfs
def evaluate_dataset_raw_no_tree(class_var, gfs_var, df):
    result = []
    for index, row in df.iterrows():
        result.append(row[class_var] - row[gfs_var])
    return result


# detail metar - gfs
def detail_evaluate_dataset(gfs_var, class_var, tree, df):
    result = []
    for index, row in df.iterrows():
        element = {}
        element[gfs_var] = row[gfs_var]
        element[class_var] = row[class_var]
        element['ctree'] = _evaluate_value(tree, row)
        result.append(element)
    return result

# detail metar - gfs
def detail_evaluate_dataset_rf(gfs_var, class_var, rf, df):
    result = []
    for index, row in df.iterrows():
        element = {}
        element[gfs_var] = row[gfs_var]
        element[class_var] = row[class_var]
        tree_values = []
        for tree in rf:
            tree_values.append(_evaluate_value(tree, row))
        tree_values.sort()
        tree_values = tree_values[10:40]
        element['rf'] = sum(tree_values)/len(tree_values)
        result.append(element)
    return result

# detail metar - gfs
def detail_evaluate_dataset_rf_tree(gfs_var, class_var, rf, tree, df):
    result = []
    for index, row in df.iterrows():
        element = {}
        element[gfs_var] = row[gfs_var]
        element[class_var] = row[class_var]
        tree_values = []
        for tree in rf:
            tree_values.append(_evaluate_value(tree, row))
        tree_values.sort()
        tree_values = tree_values[10:40]
        element['rf'] = sum(tree_values)/len(tree_values)
        element['single_tree'] = _evaluate_value(tree, row)
        result.append(element)
    return result


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
            #print("split_var: " + tree.split_var)
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