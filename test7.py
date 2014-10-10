__author__ = 'SmartWombat'

import pandas as pd
import time
import datetime
import copy
from tree_parallel import Tree
from data.data import Data
from util import cross_validate_splits, cross_validate_group
import pickle


def transform_time(a_time):
    hour = int(a_time[:2])
    minute = int(a_time[3:])

    return minute + (hour * 60)


def transform_date(a_date):

    year = int(a_date[:4])
    month = int(a_date[5:7])
    day = int(a_date[8:10])

    return time.mktime(datetime.datetime(year, month, day, 0, 0).timetuple())


airports = ['yssy', 'egll', 'zbaa']

gfs_vars = ['gfs_press', 'gfs_rh', 'gfs_temp', 'gfs_wind_dir', 'gfs_wind_spd', 'time', 'date']

gfs_types = list()
gfs_types.append({'name': 'circular', 'types': ['linear', 'linear', 'linear', 'circular', 'linear', 'time', 'date']})
gfs_types.append({'name': 'linear', 'types': ['linear'] * 7})

class_var = 'metar_wind_dir'
class_var_types = ['circular', 'linear']

for airport in airports:
    print airport
    df_master = pd.read_csv("./web/static/data/" + airport + ".csv")
    df_master['gfs_wind_dir'] = df_master['gfs_wind_dir'].apply(lambda x: round(x/10) * 10)

    print df_master.columns

    delete_vars = ['metar_press', 'metar_rh', 'metar_temp', 'metar_wind_spd']
    df_master = df_master.drop(delete_vars, 1)

    print df_master.columns

    cx_bin_number = 5
    cx_val = cross_validate_splits(df_master, cx_bin_number)

    for i in range(cx_bin_number):
        print("Cross Validate: {}".format(i+1))

        train_df_master, test_df = cross_validate_group(i+1, cx_val)

        # Pickle Test Dataframe
        with open('/home/roz016/Dropbox/Data for Tree/Results/cx5_lin_vs_cir_bin100_3/' + airport + '_' + class_var + '_bin100_cx' + str(i+1) + '_testdf.pick', 'w') as f:
            pickle.dump(test_df, f)
        # Pickle Train Dataframe
        with open('/home/roz016/Dropbox/Data for Tree/Results/cx5_lin_vs_cir_bin100_3/' + airport + '_' + class_var + '_bin100_cx' + str(i+1) + '_traindf.pick', 'w') as f:
            pickle.dump(train_df_master, f)

        for class_var_type in class_var_types:
            for gfs_type in gfs_types:
                print("Class var type: {} gfs vars types: {}".format(class_var_type, gfs_type))
                train_df = copy.deepcopy(train_df_master)

                if gfs_type["name"] == 'linear':
                    train_df['time'] = train_df.apply(lambda x: transform_time(x['time']), axis=1)
                    train_df['date'] = train_df.apply(lambda x: transform_date(x['date']), axis=1)

                df_types = gfs_type["types"][:]
                df_types.insert(0, class_var_type)

                print gfs_type["name"]
                print train_df.columns
                print df_types

                print("Start: {}".format(time.strftime("%c")))

                data = Data(train_df, class_var, df_types, True)
                tree = Tree()
                # 100 bin size
                node = tree.tree_grower(data, 100)
                # Pickle Normal Tree

                with open('/home/roz016/Dropbox/Data for Tree/Results/cx5_lin_vs_cir_bin100_3/' + airport + '_' + class_var + '_' + class_var_type + '_gfs_' + gfs_type["name"] + '_bin100_cx' + str(i+1) + '_tree.pick', 'w') as f:
                    pickle.dump(node, f)