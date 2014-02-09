__author__ = 'roz016'

from criteria import *
from criteria.criteria import Criteria

def CriteriaFactory(source, class_var):
    for cls in Criteria.__subclasses__():
        if cls.is_criteria_for(source):
            return cls(class_var)

    print("{} source not found".format(source))
    #raise ValueError

def CriteriaEnumerator():
    sources = {}
    for cls in Criteria.__subclasses__():
        if cls.source is not None:
            sources[cls.source] = cls
    return sources