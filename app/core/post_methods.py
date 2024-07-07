import dateutil
from bson import ObjectId

from app.common.logging import log_message
from app.common.utils import user_details_steps
from app.core.db import db


def add_post(new_post_doc):
    postId = None
    try: 
        postId = db.Posts.insert_one(new_post_doc).inserted_id
    except Exception as e: 
        log_message(str(e), 'error')

    return postId


def find_post(postId):
    post = None
    try:
        post = db.Posts.find_one({"_id": ObjectId(postId)})
    except Exception as e:
        log_message(str(e), 'error')
    
    return post

def delete_post_from_db(postId):
    count = 0
    try:
        count = db.Posts.delete_one({"_id": ObjectId(postId)}).deleted_count
    except Exception as e:
        log_message(str(e), 'error')
    return count

def get_user_posts_from_db(userId):
    posts = []
    try:
        posts = db.Posts.aggregate([
            {
                '$match': { 'userId': ObjectId(userId) },
            },
            user_details_steps[0],
            user_details_steps[1],
            user_details_steps[2],
            {
                '$sort': {'createdAt': -1}
            }
        ])
        posts = list(posts)
    except Exception as e:
        log_message(str(e), 'error')  

    return posts  

def get_feed_from_db(date):
    posts = []
    try:
        posts = db.Posts.aggregate([{
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
        posts = list(posts)[0]["data"]
    except Exception as e:
        log_message(str(e), 'error')
    return posts