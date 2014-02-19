__author__ = 'SmartWombat'

import numpy as np
from criteria import Criteria

class BasicRegressionCriteria(Criteria):

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

    def __init__(self, class_var):
        r"""Class constructor.

        Initialise the class' attributes. PEP-8 mentions using a leading
        underscore for "internal" names.

        Notes
        -----
        TODO: how best to document class attributes.
        """

        #: Document this instance member.

        super(BasicRegressionCriteria, self).__init__(class_var)


    def get_value(self, left_data, right_data):
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
        if left_data.df != None:
            left_cases = left_data.df.shape[0]
            left_y_sum = np.sum(left_data.df[self.class_var])
        else:
            left_cases = 1
            left_y_sum = 0.0

        if right_data.df != None:
            right_cases = right_data.df.shape[0]
            right_y_sum = np.sum(right_data.df[self.class_var])
        else:
            right_cases = 1
            right_y_sum = 0.0

        return (left_y_sum**2/left_cases) + (right_y_sum**2/right_cases)
