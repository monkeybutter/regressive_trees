__author__ = 'SmartWombat'

import pandas
from tree import Tree
from evaluator import evaluate_dataset, _evaluate_value
from data.data import Data


df = pandas.read_csv("./web/static/data/EGLL.csv")

df2 = df[['time', 'windDir', 'windSpeed', 'temp', 'dewPoint', 'pressure']]
df = df[['windDir', 'windSpeed', 'temp', 'dewPoint', 'pressure']]
train_df = df[:23000]
test_df = df[23000:]

train_df2 = df2[:23000]
test_df2 = df2[23000:]


class_var = 'windSpeed'
var_types1 = ['linear', 'linear', 'linear', 'linear', 'linear']
var_types2 = ['circular', 'linear', 'linear', 'linear', 'linear']
var_types3 = ['time', 'circular', 'linear', 'linear', 'linear', 'linear']

data1 = Data(train_df, class_var, var_types1, True)
data2 = Data(train_df, class_var, var_types2, True)
data3 = Data(train_df2, class_var, var_types3, True)
tree = Tree()
node1 = tree.tree_grower(data1, 2000)
node2 = tree.tree_grower(data2, 2000)
node3 = tree.tree_grower(data3, 2000)

print 'London'
print('Wind is linear: {}'.format(evaluate_dataset(class_var, node1, test_df)))
print('Wind is circular: {}'.format(evaluate_dataset(class_var, node2, test_df)))
print('Including time: {}'.format(evaluate_dataset(class_var, node3, test_df2)))


df = pandas.read_csv("./web/static/data/YSSY.csv")

df2 = df[['time', 'windDir', 'windSpeed', 'temp', 'dewPoint', 'pressure']]
df = df[['windDir', 'windSpeed', 'temp', 'dewPoint', 'pressure']]
train_df = df[:23000]
test_df = df[23000:]

train_df2 = df2[:23000]
test_df2 = df2[23000:]

class_var = 'windSpeed'
var_types1 = ['linear', 'linear', 'linear', 'linear', 'linear']
var_types2 = ['circular', 'linear', 'linear', 'linear', 'linear']
var_types3 = ['time', 'circular', 'linear', 'linear', 'linear', 'linear']

data1 = Data(train_df, class_var, var_types1, True)
data2 = Data(train_df, class_var, var_types2, True)
data3 = Data(train_df2, class_var, var_types3, True)
tree = Tree()
node1 = tree.tree_grower(data1, 2000)
node2 = tree.tree_grower(data2, 2000)
node3 = tree.tree_grower(data3, 2000)

print 'Sydney'
print('Wind is linear: {}'.format(evaluate_dataset(class_var, node1, test_df)))
print('Wind is circular: {}'.format(evaluate_dataset(class_var, node2, test_df)))
print('Including time: {}'.format(evaluate_dataset(class_var, node3, test_df2)))