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
        self.left_child = None
        self.right_child = None

    def get_name(self):
        return 'Node'

class Leaf(object):
    def __init__(self):

        self.value = None
        self.members = None

    def get_name(self):
        return 'Leaf'

class Tree(object):

    def __init__(self, df=None, class_var=None, class_type=None):

        self.df = df
        self.class_type = class_type
        self.class_var = class_var

    def tree_grower(self):

        criteria = CriteriaFactory(self.class_type, self.class_var)
        print(criteria)

        tree = Node()

        best_var = None
        best_value = None
        best_score = 0.0
        best_left_df = None
        best_right_df = None
        for variable in self.df.columns:
            if variable != self.class_var:
                splitter = SplitterFactory('linear', criteria)
                value, score, left_df, right_df = splitter.get_split_values(self.df, variable)
                if score > best_score:
                    best_var = variable
                    best_value = value
                    best_score = score
                    best_left_df = left_df
                    best_right_df = right_df
        tree.split_var = best_var
        tree.split_value = best_value
        tree.score = best_score
        if best_left_df.shape[0]>350 and np.var(best_left_df[self.class_var])!=0.0 and np.var(best_left_df[best_var])!=0.0:
            tree.left_child = self.tree_grower(best_left_df, self.class_var)
        else:
            left_leaf = Leaf()
            left_leaf.value = np.mean(best_left_df[self.class_var])
            left_leaf.members = best_left_df.shape[0]
            tree.left_child = left_leaf

        if best_right_df.shape[0]>350 and np.var(best_right_df[self.class_var])!=0.0 and np.var(best_right_df[best_var])!=0.0:
            tree.right_child = self.tree_grower(best_right_df, self.class_var)
        else:
            right_leaf = Leaf()
            right_leaf.value = np.mean(best_right_df[self.class_var])
            right_leaf.members = best_right_df.shape[0]
            tree.right_child = right_leaf

        return tree

    def tree_runner(self, tree, track):
        print(track)
        print(tree.split_var)
        print(tree.split_value)
        print(tree.score)

        if tree.left_child != None:
            print tree.left_child.get_name()
            if tree.left_child.get_name() == 'Node':
                self.tree_runner(tree.left_child, track+'L')
            elif tree.left_child.get_name() == 'Leaf':
                print(track+'Lx')
                print(tree.left_child.value)
                print(tree.left_child.members)

        if tree.right_child != None:
            print tree.left_child.get_name()
            if tree.right_child.get_name() == 'Node':
                self.tree_runner(tree.right_child, track+'R')
            elif tree.right_child.get_name() == 'Leaf':
                print(track+'Rx')
                print(tree.right_child.value)
                print(tree.right_child.members)