__author__ = 'SmartWombat'

from util import mid_angle

class Data(object):

    df = None
    class_var = None
    class_type = None
    var_types = None
    var_limits = {}

    __class_description__ = """Abstract class for an tree dataframe"""
    __version__ = 0.1

    def __init__(self, df, class_var, var_types):
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
        self.class_var = class_var
        self.var_types = var_types
        self.set_class_type()

        for idx, variable in enumerate(df.columns):
            if variable != class_var:
                self.var_limits[variable] = {}
                self.var_limits[variable]['type'] = var_types[idx]
                self.var_limits[variable]['start'] = None
                self.var_limits[variable]['end'] = None


    def set_class_type(self):
        for idx, variable in enumerate(self.df.columns):
            if variable == self.class_var:
                self.class_type = self.var_types[idx]


    def get_shifted(self, index):

        shifted_df = Data(self.df[index:].append(self.df[:index]), self.class_var, self.var_types)
        return shifted_df


    def sort_by(self, pred_var):

        self.df = self.df.sort([pred_var])
        self.df.index = range(0,len(self.df))


    def get_left(self, index, var_name):

        if index <= 0:
            return None

        elif index >= self.df.shape[0]-1:
            left_data = Data(self.df, self.class_var, self.var_types)
            left_data.var_limits = self.var_limits
            left_data.var_limits[var_name]['start'] = self.var_limits[var_name]['start']
            left_data.var_limits[var_name]['end'] = self.var_limits[var_name]['end']

            return left_data

        else:
            left_data = Data(self.df.iloc[:index], self.class_var, self.var_types)
            left_data.var_limits = self.var_limits
            left_data.var_limits[var_name]['start'] = self.var_limits[var_name]['start']
            left_data.var_limits[var_name]['end'] = mid_angle(self.df[var_name].iloc[index-1], self.df[var_name].iloc[index])
            return left_data


    def get_right(self, index, var_name):

        if index <= 0:
            right_data = Data(self.df, self.class_var, self.var_types)
            right_data.var_limits = self.var_limits
            right_data.var_limits[var_name]['start'] = self.var_limits[var_name]['start']
            right_data.var_limits[var_name]['end'] = self.var_limits[var_name]['end']
            return right_data

        elif index >= self.df.shape[0]-1:
            return None

        else:
            right_data = Data(self.df.iloc[index:], self.class_var, self.var_types)
            right_data.var_limits = self.var_limits
            right_data.var_limits[var_name]['start'] = mid_angle(self.df[var_name].iloc[index-1], self.df[var_name].iloc[index])
            right_data.var_limits[var_name]['end'] = self.var_limits[var_name]['end']

            return right_data