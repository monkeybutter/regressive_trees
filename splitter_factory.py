__author__ = 'roz016'

from splitter import *
from splitter.splitter import Splitter

def SplitterFactory(source):
    for cls in Splitter.__subclasses__():
        if cls.is_extractor_for(source):
            return cls()

    print("{} source not found".format(source))
    #raise ValueError

def SplitterEnumerator():
    sources = {}
    for cls in Criteria.__subclasses__():
        if cls.source is not None:
            sources[cls.source] = cls
    return sources