import numpy as np
import pandas as pd
import pymongo as pm
import pickle
import re
import json

from sklearn.externals import joblib
from sklearn.utils.extmath import density
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2, mutual_info_classif, SelectFromModel
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
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


def test(df):
    """
    experiment with training tfidf on only test data, just to verify that pipeline doesn't train tfidf on train and test data...
    Results match!
    """

    merged_df = df.sample(n = 500)
    print("build the model!")

    X = merged_df['text']
    y = merged_df['label']
    #print(y.loc[y == 'method'])

    # X_train = merged_df.loc[:31999, 'text']
    # y_train = merged_df.loc[:31999, 'label']
    # X_test = merged_df.loc[32000:, 'text']
    # y_test = merged_df.loc[32000:, 'label']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .2, stratify = y)

    tfidf_vec = TfidfVectorizer()
    train_transform = tfidf_vec.fit_transform(X_train)
    test_transform = tfidf_vec.transform(X_test)
    features_tfidf = np.array(tfidf_vec.get_feature_names())

    #chi2 test for contributing features
    # good ref: http://www.cse.chalmers.se/~richajo/dit865/files/Feature%20ranking%20examples.html
    print("chi^2")
    ch2 = SelectKBest(chi2, k=500) # kbest scores features based on difference, hence chi squared
    X_train = ch2.fit_transform(train_transform, y_train)
    X_test = ch2.transform(test_transform)
    # keep selected feature names
    feature_names = features_tfidf[ch2.get_support(indices=True)]
    feature_names = np.asarray(feature_names)

    # mutual info:
    #print("mutual information:")
    # this way just finds the features
    # # feature_scores = mutual_info_classif(train_transform, y_train)
    # # for score, fname in sorted(zip(feature_scores, feature_names), reverse=True)[:10]:
    # #     print(fname, score)

    # # and this way with kbest feature selection:
    # mutual_info = SelectKBest(mutual_info_classif, k=100)
    # X_train = mutual_info.fit_transform(train_transform, y_train)
    # X_test = mutual_info.transform(test_transform)
    # # keep selected feature names
    # feature_names = [feature_names[i] for i in mutual_info.get_support(indices=True)]
    # feature_names = np.asarray(feature_names)
    # print("feature names:", feature_names)

    #method_classifier = LinearSVC()
    method_classifier = LogisticRegression(random_state=0)
    #method_classifier = SVC(kernel='linear')

    # then run the model
    print("train classifier")
    method_classifier.fit(X_train, y_train)
    y_predictions = method_classifier.predict(X_test)

    # score
    print("scoring")
    report = classification_report(y_test, y_predictions)#, #target_names = ['method', 'result', 'conclusion', 'introduction'])
    print(report)

    #then assess contributing features
    print("Dimension of classifier:", method_classifier.coef_.shape)
    top10 = np.argsort(method_classifier.coef_[0])[-10:]
    print(top10)
    print("top 10 contributing features")
    print(feature_names[top10])

    # oh and also trying out select from model feature model_selection
    # new_model = SelectFromModel(LogisticRegression(random_state=0), prefit=False)
    # X_transform = new_model.fit_transform(train_transform, y_train)
    # print(X_transform.shape)
    # feature_names = np.asarray(feature_names)
    # print(feature_names[new_model.get_support(indices=True)])


    # print("feature names:", feature_names)

if __name__ == '__main__':
    #df = pd.read_csv('C:\\Users\\saveryme\\Documents\\full_text_project\\data\\labeled_full_text.tsv', sep = '\t')

    client = pm.MongoClient('localhost', 27017)
    db = client['full_texts'] # creates database if not there
    #documents = db['texts'] # creates new collection if not there
    documents = db['train_val']
    #df = pd.DataFrame(list(documents.find()))
    #df.fillna(value = 'none', inplace = True)

    df_conclusion = pd.DataFrame(list(documents.find({'label': 'conclusion'}).limit(10000)))
    df_result = pd.DataFrame(list(documents.find({'label': 'result'}).limit(10000)))
    df_method = pd.DataFrame(list(documents.find({'label': 'method'}).limit(10000)))
    df_intro = pd.DataFrame(list(documents.find({'label': 'introduction'}).limit(10000)))

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

    test(merged_df)
