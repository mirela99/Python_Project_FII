from pymongo import MongoClient


# conexiunea cu baza de datee
conn = MongoClient('mongodb://localhost:27017')
db = conn.forbesBillionaires
collection = db.people200


for i in collection.find({ "age": {'$ne': "" }} , {"name": 1, "age" : 2 }).sort('age').limit(10):
    print(i)

# collection.update({"age": ""}, { "$unset" : { "age" : 2 }})

def us_citizenship():
    count1 = 0
    results = collection.find({"citizenship": "United States"})
    for result in results:
        count1 = count1 + 1
        print(result)
    print("Persoane care au cetatenie americana ( United States ) :", count1)
    count2 = 0


