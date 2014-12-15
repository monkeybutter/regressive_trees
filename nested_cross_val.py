from __future__ import division
import numpy as np
import copy
import pandas as pd
import math


class Data(object):
    __class_description__ = """Abstract class for a binary tree data container"""
    __version__ = 0.1

    def __init__(self, df, class_var, var_types, var_limits={}):

        self.df = copy.deepcopy(df)
        self.class_var = class_var
        self.var_types = var_types
        self.var_limits = var_limits

        if var_limits == {}:
            for var_name in [name for name in self.df.columns if name != class_var]:
                self.var_limits[var_name] = (float("-inf"), float("inf"))


def circular_criteria(master_data, split_var):
    data = copy.deepcopy(master_data)

    if data.var_limits[split_var] == (float("-inf"), float("inf")):

        def min_indices(list_of_lists):
            return min((value, (i, j)) for i, inner_list in enumerate(list_of_lists) for j, value in enumerate(inner_list))

        data.df = data.df.sort([split_var])
        values, indices = np.unique(data.df[split_var], return_index=True)

        # scores_prime = [(idx/data.df.shape[0] * np.var(data.df[data.class_var].iloc[:idx])) + ((data.df.shape[0]-idx)/data.df.shape[0] * np.var(data.df[data.class_var].iloc[idx:])) for idx in indices[1:]]

        index_lists = [sorted(
            [indice2 - indice if indice2 - indice >= 0 else indice2 - indice + data.df.shape[0] for indice2 in indices])
                       for indice in indices]
        dfs = [copy.deepcopy(data.df).iloc[index:].append(copy.deepcopy(data.df).iloc[:index]) for index in indices]

        score, min_index = min_indices([[(idx / data.df.shape[0] * np.var(dfs[index][data.class_var].iloc[:idx])) + (
            (data.df.shape[0] - idx) / data.df.shape[0] * np.var(dfs[index][data.class_var].iloc[idx:]))
                               for idx in index_list[1:]] for (index, index_list) in enumerate(index_lists)])

        return_df_uncut = dfs[min_index[0]]
        return_indexes_uncut = index_lists[min_index[0]]

        left_data = Data(dfs[min_index[0]].iloc[:return_indexes_uncut[min_index[1] + 1]], copy.deepcopy(data.class_var),
                         copy.deepcopy(data.var_types), copy.deepcopy(data.var_limits))
        right_data = Data(dfs[min_index[0]].iloc[return_indexes_uncut[min_index[1] + 1]:], copy.deepcopy(data.class_var),
                          copy.deepcopy(data.var_types), copy.deepcopy(data.var_limits))

        left_data.var_limits[split_var] = (dfs[min_index[0]][split_var].iloc[0],
                                           dfs[min_index[0]][split_var].iloc[index_lists[min_index[0]][min_index[1] + 1]])
        right_data.var_limits[split_var] = (dfs[min_index[0]][split_var].iloc[index_lists[min_index[0]][min_index[1] + 1]],
                                            dfs[min_index[0]][split_var].iloc[0])

        return score, left_data, right_data

    else:

        data.df = data.df.sort([split_var])
        # If dataset crosses origin, it has to be reordered
        if data.var_limits[split_var][1] < data.var_limits[split_var][0]:
            data.df = copy.deepcopy(
                data.df[(data.df[split_var] >= data.var_limits[split_var][0]) & (data.df[split_var] <= 360)]).append(
                copy.deepcopy(
                    data.df[(data.df[split_var] >= 0) & (data.df[split_var] <= data.var_limits[split_var][1])]))

        return splitter(data, split_var)


def linear_criteria(master_data, split_var):
    data = copy.deepcopy(master_data)
    data.df = data.df.sort([split_var])

    return splitter(data, split_var)


def splitter(data, split_var):
    values, indices = np.unique(data.df[split_var], return_index=True)

     # In case indices are not ordered we need to sort both to leave 0 index at position 0
    values = [val for (ind, val) in sorted(zip(indices, values))]
    indices = sorted(indices)

    if len(indices) == 1:
        return float("inf"), None, None

    scores = [(idx / data.df.shape[0] * np.var(data.df[data.class_var].iloc[:idx])) + (
        (data.df.shape[0] - idx) / data.df.shape[0] * np.var(data.df[data.class_var].iloc[idx:])) for idx in indices[1:]]

    left_data = Data(copy.deepcopy(data.df.iloc[:indices[np.argmin(scores) + 1]]), copy.deepcopy(data.class_var),
                     copy.deepcopy(data.var_types), copy.deepcopy(data.var_limits))

    right_data = Data(copy.deepcopy(data.df.iloc[indices[np.argmin(scores) + 1]:]), copy.deepcopy(data.class_var),
                      copy.deepcopy(data.var_types), copy.deepcopy(data.var_limits))

    left_data.var_limits[split_var] = (data.var_limits[split_var][0], values[np.argmin(scores) + 1])
    right_data.var_limits[split_var] = (values[np.argmin(scores) + 1], data.var_limits[split_var][1])

    return np.min(scores), left_data, right_data


