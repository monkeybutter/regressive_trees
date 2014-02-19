__author__ = 'SmartWombat'

from data.data import AngularDF
import pandas
from splitter import *
from tree import *
import time
from util import circular_heterogeneity

angular_df = AngularDF(df[3:], pred_var)
angular_df.start = 345
angular_df.end = 50

heterogeneity = circular_heterogeneity(left_ang_df) + circular_heterogeneity(right_ang_df)


df = pandas.read_csv("data.csv")
pred_var = 'angle'

angular_df = AngularDF(df[3:], pred_var)
angular_df.start = 345
angular_df.end = 50

left = angular_df.get_left(3)
right = angular_df.get_right(3)

print left.start
print left.end
print left.df

print right.start
print right.end
print right.df

