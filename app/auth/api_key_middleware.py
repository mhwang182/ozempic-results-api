from functools import wraps

from flask import current_app, request


def api_key_required(func):
    @wraps(func)
    def before_func(*args, **kwargs):

        if('X_API_KEY' not in request.headers):
            print('API key not found')
            return {
                "message": "API Key not found",
                "data": None,
                "error": "Unauthorized"
            }, 401
        
        request_api_key = request.headers["X_API_KEY"]
        if(request_api_key != current_app.config["API_KEY"]):
            print('Incorrect API key')
            return {
                "message": "Incorrect Api Key",
                "data": None,
                "error": "Unauthorized"
            }, 401
        
        return func(*args, **kwargs)

    return before_func