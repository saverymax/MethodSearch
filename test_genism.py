from gensim import corpora, models, similarities
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import pymongo as pm
import pandas as pd
from sklearn.model_selection import train_test_split


client = pm.MongoClient('localhost', 27017)
db = client['full_texts'] # creates database if not there
documents = db['texts'] # creates new collection if not there

# mongo stuff I was trying to sample and find
#df = pd.DataFrame(list(documents.find({'label': {'$in': ['introduction', 'conclusion']}}).sort('date', 1).limit(200)), column)
#test = list(documents.aggregate( [{ '$sample': { 'size': 1}}]))
#test_df = pd.DataFrame(list(documents.aggregate( { '$sample': { 'size': 1}})))

# get data with each label
df_conclusion = pd.DataFrame(list(documents.find({'label': 'conclusion'}).limit(2000)))
df_result = pd.DataFrame(list(documents.find({'label': 'result'}).limit(2000)))
df_method = pd.DataFrame(list(documents.find({'label': 'method'}).limit(2000)))
df_intro = pd.DataFrame(list(documents.find({'label': 'introduction'}).limit(2000)))

dfs = [df_conclusion, df_result, df_method, df_intro]

# merge the dfs!
merged_df = pd.concat(dfs)

small_set = merged_df.iloc[:200, :].copy()

# data exploring
#print(merged_df['text'])
#df.fillna(value = 'none', inplace = True)
#null_data = df[df.isnull().any(axis=1)]
#print(null_data.head())
# for row, label in merged_df.iterrows():
#     if len(label['text']) < 500:
#         print(label['text'])
        #print(merged_df.iloc[row, :])
    #print(label['text'], "\n")

X_train, X_test, y_train, y_test = train_test_split(

# gensim work
documents = [TaggedDocument(row['text'], row['label']) for i, row in small_set.iterrows()] # 2nd argument is the label
model = Doc2Vec(vector_size=5, window=2, min_count=1, workers=4)
model.build_vocab(documents)
model.train(documents, total_examples=model.corpus_count, epochs=model.epochs)
print(model.infer_vector(['methods']))

#model.save('./imdb.d2v')

#model = Doc2Vec.load('./imdb.d2v')
