from pymongo.mongo_client import MongoClient
import os

username = 'AEPC_user'
password = 'vis041che049chi050dhy063'

uri = "mongodb+srv://%s:%s@cluster0.3fajycc.mongodb.net/?retryWrites=true&w=majority" % (
    username, password)
# uri = "mongodb://localhost:27017/"
client = MongoClient(uri)
db = client['AutoExamPaperCorrection']