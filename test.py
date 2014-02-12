import numpy as np
import pandas
from splitter import *
from tree import *


df = pandas.read_csv("/home/roz016/Desktop/data.csv", sep=r",\s+")
df = pandas.read_csv("/home/roz016/Desktop/data.csv")


var_names = ['windDir', 'windSpeed', 'pressure', 'temp', 'dewPoint']
var_types = ['circular', 'linear', 'linear', 'linear', 'linear']
#df = df[var_names]
df = df[['windDir', 'windSpeed']]



tree = Tree('windSpeed', 'linear')
node = tree.tree_grower(df)

tree.tree_runner(node, "O")