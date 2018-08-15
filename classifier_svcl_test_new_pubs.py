"""
Script to test performance of trained models on the most recently published articles
"""

import numpy as np
import pandas as pd
import pymongo as pm
import pickle
import re
import json
from title_feature import title_featurer
from location_feature import location_featurer
from item_select import ItemSelector
from nltk.tokenize import RegexpTokenizer
from sklearn.externals import joblib
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Lasso
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_validate
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


# nltk.classify.MaxentClassifier

# see here for feature selection:
#http://scikit-learn.org/stable/auto_examples/hetero_feature_union.html#example-hetero-feature-union-py

def test(df):
    """
    test trained models
    """

    X = merged_df.loc[:, ['text', 'location']]
    y = merged_df['label']
    #print(y.loc[y == 'method'])

    # load model trained in classifier_test.py
    print("load model")
    #method_classifier = joblib.load('method_classifier_trigrams_probability.pkl')
    method_classifier = joblib.load('method_classifier_location_probability.pkl')

    # run model:
    print("run model")
    y_predictions = method_classifier.predict(X)

    print("Scoring")

    # binary scoring
    # print("f1", f1_score(y_test, y_predictions, pos_label = 'method', average = "binary")) # gotta add the last bit for binary classifier
    # print("recall", recall_score(y_test, y_predictions, pos_label = 'method', average = "binary"))
    # print("accuracy", accuracy_score(y_test, y_predictions))
    # print("precision", precision_score(y_test, y_predictions, pos_label = 'method', average = "binary"))
    # print("confusion_matrix\n", confusion_matrix(y_test, y_predictions, labels = ['method', 'other']))

    report = classification_report(y, y_predictions)#, #target_names = ['method', 'result', 'conclusion', 'introduction'])
    print(report)

if __name__ == '__main__':
    #df = pd.read_csv('C:\\Users\\saveryme\\Documents\\full_text_project\\data\\labeled_full_text.tsv', sep = '\t')

    client = pm.MongoClient('localhost', 27017)
    db = client['full_texts'] # creates database if not there
    #documents = db['texts'] # creates new collection if not there
    documents = db['test_new_v2']
    #df = pd.DataFrame(list(documents.find()))
    #df.fillna(value = 'none', inplace = True)

    df_conclusion = pd.DataFrame(list(documents.find({'label': 'conclusion'})))
    df_result = pd.DataFrame(list(documents.find({'label': 'result'})))
    df_method = pd.DataFrame(list(documents.find({'label': 'method'})))
    df_intro = pd.DataFrame(list(documents.find({'label': 'introduction'})))

    dfs = [df_conclusion, df_result, df_method, df_intro]

    # merge the dfs!
    merged_df = pd.concat(dfs)
    merged_df.sort_values('date', inplace = True)

    # drop short rows
    merged_df = merged_df.loc[merged_df['text'].map(len) > 400]
    merged_df.reset_index(inplace = True, drop = True)
    print("df shape", merged_df.shape)

    # Make data binary
    pattern = r'^(?!method).*$'
    merged_df['label'].replace(pattern, 'other', regex = True, inplace = True)

    # clean punctuation...
    #punctuation = r'[\*\<\>\?\.\$\!\(\)\@\#\%\^\-\+\{\}\[\]\,\\\/:;"\'\|]'

    test(merged_df)
    #model_iterate(merged_df)
