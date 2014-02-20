__author__ = 'SmartWombat'

import numpy as np
from splitter import *
from splitter_factory import SplitterFactory
from criteria_factory import CriteriaFactory

class Node(object):
    def __init__(self):

        self.split_var = None
        self.split_value = None
        self.score = None
        self.members = None
        self.left_child = None
        self.right_child = None

    def get_name(self):
        return 'Node'

class Leaf(object):
    def __init__(self):

        self.value = None
        self.members = None
        self.start = None
        self.end = None

    def get_name(self):
        return 'Leaf'

class Tree(object):

    #def __init__(self):


    def tree_grower(self, data):

        criteria = CriteriaFactory(data.class_type, data.class_var)

        data.df = data.df[np.isfinite(data.df[data.class_var])]

        node = Node()

        best_var = None
        best_value = None
        best_score = 0.0
        best_left = None
        best_right = None

        for variable, dict in data.var_limits.iteritems():
            splitter = SplitterFactory(dict['type'], criteria)
            value, score, left_df, right_df = splitter.get_split_values(data, variable)
            if score > best_score:
                best_var = variable
                best_value = value
                best_score = score
                best_left = left_df
                best_right = right_df
        node.split_var = best_var
        node.split_value = best_value
        node.score = best_score
        node.members = data.df.shape[0]
        if best_left.df.shape[0]>10 and np.var(best_left.df[data.class_var])!=0.0 and np.var(best_left.df[best_var])!=0.0:
            node.left_child = self.tree_grower(best_left)
        else:
            left_leaf = Leaf()
            left_leaf.value = np.mean(best_left.df[data.class_var])
            left_leaf.start = best_left.var_limits[best_var]['start']
            left_leaf.end = best_left.var_limits[best_var]['end']
            left_leaf.members = best_left.df.shape[0]
            node.left_child = left_leaf

        if best_right.df.shape[0]>10 and np.var(best_right.df[data.class_var])!=0.0 and np.var(best_right.df[best_var])!=0.0:
            node.right_child = self.tree_grower(best_right)
        else:
            right_leaf = Leaf()
            right_leaf.value = np.mean(best_right.df[data.class_var])
            right_leaf.start = best_right.var_limits[best_var]['start']
            right_leaf.end = best_right.var_limits[best_var]['end']
            right_leaf.members = best_right.df.shape[0]
            node.right_child = right_leaf

        return node

    def tree_runner(self, tree, track):
        print(track)
        print(tree.split_var)
        print(tree.split_value)
        print(tree.score)
        print(tree.members)

        if tree.left_child != None:
            print tree.left_child.get_name()
            if tree.left_child.get_name() == 'Node':
                self.tree_runner(tree.left_child, track+'L')
            elif tree.left_child.get_name() == 'Leaf':
                print(track+'Lx')
                print(tree.left_child.value)
                print(tree.left_child.members)
                print('start: {}'.format(tree.left_child.start))
                print('end: {}'.format(tree.left_child.end))


        if tree.right_child != None:
            print tree.right_child.get_name()
            if tree.right_child.get_name() == 'Node':
                self.tree_runner(tree.right_child, track+'R')
            elif tree.right_child.get_name() == 'Leaf':
                print(track+'Rx')
                print(tree.right_child.value)
                print(tree.right_child.members)
                print('start: {}'.format(tree.right_child.start))
                print('end: {}'.format(tree.right_child.end))