__author__ = 'SmartWombat'

import pandas
import time
from tree_parallel import Tree
import random
from data.data import Data
from util import cross_validate_splits, cross_validate_group
import pickle

airports = ['yssy', 'egll', 'zbaa']

for airport in airports:
    df = pandas.read_csv("./web/static/data/" + airport + ".csv")
    df['gfs_wind_dir'] = df['gfs_wind_dir'].apply(lambda x: round(x/10) * 10)

    class_vars = ['metar_wind_spd', 'metar_press', 'metar_temp']

    for class_var in class_vars:
        var_types = ['linear', 'linear', 'linear', 'circular', 'linear', 'linear', 'linear', 'linear', 'circular', 'linear', 'time', 'date']

        print("{} {}: {}".format(airport, class_var, time.strftime("%c")))

        bin_number = 5
        cx_val = cross_validate_splits(df, bin_number)

        for i in range(bin_number):
            train_df, test_df = cross_validate_group(i+1, cx_val)

            with open('/Users/monkeybutter/Desktop/' + airport + '_' + class_var + '_bin100_cx' + str(i+1) + 'df' + '.pick', 'w') as f:
                    pickle.dump(test_df, f)

            print("Bin {}: {}".format(i, time.strftime("%c")))

            trees = []
            for j in range(50):
                print("Tree {} of 50: {}".format(j, time.strftime("%c")))
                # train tree with 70% of the train_df
                rows = random.sample(train_df.index, int(train_df.shape[0]*.7))
                tree_df = df.ix[rows]

                data = Data(tree_df, class_var, var_types, True)
                tree = Tree()
                # 100 bin size
                node = tree.tree_grower(data, 100)
                # Pickle object
                print(type(node))
                print(node)
                with open('/Users/monkeybutter/Desktop/' + airport + '_' + class_var + '_bin100_cx' + str(i+1) + '_rftree' + str(j+1) + '.pick', 'w') as f:
                    pickle.dump(node, f)