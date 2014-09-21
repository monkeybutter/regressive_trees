__author__ = 'SmartWombat'

import pandas as pd
import json
from util import cross_validate_splits, cross_validate_group
from regressor import *

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

airports = ['yssy', 'egll']

metar_vars = ['metar_press', 'metar_rh', 'metar_temp', 'metar_wind_dir', 'metar_wind_spd']
metar_types = ['linear', 'linear', 'linear', 'circular', 'linear']

gfs_vars = ['gfs_press', 'gfs_rh', 'gfs_temp', 'gfs_wind_dir', 'gfs_wind_spd', 'time', 'date']
gfs_types = ['linear', 'linear', 'linear', 'circular', 'linear', 'time', 'date']

for airport in airports:
    df_master = pd.read_csv("./web/static/data/" + airport + ".csv")
    df_master['gfs_wind_dir'] = df_master['gfs_wind_dir'].apply(lambda x: round(x/10) * 10)

    index = metar_vars.index('metar_wind_spd')
    del_metar_vars = metar_vars[:]
    del del_metar_vars[index]
    df = df_master.drop(del_metar_vars, 1)
    df_types = gfs_types[:]
    df_types.insert(0, metar_types[index])

    cx_bin_number = 5
    cx_val = cross_validate_splits(df, cx_bin_number)

    for i in range(cx_bin_number):
        print("{} Cross Validate {}: {}".format(airport, i, cx_bin_number+1))
        train_df, test_df = cross_validate_group(i+1, cx_val)

        test_df["std_regression"] = get_simple_linear_regression(test_df, train_df, 'metar_wind_spd', 'gfs_wind_spd')
        test_df["opt_regression"] = get_direction_speed_weighted_simple_linear_regression(test_df, train_df, 'metar_wind_spd', 'gfs_wind_spd', 'gfs_wind_dir', 25, 2)

        result = []
        for index, row in test_df.iterrows():
            element = {}
            element['gfs_wind_spd'] = row['gfs_wind_spd']
            element['metar_wind_spd'] = row['metar_wind_spd']
            element['std_regression'] = row['std_regression']
            element['opt_regression'] = row['opt_regression']
            result.append(element)

        with open('/Users/monkeybutter/Dropbox/Data for Tree/Results/cx5_bin100/' + airport + '_' + '_regression_cx' + str(i) + '.json', 'w') as outfile:
            json.dump(result, outfile)