import pandas as pd
import json
import pymongo as pm
import method_constants
import introduction_constants
import os
import lxml.etree as le
import re

client = pm.MongoClient('localhost', 27017)
db = client['full_texts'] # creates database if not there
documents = db['texts'] # creates new collection if not there

df = pd.DataFrame(list(documents.find()))

print(df.shape)
for i, row in df.iterrows():
    body_search = re.search(r'<sec', row['text'])
    if body_search != None:
        print(row['text'])
