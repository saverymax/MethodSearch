from sklearn.base import BaseEstimator, TransformerMixin
import re
import numpy as np

class ItemSelector(BaseEstimator, TransformerMixin):
    """
    For data grouped by feature, select subset of data at a provided key.
    """

    def __init__(self, column):
        self.column = column

    def fit(self, x, y=None):
        return self

    def transform(self, df):
        return df[self.column]
