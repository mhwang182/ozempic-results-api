import mimetypes
import uuid
from datetime import datetime

import blurhash
from bson.objectid import ObjectId

from app.core.db import add_post, get_feed, get_posts
from app.core.s3 import get_presigned_url, upload_image_s3


def get_extension(file):
    return mimetypes.guess_extension(file.mimetype)


def upload_post_image(image):
    if(image.content_type != 'image/jpeg' and image.content_type != 'image/png'):
        return None
    
    imageId = uuid.uuid4()
    filename = str(imageId) + get_extension(image)
 
    try:
        img_blurhash = blurhash.encode(image, x_components=3, y_components=3)
    except Exception as e:
        print(str(e))

    image.seek(0) #reset file pointer

    uploaded = upload_image_s3(image, filename)

    if(not uploaded):
        return None

    filename_blurhash = img_blurhash + '>' + filename
    return filename_blurhash

def create_post(beforeImageId, afterImageId, postDetails):
    new_post_doc = {
        "weightLost": int(postDetails["weightLost"]),
        "medicationUsed": postDetails["medicationUsed"],
        "caption": postDetails["caption"],
        "beforeImageId": beforeImageId,
        "afterImageId": afterImageId,
        "userId": ObjectId(postDetails["userId"]),
        "createdAt": datetime.today().replace(microsecond=0)
    }

    postId = add_post(new_post_doc)
    return str(postId)

def get_user_posts(userId):
    posts_data = []
    posts = get_posts(userId)
    
    for post in posts:
        post["beforeImageUrl"] = get_presigned_url(post["beforeImageId"])
        post["afterImageUrl"] = get_presigned_url(post["afterImageId"])
        post["_id"] = str(post["_id"])
        post["userId"] = str(post["userId"])
        posts_data.append(post)

    return posts_data

def get_feed_posts(date):

    posts_data = []
    data = get_feed(date)
    if(not data):
        return posts_data
    
    parsed_data = list(data)[0]
    posts = parsed_data["data"]

    for post in posts:
        post["beforeImageUrl"] = get_presigned_url(post["beforeImageId"])
        post["afterImageUrl"] = get_presigned_url(post["afterImageId"])
        post["_id"] = str(post["_id"])
        post["userId"] = str(post["userId"])
        posts_data.append(post)
    
    return posts_data