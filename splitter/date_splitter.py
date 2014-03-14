__author__ = 'SmartWombat'

from circular_splitter import CircularSplitter
from splitter import Splitter

class DateSplitter(CircularSplitter, Splitter):

    """ **Synopsis** ::

            todo = TODO()  # a brief example of using the CLASS
            todo.method()

        **Description**

        Implementation of the Extractor class

        **Copyright**

            Copyright (c) 2014 by MonkeyButter
    """
    source = 'date'
    __class_description__ = """Basic splitter for date data"""
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



