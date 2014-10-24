__author__ = 'SmartWombat'

import pandas as pd
from tree_parallel import Tree, tree_to_dict
from data.data import Data
import math


def evaluate_dataset(node, df):

    def _evaluate_value(atree, data_row):
        if atree.get_name() == 'Node':
            if atree.var_type == 'linear':
                if data_row[atree.split_var] < atree.split_values[1]:
                    return _evaluate_value(atree.left_child, data_row)
                else:
                    return _evaluate_value(atree.right_child, data_row)

            else:
                raise Exception

        if atree.get_name() == 'Leaf':
            print atree.members
            print atree.value
            return atree.value

    tree_sq_err = 0
    raw_sq_err = 0
    total_values = df.shape[0]
    for _, row in df.iterrows():
        print "_______________________"
        print row["gfs_wind_spd"]
        print row[class_var]
        pred_val = _evaluate_value(node, row)
        raw_sq_err += (row["gfs_wind_spd"] - row[class_var])**2
        tree_sq_err += (pred_val - row[class_var])**2
    return math.sqrt(raw_sq_err/total_values), math.sqrt(tree_sq_err/total_values)

if __name__ == "__main__":

    airports = ['yssy', 'egll', 'zbaa']
    airports = ['zbaa']

    for airport in airports:
        df = pd.read_csv("./web/static/data/" + airport + ".csv")
        df.drop([u'metar_press', u'metar_rh', u'metar_temp', u'metar_wind_dir', u'time', u'date'], axis=1, inplace=True)

        df['gfs_wind_dir'] = df['gfs_wind_dir'].apply(lambda x: round(x/10) * 10)
        df['gfs_press'] = df['gfs_press'].apply(lambda x: round(x))
        df['gfs_rh'] = df['gfs_rh'].apply(lambda x: round(x))
        df['gfs_temp'] = df['gfs_temp'].apply(lambda x: round(x))
        df['gfs_wind_spd'] = df['gfs_wind_spd'].apply(lambda x: 0.5 * round(x/0.5))

        class_var = 'metar_wind_spd'
        var_types = ['linear', 'linear', 'linear', 'linear', 'circular', 'linear']

        data = Data(df, class_var, var_types, True)
        tree = Tree()
        node = tree.tree_grower(data, 100)

        print tree_to_dict(node, "O")

        print evaluate_dataset(node, df)

