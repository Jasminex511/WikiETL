from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["profile_database"]
collection = db["profiles"]

# Query all documents
profiles = collection.find()
for profile in profiles:
    print(profile)
