
from datetime import datetime

from bson.objectid import ObjectId

from app.core.review_methods import add_review


def create_review(reviewData):
    new_review_doc = {
        "userId": ObjectId(reviewData["userId"]),
        "rating": reviewData["rating"],
        "medication": reviewData["medication"],
        "sideEffects": reviewData["sideEffects"],
        "reviewBody": reviewData["reviewBody"],
        "createdAt": datetime.today().replace(microsecond=0)
    }
    review_id = add_review(new_review_doc)

    return str(review_id)

def transform_review(review):
    
    review["_id"] = str(review["_id"])
    review["userId"] = str(review["userId"])
    return review

def transform_reviews(reviews):

    review_data = []
    for review in reviews:
        review_data.append(transform_review(review))
    return review_data