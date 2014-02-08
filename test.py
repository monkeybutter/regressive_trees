import numpy as np
import pandas
from splitter import *
from tree import *

df = pandas.read_csv("/Users/SmartWombat/Dropbox/Metar/LEVT3H.csv", sep=r",\s+")

print(df.shape)
#print(df.columns)

df = df[['windDir','windSpeed','pressure','temp','dewPoint']]
print(df.shape)

#result = linear_generic_splitter(df, 'temp', 'dewPoint')
tree = tree_grower(df, 'windDir')

tree_runner(tree, "O")

