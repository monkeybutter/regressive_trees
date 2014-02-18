import numpy as np
import pandas
from splitter import *
from tree import *
import time
from util import mid_angle
from angular_df.angular_df import AngularDF



def best_split(angular_df):
    criteria = CriteriaFactory('circular', pred_var)
    total_cases = df.shape[0]
    best_score = 0
    best_left = None
    best_right = None
    prev_val = -1
    for index in range(1, total_cases):
        if prev_val != df[pred_var][index]:
            right = angular_df.get_right(index)
            left = angular_df.get_left(index)
            score = criteria.get_value(left, right)
            if score > best_score:
                #print('We have a new winner: {}'.format(score))
                best_score = score
                best_left = left
                best_right = right
            prev_val = angular_df.df[pred_var].iloc[index]

    return best_score, best_left, best_right

def first_run(angular_df):
    total_cases = angular_df.df.shape[0]
    best_score = 0
    best_left = None
    best_right = None
    for index in range(total_cases):
        shifted = angular_df.get_shifted(index)
        print shifted.df
        shifted.start = mid_angle(shifted.df[shifted.var_name].iloc[shifted.df.shape[0]-1], shifted.df[shifted.var_name].iloc[0])
        shifted.end = mid_angle(shifted.df[shifted.var_name].iloc[shifted.df.shape[0]-1], shifted.df[shifted.var_name].iloc[0])
        print shifted.start
        print shifted.end
        score, left_ang_df, right_ang_df = best_split(shifted)
        if score > best_score:
            best_score = score
            best_ang_left = left_ang_df
            best_ang_right = right_ang_df



    print '_______________'
    print best_score
    print best_ang_left.df
    print best_ang_left.start
    print best_ang_left.end
    print best_ang_right.df
    print best_ang_right.start
    print best_ang_right.end

df = pandas.read_csv("data.csv")
pred_var = 'angle'
df = df.sort([pred_var])
df.index = range(0,len(df))

angular_df = AngularDF(df, pred_var)

first_run(angular_df)

#print(df)
"""
df = df.sort([pred_var])
df.index = range(0,len(df))
total_cases = df.shape[0]
prev_val = -1
best_score = 0
best_left_df = None
best_right_df = None
for index in range(total_cases):
    if prev_val != df[pred_var][index]:
        df = [df[index:], df[:index]]
        #df.index = range(0,len(df))
        score, left_df, right_df = best_split(df, pred_var)
        if score > best_score:
            best_score = score
            best_left_df = [left_df]
            best_right_df = [right_df]

        prev_val = df[pred_var][index]


print best_left_df, best_right_df
"""


"""
right_df = df[index:]
if index < total_cases-1:
    next_pred_value = df[pred_var][index+1]
else:
    next_pred_value = df[pred_var][index]

if next_pred_value != df[pred_var][index]:
    print df.angle[index]
    #new_split_value = criteria.get_value(left_df, right_df)
"""

"""
df = pandas.read_csv("/home/roz016/Desktop/data.csv", sep=r",\s+")
df = pandas.read_csv("/home/roz016/Desktop/data.csv")


var_names = ['windDir', 'windSpeed', 'pressure', 'temp', 'dewPoint']
var_types = ['circular', 'linear', 'linear', 'linear', 'linear']
#df = df[var_names]
df = df[['windDir', 'windSpeed']]



tree = Tree('windSpeed', 'linear')
node = tree.tree_grower(df)

tree.tree_runner(node, "O")
"""