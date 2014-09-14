__author__ = 'SmartWombat'

import pandas
from tree_parallel import Tree
import random
from data.data import Data
from evaluator import raw_evaluate_dataset
import json

airports = ['yssy', 'egll', 'zbaa']

for airport in airports:
    df = pandas.read_csv("./web/static/data/" + airport + ".csv")
    df['gfs_wind_dir'] = df['gfs_wind_dir'].apply(lambda x: round(x/10) * 10)

    class_vars = ['metar_wind_spd', 'metar_press', 'metar_temp']

    for class_var in class_vars:
        var_types = ['linear', 'linear', 'linear', 'circular', 'linear', 'linear', 'linear', 'linear', 'circular', 'linear', 'time', 'date']

        bin_sizes = [500, 250, 100]
        for bin_size in bin_sizes:
            print("{} {} {}".format(airport, class_var, bin_size))
            result = []
            for i in range(5):
                print(i)
                rows = random.sample(df.index, int(df.shape[0]*.8))
                train_df = df.ix[rows]
                test_df = df.drop(rows)
                data = Data(train_df, class_var, var_types, True)
                tree = Tree()
                node = tree.tree_grower(data, bin_size)
                result.extend(raw_evaluate_dataset(class_var, node, test_df))

            with open('/home/roz016/Dropbox/Data for Tree/Results/' + airport + '_' + class_var + '_' + str(bin_size) + '.json', 'w') as outfile:
                json.dump(result, outfile)









