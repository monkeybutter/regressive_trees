__author__ = 'SmartWombat'

import pandas
import random
from tree import Tree
from evaluator import evaluate_dataset
from data.data import Data


df = pandas.read_csv("./data/yssy.csv")
print(df.columns)
print(df.shape)

df.drop(['metar_wind_dir', 'gfs_wind_dir', 'time'], axis=1, inplace=True)
print(df.columns)

rows = random.sample(df.index, int(df.shape[0]*.8))
train_df = df.ix[rows]
test_df = df.drop(rows)

class_var = 'metar_wind_spd'
var_types = ['linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'linear', 'date']

data = Data(train_df, class_var, var_types, True)
tree = Tree()
#node1 = tree.tree_grower(data1, 2000)
#node2 = tree.tree_grower(data2, 2000)
print("IPS")
node = tree.tree_grower(data, 500)
print("OUI")

print 'London'
#print('Wind is linear: {}'.format(evaluate_dataset(class_var, node1, test_df2)))
#print('Wind is circular: {}'.format(evaluate_dataset(class_var, node2, test_df2)))
print('Including time: {}'.format(evaluate_dataset(class_var, node, test_df)))