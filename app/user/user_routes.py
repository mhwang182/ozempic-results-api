from flask import Blueprint, request
from flask_cors import CORS

from app.auth.api_key_middleware import api_key_required
from app.auth.signup_code_middleware import signup_code_required
from app.core.db import find_user_by, getUser
from app.user.user_service import create_user, login_user

user_api = Blueprint("user_api", "user_api", url_prefix="/user")

CORS(user_api)

@user_api.route('/login', methods=['POST'])
@api_key_required
def login():
    data = request.get_json()["credentials"]
    inputEmail = data["email"]
    inputPassword = data["password"]

    user = getUser(inputEmail)

    if(not user):
        return {
        "message": "user not found",
        "data": None,
    }, 401
    
    response = login_user(inputEmail, inputPassword, user)

    if(not response):
       return {
           "message": "password incorrect",
           "data": None
       }, 404
    
    return response, 200

@user_api.route('', methods=['POST'])
@api_key_required
@signup_code_required
def createUser():

    new_user_dto = request.get_json()["user"]

    user = find_user_by(new_user_dto["email"], new_user_dto["username"], None)

    if(user):
        return {
            "message": "user already exists",
            "data": None
        }, 403
    
    response = create_user(new_user_dto)

    if(response):
        return response, 201

    return {}, 404