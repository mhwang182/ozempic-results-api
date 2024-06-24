import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, support_credentials=True)

from app.posts.posts_routes import posts_api
from app.reviews.reviews_routes import reviews_api
from app.user.user_routes import user_api

app.register_blueprint(user_api)
app.register_blueprint(posts_api) 
app.register_blueprint(reviews_api)

@app.route("/ping", methods=["GET"])
def health_check():
    return {}, 200

@app.route("/")
def home():
    return "Hello world"

load_dotenv()

app.config['MONGO_URI'] = os.getenv("MONGO_URI")
app.config['DATABASE_NAME'] = os.getenv("DATABASE_NAME")
app.config['BUCKET_NAME'] = os.getenv("BUCKET_NAME")
app.config['S3_ACCESS_KEY_ID'] = os.getenv("S3_ACCESS_KEY_ID")
app.config['S3_SECRET_ACCESS_KEY'] = os.getenv("S3_SECRET_ACCESS_KEY")
app.config['S3_ENDPOINT_URL'] = os.getenv("S3_ENDPOINT_URL")
app.config['API_KEY'] = os.getenv("API_KEY")
app.config['SIGN_UP_CODE'] = os.getenv("SIGN_UP_CODE")
port = os.getenv("PORT")
print(port)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)