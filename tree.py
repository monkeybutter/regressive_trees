__author__ = 'SmartWombat'

import numpy as np
from splitter import *


class node(object):
    def __init__(self):
        """

        :rtype : object
        """
        self.split_var = None
        self.split_value = None
        self.score = None
        self.left_child = None
        self.right_child = None


def tree_grower(df, class_var):

    tree = node()

    best_var = None
    best_value = None
    best_score = 0.0
    best_left_df = None
    best_right_df = None
    for variable in df.columns:
        if variable != class_var:
            value, score, left_df, right_df = best_numeric_splitter(df, class_var, variable)
        if score > best_score:
            best_var = variable
            best_value = value
            best_score = score
            best_left_df = left_df
            best_right_df = right_df
    tree.split_var = best_var
    tree.split_value = best_value
    tree.score = best_score
    if best_left_df.shape[0]>350:
        tree.left_child = tree_grower(best_left_df, class_var)
    if best_right_df.shape[0]>350:
        tree.right_child = tree_grower(best_right_df, class_var)

    return tree