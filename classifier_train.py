import numpy as np
import pandas as pd
import pymongo as pm
import pickle
import re
import json
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

class title_featurer(BaseEstimator):
    """
    Class for creating custom title feature
    """

    def __init__(self):
        """
        Init custom feature
        """

        with open('section_lists_custom_dict.json') as f:
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
            if regex_search.group(0) in self.label_list:
                title_vector.append(1)
            else:
                title_vector.append(0)

        X = np.array([title_vector]).T # need the transpose to convert from [1,32000] to [32000,1]

        return X
        #return title_vector

class location_featurer(BaseEstimator):
    """
    Class for creating custom location feature
    """

    def fit(self, df, y = None):
        """
        fit method just returns the data
        """

        return self

    def transform(self, column):
        """
        See if the title is in the list jim gave me and give it a weight if so
        """

        location_vector = column.round(1)
        # round location
        X = np.array([location_vector]).T # need the transpose to convert from [1,32000] to [32000,1]

        return X


def test_v2(merged_df):
    """
    train and test individual models, with title feature and now with location feature
    """

    X_train = merged_df.loc[:31999, ['text', 'location']]#.reset_index(drop = True)
    y_train = merged_df.loc[:31999, 'label']#.reset_index(drop = True)
    X_test = merged_df.loc[32000:, ['text', 'location']]#.reset_index(drop = True)
    y_test = merged_df.loc[32000:, 'label']#.reset_index(drop = True)

    # Check out this fancy pipeline
    pipeline = Pipeline([
        # Use FeatureUnion to combine the features from subject and body
        ('union', FeatureUnion(
            transformer_list=[

                ('location_pipe', Pipeline([
                    ('selector', ItemSelector(column='location')),
                    ('location', location_featurer()),
                ])),
                #
                ('title_pipe', Pipeline([
                    ('selector', ItemSelector(column='text')),
                    ('title', title_featurer()),
                ])),
                ('text_pipe', Pipeline([
                    ('selector', ItemSelector(column='text')),
                    ('tfidf', TfidfVectorizer()),
                ])),

            ],
        transformer_weights={
            'titles': .9,
            'location': 1,
            'tfidf': .7
            }
        )),

        # Use a SVC classifier on the combined features
        ('svcl', SVC(kernel='linear', probability = True)),
        #('lg', LogisticRegression(random_state=0)),
    ])

    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    print(classification_report(y_pred, y_test))
    # save if I want
    #print("saving")
    #joblib.dump(method_classifier, 'method_classifier_trigrams_probability.pkl')
    #joblib.dump(pipeline, 'method_classifier_location_probability.pkl')


def test_classic(merged_df):
    """
    train and test individual models, with title feature
    Uses cv and RepeatedStratifiedKFold, or run without
    """

    #small_df = merged_df.iloc[:200, :].copy()

    #print(y.loc[y == 'method'])

    X_train = merged_df.loc[:31999, 'text']
    y_train = merged_df.loc[:31999, 'label']
    X_test = merged_df.loc[32000:, 'text']
    y_test = merged_df.loc[32000:, 'label']
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .2, stratify = y)

    X_train_location = merged_df.loc[:31999, 'location']
    X_test_location = merged_df.loc[32000:, 'location']
    method_classifier = Pipeline([
                        ('union', FeatureUnion([
                        #('location', location_featurer())
                        ('titles', title_featurer()), # yay this is how to add a custom features https://stackoverflow.com/questions/36253258/how-to-fit-different-inputs-into-an-sklearn-pipeline
                        ('tfidf', TfidfVectorizer()),#ngram_range = (1, 3))),
                        ])),
                        #('mnb', MultinomialNB()),
                        #('sgd', SGDClassifier(loss='hinge', penalty='l2', alpha=.001, random_state=42, max_iter=5, tol=None))
                        #('lg', LogisticRegression(random_state=0))
                        #('lsvc', LinearSVC())
                        #('svcl', SVC(kernel='linear', probability = True))
                        ('svcl', SVC(kernel='linear'))
                        #('bnb', BernoulliNB())
                        #('lasso', Lasso())
                        #('rf', RandomForestClassifier(n_estimators = 100, random_state = 1))
                        #('ovr', OneVsRestClassifier(LinearSVC()))
                        #('ovr', OneVsRestClassifier(LogisticRegression()))
                        ])


        # weight components for feature FeatureUnion
    transformer_weights={
            'titles': 1.0,
            'location': 1.0,
            'tfidf': .9
            }
    lsvc_parameter_grid = [{
                    'tfidf__max_features': (50, 100, 200, 1000)
                    #"lsvc__penalty": ('l1', 'l2')
                    #"loss": ('hinge', 'squared_hinge'),
                    #'lsvc__C': (np.arange(0.01,10,10))
                    }]

    # grid search:
    # grid_search = GridSearchCV(method_classifier, lsvc_parameter_grid, cv=10, scoring = 'f1_macro')
    # grid_search.fit(X_train, y_train)
    # print(grid_search.best_params_)
    # print("Parameters to use:", grid_search.best_estimator_)

    # run model:
    print("train classifier")
    method_classifier.fit(X_train, y_train)
    #y_probability = method_classifier.predict_proba(X_test)
    y_predictions = method_classifier.predict(X_test)
    #print("classes:", method_classifier.classes_)

    # score
    #print("Scoring")
    #rskf = RepeatedStratifiedKFold(n_splits = 5, n_repeats = 1, random_state = 1)

    # cross validation with cros_val_score:
    # print("Cross validation with rskf")
    # cv_scores = cross_val_score(method_classifier, X, y, cv = rskf, scoring = 'f1_macro', n_jobs = -1)
    # print(cv_scores)

    # cross validation with corss_validate, which allows for multiple scoring metrics
    # scoring = ['f1_macro', 'precision_macro', 'recall_macro', 'accuracy']
    # scores = cross_validate(method_classifier, X, y,
    #                         scoring = scoring, cv = rskf) # cv =rskf

    # print(scores)

    # binary scoring
    # print("f1", f1_score(y_test, y_predictions, pos_label = 'method', average = "binary")) # gotta add the last bit for binary classifier
    # print("recall", recall_score(y_test, y_predictions, pos_label = 'method', average = "binary"))
    # print("accuracy", accuracy_score(y_test, y_predictions))
    # print("precision", precision_score(y_test, y_predictions, pos_label = 'method', average = "binary"))
    # print("confusion_matrix\n", confusion_matrix(y_test, y_predictions, labels = ['method', 'other']))

    # nice report thast won't work if predict_proba
    report = classification_report(y_test, y_predictions)#, #target_names = ['method', 'result', 'conclusion', 'introduction'])
    print(report)
    # with open("C:\\Users\saveryme\Documents\\full_text_project\\results_svc_trigrams.txt", 'w') as f:
    #     f.write("{}".format(report))

    # multiclass scoring
    # print("f1", f1_score(y_test, y_predictions, average = "macro")) # gotta add the last bit for binary classifier
    # print("recall", recall_score(y_test, y_predictions, average = "macro"))
    # print("accuracy", accuracy_score(y_test, y_predictions))
    # print("precision", precision_score(y_test, y_predictions, average = "macro"))
    # print("confusion_matrix\n", confusion_matrix(y_test, y_predictions))

    # save if I want
    #print("saving")
    #joblib.dump(method_classifier, 'method_classifier_trigrams_probability.pkl')
    #joblib.dump(method_classifier, 'method_classifier_probability.pkl')

