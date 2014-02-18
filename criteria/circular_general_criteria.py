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
