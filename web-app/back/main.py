# Import flask and datetime module for showing date and time
from flask import Flask, jsonify, request
from flask_cors import CORS
import couchdb
import base64
  
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

@app.route("/add", methods=["POST"])
def add_images():
    infos = request.files
    print(infos)
    return jsonify({"image": "coucou"})

@app.route("/db", methods=["GET"])
def test_DB():
    # CouchDB
    couch = couchdb.Server("http://user:user@localhost:5984")
    db = couch['images']
    for id in db:
        print(base64.b64encode(db.get_attachment(id, list(db.get(id) ['_attachments'].keys())).read()).decode('utf-8'))
    return jsonify({"data": base64.b64encode(db.get_attachment(id, list(db.get(id) ['_attachments'].keys())).read()).decode('utf-8')})
      
# Running app
if __name__ == '__main__':
    app.run(debug=True)