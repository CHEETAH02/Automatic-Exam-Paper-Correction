from pymongo.mongo_client import MongoClient
import os

username = os.environ.get('DB_USERNAME')
password = os.environ.get('DB_PASSWORD')
uri = "YOUR_MONGODB_URI"
client = MongoClient(uri)
db = client['AutoExamPaperCorrection']