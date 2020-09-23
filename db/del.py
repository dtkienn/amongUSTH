import pymongo

client = pymongo.MongoClient("mongodb+srv://Sm00thiee:123@cluster0.3ihx5.mongodb.net/?retryWrites=true&w=majority")
db = client['mydatabase']
col = db["student"]

col.drop()