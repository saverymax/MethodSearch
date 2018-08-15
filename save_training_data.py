import pymongo as pm
import pandas as pd
from sqlalchemy import create_engine
import re

"""
"Quick" script to take all sections from full_texts, clean the dates, sort them by date, and insert the first n docs of each label in collection
"""
#psql
#conn = psycopg2.connect("dbname='savorydb' user='savoryuser' host='localhost' password='5@v0ry'")
#engine = create_engine('sqlite://', echo=False)
#df.to_sql('users', con=engine)

client = pm.MongoClient('localhost', 27017)
db = client['full_texts'] # creates database if not there
#collection = db['train_val_v2']
df = pd.DataFrame(list(db.texts_v2.find()))#.limit(5000)))

# A good number of dates are not in month-year format. So clean that up
def clean_dates(date):
    date_pattern = r'(\d+-\d{4})' #  search for expected m-yyyy format
    if not re.fullmatch(date_pattern, date):
        if re.match(r'(\d+-\d{4})', date): # check for date that might be followed by string
            clean_date = re.match(r'(\d+-\d{4})', date).group(0)
            return clean_date
        else:
            clean_date = re.search(r'(\d{4})', date).group(0) # just grab year because that's all that's in the field
            return clean_date
    else:
        return date

print("deal with these pesky dates")
df['date'] = df['date'].apply(clean_dates)

#print(df.loc[df['date'].str.contains(r'[a-zA-Z]')])
#print(df.loc[df['date'] == '2015'], 'date')

df['date'] = pd.to_datetime(df['date'])
df.sort_values('date', inplace = True)
df.reset_index(drop = True, inplace = True)

df_methods = df.loc[df['label'] == 'method']
df_intro = df.loc[df['label'] == 'introduction']
df_conclusion = df.loc[df['label'] == 'conclusion']
df_results = df.loc[df['label'] == 'result']

df_list = [df_methods[:10000], df_intro[:10000], df_conclusion[:10000], df_results[:10000]]
merged_df = pd.concat(df_list)

mongo_entry = merged_df.to_dict('record')

print("saving")
db.train_val_v2.remove({})
db.train_val_v2.insert_many(mongo_entry)
#db.train_val.remove({})
#db.train_val_v2.insert_many(mongo_entry)