class Node(object):
    __class_description__ = """Abstract class for a binary tree node"""
    __version__ = 0.1

    def __init__(self, node_data):

        self.split_var = None
        self.data = node_data
        self.left_child = None
        self.right_child = None

    def split(self):

        best_right = None
        best_left = None
        best_score = float("inf")
        for idx, split_var in enumerate(self.data.df.columns):

            if split_var != self.data.class_var:

                if self.data.var_types[idx] == "circular":
                    score, left, right = circular_criteria(self.data, split_var)

                elif self.data.var_types[idx] == "linear":
                    score, left, right = linear_criteria(self.data, split_var)

                else:
                    raise NotImplementedError('Other types need to be implemented!')

                if best_score > score:
                    best_score = score
                    self.split_var = split_var

                    best_left = left
                    best_right = right
                else:
                    pass

        # print best_score
        self.left_child = Node(best_left)
        self.right_child = Node(best_right)


def tree_grower(tree_data, min_leaf):
    node = Node(tree_data)
    node.split()

    if node.left_child.data.df.shape[0] > min_leaf:
        node.left_child = tree_grower(node.left_child.data, min_leaf)

    if node.right_child.data.df.shape[0] > min_leaf:
        node.right_child = tree_grower(node.right_child.data, min_leaf)

    return node


def tree_walk_printer(tree, level=0):

    if tree.split_var is not None:
        print level*"  " + tree.split_var
        tree_walk_printer(tree.left_child, level+1)
        tree_walk_printer(tree.right_child, level+1)

    else:
        print level*"  " + "LEAF!"


def tree_walk_count_var(tree, var_name):

    if tree.split_var is not None:

        if tree.split_var == var_name:
            return 1 + tree_walk_count_var(tree.left_child, var_name) + tree_walk_count_var(tree.right_child, var_name)
        else:
            return tree_walk_count_var(tree.left_child, var_name) + tree_walk_count_var(tree.right_child, var_name)

    else:
        return 0


"""*************************
*********Evaluation*********
*************************"""

def evaluate_value_mean(anode, data_row):
        if anode.split_var is not None:

            #try on left limits
            if anode.left_child.data.var_limits[anode.split_var][0] > anode.left_child.data.var_limits[anode.split_var][1]:
                if anode.left_child.data.var_limits[anode.split_var][0] <= data_row[anode.split_var] <= 360 or \
                        0 <= data_row[anode.split_var] < anode.left_child.data.var_limits[anode.split_var][1]:

                    return evaluate_value_mean(anode.left_child, data_row)
            else:
                if anode.left_child.data.var_limits[anode.split_var][0] <= data_row[anode.split_var] < \
                        anode.left_child.data.var_limits[anode.split_var][1]:

                    return evaluate_value_mean(anode.left_child, data_row)

            #try on right limits
            if anode.right_child.data.var_limits[anode.split_var][0] > anode.right_child.data.var_limits[anode.split_var][1]:
                if anode.right_child.data.var_limits[anode.split_var][0] <= data_row[anode.split_var] <= 360 or \
                        0 <= data_row[anode.split_var] < anode.right_child.data.var_limits[anode.split_var][1]:

                    return evaluate_value_mean(anode.right_child, data_row)
            else:
                if anode.right_child.data.var_limits[anode.split_var][0] <= data_row[anode.split_var] < \
                        anode.right_child.data.var_limits[anode.split_var][1]:

                    return evaluate_value_mean(anode.right_child, data_row)
        else:
            #print anode.data.df
            return anode.data.df[anode.data.class_var].mean()


def evaluate_dataset_rmse(node, df_to_eval):

    err = 0
    n = df_to_eval.shape[0]
    for _, row in df_to_eval.iterrows():
        pred_val = evaluate_value_mean(node, row)
        err += (pred_val - row[node.data.class_var]) ** 2

    return math.sqrt(err / n)


