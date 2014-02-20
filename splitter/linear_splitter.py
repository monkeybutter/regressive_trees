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


    def get_split_values(self, data, pred_var):
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
        data.df = data.df[np.isfinite(data.df[pred_var])]
        data.df = data.df.sort([pred_var])
        data.df.index = range(0,len(data.df))

        #print('Total values {}'.format(data.df.shape[0]))

        best_till_now = 0
        best_cut_point = None
        best_index = None

        for index in range(1, data.df.shape[0]):

            left_data = data.get_left(index, pred_var, 'linear')
            right_data = data.get_right(index, pred_var, 'linear')

            new_split_value = self.criteria.get_value(left_data, right_data)

            if new_split_value > best_till_now:
                best_till_now = new_split_value
                best_index = index


        # sequence indexing is [start_pos:end_pos(excluded)]
        return best_cut_point, best_till_now, data.get_left(best_index, pred_var, 'linear'), data.get_right(best_index, pred_var, 'linear')
