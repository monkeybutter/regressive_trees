import numpy as np
import pandas
from splitter import find_best_splitter

df = pandas.read_csv("/Users/SmartWombat/Dropbox/Metar/LEVT3H.csv", sep=r",\s+")

print(type(df))
print(df.shape)


print(find_best_splitter(df, 'temp', 'dewPoint'))