def list_rmse(pairs):

    err = 0
    for pair in pairs:
        err += (pair[1] - pair[0]) ** 2

    return math.sqrt(err / len(pairs))


def evaluate_dataset_mae(node, df_to_eval):

    err = 0
    n = df_to_eval.shape[0]
    for _, row in df_to_eval.iterrows():
        pred_val = evaluate_value_mean(node, row)
        err += pred_val - row[node.data.class_var]

    return err / n


def list_mae(pairs):

    err = 0
    for pair in pairs:
        err += pair[1] - pair[0]

    return err / len(pairs)


def evaluate_dataset_cc(node, df_to_eval):

    sum_x_sqr = 0
    sum_y_sqr = 0
    sum_x = 0
    sum_y = 0
    sum_x_y = 0
    n = df_to_eval.shape[0]
    for _, row in df_to_eval.iterrows():
        sum_x_sqr += row[node.data.class_var] ** 2
        sum_y_sqr += evaluate_value_mean(node, row) ** 2
        sum_x += row[node.data.class_var]
        sum_y += evaluate_value_mean(node, row)
        sum_x_y += row[node.data.class_var] * evaluate_value_mean(node, row)

    return (sum_x_y - (sum_x * sum_y)/n) / math.sqrt((sum_x_sqr - (sum_x ** 2) / n) * (sum_y_sqr - (sum_y ** 2) / n))


def list_cc(pairs):

    sum_x_sqr = 0
    sum_y_sqr = 0
    sum_x = 0
    sum_y = 0
    sum_x_y = 0
    n = len(pairs)

    for pair in pairs:
        sum_x_sqr += pair[0] ** 2
        sum_y_sqr += pair[1] ** 2
        sum_x += pair[0]
        sum_y += pair[1]
        sum_x_y += pair[0] * pair[1]

    return (sum_x_y - (sum_x * sum_y)/n) / math.sqrt((sum_x_sqr - (sum_x ** 2) / n) * (sum_y_sqr - (sum_y ** 2) / n))


def evaluate_dataset_raw(results_list, node, df_to_eval):
    # This function appends to list (x, y) tuples
    # where x is the raw value and y is the tree result

    for _, row in df_to_eval.iterrows():
        results_list.append((row[node.data.class_var], evaluate_value_mean(node, row)))

    return results_list


"""*************************
******Cross Validation******
*************************"""

import random

def cxval_k_folds_split(df, k_folds):

    dataframes = []
    group_size = int(round(df.shape[0]*(1.0/k_folds)))

    for i in range(k_folds-1):
        rows = random.sample(df.index, group_size)
        dataframes.append(df.ix[rows])
        df = df.drop(rows)

    dataframes.append(df)

    return dataframes


def cxval_select_fold(i_fold, df_folds):
    df_folds_copy = copy.deepcopy(df_folds)

    if 0 <= i_fold < len(df_folds):

        test_df = df_folds_copy[i_fold]
        del df_folds_copy[i_fold]
        train_df = pd.concat(df_folds_copy)

        return train_df, test_df

    else:
        raise Exception('Group not in range!')


def cxval_test(df, class_var, var_types, bin_size, k_folds):

    df_folds = cxval_k_folds_split(df, k_folds)
    results = []

    for i in range(k_folds):
        print("Cross Validation: {}".format(i+1))
        train_df, test_df = cxval_select_fold(i, df_folds)
        train_data = Data(train_df, class_var, var_types)
        tree = tree_grower(test_data, bin_size)

        print("Cross Correlation: {}".format(evaluate_dataset_cc(tree, test_df)))
        print("Root Mean Square Error: {}".format(evaluate_dataset_rmse(tree, test_df)))
        print("Mean Absolute Error: {}".format(evaluate_dataset_mae(tree, test_df)))


def cxval_test2(df, class_var, var_types, bin_size, k_folds):

    df_folds = cxval_k_folds_split(df, k_folds)
    results = []

    for i in range(k_folds):
        train_df, test_df = cxval_select_fold(i, df_folds)
        train_data = Data(train_df, class_var, var_types)
        tree = tree_grower(train_data, bin_size)

        evaluate_dataset_raw(results, tree, test_df)


    print("Cross Correlation: {}".format(list_cc(results)))
    print("Root Mean Square Error: {}".format(list_rmse(results)))
    print("Mean Absolute Error: {}".format(list_mae(results)))


