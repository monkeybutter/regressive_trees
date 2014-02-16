__author__ = 'SmartWombat'

import numpy as np
from criteria import Criteria
from util import circular_heterogeneity
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


    def get_value(self, left_df, right_df):
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
        #criteria has to maximise optimal value
        #print('inside criteria left_df {}'.format(left_df))
        #print('inside criteria left_df.class_var {}'.format(left_df[self.class_var]))

        heterogeneity = circular_heterogeneity(left_df, self.class_var) + circular_heterogeneity(right_df, self.class_var)
        #print('heterogeneity {}'.format(heterogeneity))

        if heterogeneity == 0.0:
            return sys.float_info.max
        else:
            return 1.0/heterogeneity
