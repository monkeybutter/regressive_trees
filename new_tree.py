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


def evaluate_dataset(node, df_to_eval):
    def _evaluate_value(anode, data_row):
        if anode.split_var is not None:
            if anode.left_child.data.var_limits[anode.split_var][0] <= data_row[anode.split_var] < \
                    anode.left_child.data.var_limits[anode.split_var][1]:
                return _evaluate_value(anode.left_child, data_row)
            else:
                return _evaluate_value(anode.right_child, data_row)
        else:
            return anode.data.df[anode.data.class_var].mean()

    tree_sq_err = 0
    raw_sq_err = 0
    total_values = df_to_eval.shape[0]
    for _, row in df_to_eval.iterrows():
        pred_val = _evaluate_value(node, row)
        raw_sq_err += (row["gfs_wind_spd"] - row[class_var]) ** 2
        tree_sq_err += (pred_val - row[class_var]) ** 2
    return math.sqrt(raw_sq_err / total_values), math.sqrt(tree_sq_err / total_values)


if __name__ == "__main__":

    from datetime import datetime
    import calendar

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

    """
    df = pd.read_csv("/home/roz016/Dropbox/Data for Tree/New Tree/test.csv")
    df.drop([u'Unnamed: 0'], axis=1, inplace=True)

    print df

    class_var = 'value'
    var_types = ['circular', 'linear']

    data = Data(df, class_var, var_types)

    new_tree = tree_grower(data, 10)

    print var_types

    """
    airports = ['yssy', 'egll', 'zbaa']

    for airport in airports:
        print airport

        var_types_linear = ['linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear']
        var_types_circular = ['linear', 'linear', 'linear', 'linear', 'circular', 'linear', 'circular', 'circular']

        var_types_list = [var_types_linear, var_types_circular]

        bins = [2000, 1000, 500, 200, 100]
        for bin_size in bins:
            print bin_size

            for var_types in var_types_list:

                df = pd.read_csv("./web/static/data/" + airport + ".csv")
                df.drop([u'metar_press', u'metar_rh', u'metar_temp', u'metar_wind_dir'], axis=1, inplace=True)

                df['gfs_wind_dir'] = df['gfs_wind_dir'].apply(lambda x: round(x / 10) * 10)
                df['gfs_press'] = df['gfs_press'].apply(lambda x: round(x))
                df['gfs_rh'] = df['gfs_rh'].apply(lambda x: round(x))
                df['gfs_temp'] = df['gfs_temp'].apply(lambda x: round(x))
                df['gfs_wind_spd'] = df['gfs_wind_spd'].apply(lambda x: 0.5 * round(x / 0.5))

                df['date'] = df['date'].apply(lambda x: date_to_angle(datetime.strptime(x, "%Y-%m-%d").date()))
                df['time'] = df['time'].apply(lambda x: time_to_angle(datetime.strptime(x, "%H:%M").time()))

                df2 = pd.read_csv("./web/static/data/" + airport + ".csv")
                df2.drop([u'metar_press', u'metar_rh', u'metar_temp', u'metar_wind_dir', u'date', u'time'], axis=1, inplace=True)

                df2['gfs_wind_dir'] = df2['gfs_wind_dir'].apply(lambda x: round(x / 10) * 10)
                df2['gfs_press'] = df2['gfs_press'].apply(lambda x: round(x))
                df2['gfs_rh'] = df2['gfs_rh'].apply(lambda x: round(x))
                df2['gfs_temp'] = df2['gfs_temp'].apply(lambda x: round(x))
                df2['gfs_wind_spd'] = df2['gfs_wind_spd'].apply(lambda x: 0.5 * round(x / 0.5))

                class_var = 'metar_wind_spd'

                print("Full Columns")
                data = Data(df, class_var, var_types)
                new_tree = tree_grower(data, bin_size)
                print var_types
                print evaluate_dataset(new_tree, df)

                print("Reduced Columns")
                data = Data(df2, class_var, var_types)
                new_tree = tree_grower(data, bin_size)
                print var_types
                print evaluate_dataset(new_tree, df2)