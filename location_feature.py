"""
Module that uses normalized location as feature. See location_distribution.ipynb for normalization computations
The location is on a (0, 1) scale.
"""

from sklearn.base import BaseEstimator
import numpy as np
import pandas as pd

class location_featurer(BaseEstimator):
    """
    Class for creating custom location feature
    """

    def fit(self, column, y = None):
        """
        fit method just returns the data
        """

        return self

    def transform(self, location):
        """
        Round the location and return it in np array
        """

        # location_vector = np.round(column)
        location_vector = np.round(location, 1)
        # round location
        X = np.array([location_vector]).T # need the transpose to convert from [1,32000] to [32000,1]

        return X
