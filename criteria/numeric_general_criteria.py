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


    def get_value(self, data, left_data, right_data):
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
        left_cases = float(left_data.df.shape[0])
        right_cases = float(right_data.df.shape[0])
        total_cases = left_cases + right_cases
        error_split = (left_cases/total_cases * np.var(left_data.df[self.class_var])) + (right_cases/total_cases * np.var(right_data.df[self.class_var]))
        #error_split = (left_cases/total_cases * left_data.df[self.class_var].var) + (right_cases/total_cases * right_data.df[self.class_var].var)
        error = np.var(data.df[self.class_var])

        return error - error_split