
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

def validate_new_review(review):
    if not isinstance(review, dict):
        return False

    required_keys = ['rating', 'medication', 'sideEffects', 'reviewBody']
    for key in required_keys:
        if key not in review:
            return False
    
    if not isinstance(review['rating'], int) or review['rating'] < 1 or review['rating'] > 5:
        return False
    
    if not isinstance(review['medication'], str):
        return False
    
    if not isinstance(review['sideEffects'], list) or not all(isinstance(effect, str) for effect in review['sideEffects']):
        return False
    
    if not isinstance(review['reviewBody'], str):
        return False
    
    return True
