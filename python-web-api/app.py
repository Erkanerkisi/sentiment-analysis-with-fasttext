from flask import Flask
from flask import request
from fasttext import train_supervised, load_model
from pymongo import MongoClient
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
cluster = "mongodb://mongo/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"

@app.route('/data', methods=['POST'])
def sendData():
    data = request.get_json()
    reviewtext = data["text"]
    reviewlabel = data["label"]
    insertToDB(reviewlabel, reviewtext)
    return "saved"


def insertToDB(label, review):
    with MongoClient(cluster) as client:
        # client = MongoClient(cluster)

        db = client.fasttext
        ec = db.ecommercereviews
        insert = {"label": label, "review": review}
        print(insert)
        result = ec.insert_one(insert)


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

    if not os.path.exists("comments.bin"):
        create_model()
        print("predict comments.bin not exist")

    model = load_model("comments.bin")

    # print(model.test())
    result = model.predict(review)
    # insertToDB(result[0][0], review)
    return result[0][0]


@app.route('/insert-to-db', methods=['GET'])
def insertToDbFromText():
    with MongoClient(cluster) as client:
        # client = MongoClient(cluster)
        db = client.fasttext
        ec = db.ecommercereviews
        result1 = ec.delete_many({})

        ecommerceReviewsFile = open("eticaretyorumlari.txt", encoding="utf8")
        # contents = ecommerceReviewsFile.readlines()

        for line in ecommerceReviewsFile:
            lineStrip = line.strip()
            label = lineStrip[0:10]
            review = lineStrip[11:]

            insert = {"label": label, "review": review}
            print(insert)
            result = ec.insert_one(insert)
        ecommerceReviewsFile.close()
        response = refreshModel()
    return response


@app.route('/write-to-txt', methods=['GET'])
def writeToText():
    with MongoClient(cluster) as client:
        # client = MongoClient(cluster)
        print("******Write To text started *******")
        db = client.fasttext
        ec = db.ecommercereviews
        if os.path.exists("ecommercereview.txt"):
            os.remove("ecommercereview.txt")
        else:
            print("The file does not exist")

        ecommerceReviewsFile = open("ecommercereview.txt", "w")
        result = ec.find({})
        # ecommerceReviewsFile.writelines(' '.join(map(str, list(result))))

        resultArray = list(result)
        resultSize = len(resultArray)
        count = 0
        for res in resultArray:
            count += 1
            if count != resultSize:
                string = res["label"] + " " + res["review"] + "\n"
            else:
                string = res["label"] + " " + res["review"]

            ecommerceReviewsFile.writelines(string)
        ecommerceReviewsFile.close()
        print("******Write To text ended *******")
    return "All data from the DB has been added to a text file!"


@app.route('/refresh-model', methods=['GET'])
def refreshModel():
    res = writeToText()
    response_model = create_model()
    return res + " - " + response_model


@app.route('/test', methods=['GET'])
def test():
    model = load_model("comments.bin")
    result = model.test("test.txt")
    print(result)
    str1 = ''.join(" " + str(e) for e in result)
    return str1


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
