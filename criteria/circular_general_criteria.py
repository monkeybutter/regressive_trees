__author__ = 'SmartWombat'

import numpy as np
from criteria import Criteria
from util import circular_heterogeneity,mid_angle
import sys

class CircularRegressionCriteria(Criteria):

    """ **Synopsis** ::

            todo = TODO()  # a brief example of using the CLASS
            todo.method()

        **Description**

        Implementation of the Extractor class

        **Copyright**

            Copyright (c) 2014 by MonkeyButter
    """
    source = 'circular'
    class_var = None

    __class_description__ = """Basic criteria for measuring split quality in regression trees with circular data"""

    __version__ = 0.1

    def __init__(self, class_var):
        r"""Class constructor.

        Initialise the class' attributes. PEP-8 mentions using a leading
        underscore for "internal" names.

        Notes
        -----
        TODO: how best to document class attributes.
        """

        #: Document this instance member.

        super(CircularRegressionCriteria, self).__init__(class_var)


    def get_value(self, left_ang_df, right_ang_df):
        r"""Returns a value with the average height of crop

        Returns
        -------
        float
            Average height of crop

        Raises
        ------
        NotImplementedError
            If the function hasn't been implemented yet.
        """

        heterogeneity = circular_heterogeneity(left_ang_df) + circular_heterogeneity(right_ang_df)

        if heterogeneity == 0.0:
            return sys.float_info.max
        else:
            return 1.0/heterogeneity


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
