import pymongo as pm
import pandas as pd

def mongo_connection():
    """
    Connect to the mongo db
    """
    client = pm.MongoClient('localhost', 27017)
    db = client['full_texts'] # creates database if not there
    documents = db['texts'] # creates new collection if not there
    print(documents.find().count())
    #client.drop_database("pymongo_test")
    data = pd.DataFrame(list(documents.find()))
    print(data.head())

mongo_connection()
