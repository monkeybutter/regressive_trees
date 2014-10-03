__author__ = 'SmartWombat'

import pandas
import pickle
from tree_parallel import Tree, tree_to_dict
from tree import Tree
from data.data import Data
from evaluator import evaluate_dataset_rmse, evaluate_dataset_mae
import pprint


df = pandas.read_csv("./web/static/data/artif.csv")
df_cir = df.drop(['Unnamed: 0', 'time_of_day', 'day_of_year'], axis=1)
df_lin = df.drop(['Unnamed: 0', 'time', 'date'], axis=1)


bins = [5000]#, 2000, 1000, 500, 100, 50]
"""
for bin in bins:
    print bin
    var_types = ['linear', 'linear', 'linear']
    data = Data(df_lin, "temp", var_types, True)
    tree = Tree()
    node = tree.tree_grower(data, bin)
    with open('./web/static/data/artif_lin_{}.pick'.format(bin), 'w') as f:
        pickle.dump(node, f)

    var_types = ['linear', 'date', 'time']
    data = Data(df_cir, "temp", var_types, True)
    tree = Tree()
    node = tree.tree_grower(data, bin)
    with open('./web/static/data/artif_cir_{}.pick'.format(bin), 'w') as f:
        pickle.dump(node, f)

"""

for bin in bins:
    lin_tree = pickle.load(open('./web/static/data/artif_lin_{}.pick'.format(bin), "rb" ))
    cir_tree = pickle.load(open('./web/static/data/artif_cir_{}.pick'.format(bin), "rb" ))

    print('Linear RMSE {}: {}'.format(bin, evaluate_dataset_rmse("temp", lin_tree, df_lin)))
    print('Linear MAE {}: {}'.format(bin, evaluate_dataset_mae("temp", lin_tree, df_lin)))
    pprint.pprint(tree_to_dict(lin_tree, "O"))

    print('Circular RMSE {}: {}'.format(bin, evaluate_dataset_rmse("temp", cir_tree, df_cir)))
    print('Circular MAE {}: {}'.format(bin, evaluate_dataset_mae("temp", cir_tree, df_cir)))
    pprint.pprint(tree_to_dict(cir_tree, "O"))
    print("-----------------")








