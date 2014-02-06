__author__ = 'SmartWombat'

import numpy as np
from splitter import *


class node(object):
    def __init__(self):

        self.split_var = None
        self.split_value = None
        self.score = None
        self.left_child = None
        self.right_child = None

    def _get_name(self):
        return 'node'

class leaf(object):
    def __init__(self):

        self.value = None
        self.members = None

    def _get_name(self):
        return 'leaf'


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
    else:
        left_leaf = leaf()
        left_leaf.value = np.mean(best_left_df[class_var])
        left_leaf.members = best_left_df.shape[0]
        tree.left_child = left_leaf

    if best_right_df.shape[0]>350:
        tree.right_child = tree_grower(best_right_df, class_var)
    else:
        right_leaf = leaf()
        right_leaf.value = np.mean(best_right_df[class_var])
        right_leaf.members = best_right_df.shape[0]
        tree.right_child = right_leaf

    return tree

def tree_runner(tree, track):
    print(track)
    print(tree.split_var)
    print(tree.split_value)
    print(tree.score)

    if tree.left_child != None:
        print tree.left_child._get_name()
        if tree.left_child._get_name() == 'node':
            tree_runner(tree.left_child, track+'L')
        elif tree.left_child._get_name() == 'leaf':
            print(track+'Lx')
            print(tree.left_child.value)
            print(tree.left_child.members)

    if tree.right_child != None:
        print tree.left_child._get_name()
        if tree.right_child._get_name() == 'node':
            tree_runner(tree.right_child, track+'R')
        elif tree.right_child._get_name() == 'leaf':
            print(track+'Rx')
            print(tree.right_child.value)
            print(tree.right_child.members)