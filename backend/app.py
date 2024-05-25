from flask import Flask, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def say_hello():
    return make_response("User is not logged in", 400)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)