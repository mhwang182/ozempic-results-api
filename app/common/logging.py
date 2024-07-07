import logging

from flask import request


def log_message(message, level='info'):

    log_data = {
        'method': request.method,
        'endpoint': request.endpoint
    }
    
    if(level == 'error'):
        log_data["error"] = message
        logging.error(log_data)