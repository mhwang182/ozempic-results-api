from flask import current_app, g
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from werkzeug.local import LocalProxy

from app.common.logging import log_message


def getUser(email):
    user = db.Users.find_one({"email": email})
    return user

def find_user_by(email, username, userId):

    fields = []
    if(email):
        fields.append({'email': email})
    
    if(username):
        fields.append({'username': username})
    
    if(userId):
        fields.append({'_id': userId})

    print(fields)
    try:
        users = db.Users.aggregate([
            {
                '$match': {'$or': fields}
            }
        ])
        users = list(users)

        if(len(users) == 0):
            return None
        
        return users[0]
            
    except Exception as e:
        log_message(str(e), 'error')
    
    return {}
    

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
        log_message(str(e), 'error')
    
    return objectId

def get_db():
    uri = current_app.config['MONGO_URI']
    db_name = current_app.config['DATABASE_NAME']
    db = getattr(g, "_database", None)

    if(db == None):
        client = MongoClient(uri, server_api=ServerApi('1'))
        g._database = db = client.get_database(db_name)
    return db

db = LocalProxy(get_db)
    
