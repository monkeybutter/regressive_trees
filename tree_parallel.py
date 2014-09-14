__author__ = 'SmartWombat'

import numpy as np
import json
from splitter_factory import SplitterFactory
from criteria_factory import CriteriaFactory
from util import angle_to_time, angle_to_date, circular_mean
from datetime import date, time
from multiprocessing import Process, Manager

class Node(object):
    def __init__(self):

        self.split_var = None
        self.var_type = None
        self.score = None
        self.members = None
        self.split_values = None
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

    def tree_grower(self, data, min_leaf):

        criteria = CriteriaFactory(data.class_type, data.class_var)

        data.df = data.df[np.isfinite(data.df[data.class_var])]

        node = Node()

        best_var = None
        best_score = 0.0
        best_left = None
        best_right = None

        processes = []
        manager = Manager()
        queue = manager.Queue()

        for variable, dic in data.var_limits.iteritems():
            splitter = SplitterFactory(dic['type'], criteria)
            p = Process(target=splitter.get_split_values_queue, args=(queue, data, variable, dic['type']))
            processes.append(p)
            p.start()

        # Wait for all processes to finish
        for p in processes:
            p.join()

        for _ in processes:
            variable, type_var, score, left_df, right_df = queue.get()
            if score > best_score:
                best_var = variable
                best_type = type_var
                best_score = score
                best_left = left_df
                best_right = right_df

        #print("Best var: " + best_var + " type " + best_type)

        node.split_var = best_var
        node.var_type = best_type
        node.split_values = best_left.var_limits[best_var]['start'], best_left.var_limits[best_var]['end'], best_right.var_limits[best_var]['start'], best_right.var_limits[best_var]['end']
        node.score = best_score
        node.members = data.df.shape[0]

        if best_left.df.shape[0]>min_leaf and np.var(best_left.df[data.class_var])!=0.0 and np.var(best_left.df[best_var])!=0.0:
            node.left_child = self.tree_grower(best_left,min_leaf)
        else:
            left_leaf = Leaf()
            #left_leaf.value = np.mean(best_left.df[data.class_var])
            left_leaf.value = self._get_leaf_value(best_left)
            left_leaf.members = best_left.df.shape[0]
            node.left_child = left_leaf

        if best_right.df.shape[0]>min_leaf and np.var(best_right.df[data.class_var])!=0.0 and np.var(best_right.df[best_var])!=0.0:
            node.right_child = self.tree_grower(best_right,min_leaf)
        else:
            right_leaf = Leaf()
            #right_leaf.value = np.mean(best_right.df[data.class_var])
            right_leaf.value = self._get_leaf_value(best_right)
            right_leaf.members = best_right.df.shape[0]
            node.right_child = right_leaf

        return node

    def _get_leaf_value(self, data):
        if data.class_type == 'linear':
            return np.mean(data.df[data.class_var])
        elif data.class_type == 'circular':
            return circular_mean(data)
        elif data.class_type == 'date':
            print circular_mean(data)
            print angle_to_date(circular_mean(data))
            return angle_to_date(circular_mean(data))
        elif data.class_type == 'time':
            print circular_mean(data)
            print angle_to_time(circular_mean(data))
            return angle_to_time(circular_mean(data))
        else:
            raise Exception

    def tree_runner(self, tree, track):
        print('Node location: {}'.format(track))
        print('Split variable: {}'.format(tree.split_var))
        print('Split values: {}'.format(tree.split_value))
        print('Split score: {}'.format(tree.score))
        print('Node members: {}'.format(tree.members))

        if tree.left_child != None:
            if tree.left_child.get_name() == 'Node':
                self.tree_runner(tree.left_child, track+'L')
            elif tree.left_child.get_name() == 'Leaf':
                print('Leaf location: {}'.format(track+'Lx'))
                print('Leaf members: {}'.format(tree.left_child.members))
                print('Value {}'.format(tree.left_child.value))


        if tree.right_child != None:
            print tree.right_child.get_name()
            if tree.right_child.get_name() == 'Node':
                self.tree_runner(tree.right_child, track+'R')
            elif tree.right_child.get_name() == 'Leaf':
                print('Leaf location: {}'.format(track+'Rx'))
                print('Leaf members: {}'.format(tree.right_child.members))
                print('Value {}'.format(tree.right_child.value))

    def tree_to_dict(self, tree, track):
        tree_dict = {}
        tree_dict['name'] = track
        tree_dict['var_name'] = tree.split_var
        tree_dict['var_type'] = tree.var_type
        tree_dict['var_limits'] = tree.split_values
        if tree.var_type == 'time':
            tree_dict['var_limits'] = angle_to_time(tree.split_values[0]).strftime("%H:%M"), angle_to_time(tree.split_values[1]).strftime("%H:%M"), angle_to_time(tree.split_values[2]).strftime("%H:%M"), angle_to_time(tree.split_values[3]).strftime("%H:%M")
        elif tree.var_type == 'date':
            tree_dict['var_limits'] = angle_to_date(tree.split_values[0]).strftime("%b %d"), angle_to_date(tree.split_values[1]).strftime("%b %d"), angle_to_date(tree.split_values[2]).strftime("%b %d"), angle_to_date(tree.split_values[3]).strftime("%b %d")
        else:
            tree_dict['var_limits'] = tree.split_values
        tree_dict['children'] = []

        if tree.left_child != None:
            if tree.left_child.get_name() == 'Node':
                #tree_dict['var_name'] = tree.left_child.split_var
                tree_dict['children'].append(self.tree_to_dict(tree.left_child, track+'L'))
            elif tree.left_child.get_name() == 'Leaf':
                leaf = {}
                leaf['name'] = track+'L'
                leaf['members'] = tree.left_child.members
                if isinstance(tree.left_child.value, float):
                    leaf['value'] = '{0:.2f}'.format(tree.left_child.value)
                if isinstance(tree.left_child.value, time):
                    leaf['value'] = tree.left_child.value.strftime('%H:%M')
                if isinstance(tree.left_child.value, date):
                    leaf['value'] = tree.left_child.value.strftime('%b %d')
                tree_dict['children'].append(leaf)


        if tree.right_child != None:
            if tree.right_child.get_name() == 'Node':
                #tree_dict['var_name'] = tree.right_child.split_var
                tree_dict['children'].append(self.tree_to_dict(tree.right_child, track+'R'))
            elif tree.right_child.get_name() == 'Leaf':
                leaf = {}
                leaf['name'] = track+'R'
                leaf['members'] = tree.right_child.members
                if isinstance(tree.right_child.value, float):
                    leaf['value'] = '{0:.2f}'.format(tree.right_child.value)
                if isinstance(tree.right_child.value, time):
                    leaf['value'] = tree.right_child.value.strftime('%H:%M')
                if isinstance(tree.right_child.value, date):
                    leaf['value'] = tree.right_child.value.strftime('%b %d')
                tree_dict['children'].append(leaf)

        return json.dumps(tree_dict).replace("\"{", "{").replace("}\"", "}").replace("\\", "")