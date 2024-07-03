from bson import ObjectId
from flask import Blueprint, request
from flask_cors import CORS

from app.auth.api_key_middleware import api_key_required
from app.auth.auth_middleware import token_required
from app.common.utils import create_response
from app.core.db import find_user_by
from app.core.review_methods import (
    delete_review_from_db,
    fetch_reviews_feed,
    get_review_from_db,
    get_reviews_from_db,
)
from app.reviews.reviews_service import (
    create_review,
    transform_review,
    transform_reviews,
)

reviews_api = Blueprint("reviews_api", "reviews_api", url_prefix="/reviews")

CORS(reviews_api)


def validate_review(review):
    return True

@reviews_api.route("/create", methods=["POST"])
@api_key_required
@token_required
def add_review():
    data = request.get_json()
    if("review" not in data):
        return None
    
    if("userId" not in data):
        return None
    
    reviewData = data["review"]
    reviewData["userId"] = data["userId"]

    print(data)
    create_review(reviewData)

    return {
        "message": "",
        "data": None
    }

@reviews_api.route("/delete", methods=["POST"])
@api_key_required
@token_required
def delete_review():
    
    data = request.get_json()

    if("reviewId" not in data or "userId" not in data):
        return create_response("", None, None), 401
    
    review = get_review_from_db(data["reviewId"])

    if(not review):
        return create_response("", None, None), 404
    
    if(str(review["userId"]) != data["userId"]):
        return create_response("Not authorized to delete this review", None, None), 401
    
    deleted_count = delete_review_from_db(data["reviewId"])

    if(deleted_count == 0):
        return create_response("Unable to delete review", None, None), 404
    
    return create_response("Review deleted successfully", None, None), 200

@reviews_api.route("/listByUserId", methods=["POST"])
@api_key_required
@token_required
def get_reviews_by_id():

    data = request.get_json()
    if("userId" not in data):
        return {
            "data": None
        }, 400
    
    reviews = get_reviews_from_db(data["userId"])
    if(not reviews):
        return {
            "data": None
        }, 404
    
    reviews = transform_reviews(reviews)

    return {
        "data": {"reviews": reviews}
    }, 200

@reviews_api.route("/get", methods=["GET"])
@api_key_required
def get_review_by_id():

    reviewId = request.args.get("reviewId")

    if(not reviewId):
        return {"data": None}, 401

    review = get_review_from_db(reviewId)

    if(not review):
        return {"data": None}, 404
    
    review = transform_review(review)
    user = find_user_by(None, None, ObjectId(review["userId"]))

    if(user):
        review["userDetails"] = {"username": user["username"]}

    return {"data": {"review": review}}, 200

@reviews_api.route("/feed", methods=["POST"])
@api_key_required
def get_reviews_feed():

    data = request.get_json()
    if("date" not in data):
        return {
            "data": None
        }, 400

    date = data["date"]

    reviews_aggregate = fetch_reviews_feed(date)

    reviews = transform_reviews(reviews_aggregate)

    return {
        "data": {"reviews": reviews}
    }, 200