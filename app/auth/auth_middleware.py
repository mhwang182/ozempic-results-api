from functools import wraps

import jwt
from flask import current_app, g, request

from app.common.logging import log_message
from app.common.utils import create_response


def token_required(func):
    # *args means variable number of args, kwargs is keyword args
    @wraps(func)
    def before_func(*args, **kwargs):

        if('Authorization' not in request.headers):
            return create_response("Unauthorized", None, "Access Token not found")
                
        token_split = request.headers['Authorization'].split(" ")
        if(len(token_split ) < 2):
            return create_response("Unauthorized", None, "Incorrect Access Token")
        
        jwt_section = token_split[1]

        token = None
        try:
            token = jwt.decode(jwt_section, current_app.config["JWT_KEY"], algorithms=["HS256"])
        except Exception as e:
            log_message(str(e), 'error')
            return create_response("Unauthorized", None, "Cannot decode token")
                
        if("id" not in token):
            return create_response("Unauthorized", None, "Incorrect Access Token")
        
        g.userId = token["id"]

        return func(*args, **kwargs)
        
    return before_func
