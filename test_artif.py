__author__ = 'SmartWombat'

import pandas
from tree import Tree
from data.data import Data
import pprint


df = pandas.read_csv("./web/static/data/temp.csv")
#df = df.drop(['Unnamed: 0', 'time_of_day', 'day_of_year'], axis=1)
#df = df.drop(['Unnamed: 0', 'time', 'date'], axis=1)

var_types = ['date', 'time', 'linear']
#var_types = ['linear', 'linear', 'linear']
data = Data(df, "temperature", var_types, True)
tree = Tree()
node = tree.tree_grower(data, 2500)
pprint.pprint(tree.tree_to_dict(node, "O"))








