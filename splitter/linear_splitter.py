__author__ = 'SmartWombat'

import numpy as np
from splitter import Splitter

class LinearSplitter(Splitter):

    """ **Synopsis** ::

            todo = TODO()  # a brief example of using the CLASS
            todo.method()

        **Description**

        Implementation of the Extractor class

        **Copyright**

            Copyright (c) 2014 by MonkeyButter
    """
    source = 'linear'
    __class_description__ = """Basic criteria for measuring split quality in regression trees"""
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

        super(LinearSplitter, self).__init__(criteria)


    def get_split_values(self, df, pred_var):
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



        df = df.sort([pred_var])
        df.index = range(0,len(df))

        total_cases = df.shape[0]

        best_till_now = 0
        best_cut_point = None
        best_index = None

        for index in range(1, df.shape[0]):

            left_df = df[:index]
            right_df = df[index:]

            if index < total_cases-1:
                next_pred_value = df[pred_var][index+1]
            else:
                next_pred_value = df[pred_var][index]

            if next_pred_value != df[pred_var][index]:
                new_split_value = self.criteria.get_value(left_df, right_df)
                print(new_split_value)
                if new_split_value > best_till_now:
                    best_till_now = new_split_value
                    best_cut_point = (next_pred_value + df[pred_var][index])/2
                    best_index = index

        return best_cut_point, best_till_now, df[:best_index], df[best_index:]
