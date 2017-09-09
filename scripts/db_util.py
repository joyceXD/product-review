import gzip
import json
import pandas as pd
import pymongo
from pymongo import MongoClient
import time


def connect_mongo(host, port, username, password, db):

    if username and password:
        mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (username, password, host, port, db)
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db]


def read_mongo(db, collection, query={}, host='localhost', port=27017, username=None, password=None):

    db = _connect_mongo(host=host, port=port, username=username, password=password, db=db)
    cursor = db[collection].find(query)

    # Expand the cursor and construct the DataFrame
    df =  pd.DataFrame(list(cursor))
    return df

