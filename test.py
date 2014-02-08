import numpy as np
import pandas
from splitter import *
from tree import *

df = pandas.read_csv("/Users/SmartWombat/Dropbox/Metar/LEVT3H.csv", sep=r",\s+")

var_names = ['windDir', 'windSpeed', 'pressure', 'temp', 'dewPoint']
var_types = ['circular', 'linear', 'linear', 'linear', 'linear']
df = df[var_names]



tree = Tree(df, 'windDir', 'circular')
node = tree.tree_grower()

tree.tree_runner(node, "O")

