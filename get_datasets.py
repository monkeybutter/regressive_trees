__author__ = 'SmartWombat'

import pandas as pd
import time
import datetime
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
class_vars = ['metar_press', 'metar_rh', 'metar_temp', 'metar_wind_dir', 'metar_wind_spd']

for class_var in class_vars:
    print class_var

    for airport in airports:
        print airport

        df_master = pd.read_csv("./web/static/data/" + airport + ".csv")
        df_master['gfs_wind_dir'] = df_master['gfs_wind_dir'].apply(lambda x: round(x/10) * 10)

        index = class_vars.index(class_var)
        del_metar_vars = class_vars[:]
        del del_metar_vars[index]
        df_master = df_master.drop(del_metar_vars, 1)

        cx_bin_number = 5
        cx_val = cross_validate_splits(df_master, cx_bin_number)

        for i in range(cx_bin_number):
            print("Cross Validate: {}".format(i+1))

            train_df, test_df = cross_validate_group(i+1, cx_val)

            # Pickle Test Dataframe
            with open('/home/roz016/Dropbox/Data for Tree/Results/cx5_lin_vs_cir/' + airport + '_' + class_var + '_cx' + str(i+1) + '_cir_testdf.pick', 'w') as f:
                pickle.dump(test_df, f)
            # Pickle Train Dataframe
            with open('/home/roz016/Dropbox/Data for Tree/Results/cx5_lin_vs_cir/' + airport + '_' + class_var + '_cx' + str(i+1) + '_cir_traindf.pick', 'w') as f:
                pickle.dump(train_df, f)

            train_df['time'] = train_df.apply(lambda x: transform_time(x['time']), axis=1)
            train_df['date'] = train_df.apply(lambda x: transform_date(x['date']), axis=1)
            test_df['time'] = test_df.apply(lambda x: transform_time(x['time']), axis=1)
            test_df['date'] = test_df.apply(lambda x: transform_date(x['date']), axis=1)

            # Pickle Test Dataframe
            with open('/home/roz016/Dropbox/Data for Tree/Results/cx5_lin_vs_cir/' + airport + '_' + class_var + '_cx' + str(i+1) + '_lin_testdf.pick', 'w') as f:
                pickle.dump(test_df, f)
            # Pickle Train Dataframe
            with open('/home/roz016/Dropbox/Data for Tree/Results/cx5_lin_vs_cir/' + airport + '_' + class_var + '_cx' + str(i+1) + '_lin_traindf.pick', 'w') as f:
                pickle.dump(train_df, f)

