from flask import Flask
app = Flask(__name__)

@app.route("/ind",methods=['GET'])
def hello():
    return "Hello world"


if __name__ == "__main__":
    app.run(debug=True)
