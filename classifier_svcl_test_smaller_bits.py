"""
Script to test svm on sections that are parsed into smaller children
"""

import pandas as pd
import json
import pymongo as pm
import numpy as np
import lxml.etree as le
import re
from sklearn.externals import joblib
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from title_feature import title_featurer

client = pm.MongoClient('localhost', 27017)
db = client['full_texts'] # creates database if not there
#documents = db['test_new'] # creates new collection if not there
documents = db['train_val']

df = pd.DataFrame(list(documents.find()))
#df = pd.DataFrame(list(documents.find().limit(100)))
df.sort_values('date', inplace = True)
df = df.loc[df['text'].map(len) > 400]
df.reset_index(inplace = True, drop = True)
print("df shape", df.shape)

# Make data binary
pattern = r'^(?!method).*$'
df['label'].replace(pattern, 'other', regex = True, inplace = True)

# small experimental dataset
df = df.sample(20)

# get the model and stuff
model = joblib.load('method_classifier_probability.pkl')
y_predictions = []
y_true = []

def get_title(section):
    """
    get the title of the section, if there
    """

    pattern_title = r'(?<=<title>)(.*?)(?=<\/title>)'
    title_search = re.search(pattern_title, section)
    title = None
    if title_search:
        title = title_search.group(0)

    return title

def classify(row):
    """
    Make a prediction for each child of each section, and write it + useful info to file.
    """

    try:

        root = le.fromstring(row['text'])
        for child in root:
            try:
                section = le.tostring(child, encoding = 'unicode', method = 'xml')
                #print(section,"\n")
                prob = model.predict_proba([section])
                prediction = model.predict([section])
                y_predictions.append(prediction[0])
                y_true.append(row['label'])
                if prediction[0] == 'method':
                    clean_section = whitespaces.sub(' ', section)
                    article = row['article']
                    title = get_title(section)
                    methods, other = zip(model.classes_, prob[0])
                    line = "{0}|{1}|{2}|{3}|{4}\n".format(article, title, methods, other, clean_section)
                    f.write(line)#.encode('utf8'))
            except BaseException as e:
                print(e)
                #print(e, row['text'])
                #print(child.text)
    except BaseException as e:
        # print(e, row['text'])
        # print(child.text,"\n\n")
        print(e)

whitespaces = re.compile(r'\s+')
f = open("methods_small_bits.txt", "w", encoding = "utf")
f.close()
f = open("methods_small_bits.txt", "a", encoding = "utf")
df.apply(classify, axis = 1)
f.close()
report = classification_report(np.array(y_true), np.array(y_predictions))
print("report")
print(report)
