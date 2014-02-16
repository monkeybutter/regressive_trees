import numpy as np
import pandas
from splitter import *
from tree import *
import time
from util import mid_angle



def best_split(df, pred_var):
    criteria = CriteriaFactory('circular', pred_var)
    total_cases = df.shape[0]
    best_score = 0
    best_index = 0
    prev_val = -1
    for index in range(1, total_cases):
        if prev_val != df[pred_var][index]:
            score = criteria.get_value(df[:index], df[index:])
            if score > best_score:
                #print('We have a new winner: {}'.format(score))
                best_score = score
                best_index = index
            prev_val = df[pred_var][index]

    return best_score, df[:best_index], df[best_index:]

def first_run(df, pred_var):
    df = df.sort([pred_var])
    df.index = range(0,len(df))
    total_cases = df.shape[0]
    best_score = 0
    best_left = None
    best_right = None
    for index in range(total_cases):
        #df = pandas.concat([df[index:], df[:index]])
        #df = df[index:].append(df[:index]).copy(deep=True)
        #df.index = range(0,df.shape[0])
        #df.index = range(0,df.shape[0])
        #print('Best split called: {}'.format(df[index:].append(df[:index])))
        score, left_df, right_df = best_split(df[index:].append(df[:index]), pred_var)
        #print('score received: {}'.format(score))
        if score > best_score:
            best_score = score
            best_left = left_df
            best_right = right_df

            #print best_score
            #print best_left.angle
            #print best_right.angle

    print '_______________'
    print best_score
    print best_right
    print best_left
    print mid_angle(best_left[pred_var].max(), best_right[pred_var].min())
    print mid_angle(best_right[pred_var].max(), best_left[pred_var].min())

df = pandas.read_csv("data.csv")
pred_var = 'angle'


#print circular_heterogeneity(df.angle[:12])
#print circular_heterogeneity(df.angle[12:])

uno = [100, 101, 101, 102, 102]
dos = [0, 1, 2]


first_run(df, pred_var)

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