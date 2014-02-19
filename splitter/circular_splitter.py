__author__ = 'SmartWombat'

import numpy as np
from splitter import Splitter
from util import *

class CircularSplitter(Splitter):

    """ **Synopsis** ::

            todo = TODO()  # a brief example of using the CLASS
            todo.method()

        **Description**

        Implementation of the Extractor class

        **Copyright**

            Copyright (c) 2014 by MonkeyButter
    """
    source = 'circular'
    __class_description__ = """Basic splitter for circular data"""
    __version__ = 0.1

    def __init__(self, criteria):
        r"""Class constructor.

        Initialise the class' attributes. PEP-8 mentions using a leading
        underscore for "internal" names.

        Notes
        -----
        TODO: how best to document class attributes.
        """

        #: Document this instance member.

        super(CircularSplitter, self).__init__(criteria)


    def get_split_values(self, data, pred_var):
        r"""Returns a value

        Returns
        -------
        float

        """

        #TODO Filter before calling tree


        # This case comprises the first call to a
        if data.var_limits['pred_var']['start'] == None or data.var_limits['pred_var']['end'] == None:
            pass

        if bearing_a == bearing_b:
            #This is the first call to the circular splitter
            #We need to check every split!
            df = df.sort([pred_var])
            df.index = range(0,len(df))
            total_cases = df.shape[0]
            for index in range(1, total_cases):
                pass

        else:
            best_split_value = 0
            best_cut_point = None
            best_index = None
            df = sort_in_arc(df, bearing_a, bearing_b, pred_var)
            total_cases = df.shape[0]
            for index in range(1, total_cases):
                left_df = df[:index]
                right_df = df[index:]
                if index < total_cases-1:
                    next_pred_value = df[pred_var][index+1]
                else:
                    next_pred_value = df[pred_var][index]

                if next_pred_value != df[pred_var][index]:
                    new_split_value = criteria.get_value(left_df, right_df)
                    if new_split_value > best_split_value:
                        best_split_value = new_split_value
                        best_cut_point = (next_pred_value + df[pred_var][index])/2.0
                        best_index = index

        # Test if returning parts of df and not new instances could affect the results
        # sequence indexing is [start_pos:end_pos(excluded)]
        return best_cut_point, best_split_value, df[:best_index+1], df[best_index+1:]


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
