import gzip
import json
import pandas as pd
import pymongo
from pymongo import MongoClient
import time

START_TIME = 1393631999     # Y-M-D: 2014-3-1 00:00:00
END_TIME = 1396310400       # Y-M-D: 2014-4-1 00:00:00


def parse(path):
    g = gzip.open(path, 'r')
    for l in g:
        yield eval(l)


def get_df(path):
    i = 0
    df = {}
    for d in parse(path):
        df[i] = d
        i += 1
    return pd.DataFrame.from_dict(df, orient='index')


def insert_item_metadata(meta_collection, meta_path):
    item_meta_data = []

    for item_meta in parse(meta_path):
        if len(item_meta_data) < 1000:
            item_meta_data.append(item_meta)
        else:
            meta_collection.insert_many(item_meta_data)
            item_meta_data = []

    if not meta_collection:
        meta_collection.insert_many(item_meta_data)

    meta_collection.create_index([('asin', pymongo.ASCENDING)])


def insert_item_review(review_collection, review_path):
    item_reviews = []

    for review in parse(review_path):
        if 'unixReviewTime' in review.keys():
            if START_TIME < review['unixReviewTime'] < END_TIME:
                if len(item_reviews) < 1000:
                    item_reviews.append(review)
                else:
                    review_collection.insert_many(item_reviews)
                    item_reviews = []

    if not item_reviews:
        review_collection.insert_many(item_reviews)


# path = 'https://s3-eu-west-1.amazonaws.com/bigdata-team/job-interview/metadata.json.gz'
review_data_path = '../data/item_dedup.json.gz'
meta_data_path = '../data/metadata.json.gz'

client = MongoClient('mongodb://localhost:27017/')
db = client.product
meta_collection = db.metadata
review_collection = db.review

insert_item_metadata(meta_collection, meta_data_path)
insert_item_review(review_collection, review_data_path)

db.review.aggregate([
    {'$lookup': {'from': "metadata",
                 'localField': "asin",
                 'foreignField': "asin",
                 'as': "metadata"}
     },
    {'$unwind': "$metadata"},
    {'$project': {
            "_id": 1,
            "asin": 1,
            "reviewerID": 1,
            "reviewerName": 1,
            "helpful": 1,
            "unixReviewTime": 1,
            "reviewText": 1,
            "overall": 1,
            "summary": 1,
            "itemTitle": "$metadata.title",
            "itemPrice": "$metadata.price",
            "itemRelated": "$metadata.related",
            "itemSalesRank": "$metadata.salesRank",
            "itemBrand": "$metadata.brand",
            "itemCategories": "$metadata.categories"
        }
     },
    {'$out': "item_review"}
])


