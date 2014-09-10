__author__ = 'SmartWombat'

import pandas
from tree_parallel import Tree
from data.data import Data


df = pandas.read_csv("./web/static/data/YSSY.csv")

print df.shape

class_var = 'metar_temp'
var_types = ['linear', 'linear', 'linear', 'circular', 'linear', 'linear', 'linear', 'linear', 'circular', 'linear', 'time', 'date']

data = Data(df, class_var, var_types, True)
tree = Tree()
node = tree.tree_grower(data, 50)

#tree.tree_runner(node, "O")
print tree.tree_to_dict(node, "O")


