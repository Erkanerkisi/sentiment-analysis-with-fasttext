from flask import Flask
from fasttext import train_supervised, load_model

app = Flask(__name__)


@app.route('/create/', methods=['GET', 'POST'])
def save():
    # train_supervised uses the same arguments and defaults as the fastText cli
    model = train_supervised(
        input="eticaretyorumlari.txt", epoch=25, lr=1.0, wordNgrams=2, verbose=2, minCount=1
    )
    model.save_model("comments.bin")
    return "Saved"


@app.route('/predict/', methods=['GET'])
def predict():
    # train_supervised uses the same arguments and defaults as the fastText cli
    model = load_model("comments.bin")
    # print(model.test())
    print(model.predict("Ürün harika. tam istediğim birşey"))
    return "Predicted!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
