from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://arpi:sfUabBK5WNxnTz4@cluster0.uerlw.mongodb.net/test?retryWrites=true&w=majority")
db = cluster["test"]
collection = db["test"]
post1 = {"_id": 5,
         "name": "joe"}
post2 = {"_id": 6,
         "name": "bill"}

results = collection.find({})
#
# print(results)
# for result in results:
#     print(result["name"])
