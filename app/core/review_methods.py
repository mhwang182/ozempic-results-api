import dateutil
from bson import ObjectId

from app.common.utils import user_details_steps
from app.core.db import db


def add_review(new_review_doc):
    post_id = None
    try:
        post_id = db.Reviews.insert_one(new_review_doc).inserted_id
    except Exception as e:
        print(str(e))
    
    return post_id

def get_review_from_db(reviewId):
    review = None
    try:
        review = db.Reviews.find_one({"_id": ObjectId(reviewId)})
    except Exception as e:
        print(str(e))
    
    return review

def delete_review_from_db(reviewId):
    deleted_count = 0
    try:
        deleted_count = db.Reviews.delete_one({"_id": ObjectId(reviewId)}).deleted_count
    except Exception as e:
        print(str(e))

    return deleted_count

def get_reviews_from_db(user_id):
    reviews = None
    try:
        reviews = db.Reviews.aggregate([
            {
                '$match': { 'userId': ObjectId(user_id) },
            },
            user_details_steps[0],
            user_details_steps[1],
            user_details_steps[2],
            {
                '$sort': {'createdAt': -1}
            }
        ])
        reviews = list(reviews)[0]
    except Exception as e:
        print(str(e))

    return reviews

def fetch_reviews_feed(date):
    reviews = []
    try:
        reviews = db.Reviews.aggregate([{
            '$facet' : {
                'metaData': [ {'$count': 'totalCount'} ],
                'data': [
                    {'$sort': {'createdAt': -1}}, 
                    {
                        '$match': {'createdAt': {'$lt': dateutil.parser.parse(date)}}
                    },
                    {'$limit': 6},
                    user_details_steps[0],
                    user_details_steps[1],
                    user_details_steps[2],
                ]
            }
        }])
        reviews = list(reviews)[0]["data"]
    except Exception as e:
        print(str(e))

    return reviews