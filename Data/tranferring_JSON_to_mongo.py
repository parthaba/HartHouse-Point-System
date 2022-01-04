from pymongo import MongoClient
import json

FALL_2018 = "Semesters/Fall 2018.json"
FALL_2019 = "Semesters/Fall 2019.json"
FALL_2020 = "Semesters/Fall 2020.json"
FALL_2021 = "Semesters/Fall 2021.json"
WINTER_2018 = "Semesters/Winter 2018.json"
WINTER_2019 = "Semesters/Winter 2019.json"
WINTER_2020 = "Semesters/Winter 2020.json"
WINTER_2021 = "Semesters/Winter 2021.json"

cluster = MongoClient("mongodb+srv://arpi:sfUabBK5WNxnTz4@cluster0.uerlw.mongodb.net/test?retryWrites=true&w=majority")
db = cluster["Semesters"]
collection = db["Fall 2021"]

with open(FALL_2021, 'r') as openfile:
    json_file = json.load(openfile)
    file = json_file["entry"]

for data_entry in file:
    data_entry["_id"] = data_entry.pop('entry_id')
    print(data_entry)
    collection.insert_one(data_entry)
