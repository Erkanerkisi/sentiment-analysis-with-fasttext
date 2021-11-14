from flask import Flask
from flask import request
from fasttext import train_supervised, load_model
from pymongo import MongoClient
import os
from flask_cors import CORS




app = Flask(__name__)
CORS(app)

def insertToDB(label, review):
    cluster = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"

    with MongoClient(cluster) as client:
        # client = MongoClient(cluster)

        db = client.fasttext
        todos = db.ecommercereviews
        insert = {"label": label, "review": review}
        print(insert)
        result = todos.insert_one(insert)


@app.route('/model', methods=['POST'])
def create_model():
    # train_supervised uses the same arguments and defaults as the fastText cli
    if os.path.exists("ecommercereview.txt"):
        model = train_supervised(
            input="ecommercereview.txt", epoch=25, lr=1.0, wordNgrams=2, verbose=2, minCount=1
        )
        model.save_model("comments.bin")
        return "Saved"
    else:
        return "ERROR!!! First you need to call insert-to-db!"



@app.route('/prediction', methods=['POST'])
def predict_text():
    data = request.get_json()
    # train_supervised uses the same arguments and defaults as the fastText cli
    review = data["text"]
    model = load_model("comments.bin")
    # print(model.test())
    result = model.predict(review)
    insertToDB(result[0][0], review)
    return result[0][0]

@app.route('/insert-to-db/', methods=['GET'])
def insertToDbFromText():
    cluster = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"

    with MongoClient(cluster) as client:
        # client = MongoClient(cluster)

        db = client.fasttext
        todos = db.ecommercereviews
        result1 = todos.delete_many({})

        ecommerceReviewsFile = open("eticaretyorumlari.txt", "r")
        # contents = ecommerceReviewsFile.readlines()

        for line in ecommerceReviewsFile:
            lineStrip = line.strip()
            label = lineStrip[0:10]
            review = lineStrip[10:]

            insert = {"label": label, "review": review}
            print(insert)
            result = todos.insert_one(insert)
        ecommerceReviewsFile.close()
    return "All data from the text file has been added to the DB!"


@app.route('/write-to-txt/', methods=['GET'])
def writeToText():
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
        # ecommerceReviewsFile.writelines(' '.join(map(str, list(result))))

        resultArray = list(result)
        resultSize = len(resultArray)
        count = 0
        for res in resultArray:
            count += 1
            if count != resultSize:
                string = res["label"] + res["review"] + "\n"
            else:
                string = res["label"] + res["review"]

            ecommerceReviewsFile.writelines(string)
        ecommerceReviewsFile.close()
    return "All data from the DB has been added to a text file!"




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
