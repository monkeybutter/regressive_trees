__author__ = 'SmartWombat'

class Criteria(object):

    source = None
    class_var = None

    __class_description__ = """Abstract class for feature extracting"""
    __version__ = 0.1


    @classmethod
    def is_criteria_for(cls, source):
        return source == cls.source

    @classmethod
    def get_source_name(cls):
        return cls.source

    @classmethod
    def get_help_string(cls):
        help_string = """Help for {source_name}.
        Version: {version}
        {class_description}\n""".format(source_name=cls.source, version=cls.__version__,
                                        class_description=cls.__class_description__)

        if len(cls.required_config) > 0:
            help_string = "{}\n\tRequired parameters:\n".format(help_string)
            for required_parameter in cls.required_config:
                help_string = "{}\t\t{required_parameter}\n".format(
                    help_string, required_parameter=required_parameter)
        if len(cls.optional_config_defaults) > 0:
            help_string = "{}\n\tOptional parameters (default):\n".format(
                help_string)
        for optional_parameter, default_value in cls.optional_config_defaults.iteritems():
            help_string = "{}\t\t{optional_parameter} ({default_value})\n".format(help_string,
                                                                                  optional_parameter=optional_parameter,
                                                                                  default_value=default_value)

        return help_string

    def __init__(self, class_var):
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

        self.class_var = class_var


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
        raise NotImplementedError('I need to be implemented!')