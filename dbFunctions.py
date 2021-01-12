from pymongo import MongoClient
import pymongo

# database connection
conn = MongoClient('mongodb://localhost:27017')
db = conn.forbesBillionaires
collection = db.people1


def youngest_10():
    print("------------------------------------------")
    print("Youngest 10 people in the first 200 forbes billionaires are: \n")
    for i in collection.find({"age": {"$ne": ""}},
                             {"forbes_id": 1,"name": 2, "age": 3, "_id": False}).sort([("age", 1), ("_id", pymongo.ASCENDING)]).limit(10):
        print(i)
    print("------------------------------------------")


# collection.update({"age": ""}, { "$unset" : { "age" : 2 }})

def us_citizenship():
    print("------------------------------------------")
    print("People with US citizenship are:\n ")
    count1 = 0
    results = collection.find({"citizenship": "United States"},
                              {"forbes_id": 1, "name": 2, "age": 3, "citizenship": 4, "_id": False})
    for result in results:
        count1 = count1 + 1
    # print(result)
    print("Number of people with US citizenship ( United States ) :", count1)
    print("Number of people without US citizenship", (200 - count1))

    print("------------------------------------------")


def philantropyscore():
    print("------------------------------------------")
    print("Top 10 people with the highest philanthropy scores: \n")
    for i in collection.find({"philanthropyScore": {'$ne': ""}},
                             {"forbes_id": 1, "name": 2, "philanthropyScore": 3, "_id": False}).sort([("philanthropyScore", pymongo.DESCENDING),("_id", pymongo.ASCENDING)]).limit(10):
        print(i)
    print("------------------------------------------")
    # for i in collection.find({ "$query":
    #                          {"forbes_id": 1, "name": 2, "philanthropyScore": 3, "_id": False}},
    #                           "$orderby":{"philanthropyScore:" -1}} ):
    #     print(i)


def rank():
    print("------------------------------------------")
    print(" People on same rank position in Forbes \n ")
    position = input("Give us a number for the searched rank:")
    for i in collection.find({"forbes_id": str(position)},
                             {"forbes_id": 1, "name": 2, "age": 3, "_id": False}).sort("age", 1):
        print(i)
    print("------------------------------------------")


youngest_10()
us_citizenship()
philantropyscore()
rank()
