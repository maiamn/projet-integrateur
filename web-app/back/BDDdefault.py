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

# Get n images de celebrites
@app.route("/celebs", methods=["GET"])
def get_images():
    try :
        # Get JSON request
        req = request.get_json()
        nb_images = (int)( req['nb_images'] )

        # CouchDB
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['images']
        
        # Mango query
        mango = ({  'selector': {},
                    'fields': ['_id']})

        query_result = db.find(mango)    
        id_list=[]         
        for row in query_result:                          
            id_list.append(row['_id'])         

        id_images = random.sample(id_list, nb_images)

        """ images = []
        for id in id_images:
            images.append(base64.b64encode(db.get_attachment(id, list(db.get(id) ['_attachments'].keys())).read()).decode('utf-8')) """

        response = {
            "title": "AnswerSrV",
            "user": req['user'],
            "id_partie": req['id_partie'],
            "nb_images": nb_images,
            "answer": {"images": id_images},
            "confirm": True
        }
        
    except Exception as e:
        response = {
            "title": "AnswerSrV",
            "user": req['user'],
            "id_partie": req['id_partie'],
            "nb_images": nb_images,
            "answer": {"images": []},
            "confirm": False,
            "error": repr(e)
        }
    finally :
        return jsonify(response)
      
# Get n images de celebrites
@app.route("/labels", methods=["GET"])
def get_labels():
    try :
        # Get JSON request
        req = request.get_json()

        ## for now we don't get the labels associated to the images of a "partie" but the labels associated to the following images 
        images = [
                "000003.jpg",
                "000004.jpg",
                "000002.jpg"
        ]

        # CouchDB
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['images']
        
        labels_dic = {}

        for image in images:
            # Mango query
            mango = ({  'selector': {'_id': image},
                        'fields': ['labels']})
            query_result = list(db.find(mango)) 
            labels_image = query_result[0]['labels'] 
            labels_dic[image] = labels_image

        response = {
            "title": "AnswerSrV",
            "user": req['user'],
            "id_partie": req['id_partie'],
            "answer": {"labels" : labels_dic},
            "confirm": True
        }

    except Exception as e:
        response = {
            "title": "AnswerSrV",
            "user": req['user'],
            "id_partie": req['id_partie'],
            "answer": {"labels" : {}},
            "confirm": False,
            "error": repr(e)
        }
    finally :
        return jsonify(response)

# Running app
if __name__ == '__main__':
    app.run(debug=True)