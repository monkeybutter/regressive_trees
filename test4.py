__author__ = 'SmartWombat'

import pandas as pd
import time
from tree_parallel import Tree
import random
from data.data import Data
from util import cross_validate_splits, cross_validate_group
import pickle

#airports = ['yssy', 'egll', 'zbaa']
airports = ['yssy']

metar_vars = ['metar_press', 'metar_rh', 'metar_temp', 'metar_wind_dir', 'metar_wind_spd']
metar_types = ['linear', 'linear', 'linear', 'circular', 'linear']

gfs_vars = ['gfs_press', 'gfs_rh', 'gfs_temp', 'gfs_wind_dir', 'gfs_wind_spd', 'time', 'date']
gfs_types = ['linear', 'linear', 'linear', 'circular', 'linear', 'time', 'date']

for airport in airports:
    df_master = pd.read_csv("./web/static/data/" + airport + ".csv")
    df_master['gfs_wind_dir'] = df_master['gfs_wind_dir'].apply(lambda x: round(x/10) * 10)

    class_vars = ['metar_wind_spd', 'metar_rh', 'metar_press', 'metar_temp']
    #class_vars = ['metar_wind_dir']

    for class_var in class_vars:
        print class_var
        index = metar_vars.index(class_var)
        del_metar_vars = metar_vars[:]
        del del_metar_vars[index]
        df = df_master.drop(del_metar_vars, 1)
        df_types = gfs_types[:]
        df_types.insert(0, metar_types[index])

        cx_bin_number = 5
        cx_val = cross_validate_splits(df, cx_bin_number)

        for i in range(cx_bin_number):
            print("Cross Validate {}: {}".format(i, cx_bin_number+1))
            print len(cx_val)
            train_df, test_df = cross_validate_group(i+1, cx_val)

            # Pickle Random Forest
            with open('/home/roz016/Dropbox/Data for Tree/Results/cx5_rf50_bin100/' + airport + '_' + class_var + '_cx' + str(i+1) + '_testdf.pick', 'w') as f:
                pickle.dump(test_df, f)

            print("Bin {}: {}".format(i, time.strftime("%c")))

            trees = []
            for j in range(50):
                print("Tree {} of 50: {}".format(j, time.strftime("%c")))
                # train tree with 70% of the train_df
                rows = random.sample(train_df.index, int(train_df.shape[0]*.7))
                randomforest_df = train_df.ix[rows]

                data = Data(randomforest_df, class_var, df_types, True)
                tree = Tree()
                # 100 bin size
                node = tree.tree_grower(data, 100)

                trees.append(node)

            # Pickle Test Dataframe
            with open('/home/roz016/Dropbox/Data for Tree/Results/cx5_rf50_bin100/' + airport + '_' + class_var + '_bin100_cx' + str(i+1) + '_rf.pick', 'w') as f:
                pickle.dump(test_df, f)