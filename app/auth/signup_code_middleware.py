from functools import wraps

from flask import current_app, request


def signup_code_required(func):
    @wraps(func)
    def before_func(*args, **kwargs):
        data = request.get_json()
        if("signUpCode" not in data or data["signUpCode"] != current_app.config['SIGN_UP_CODE']):
            return {
                "message": "invalid sign up code",
                "data": None
            }, 403
    
        return func(*args, **kwargs)
    return before_func
