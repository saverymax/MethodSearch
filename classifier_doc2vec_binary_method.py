import gensim
from gensim import corpora, models, similarities
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import pymongo as pm
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from nltk.tokenize import word_tokenize
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix

client = pm.MongoClient('localhost', 27017)
db = client['full_texts'] # creates database if not there
#documents = db['texts'] # creates new collection if not there
documents = db['train_val']

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
print("df shape after dropping", merged_df.shape)

# Make data binary
pattern = r'^(?!method).*$'
merged_df['label'].replace(pattern, 'other', regex = True, inplace = True)

#merged_df = merged_df.sample(200) # use a small set for playin'

# my way of train test n_split
X_train = merged_df.loc[:31999, 'text']
y_train = merged_df.loc[:31999, 'label']
X_test = merged_df.loc[32000:, 'text']
y_test = merged_df.loc[32000:, 'label']

# sklearn way
# X_train, X_test, y_train, y_test = train_test_split(
#     merged_df['text'],
#     merged_df['label'],
#     test_size=0.2,
#     stratify = merged_df['label'])

print("Length of training data, training labels:", len(X_train), len(y_train))

print("preprocesing...")
train_docs = [TaggedDocument(gensim.utils.simple_preprocess(row), [label]) for label, row in zip(y_train, X_train)]
test_docs = [TaggedDocument(gensim.utils.simple_preprocess(row), [label]) for label, row in zip(y_test, X_test)]

# Build model
print("building model")
model = Doc2Vec(train_docs, vector_size = 100, epochs = 20, window=10, workers = 6) #min_count=0)
#model.save("test_doc2vec_binary.model")

# Retrain model
print("retraining model")
labels_train, embeddings_train = zip(*[(doc.tags[0], model.infer_vector(doc.words, steps=20)) for doc in train_docs])
labels_test, embeddings_test = zip(*[(doc.tags[0], model.infer_vector(doc.words, steps=20)) for doc in test_docs])

rskf = RepeatedStratifiedKFold(n_splits = 5, n_repeats = 5, random_state = 1)

#model_svc = LinearSVC()
print("run sklearn")
sk_model = LogisticRegression(random_state=0)
sk_model.fit(embeddings_train, labels_train)

#cv_scores = cross_val_score(method_classifier, embeddings_train, labels_train, cv = rskf, scoring = 'f1_macro', n_jobs = -1)
#print(cv_scores)

y_predictions = sk_model.predict(embeddings_test)

# print("f1", f1_score(labels_test, y_predictions, pos_label = 'method', average = "binary"))
# print("recall", recall_score(labels_test, y_predictions, pos_label = 'method', average = "binary"))
# print("accuracy", accuracy_score(labels_test, y_predictions))
# print("precision", precision_score(labels_test, y_predictions, pos_label = 'method', average = "binary"))
# print("confusion_matrix\n", confusion_matrix(labels_test, y_predictions, labels=['method', 'other']))

f1 = f1_score(labels_test, y_predictions, pos_label = 'method', average = "binary")
recall = recall_score(labels_test, y_predictions, pos_label = 'method', average = "binary")
accuracy = accuracy_score(labels_test, y_predictions)
precision = precision_score(labels_test, y_predictions, pos_label = 'method', average = "binary")
c_matrix = confusion_matrix(labels_test, y_predictions, labels=['method', 'other'])

with open("C:\\Users\saveryme\Documents\\full_text_project\\results_doc2vec_binary_lg.txt", 'w') as f:
    f.write("{0}\n{1}\n{2}\n{3}\n{4}".format(f1, recall, accuracy, precision, c_matrix))
