import bcrypt
import jwt
from flask import current_app

from app.core.db import add_user


def create_user_dto(user):
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "username": user["username"],
        "firstname": user["firstname"],
        "lastname": user["lastname"]
    }

def passwords_match(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('ASCII'), hashed_password.encode('ASCII'))

def create_jwt_token(userId):
    return jwt.encode({
                "id": str(userId),
                "timestamp": ""
            }, 
            current_app.config["JWT_KEY"], 
            algorithm="HS256")


def login_user(password, user):
    if(passwords_match(password, user["password"])):
        token = create_jwt_token(user["_id"])
        userDto = create_user_dto(user)
        return { 
            "user": userDto, 
            "token": token 
        }
    
    return None

def create_user(new_user_dto):
    plain_text_password = new_user_dto["password"]
    hashed_password = bcrypt.hashpw(plain_text_password.encode('ASCII'), bcrypt.gensalt())
    #insert into db
    objectId = add_user(new_user_dto, hashed_password.decode('ASCII'))

    if(objectId):
        token = create_jwt_token(objectId)
        new_user_dto["_id"] = objectId
        return {
            "user": create_user_dto(new_user_dto),
            "token": token
        }
    
    return None
