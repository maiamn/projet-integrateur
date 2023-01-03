# Import flask and datetime module for showing date and time
from flask import Flask, jsonify, request
from flask_cors import CORS
import couchdb
import base64
import random
  
# Initializing flask app
app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.secret_key = "123"
cors.init_app(app)


# Get images uploadees
@app.route("/images", methods=["GET"])
def get_images():
    try :
        # Get JSON request
        req = request.get_json()

        # CouchDB
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['images']
        
        id_images = [
                "000003.jpg",
                "000004.jpg",
                "000002.jpg"
        ]

        images_data = []
        for id in id_images:
            images_data.append(base64.b64encode(db.get_attachment(id, list(db.get(id) ['_attachments'].keys())).read()).decode('utf-8'))


        response = {
            "title": "AnswerSrV",
            "user": req['user'],
            "id_partie": req['id_partie'],
            "answer": {"images": [images]},
            "confirm": True
        }

    except Exception as e:
        response = {
            "title": "AnswerSrV",
            "user": req['user'],
            "id_partie": req['id_partie'],
            "answer": {"images": []},
            "confirm": False,
            "error": repr(e)
        }

    finally :
        return jsonify(response)


# Upload Images
## TO DO !
@app.route("/upload", methods=["POST"])
def upload_images():
    try :
        # Get JSON request
        req = request.get_json()


        response = {
            "title": "ConfirmSrV",
            "user": req['user'],
            "id_partie": req['id_partie'],
            "images": req['images'],
            "confirm": True
        }
    
    except Exception as e:
        response = {
            "title": "AnswerSrV",
            "user": req['user'],
            "id_partie": req['id_partie'],
            "images": req['images'],
            "confirm": False,
            "error": repr(e)
        }
        
    finally :
        return jsonify(response)


# Delete Images associated with a party
@app.route("/delete", methods=["DELETE"])
def delete_images():
    try :
        # Get JSON request
        req = request.get_json()

        # CouchDB
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['images']

        id_images = [
                "test"
        ]

        for id in id_images:
            # Mango query
            mango = ({  'selector': {'_id': id},
                        'fields': ['_id']})
            query_result = list(db.find(mango))
            del db[query_result[0].id]

        response = {
            "title": "AnswerSrV",
            "user": req['user'],
            "id_partie": req['id_partie'],
            "confirm": True
        }                      

    
    except Exception as e:
        print(e)
        response = {
            "title": "AnswerSrV",
            "user": req['user'],
            "id_partie": req['id_partie'],
            "confirm": False,
            "error": repr(e)
        }
        
    finally :
        return jsonify(response)

# Running app
if __name__ == '__main__':
    app.run(debug=True)