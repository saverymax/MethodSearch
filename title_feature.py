from sklearn.base import BaseEstimator
import re
import numpy as np

class title_featurer(BaseEstimator):
    """
    Class for creating custom title feature
    """

    def __init__(self):
        """
        Init custom feature
        """

        with open('constant_lists\\section_lists_custom_dict.json') as f:
            label_lists = json.load(f)

        self.label_list = label_lists['methods']

    def fit(self, df, y = None):
        """
        fit method just returns the data
        """

        return self

    def transform(self, df):
        """
        See if the title is in the list jim gave me and give it a weight if so
        """

        title_vector = []
        pattern = r'(?<=<title>)(.*?)(?=<\/title>)'
        #for index, row in df.iterrows():
        for row in df:
            regex_search = re.search(pattern, row)
            #if regex_search:
                #print(regex_search.group(0))
            if regex_search:
                if regex_search.group(0) in self.label_list:
                    title_vector.append(1)
                else:
                    title_vector.append(0)
            else:
                title_vector.append(0)

        X = np.array([title_vector]).T # need the transpose to convert from [1,32000] to [32000,1]

        return X
