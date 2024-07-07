
from flask import Blueprint
from flask_cors import CORS

health_api = Blueprint("health_api", __name__)

CORS(health_api)

@health_api.route("/ping", methods=["GET"])
def health_check():
    return {}, 200

@health_api.route("/")
def home():
    return "Hello world"
