import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from app.posts.posts_routes import posts_api
from app.user.user_routes import user_api

app = Flask(__name__)
CORS(app, support_credentials=True)

app.register_blueprint(user_api)
app.register_blueprint(posts_api)

load_dotenv()

app.config['MONGO_URI'] = os.getenv("MONGO_URI")
app.config['DATABASE_NAME'] = os.getenv("DATABASE_NAME")
app.config['BUCKET_NAME'] = os.getenv("BUCKET_NAME")
app.config['S3_ACCESS_KEY_ID'] = os.getenv("S3_ACCESS_KEY_ID")
app.config['S3_SECRET_ACCESS_KEY'] = os.getenv("S3_SECRET_ACCESS_KEY")
app.config['S3_ENDPOINT_URL'] = os.getenv("S3_ENDPOINT_URL")
app.config['API_KEY'] = os.getenv("API_KEY")

if __name__ == '__main__':
    app.run(port=5000)