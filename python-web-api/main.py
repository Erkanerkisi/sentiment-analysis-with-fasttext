import datetime

from pymongo import MongoClient

cluster = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"
client = MongoClient(cluster)

print(client.list_database_names())

db = client.test

print(db.list_collection_names())

todo1 = {"name": "Patrick", "text": "first todo", "status": "open",
         "tags": ["python", "coding"], "date": datetime.datetime.utcnow()}
todos = db.todos

#result = todos.insert_one(todo1)

todo2 = [{"name": "Patrick", "text": "second todo", "status": "open",
          "tags": ["python", "coding"], "date": datetime.datetime.utcnow()},
         {"name": "Mary", "text": "third todo", "status": "open",
          "tags": ["python", "coding"], "date": datetime.datetime.utcnow()}]

#result = todos.insert_many(todo2)

result = todos.find_one()

print(result)

result2 = todos.find_one({"name": "Mary"})
print(result2)

result3 = todos.find_one({"name": "Patrick", "text": "second todo"})

print(result3)

result4 = todos.find_one({"tags": "python"})

print(result4)

from bson import ObjectId
result5 = todos.find_one({'_id': ObjectId('61911a051aacce3f7aa57d5a')})

print(result5)

results = todos.find({"name": "Patrick"})
print(list(results))
for res in results:
    print(res)

print(todos.count_documents({}))

print(todos.count_documents({"name": "Patrick"}))

from bson.objectid import ObjectId

#result = todos.delete_one({'_id': ObjectId('61911a051aacce3f7aa57d5a')})
#result = todos.delete_many({"name": "Patrick"})
#result = todos.delete_many({})
result = todos.update_one({"name": "Patrick"},{"$set": {"tags": ["c++", "coding"]}})

results2 = todos.find({})
print(list(results2))