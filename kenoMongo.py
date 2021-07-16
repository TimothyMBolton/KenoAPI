import pymongo
from pymongo import MongoClient
import ssl, json

mongoDBUrl = 'mongodb+srv://timothybolton:1234@kenocluster.5epmw.mongodb.net/test?retryWrites=true&w=majority'


cluster = MongoClient(mongoDBUrl, ssl_cert_reqs=ssl.CERT_NONE)

db = cluster['Keno']
collection = db['KenoGames']

with open('./Data/2021-07-09 Keno Games.json') as f:
    data = json.load(f)
    for object in data:
        collection.insert_one(object)


# Delete Everything
# results = collection.find()
# for result in results:
#     collection.find_one_and_delete({"_id": result['_id']})

