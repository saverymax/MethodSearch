from sklearn.base import BaseEstimator
import re
import numpy as np
from pathlib import Path

class title_featurer(BaseEstimator):
    """
    Class for creating custom title feature. This class will look
    for the <title> tag in a section, and see if it matches any of the strings
    in a predefined list of ways to say "methods".
    """

    def __init__(self):
        """
        Init custom title feature
        """

        constant_parts = ["constant_list", "section_lists_custom_dict.json"]
        constant_path = Path.cwd().joinpath(*constant_parts)
        with open(constant_path) as f:
            label_lists = json.load(f)
        self.label_list = label_lists['methods']

    def fit(self, df, y = None):
        """
        fit method just returns the data
        """
        return self

    def transform(self, df):
        """
        See if the title is in the constant list and give it a binary weight
        if so.
        """

        title_vector = []
        pattern = r'(?<=<title>)(.*?)(?=<\/title>)'

        for row in df:
            regex_search = re.search(pattern, row)
            if regex_search:
                if regex_search.group(0) in self.label_list:
                    title_vector.append(1)
                else:
                    title_vector.append(0)
            else:
                title_vector.append(0)

        X = np.array([title_vector]).T # need the transpose to convert from [1,32000] to [32000,1]

        return X
