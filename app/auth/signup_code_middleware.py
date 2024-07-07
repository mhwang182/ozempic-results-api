from functools import wraps

from flask import current_app, request

from app.common.utils import create_response


def signup_code_required(func):
    @wraps(func)
    def before_func(*args, **kwargs):
        data = request.get_json()
        if("signUpCode" not in data or data["signUpCode"] != current_app.config['SIGN_UP_CODE']):
            return create_response("Incorrect Sign Up Code", None, None), 403
    
        return func(*args, **kwargs)
    return before_func