def cxval_test3(df_folds, class_var, var_types, bin_size):

    results_test = []
    results_train = []

    for i_fold, _ in enumerate(df_folds):
        train_df, test_df = cxval_select_fold(i_fold, df_folds)
        train_data = Data(train_df, class_var, var_types)
        tree = tree_grower(train_data, bin_size)

        evaluate_dataset_raw(results_test, tree, test_df)
        evaluate_dataset_raw(results_train, tree, train_df)
        print("gfs_wind_dir: {} times".format(tree_walk_count_var(tree, 'gfs_wind_dir')))
        print("date: {} times".format(tree_walk_count_var(tree, 'date')))
        print("time: {} times".format(tree_walk_count_var(tree, 'time')))

    return list_cc(results_test), list_rmse(results_test), list_cc(results_train), list_rmse(results_train)


def cxval_test4(df_folds, class_var, var_types, bin_size):

    results_test = []

    for i_fold, _ in enumerate(df_folds):
        train_df, test_df = cxval_select_fold(i_fold, df_folds)
        train_data = Data(train_df, class_var, var_types)
        tree = tree_grower(train_data, bin_size)

        evaluate_dataset_raw(results_test, tree, test_df)

    return list_rmse(results_test)


if __name__ == "__main__":

    from datetime import datetime
    import calendar
    import csv
    import collections

    import os
    print os.getcwd()

    def time_to_angle(a_time):
        #return 360.0*(a_time.hour*3600+a_time.minute*60+a_time.second)/86400.0
        # Limit time values to 24
        return 360.0*a_time.hour/24.0

    def date_to_angle(a_date):
        # Limit time values to 36
        if calendar.isleap(a_date.year):
            #return 360.0*(a_date.timetuple().tm_yday-1)/366.0
            return 10*int(a_date.timetuple().tm_yday/10.0)

        else:
            #return 360.0*(a_date.timetuple().tm_yday-1)/365.0
            return 10*int(a_date.timetuple().tm_yday/10.0)

    var_types_linear = ['linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear']
    var_types_circular = ['linear', 'linear', 'linear', 'linear', 'circular', 'linear', 'circular', 'circular']

    var_types_list = [var_types_linear, var_types_circular]

    airports = ['eddt', 'lebl', 'lfpg', 'limc', 'yssy', 'egll', 'zbaa']

    for airport in airports:
        print airport

        df = pd.read_csv("./web/static/data/" + airport + ".csv")
        df.drop([u'metar_press', u'metar_rh', u'metar_temp', u'metar_wind_dir'], axis=1, inplace=True)

        df['gfs_wind_dir'] = df['gfs_wind_dir'].apply(lambda x: round(x / 10) * 10)
        df['gfs_press'] = df['gfs_press'].apply(lambda x: round(x))
        df['gfs_rh'] = df['gfs_rh'].apply(lambda x: round(x))
        df['gfs_temp'] = df['gfs_temp'].apply(lambda x: round(x))
        df['gfs_wind_spd'] = df['gfs_wind_spd'].apply(lambda x: 0.5 * round(x / 0.5))

        df['date'] = df['date'].apply(lambda x: date_to_angle(datetime.strptime(x, "%Y-%m-%d").date()))
        df['time'] = df['time'].apply(lambda x: time_to_angle(datetime.strptime(x, "%H:%M").time()))

        class_var = 'metar_wind_spd'

        df_folds = cxval_k_folds_split(df, 5)

        results_test = []

        for i_fold, _ in enumerate(df_folds):
            print i_fold

            inner_df_folds = copy.deepcopy(df_folds)

            test_df = inner_df_folds[i_fold]
            del inner_df_folds[i_fold]
            train_df = pd.concat(inner_df_folds)

            bins = [2000, 1000, 500, 200, 100, 50]

            opt_bin = None
            opt_method = None
            best_rmse = float('inf')

            for bin_size in bins:

                for type_idx, var_types in enumerate(var_types_list):
                    rmse_value_test = cxval_test4(inner_df_folds, class_var, var_types, bin_size)
                    if rmse_value_test < best_rmse:
                        opt_bin = bin_size
                        opt_method = type_idx
                        best_rmse = rmse_value_test

            print("Use {} bin size and {} method".format(opt_bin, opt_method))

            train_data = Data(train_df, class_var, var_types_list[opt_method])
            tree = tree_grower(train_data, opt_bin)

            evaluate_dataset_raw(results_test, tree, test_df)

        print("RMSE {}".format(list_rmse(results_test)))
