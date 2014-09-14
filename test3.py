__author__ = 'SmartWombat'

import pandas as pd
import time
from tree_parallel import Tree
import random
from data.data import Data
from util import cross_validate_splits, cross_validate_group
from evaluator import detail_evaluate_dataset
import json

airports = ['yssy', 'egll', 'zbaa']

metar_vars = ['metar_press', 'metar_rh', 'metar_temp', 'metar_wind_dir', 'metar_wind_spd']
metar_types = ['linear', 'linear', 'linear', 'circular', 'linear']

gfs_vars = ['gfs_press', 'gfs_rh', 'gfs_temp', 'gfs_wind_dir', 'gfs_wind_spd', 'time', 'date']
gfs_types = ['linear', 'linear', 'linear', 'circular', 'linear', 'time', 'date']

for airport in airports:
    df_master = pd.read_csv("./web/static/data/" + airport + ".csv")

    class_vars = ['metar_wind_spd', 'metar_wind_dir', 'metar_press', 'metar_temp']

    for class_var in class_vars:
        print class_var
        index = metar_vars.index(class_var)
        del_metar_vars = metar_vars[:]
        del del_metar_vars[index]
        df = df_master.drop(del_metar_vars, 1)
        df_types = gfs_types[:]
        df_types.insert(0, metar_types[index])

        bin_number = 5
        cx_val = cross_validate_splits(df, bin_number)

        for i in range(bin_number):
            print("Cross Validate {}: {}".format(i, bin_number))
            print len(cx_val)
            train_df, test_df = cross_validate_group(i+1, cx_val)

            print("Bin {}: {}".format(i, time.strftime("%c")))

            rows = random.sample(train_df.index, int(train_df.shape[0]*.7))
            tree_df = df.ix[rows]

            data = Data(train_df, class_var, df_types, True)
            tree = Tree()
            # 100 bin size
            node = tree.tree_grower(data, 1000)

            with open('/Users/monkeybutter/Desktop/' + airport + '_' + class_var + '_bin' + str(i) + '.json', 'w') as outfile:
                json.dump(detail_evaluate_dataset('gfs' + class_var[5:], class_var, node, test_df), outfile)