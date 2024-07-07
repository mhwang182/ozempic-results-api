import dateutil
from bson import ObjectId

from app.common.logging import log_message
from app.common.utils import user_details_steps
from app.core.db import db


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
        posts = list(posts)
    except Exception as e:
        print(str(e))

    return posts

def search_user_posts(userId, date):
    posts = []
    try:
        posts = db.Posts.aggregate([
        {'$match': {'userId': ObjectId(userId)}},
        {'$sort': {'createdAt': -1}}, 
        {
            '$match': {'createdAt': {'$lt': dateutil.parser.parse(date)}}
        },
        {'$limit': 6},
        user_details_steps[0],
        user_details_steps[1],
        user_details_steps[2]])

        posts = list(posts)
    except Exception as e:
        log_message(str(e), 'error')

    return posts