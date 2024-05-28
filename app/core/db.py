import dateutil.parser
from bson.objectid import ObjectId
from flask import current_app, g
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from werkzeug.local import LocalProxy


def getUser(email):
    user = db.Users.find_one({"email": email})
    return user

def find_user_by(email, username):
    user = None
    try:
        user = db.Users.aggregate([
            {
                '$match': {'$or': [{'email': email}, {'username': username}]}
            }
        ])
    except Exception as e:
        print(str(e))
    
    return user
    

def add_user(new_user, hashed_password):
    user_doc = {
        'email': new_user["email"],
        "password": hashed_password,
        "username": new_user["username"],
        "firstname": new_user["firstname"],
        "lastname": new_user["lastname"]
    }

    try:
        objectId = db.Users.insert_one(user_doc).inserted_id
    except Exception as e:
        print(str(e))
    
    return objectId

def add_post(new_post_doc):
    print('trying post to mongo')
    postId = None
    try: 
        postId = db.Posts.insert_one(new_post_doc).inserted_id
    except Exception as e: 
        print(str(e))

    return postId

def get_posts(userId):
    posts = []
    try:
        # posts = db.Posts.find({"userId": userId})
        posts = db.Posts.aggregate([
            {
                '$match': { 'userId': ObjectId(userId) },
            },
            {
                '$lookup': {
                    'from': 'Users',
                    'localField': 'userId',
                    'foreignField': '_id',
                    'as': 'user_object'
                }
            },
            {
                '$set': {
                    'userDetails': {
                        'username': {'$arrayElemAt': ['$user_object.username', 0]}
                    }
                }
            },
            {
                '$unset': 'user_object'
            },
            {
                '$sort': {'createdAt': -1}
            }
        ])
    except Exception as e:
        print(str(e))  

    return posts  

def get_feed(date):
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
                    {
                        '$lookup': {
                            'from': 'Users',
                            'localField': 'userId',
                            'foreignField': '_id',
                            'as': 'user_object'
                        }
                    },
                    {
                        '$set': {
                            'userDetails': {
                                'username': {'$arrayElemAt': ['$user_object.username', 0]}
                            }
                        }
                    },
                    {
                        '$unset': 'user_object'
                    }
                ]
            }
        }])
    except Exception as e:
        print(str(e))
    return posts

def get_db():
    uri = current_app.config['MONGO_URI']
    db_name = current_app.config['DATABASE_NAME']
    db = getattr(g, "_database", None)

    if(db == None):
        client = MongoClient(uri, server_api=ServerApi('1'))
        g._database = db = client.get_database(db_name)
    return db

db = LocalProxy(get_db)
    
