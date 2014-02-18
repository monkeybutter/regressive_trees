__author__ = 'SmartWombat'

from util import mid_angle

class AngularDF(object):

    df = None
    var_name = None
    start = None
    end = None

    __class_description__ = """Abstract class for an angular dataframe"""
    __version__ = 0.1

    def __init__(self, df, var_name, start=None, end=None):
        r"""Class constructor.

        Initialise the class' attributes. PEP-8 mentions using a leading
        underscore for "internal" names.

        Parameters
        ----------
        required_config : list of strings
            List of config options that are required by the harvester.
            If not all the options are defined it will raise an excpetion.
        optional_config_defaults : dict
            A dictionary with the optional configuration parameters and its defaults.
            TODO: Explain the default options
        kwargs : dict
            Arguments that are specific to the harvester type.

        Raises
        ------
        ValueError
            If there are missing configuration values in the kwargs for the harvester type.

        Notes
        -----
        TODO: how best to document class attributes.
        """

        self.df = df
        self.var_name = var_name
        self.start = start
        self.end = end

    def get_shifted(self, index):

        shifted_df = AngularDF(self.df[index:].append(self.df[:index]), self.var_name)
        return shifted_df


    def get_left(self, index):

        if index <= 0:
            return None

        elif index >= self.df.shape[0]-1:
            left_df = AngularDF(self.df, self.var_name)
            left_df.start = self.start
            left_df.end = self.end
            return left_df

        else:
            left_df = AngularDF(self.df.iloc[:index], self.var_name)
            left_df.start = self.start
            left_df.end = mid_angle(self.df[self.var_name].iloc[index-1], self.df[self.var_name].iloc[index])
            return left_df


    def get_right(self, index):

        if index <= 0:
            right_df = AngularDF(self.df, self.var_name)
            right_df.start = self.start
            right_df.end = self.end
            return right_df

        elif index >= self.df.shape[0]-1:
            return None

        else:
            right_df = AngularDF(self.df.iloc[index:], self.var_name)
            right_df.start = mid_angle(self.df[self.var_name].iloc[index-1], self.df[self.var_name].iloc[index])
            right_df.end = self.end

            return right_df