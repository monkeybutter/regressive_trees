__author__ = 'SmartWombat'

import pandas
from tree import *
from util import mid_angle
from data.data import Data


df = pandas.read_csv("/Users/SmartWombat/Desktop/LEVT.csv")


#print df.head(10)

df = df[['windSpeed', 'temp', 'dewPoint', 'pressure']]

pred_var = 'temp'
var_types = ['linear', 'linear', 'linear', 'linear']
df = df.sort([pred_var])
df.index = range(0,len(df))


data = Data(df, pred_var, var_types)

tree = Tree()

tree.tree_grower(data)


