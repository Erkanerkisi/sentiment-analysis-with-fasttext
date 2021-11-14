from flask import Flask
from flask import request
from fasttext import train_supervised, load_model
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/model', methods=['POST'])
def create_model():
    # train_supervised uses the same arguments and defaults as the fastText cli
    model = train_supervised(
        input="eticaretyorumlari.txt", epoch=25, lr=1.0, wordNgrams=2, verbose=2, minCount=1
    )
    model.save_model("comments.bin")
    return "Saved"


@app.route('/prediction', methods=['POST'])
def predict_text():
    data = request.get_json()
    # train_supervised uses the same arguments and defaults as the fastText cli
    model = load_model("comments.bin")
    # print(model.test())
    result = model.predict(data["text"])
    return result[0][0]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
