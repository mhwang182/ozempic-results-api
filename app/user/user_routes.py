from flask import Blueprint, request
from flask_cors import CORS

from app.auth.api_key_middleware import api_key_required
from app.auth.signup_code_middleware import signup_code_required
from app.common.utils import create_response
from app.core.db import find_user_by, getUser
from app.user.user_service import create_user, login_user

user_api = Blueprint("user_api", "user_api", url_prefix="/user")

CORS(user_api)

@user_api.route('/login', methods=['POST'])
@api_key_required
def login():

    data = request.get_json()

    if("credentials" not in data):
        return create_response("Incorrect request data", None, None), 400
    
    if("email" not in data["credentials"] or "password" not in data["credentials"]):
        return create_response("Incorrect request data", None, None), 400
    
    inputEmail = data["credentials"]["email"]
    inputPassword = data["credentials"]["password"]

    user = getUser(inputEmail)

    if(not user):
        return create_response("user not found", None, None), 404
    
    response = login_user(inputEmail, inputPassword, user)

    if(not response or response == None):
       return create_response("password incorrect", None, None), 401
    
    return response, 200

@user_api.route('', methods=['POST'])
@api_key_required
@signup_code_required
def createUser():

    new_user_dto = request.get_json()["user"]

    user = find_user_by(new_user_dto["email"], new_user_dto["username"], None)

    if(user):
        return create_response("User already exists"), 400
    
    response = create_user(new_user_dto)

    if(not response):
        return create_response("User not created", None, "Unable to create new user")
        
    return response, 201