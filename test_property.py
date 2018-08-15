import xml.etree.ElementTree as ET
import os
import method_constants

class method_retriever():
    """
    Class to retrieve methods sections:
    """

    def __init__(self, method_titles, method_sec_type):
        """
        Initiate class for method retrieval
        """

        self.titles = method_titles
        self.sec_type = method_sec_type

    # just playing with property
    @property
    def info(self):
        return self.titles

    @info.deleter
    def info(self):
        print("test")
        del(self.titles)

    def find_methods(self):
        """
        Match the name of the methods section
        """
        pass

    def get_methods(self):
        """
        Return the methods section
        """
        pass

    def save_methods(self):
        """
        Save the methods.
        Figure out how do to this
        """
        pass


methods = method_retriever(method_constants.titles, method_constants.sections)
#methods = property(methods.return_info())
print(methods.info)
del(methods.info)
print(methods.info)
