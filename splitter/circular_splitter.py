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

    def __init__(self):
        r"""Class constructor.

        Initialise the class' attributes. PEP-8 mentions using a leading
        underscore for "internal" names.

        Notes
        -----
        TODO: how best to document class attributes.
        """

        #: Document this instance member.

        super(CircularSplitter, self).__init__()


    def get_split_values(self, df, pred_var, criteria, bearing_a, bearing_b):
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

        #TODO Filter before calling tree
        # Drop NaNs and sort under pred_var values
        df = df[np.isfinite(df[pred_var])]

        if bearing_a == bearing_b:
            #This is the first call to the circular splitter
            #We need to check every split!
            df = df.sort([pred_var])
            df.index = range(0,len(df))
            pass

        else:
            best_till_now = 0
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
                    if new_split_value > best_till_now:
                        best_till_now = new_split_value
                        best_cut_point = (next_pred_value + df[pred_var][index])/2
                        best_index = index

        return best_cut_point, best_till_now, df[:best_index], df[best_index:]
