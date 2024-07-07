import mimetypes
import uuid
from datetime import datetime

import blurhash
from bson.objectid import ObjectId

from app.common.logging import log_message
from app.core.post_methods import add_post
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
        log_message(str(e), 'error')

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

def transofrm_post(post):
    post["beforeImageUrl"] = get_presigned_url(post["beforeImageId"])
    post["afterImageUrl"] = get_presigned_url(post["afterImageId"])
    post["_id"] = str(post["_id"])
    post["userId"] = str(post["userId"])
    return post

def transform_posts(posts):

    transformed_posts = []

    for post in posts:
        transformed_posts.append(transofrm_post(post))
    
    return transformed_posts