"""

"""

from sklearn.base import BaseEstimator
import numpy as np
import pandas as pd

class location_featurer(BaseEstimator):
    """
    Class for creating custom location feature
    Module uses normalized location as feature:
    location index of section / length of body

    """

    def fit(self, column, y = None):
        """
        fit method just returns the data
        """

        return self

    def transform(self, location):
        """
        Round the location to one decimal and return it in np array
        """

        # location_vector = np.round(column)
        location_vector = np.round(location, 1)
        # round location
        X = np.array([location_vector]).T # need the transpose to convert from [1,32000] to [32000,1]

        return X