def model_iterate(df):
    """
    Iterate through all the models
    """

    X = df['text']
    y = df['label']
    #print(y.loc[y == 'method'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .2, stratify = y)

    rskf = RepeatedStratifiedKFold(n_splits = 5, n_repeats = 10, random_state = 1)

    models = [
            ('sgd', SGDClassifier()),
            #('lg', LogisticRegression()),
            ('bnb', BernoulliNB()),
            ('svcl', SVC(kernel='linear')),
            ('svc_rbf', SVC(kernel='rbf')),
            ('svc_poly', SVC(kernel='poly')),
            ('lasso', Lasso())
            ]

    for model in models:
        method_classifier = Pipeline([
                            ('tfidf', TfidfVectorizer()), #ngram_range = (1, 2)
                            model
                            ])

        method_classifier.fit(X_train, y_train)
        y_predictions = method_classifier.predict(X_test)

        print(model)
        print("f1", f1_score(y_test, y_predictions, pos_label = 'method', average = "binary")) # gotta add the last bit for binary classifier
        print("recall", recall_score(y_test, y_predictions, pos_label = 'method', average = "binary"))
        print("accuracy", accuracy_score(y_test, y_predictions))
        print("precision", precision_score(y_test, y_predictions, pos_label = 'method', average = "binary"))
        print("confusion_matrix\n", confusion_matrix(y_test, y_predictions, ['method', 'other']), "\n")


if __name__ == '__main__':
    #df = pd.read_csv('C:\\Users\\saveryme\\Documents\\full_text_project\\data\\labeled_full_text.tsv', sep = '\t')


    client = pm.MongoClient('localhost', 27017)
    db = client['full_texts'] # creates database if not there
    #documents = db['texts'] # creates new collection if not there
    documents = db['train_val_v2']
    #df = pd.DataFrame(list(documents.find()))
    #df.fillna(value = 'none', inplace = True)

    df_conclusion = pd.DataFrame(list(documents.find({'label': 'conclusion'}).limit(10000)))
    df_result = pd.DataFrame(list(documents.find({'label': 'result'}).limit(10000)))
    df_method = pd.DataFrame(list(documents.find({'label': 'method'}).limit(10000)))
    df_intro = pd.DataFrame(list(documents.find({'label': 'introduction'}).limit(10000)))

    dfs = [df_conclusion, df_result, df_method, df_intro]

    # merge the dfs!
    merged_df = pd.concat(dfs)
    print(merged_df.shape)
    merged_df.sort_values('date', inplace = True)

    # drop short rows
    merged_df = merged_df.loc[merged_df['text'].map(len) > 400]
    merged_df.reset_index(inplace = True, drop = True)
    print("df shape", merged_df.shape)

    # Make data binary
    pattern = r'^(?!method).*$'
    merged_df['label'].replace(pattern, 'other', regex = True, inplace = True)

    # round data

    # clean punctuation... didn't do anything
    # punctuation = r'[\s{2,}\*\?\.\$\(\)\^\-\+\{\}\[\]\\\|\'%#@:&;!",]' # didn't includ <>/ for xml tag integrity
    # merged_df['text'].replace(punctuation, ' ', regex = True, inplace = True)

    test_v2(merged_df)
    #model_iterate(merged_df)
