# Import flask and datetime module for showing date and time
from flask import Flask, jsonify, request
from flask_cors import CORS
  
# Initializing flask app
app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.secret_key = "123"
cors.init_app(app)
  
  
@app.route('/', methods=["GET"])
def firstRoute():
    return jsonify({"message" : "Hello world"})

@app.route("/sent", methods=["POST"])
def test_receive():
    infos = request.get_json()
    print(infos)
    name = infos["message"]["name"]
    print(name)
    return jsonify({"message": "Hello "+name})
      
# Running app
if __name__ == '__main__':
    app.run(debug=True)