import dateutil
from bson import ObjectId

from app.common.utils import user_details_steps
from app.core.db import db


def add_post(new_post_doc):
    print('trying post to mongo')
    postId = None
    try: 
        postId = db.Posts.insert_one(new_post_doc).inserted_id
    except Exception as e: 
        print(str(e))

    return postId


def find_post(postId):
    post = None
    try:
        post = db.Posts.find_one({"_id": ObjectId(postId)})
    except Exception as e:
        print(str(e))
    
    return post

def delete_post_from_db(postId):
    count = 0
    try:
        count = db.Posts.delete_one({"_id": ObjectId(postId)}).deleted_count
    except Exception as e:
        print(str(e))
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
    except Exception as e:
        print(str(e))  

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
    except Exception as e:
        print(str(e))
    return posts

def search_posts(search_term, pagination_token):

    posts = []

    search_stage = {
        "index": "PostMedicationSearch",
        "text": {
            "query": search_term,
            "path": {
            "wildcard": "*"
            }
        },
    }

    if(pagination_token):
        search_stage["searchAfter"] = pagination_token

    try:
        posts = db.Posts.aggregate([
            {
                "$search": search_stage
            },
            {
                "$limit": 6
            },
            user_details_steps[0],
            user_details_steps[1],
            user_details_steps[2],
            {
                "$project": {
                    "medicationUsed": 1,
                    "userId": 1,
                    "createdAt": 1,
                    "weightLost": 1,
                    "beforeImageId": 1,
                    "afterImageId": 1,
                    "caption": 1,
                    "userDetails": 1,
	                "paginationToken": { "$meta" : "searchSequenceToken" },
                }
            }
        ])
    except Exception as e:
        print(str(e))

    return posts