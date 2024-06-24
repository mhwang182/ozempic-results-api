from flask import Blueprint, request
from flask_cors import CORS

from app.auth.api_key_middleware import api_key_required
from app.auth.auth_middleware import token_required
from app.common.utils import create_response
from app.core.post_methods import (
    delete_post_from_db,
    find_post,
    get_feed_from_db,
    get_user_posts_from_db,
    search_posts,
)
from app.posts.posts_service import create_post, transform_posts, upload_post_image

posts_api = Blueprint("posts_api", __name__, url_prefix="/posts")

CORS(posts_api)

@posts_api.route("/create", methods=["POST"])
@api_key_required
@token_required
def addPost():
    postDetails = request.form.to_dict()
    print(postDetails)
    files = request.files

    beforeImage = files.getlist('beforeImage')
    afterImage = files.getlist('afterImage')

    if(len(beforeImage) < 1 or len(afterImage) < 1):
        return None
    
    beforeImageId = upload_post_image(beforeImage[0])
    afterImageId = upload_post_image(afterImage[0])

    if(not beforeImageId or not afterImageId):
        return  {
            "message": "post added unsuccessfully",
            "data": None,
            "error": "image upload error"
        }, 500

    postId = create_post(beforeImageId, afterImageId, postDetails)

    if(not postId):
        return  {
        "message": "post added unsuccessfully",
        "data": None,
        "error": "mongodb error"
    }, 500

    return  {
        "message": "added post successfully",
        "data": {"postId": postId},
    }, 200


@posts_api.route("/get", methods=["POST"])
@api_key_required
@token_required
def getUserPosts():
    data = request.get_json()

    if( "userId" not in data):
        return {
            "data": None
        }, 401
    
    posts = get_user_posts_from_db(data["userId"])
    posts = transform_posts(posts)

    return {
        "data": {"posts": posts}
    }, 200

@posts_api.route("/feed", methods=["POST"])
@api_key_required
def get_feed():
    data = request.get_json()

    if ("date" not in data):
        return create_response("date not found", None, None), 401

    posts_aggregate_cursor = get_feed_from_db(data["date"])
    parsed_data = (list(posts_aggregate_cursor)[0])["data"]

    posts = transform_posts(parsed_data)

    return create_response("feed posts", {"posts": posts}, None), 200

@posts_api.route("/delete", methods=["POST"])
@token_required
@api_key_required
def delete_post():
    data = request.get_json()

    if("postId" not in data or "userId" not in data):
        return create_response("", None, None), 401
    
    post = find_post(data["postId"])

    if(not post):
        return create_response("", None, None), 404
    
    if(str(post["userId"]) != data["userId"]):
        return create_response("", None, None), 401
    
    delete_count = delete_post_from_db(data["postId"])

    if(delete_count == 0):
        return create_response("Unable to delete post", None, None), 404

    return create_response("Successfully deleted post", None, None), 200

@posts_api.route("/search", methods=["POST"])
@api_key_required
def get_search_results_by_medication():

    data = request.get_json()

    if("searchTerm" not in data):
        return {
            "data": None
        }, 401

    search_term = data["searchTerm"]

    pagination_token = None
    if("paginationToken" in data):
        pagination_token = data["paginationToken"]

    posts_aggregate_cursor = search_posts(search_term, pagination_token)

    posts = transform_posts(list(posts_aggregate_cursor))

    return {
        "data": { "posts": posts }
    }, 200