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

        def f(L):
            """Return indices of the first minimum value in a list of lists."""
            return min(min(e) for e in L), min((n, i, j) for i, L2 in enumerate(L) for j, n in enumerate(L2))[1:]

        data.df = data.df.sort([split_var])
        values, indices = np.unique(data.df[split_var], return_index=True)

        #scores_prime = [(idx/data.df.shape[0] * np.var(data.df[data.class_var].iloc[:idx])) + ((data.df.shape[0]-idx)/data.df.shape[0] * np.var(data.df[data.class_var].iloc[idx:])) for idx in indices[1:]]

        index_lists = [sorted([indice2-indice if indice2-indice >= 0 else indice2-indice+data.df.shape[0] for indice2 in indices]) for indice in indices]
        dfs = [copy.deepcopy(data.df).iloc[index:].append(copy.deepcopy(data.df).iloc[:index]) for index in indices]

        score, min_index = f([[(idx/data.df.shape[0] * np.var(dfs[index][data.class_var].iloc[:idx])) + ((data.df.shape[0]-idx)/data.df.shape[0] * np.var(dfs[index][data.class_var].iloc[idx:]))
                for idx in index_list[1:]] for (index, index_list) in enumerate(index_lists)])

        #return_df_uncut = dfs[min_index[0]]
        return_indexes_uncut = index_lists[min_index[0]]

        left_data = Data(dfs[min_index[0]].iloc[:return_indexes_uncut[min_index[1]+1]], copy.deepcopy(data.class_var), copy.deepcopy(data.var_types), copy.deepcopy(data.var_limits))
        right_data = Data(dfs[min_index[0]].iloc[return_indexes_uncut[min_index[1]+1]:], copy.deepcopy(data.class_var), copy.deepcopy(data.var_types), copy.deepcopy(data.var_limits))

        left_data.var_limits[split_var] = (dfs[min_index[0]][split_var].iloc[0], dfs[min_index[0]][split_var].iloc[index_lists[min_index[0]][min_index[1]+1]])
        right_data.var_limits[split_var] = (dfs[min_index[0]][split_var].iloc[index_lists[min_index[0]][min_index[1]+1]], dfs[min_index[0]][split_var].iloc[0])

        return score, left_data, right_data

    else:
        data.df = data.df.sort([split_var])
        # If dataset crosses origin, it has to be reordered
        if data.var_limits[split_var][1] < data.var_limits[split_var][0]:
            data.df = copy.deepcopy(data.df[(data.df[split_var] >= data.var_limits[split_var][0]) & (data.df[split_var] <= 360)]).append(copy.deepcopy(data.df[(data.df[split_var] >= 0) & (data.df[split_var] <= data.var_limits[split_var][1])]))

        return splitter(data, split_var)

def linear_criteria(master_data, split_var):

    data = copy.deepcopy(master_data)
    data.df = data.df.sort([split_var])

    return splitter(data, split_var)


def splitter(data, split_var):

    values, indices = np.unique(data.df[split_var], return_index=True)

    if len(indices) == 1:
        return float("inf"), None, None

    scores = [(idx/data.df.shape[0] * np.var(data.df[data.class_var].iloc[:idx])) + ((data.df.shape[0]-idx)/data.df.shape[0] * np.var(data.df[data.class_var].iloc[idx:])) for idx in indices[1:]]

    left_data = Data(copy.deepcopy(data.df.iloc[:indices[np.argmin(scores) + 1]]), copy.deepcopy(data.class_var), copy.deepcopy(data.var_types), copy.deepcopy(data.var_limits))
    right_data = Data(copy.deepcopy(data.df.iloc[indices[np.argmin(scores) + 1]:]), copy.deepcopy(data.class_var), copy.deepcopy(data.var_types), copy.deepcopy(data.var_limits))

    left_data.var_limits[split_var] = (data.var_limits[split_var][0], values[np.argmin(scores) + 1])
    right_data.var_limits[split_var] = (values[np.argmin(scores) + 1], data.var_limits[split_var][1])

    return np.min(scores), left_data, right_data


class Node(object):

    __class_description__ = """Abstract class for a binary tree node"""
    __version__ = 0.1

    def __init__(self, data):

        self.split_var = None
        self.data = data
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

        print best_score
        self.left_child = Node(best_left)
        self.right_child = Node(best_right)


def tree_grower(data, min_leaf):
    node = Node(data)
    node.split()
    print(node.split_var)
    print(node.data.df.shape[0])
    print(node.data.var_limits)
    print("Left {}".format(node.left_child.data.var_limits))
    print("Right {}".format(node.right_child.data.var_limits))

    if node.left_child.data.df.shape[0] > min_leaf:
        node.left_child = tree_grower(node.left_child.data, min_leaf)

    if node.right_child.data.df.shape[0] > min_leaf:
        node.right_child = tree_grower(node.right_child.data, min_leaf)

    return node


def evaluate_dataset(node, df):

    def _evaluate_value(anode, data_row):
        if anode.split_var is not None:
            if anode.left_child.data.var_limits[anode.split_var][0] < data_row[anode.split_var] < anode.left_child.data.var_limits[anode.split_var][1]:
                return _evaluate_value(anode.left_child, data_row)
            else:
                return _evaluate_value(anode.right_child, data_row)
        else:
            #print anode.data.df.shape
            #print np.var(anode.data.df[anode.data.class_var])
            #print anode.data.df[anode.data.class_var].mean()
            return anode.data.df[anode.data.class_var].mean()

    tree_sq_err = 0
    raw_sq_err = 0
    total_values = df.shape[0]
    for _, row in df.iterrows():
        pred_val = _evaluate_value(node, row)
        raw_sq_err += (row["gfs_wind_spd"] - row[class_var])**2
        #raw_ac_sq_err += (row["metar_wind_spd"] - real_val)**2
        tree_sq_err += (pred_val - row[class_var])**2
    return math.sqrt(raw_sq_err/total_values), math.sqrt(tree_sq_err/total_values)
    #return acum_error/total_values


if __name__ == "__main__":

    airports = ['yssy', 'egll', 'zbaa']
    airports = ['yssy']

    for airport in airports:
        df = pd.read_csv("./web/static/data/" + airport + ".csv")
        df.drop([u'metar_press', u'metar_rh', u'metar_temp', u'metar_wind_dir', u'time', u'date'], axis=1, inplace=True)

        df['gfs_wind_dir'] = df['gfs_wind_dir'].apply(lambda x: round(x/10) * 10)
        df['gfs_press'] = df['gfs_press'].apply(lambda x: round(x))
        df['gfs_rh'] = df['gfs_rh'].apply(lambda x: round(x))
        df['gfs_temp'] = df['gfs_temp'].apply(lambda x: round(x))
        df['gfs_wind_spd'] = df['gfs_wind_spd'].apply(lambda x: 0.5 * round(x/0.5))

        print df.shape

        class_var = 'metar_wind_spd'
        var_types = ['linear', 'linear', 'linear', 'linear', 'linear', 'linear']
        data = Data(df, class_var, var_types)

        new_tree_200 = tree_grower(data, 3200)

        print evaluate_dataset(new_tree_200, df)