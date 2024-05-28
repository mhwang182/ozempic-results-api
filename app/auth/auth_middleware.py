from functools import wraps

import jwt
from flask import request


def get_error_response(message, error):
    return {
        "message": message,
        "data": None,
        "error": error
    }, 401

def token_required(func):
    # *args means variable number of args, kwargs is keyword args
    @wraps(func)
    def before_func(*args, **kwargs):

        if('Authorization' not in request.headers):
            return get_error_response("Access Token not found", "Unauthorized")
        
        token_split = request.headers['Authorization'].split(" ")
        if(len(token_split ) < 2):
            return get_error_response("Incorrect Access Token", "Unauthorized")
        
        jwt_section = token_split[1]

        try:
            decode_token = jwt.decode(jwt_section, 'secret', algorithms=["HS256"])
            if(decode_token):
                return func(*args, **kwargs)
        except Exception as e:
            return get_error_response("", str(e))
        
    return before_func
