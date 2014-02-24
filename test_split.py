__author__ = 'SmartWombat'
import pandas
import numpy as np


def get_value(left_data, right_data, class_var):

    left_cases = float(left_data.shape[0])
    right_cases = float(right_data.shape[0])
    total_cases = left_cases + right_cases
    error_split = (left_cases/total_cases * np.var(left_data[class_var])) + (right_cases/total_cases * np.var(right_data[class_var]))
    error = np.var(left_data.append(right_data)[class_var])

    return error - error_split

a = [1019,1019,1020,1021,1021,1020,1020,1021,1020,1020,1020,1020,1021,1021,1022,1023,1023,1022,1021,1022,1021,1020,1019,1020,1019,1018]
df = pandas.DataFrame(a, columns=['pressure'])
df = df.sort(['pressure'])
df.index = range(0,len(df))

best_index = -1
best_score = 0.0
for index in range(1, df.shape[0]):
    score = get_value(df[:index], df[index:], 'pressure')
    if score > best_score:
        best_score = score
        best_index = index

print(df[:best_index])
print(df[best_index:])
print(best_score)