from bson import ObjectId
from flask import Blueprint, g, request
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
    validate_new_review,
)

reviews_api = Blueprint("reviews_api", "reviews_api", url_prefix="/reviews")

CORS(reviews_api)

@reviews_api.route("/create", methods=["POST"])
@api_key_required
@token_required
def add_review():
    data = request.get_json()
    if("review" not in data):
        return create_response("Incorrect request data", None, None), 400
    
    if("userId" not in g):
        return create_response("Incorrect request data", None, None), 400
    
    reviewData = data["review"]
    reviewData["userId"] = g.userId
    
    if(not validate_new_review(reviewData)):
        return create_response("Incorrect request data", None, None), 400
    
    reviewId = create_review(reviewData)

    if(not reviewId):
        return create_response("Unable to add review", None, None), 500

    return create_response("Successfuly created review", {"reviewId": reviewId}, None), 200

@reviews_api.route("/delete", methods=["POST"])
@api_key_required
@token_required
def delete_review():
    
    data = request.get_json()

    if("reviewId" not in data or "userId" not in g):
        return create_response("Incorrect request data", None, None), 400
    
    review = get_review_from_db(data["reviewId"])

    if(not review):
        return create_response("Review not found", None, None), 404
    
    if(str(review["userId"]) != g.userId):
        return create_response("Not authorized to delete this review", None, None), 401
    
    deleted_count = delete_review_from_db(data["reviewId"])

    if(deleted_count == 0):
        return create_response("Review not deleted", None, None), 404
    
    return create_response("Review deleted successfully", None, None), 200

@reviews_api.route("/listByUserId", methods=["POST"])
@api_key_required
@token_required
def get_reviews_by_id():

    if("userId" not in g):
        return create_response("Incorrect request data", None, None), 400
    
    reviews = get_reviews_from_db(g.userId)
    if(not reviews):
        return create_response("Review not found", None, None), 404
    
    reviews = transform_reviews(reviews)

    return create_response("Reviews returned successfully", {"reviews": reviews}, None), 200

@reviews_api.route("/get", methods=["GET"])
@api_key_required
def get_review_by_id():

    reviewId = request.args.get("reviewId")

    if(not reviewId):
        return create_response("Incorrect request data", None, None), 400

    review = get_review_from_db(reviewId)

    if(not review):
        return create_response("Review not found", None, None), 404
    
    review = transform_review(review)
    user = find_user_by(None, None, ObjectId(review["userId"]))

    if(user):
        review["userDetails"] = {"username": user["username"]}

    return create_response("Reviews returned successfully", {"review": review}, None), 200

@reviews_api.route("/feed", methods=["POST"])
@api_key_required
def get_reviews_feed():

    data = request.get_json()
    if("date" not in data):
        return create_response("Incorrect request data", None, None), 400

    date = data["date"]

    reviews_aggregate = fetch_reviews_feed(date)

    reviews = transform_reviews(reviews_aggregate)

    return create_response("Reivews returned successfully", {"reviews": reviews}, None), 200