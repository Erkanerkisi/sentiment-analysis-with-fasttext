from pymongo import MongoClient


cluster = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"

with MongoClient(cluster) as client:
#client = MongoClient(cluster)

    db = client.fasttext
    todos = db.ecommercereviews
    result1 = todos.delete_many({})

    ecommerceReviewsFile = open("eticaretyorumlari.txt", "r")
#contents = ecommerceReviewsFile.readlines()

    for line in ecommerceReviewsFile:
        lineStrip = line.strip()
        label = lineStrip[0:10]
        review = lineStrip[10:]

        insert = { "label":   label  ,   "review":   review  }
        print(insert)
        result = todos.insert_one(insert)
    ecommerceReviewsFile.close()