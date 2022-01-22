# from traceback import print_tb
from pymongo import MongoClient

client = MongoClient("mongodb+srv://vk:1234@ide.gt9wy.mongodb.net/ide?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE", connect=False)
print(client)
ideDB = client.ide

cols = ideDB.list_collection_names()

print(cols)
