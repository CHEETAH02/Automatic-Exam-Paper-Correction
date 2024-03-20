from pymongo.mongo_client import MongoClient
import os

username = os.environ.get('DB_USERNAME')
password = os.environ.get('DB_PASSWORD')
uri = "mongodb+srv://%s:%s@cluster0.3fajycc.mongodb.net/?retryWrites=true&w=majority" % (
    username, password)
# uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
db = client['AutoExamPaperCorrection']