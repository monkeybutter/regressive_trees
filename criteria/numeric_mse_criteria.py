__author__ = 'SmartWombat'

import numpy as np
from criteria import Criteria

class MSERegressionCriteria(Criteria):

    """ **Synopsis** ::

            todo = TODO()  # a brief example of using the CLASS
            todo.method()

        **Description**

        Implementation of the Extractor class

        **Copyright**

            Copyright (c) 2014 by MonkeyButter
    """
    source = 'mse_regression'
    __class_description__ = """Mean squared error impurity criterion.
                               MSE = var_left + var_right"""
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

        super(MSERegressionCriteria, self).__init__()


    def get_value(self, left_df, right_df, class_var):
        r"""
        Returns
        -------
        float
            MSE
        """

        return np.var(left_df[class_var]) + np.var(right_df[class_var])
