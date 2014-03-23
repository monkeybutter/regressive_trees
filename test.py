__author__ = 'SmartWombat'

import pandas
from tree import Tree
from data.data import Data


df = pandas.read_csv("./web/static/data/YSSY.csv")

df = df[['date', 'time', 'windDir', 'windSpeed', 'temp', 'dewPoint', 'pressure']]
df = df[:10000]
#df = df[:10000:20]

print df.shape
#df = df[['windDir', 'windSpd', 'temp']]



class_var = 'temp'
#var_types = ['circular', 'linear', 'linear', 'linear', 'linear']
var_types = ['date', 'time', 'circular', 'linear', 'linear', 'linear', 'linear']
#var_types = ['circular', 'linear', 'linear']

data = Data(df, class_var, var_types, True)
tree = Tree()
node = tree.tree_grower(data, 50)

#tree.tree_runner(node, "O")
print tree.tree_to_dict(node, "O")


