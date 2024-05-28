import bcrypt
import jwt

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

def create_jwt_token(email):
    return jwt.encode({
                "email": email,
                "timestamp": ""
            }, 
            "secret", 
            algorithm="HS256")


def login_user(email, password, user):
    if(passwords_match(password, user["password"])):
        token = create_jwt_token(email)
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
        token = create_jwt_token(new_user_dto["email"])
        new_user_dto["_id"] = objectId
        return {
            "user": create_user_dto(new_user_dto),
            "token": token
        }
    
    return None
