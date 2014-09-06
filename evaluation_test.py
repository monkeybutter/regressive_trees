__author__ = 'SmartWombat'

import pandas
import random
import numpy as np
from tree import Tree
from evaluator import evaluate_dataset, _evaluate_value
from data.data import Data

for i in range(20):

    df = pandas.read_csv("./web/static/data/egll.csv")
    df = df[[u'metar_press', u'metar_rh', u'metar_temp', u'metar_wind_dir', u'metar_wind_spd', u'gfs_press', u'gfs_rh', u'gfs_temp', u'gfs_wind_dir', u'gfs_wind_spd', u'time', u'date']]

    rows = random.sample(df.index, 23000)
    train_df = df.ix[rows]
    test_df = df.drop(rows)

    3#train_df2 = train_df[['windDir', 'windSpeed', 'temp', 'dewPoint', 'pressure']]
    test_df2 = test_df[['windDir', 'windSpeed', 'temp', 'dewPoint', 'pressure']]

    class_var = 'time'
    #var_types1 = ['linear', 'linear', 'linear', 'linear', 'linear']
    #var_types2 = ['circular', 'linear', 'linear', 'linear', 'linear']
    var_types3 = ['time', 'circular', 'linear', 'linear', 'linear', 'linear']

    #data1 = Data(train_df2, class_var, var_types1, True)
    #data2 = Data(train_df2, class_var, var_types2, True)
    data3 = Data(train_df, class_var, var_types3, True)
    tree = Tree()
    #node1 = tree.tree_grower(data1, 2000)
    #node2 = tree.tree_grower(data2, 2000)
    node3 = tree.tree_grower(data3, 2000)

    print 'London'
    #print('Wind is linear: {}'.format(evaluate_dataset(class_var, node1, test_df2)))
    #print('Wind is circular: {}'.format(evaluate_dataset(class_var, node2, test_df2)))
    print('Including time: {}'.format(evaluate_dataset(class_var, node3, test_df)))

"""
    df = pandas.read_csv("./web/static/data/YSSY.csv")
    df = df[['time', 'windDir', 'windSpeed', 'temp', 'dewPoint', 'pressure']]

    rows = random.sample(df.index, 23000)
    train_df = df.ix[rows]
    test_df = df.drop(rows)

    train_df2 = train_df[['windDir', 'windSpeed', 'temp', 'dewPoint', 'pressure']]
    test_df2 = test_df[['windDir', 'windSpeed', 'temp', 'dewPoint', 'pressure']]

    class_var = 'pressure'
    var_types1 = ['linear', 'linear', 'linear', 'linear', 'linear']
    var_types2 = ['circular', 'linear', 'linear', 'linear', 'linear']
    var_types3 = ['time', 'circular', 'linear', 'linear', 'linear', 'linear']

    data1 = Data(train_df2, class_var, var_types1, True)
    data2 = Data(train_df2, class_var, var_types2, True)
    data3 = Data(train_df, class_var, var_types3, True)
    tree = Tree()
    node1 = tree.tree_grower(data1, 2000)
    node2 = tree.tree_grower(data2, 2000)
    node3 = tree.tree_grower(data3, 2000)

    print 'Sydney'
    print('Wind is linear: {}'.format(evaluate_dataset(class_var, node1, test_df2)))
    print('Wind is circular: {}'.format(evaluate_dataset(class_var, node2, test_df2)))
    print('Including time: {}'.format(evaluate_dataset(class_var, node3, test_df)))
"""