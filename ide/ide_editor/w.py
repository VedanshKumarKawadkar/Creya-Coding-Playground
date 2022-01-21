# from traceback import print_tb
from pymongo import MongoClient

client = MongoClient("mongodb+srv://vk:1234@ide.gt9wy.mongodb.net/ide?retryWrites=true&w=majority")
dbs = client.list_database_names()
print(dbs)
db = client.ide
cols = db.list_collection_names()
print(cols)