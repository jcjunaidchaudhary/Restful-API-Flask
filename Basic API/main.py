import re
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/CheckEven/<int:term>")
def CheckEven(term):
    if term%2==0:
        result={
            "Number":term,
            "Even":True,
            "Server IP":"123.4343.53"
        }
    else:
         result={
            "Number":term,
            "Even":False,
            "Server IP":"123.4343.53"
        }

    return jsonify(result)


if __name__== "__main__":
    app.run(debug=True)