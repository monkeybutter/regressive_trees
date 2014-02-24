__author__ = 'SmartWombat'

import pandas
from tree import *
from util import mid_angle
from data.data import Data


df = pandas.read_csv("data.csv")

df = df[['windDir', 'windSpeed', 'temp', 'dewPoint', 'pressure']]
#df = df[['windSpeed', 'temp', 'dewPoint', 'pressure']]
#df = df[['windDir', 'currentDir']]


class_var = 'windSpeed'
var_types = ['circular', 'linear', 'linear', 'linear', 'linear']
df = df.sort([class_var])
df.index = range(0,len(df))

data = Data(df, class_var, var_types)
tree = Tree()
node = tree.tree_grower(data)
tree.tree_runner(node, "O")



