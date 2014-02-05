import numpy as np
import pandas
from splitter import *
from tree import *

df = pandas.read_csv("/Users/SmartWombat/Dropbox/Metar/LEVT3H.csv", sep=r",\s+")

print(df.shape)
#print(df.columns)

df = df[['windSpeed','pressure','temp','dewPoint']]
print(df.shape)

result = best_numeric_splitter(df, 'temp', 'dewPoint')
tree = tree_grower(df, 'temp')

print(tree)
print(tree.split_var)
print(tree.left_child.split_var)
print(tree.left_child.left_child.left_child.split_var)

