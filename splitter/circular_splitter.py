__author__ = 'SmartWombat'

import numpy as np
from splitter import Splitter
from util import mid_angle, sort_in_arc

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

        if data.var_limits[pred_var]['start'] == None or data.var_limits[pred_var]['end'] == None:
            return self._first_run(data, pred_var)

        else:
            data.df = sort_in_arc(data.df, data.var_limits[pred_var]['start'], data.var_limits[pred_var]['end'], pred_var)
            return self._get_split_values(data, pred_var)


    def _get_split_values(self, data, pred_var):

        #TODO Filter before calling tree
        # Drop NaNs and sort under pred_var values
        #data.df = data.df[np.isfinite(data.df[pred_var])]
        #data.df = data.df.sort([pred_var])
        #data.df.index = range(0,len(data.df))

        best_score = 0
        best_index = None

        prev_val = data.df[pred_var].iloc[1]

        for index in range(1, data.df.shape[0]-1):
            if prev_val != data.df[pred_var].iloc[index]:

                left_data = data.get_left(index, pred_var, 'circular')
                right_data = data.get_right(index, pred_var, 'circular')

                score = self.criteria.get_value(left_data, right_data)

                if score > best_score:
                    best_score = score
                    best_index = index

                prev_val = data.df[pred_var].iloc[index]

        # sequence indexing is [start_pos:end_pos(excluded)]
        return best_score, data.get_left(best_index, pred_var, 'circular'), data.get_right(best_index, pred_var, 'circular')


    def _first_run(self, data, pred_var):
        best_score = 0
        best_left = None
        best_right = None

        data.df = data.df[np.isfinite(data.df[pred_var])]
        data.df = data.df.sort([pred_var])
        data.df.index = range(0,len(data.df))

        shifter = self._shif_data(data, pred_var)

        for shifted in shifter:

            shifted.var_limits[pred_var]['start'] = mid_angle(shifted.df[pred_var].iloc[shifted.df.shape[0]-1], shifted.df[pred_var].iloc[0])
            shifted.var_limits[pred_var]['end'] = mid_angle(shifted.df[pred_var].iloc[shifted.df.shape[0]-1], shifted.df[pred_var].iloc[0])
            score, left_ang_df, right_ang_df = self._get_split_values(shifted, pred_var)
            if score > best_score:
                best_score = score
                best_left = left_ang_df
                best_right = right_ang_df

        return best_score, best_left, best_right


    def _shif_data(self, data, pred_var):

        # TODO change -1 for None (more elegant)
        shifted_data = data.get_copy()
        prev_element = -1

        for i in range(data.df.shape[0]):
            if data.df[pred_var][i] != prev_element:
                shifted_data.df = data.df[i:].append(data.df[:i])
                yield shifted_data
            prev_element = data.df[pred_var][i]
