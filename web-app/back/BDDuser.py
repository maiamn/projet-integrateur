# Import flask and datetime module for showing date and time
from flask import Flask, jsonify, request
from flask_cors import CORS
import couchdb
import base64
import random
import io
import json
import logging
import traceback
  
# Initializing flask app
app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.secret_key = "123"
cors.init_app(app)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

labels_name = ['5_o_Clock_Shadow', 'Bags_Under_Eyes', 'Bald', 'Bangs', 'Big_Lips',
 'Big_Nose', 'Black_Hair', 'Blond_Hair', 'Brown_Hair', 'Bushy_Eyebrows',
 'Chubby', 'Eyeglasses', 'Goatee', 'Gray_Hair', 'Heavy_Makeup',
 'High_Cheekbones', 'Male', 'Mouth_Slightly_Open', 'Mustache', 'No_Beard',
 'Oval_Face', 'Pale_Skin', 'Pointy_Nose', 'Receding_Hairline', 'Rosy_Cheeks',
 'Sideburns', 'Smiling', 'Straight_Hair', 'Wavy_Hair', 'Wearing_Earrings',
 'Wearing_Hat', 'Wearing_Lipstick', 'Wearing_Necklace', 'Wearing_Necktie',
 'Young'
]

# Get images uploadees
@app.route("/img/<id>", methods=["GET"])
def get_images(id):

    # CouchDB
    couch = couchdb.Server("http://user:user@localhost:5984")
    db = couch['user']

    db.get_attachment(id, list(db.get(id) ['_attachments'].keys())).read()

    return send_file(
        io.BytesIO(image),
        mimetype='image/jpeg',
        download_name=id)


# Upload Images
@app.route("/upload", methods=["POST"])
def upload_images():

    logging.info('upload route')

    try :
        infos = request.files
        content = request.form

        logging.debug("infos %s",infos)
        logging.debug("content %s",content)

        # CouchDB
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['user']

        #Recup les images et les labels pour chacunes
        for file in infos.keys():
            labels = [int(e) for e in list(content[file].split(" "))]
            labels_dic = {labels_name[i]:labels[i] for i in range(len(labels))}
            logging.debug('labels %s',labels_dic)

            doc = {'labels': labels_dic}
            db.save(doc)

            logging.debug('debugs %s : %s',file,infos[file])
            f = infos[file].read()

            db.put_attachment(doc=doc, content=f, filename="image", content_type="image/jpg")

        response = {
            "title": "ConfirmSrV",
            "confirm": True
        }
    
    except Exception as e:
        logging.error(traceback.format_exc())
        response = {
            "title": "ConfirmSrV",
            "confirm": False,
            "error": repr(e)
        }
        
    finally :

        return jsonify(response)


# Delete Images associated with a party
@app.route("/delete", methods=["DELETE"])
def delete_images():

    logging.info("delete")

    try :
        # Get JSON request
        req = request.get_json()

        logging.debug("req %s",req)

        # CouchDB
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['user']

        #TO DO : mettre les ids des images
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
        logging.error(traceback.format_exc())
        response = {
            "title": "AnswerSrV",
            "user": req['user'],
            "id_partie": req['id_partie'],
            "confirm": False,
            "error": repr(e)
        }
        
    finally :
        return jsonify(response)

# Get labels 
@app.route("/labels", methods=["GET"])
def get_labels():
    try :
        # Get JSON request
        req = request.get_json()

        #images = [
        #        "000003.jpg",
        #        "000004.jpg",
        #        "000002.jpg"
        #]
        images = req['images']

        # CouchDB
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['user']
        
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
    app.run(debug=True, port=8000)