__author__ = 'SmartWombat'

import pandas
from tree import *
from util import mid_angle
from data.data import Data


df = pandas.read_csv("data.csv")


#print df.head(10)

#df = df[['angle', 'value']]

class_var = 'value'
var_types = ['linear', 'linear']
df = df.sort([class_var])
df.index = range(0,len(df))


data = Data(df, class_var, var_types)

tree = Tree()
node = tree.tree_grower(data)

tree.tree_runner(node, "O")



