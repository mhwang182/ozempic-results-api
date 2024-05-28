from flask import Blueprint, request
from flask_cors import CORS

from app.auth.api_key_middleware import api_key_required
from app.auth.auth_middleware import token_required
from app.posts.posts_service import (
    create_post,
    get_feed_posts,
    get_user_posts,
    upload_post_image,
)

posts_api = Blueprint("posts_api", "posts_api", url_prefix="/posts")

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

    posts = get_user_posts(data["userId"])

    return {
        "data": {"posts": posts}
    }, 200

@posts_api.route("/feed", methods=["POST"])
@api_key_required
def get_feed():
    data = request.get_json()
    posts = get_feed_posts(data["date"])

    return {
        "message": "feed posts",
        "data": {"posts": posts}
    }, 200