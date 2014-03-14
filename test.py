__author__ = 'SmartWombat'

import pandas
from util import time_to_angle, date_to_angle
from datetime import datetime
from tree import *
import numpy as np
from data.data import Data


df = pandas.read_csv("./web/static/data/LEVTdatetime.csv")

df = df[['date', 'time', 'windDir', 'windSpeed', 'temp', 'dewPoint', 'pressure']]
#df = df[['windSpeed', 'temp', 'dewPoint', 'pressure']]
#df = df[['windDir', 'currentDir']]


class_var = 'windSpeed'
var_types = ['date', 'time', 'circular', 'linear', 'linear', 'linear', 'linear']
#df = df[np.isfinite(df[class_var])]
#df = df.sort([class_var])
#df.index = range(0, len(df))

data = Data(df, class_var, var_types, True)
tree = Tree()
node = tree.tree_grower(data, 3000)

#tree.tree_runner(node, "O")
print tree.tree_to_dict(node, "O")

