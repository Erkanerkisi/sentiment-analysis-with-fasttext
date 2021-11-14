from pymongo import MongoClient
import os

cluster = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"

with MongoClient(cluster) as client:
    # client = MongoClient(cluster)

    db = client.fasttext
    todos = db.ecommercereviews
    if os.path.exists("ecommercereview.txt"):
        os.remove("ecommercereview.txt")
    else:
        print("The file does not exist")

    ecommerceReviewsFile = open("ecommercereview.txt", "w")
    result = todos.find({})
    #ecommerceReviewsFile.writelines(' '.join(map(str, list(result))))

    resultArray = list(result)
    resultSize = len(resultArray)
    count = 0
    for res in resultArray:
        count+=1
        if count != resultSize :
            string = res["label"] + res["review"]  + "\n"
        else:
            string = res["label"] + res["review"]

        ecommerceReviewsFile.writelines(string)
    ecommerceReviewsFile.close()