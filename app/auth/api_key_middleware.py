from functools import wraps

from flask import current_app, g, request

from app.common.utils import create_response


def api_key_required(func):
    @wraps(func)
    def before_func(*args, **kwargs):

        if('X_API_KEY' not in request.headers):
            return create_response("Unauthorized", None, "API Key not found"), 401
        
        request_api_key = request.headers["X_API_KEY"]
        if(request_api_key != current_app.config["API_KEY"]):
            return create_response("Unauthorized", None, "Incorrect API Key"), 401
        
        g.test = "hello world"

        return func(*args, **kwargs)

    return before_func