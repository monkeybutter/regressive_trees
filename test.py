import numpy as np
import pandas
from splitter import *
from tree import *


df = pandas.read_csv("/Users/SmartWombat/Desktop/LEVT3H.csv", sep=r",\s+")

var_names = ['windDir', 'windSpeed', 'pressure', 'temp', 'dewPoint']
var_types = ['circular', 'linear', 'linear', 'linear', 'linear']
#df = df[var_names]
df = df[['windDir', 'pressure']]



tree = Tree('windDir', 'circular')
node = tree.tree_grower(df)

tree.tree_runner(node, "O")