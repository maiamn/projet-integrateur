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

#Route pour vérifier que le microservice est bien lancé
@app.route("/", methods=["GET"])
def defaultRoute():
    return jsonify("BDD user OK on port 8000")

# # Get images uploadees
# @app.route("/img/<id>", methods=["GET"])
# def get_images(id):

#     # CouchDB
#     couch = couchdb.Server("http://user:user@localhost:5984")
#     db = couch['user']

#     db.get_attachment(id, list(db.get(id) ['_attachments'].keys())).read()

#     return send_file(
#         io.BytesIO(image),
#         mimetype='image/jpeg',
#         download_name=id)


# Upload Images
@app.route("/upload", methods=["POST"])
def upload_images():
    #on upload les images et leurs labels à la bdd user
    logging.info('upload route')

    try :
        infos = request.files
        content = request.form

        logging.debug("infos %s",infos)
        logging.debug("content %s",content)

        # CouchDB
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['user']

        #Recup les images et les labels pour chacunes des images
        for file in infos.keys():
            labels = [int(e) for e in list(content[file].split(" "))]
            labels_dic = {labels_name[i]:labels[i] for i in range(len(labels))}
            logging.debug('labels %s',labels_dic)

            doc = {'_id':file,'labels': labels_dic}
            db.save(doc)

            logging.debug('debugs %s : %s',file,infos[file])
            f = infos[file].read()

            db.put_attachment(doc=doc, content=f, filename="image", content_type="image/jpg")
            
        logging.debug("id_images %s",infos.keys())

        response = {
            "title": "ConfirmSrV",
            "id_images" : list(infos.keys()),
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


# # Delete Images associated with a party
# @app.route("/delete", methods=["DELETE"])
# def delete_images():

#     logging.info("delete")

#     try :
#         # Get JSON request
#         req = request.get_json()

#         logging.debug("req %s",req)

#         # CouchDB
#         couch = couchdb.Server("http://user:user@localhost:5984")
#         db = couch['user']

#         #TO DO : mettre les ids des images
#         id_images = [
#             "test"
#         ]

#         for id in id_images:
#             # Mango query
#             mango = ({  'selector': {'_id': id},
#                         'fields': ['_id']})
#             query_result = list(db.find(mango))
#             del db[query_result[0].id]

#         response = {
#             "title": "AnswerSrV",
#             "user": req['user'],
#             "id_partie": req['id_partie'],
#             "confirm": True
#         }                      

    
#     except Exception as e:
#         logging.error(traceback.format_exc())
#         response = {
#             "title": "AnswerSrV",
#             "user": req['user'],
#             "id_partie": req['id_partie'],
#             "confirm": False,
#             "error": repr(e)
#         }
        
#     finally :
#         return jsonify(response)

# Get labels par id 
@app.route("/labels", methods=["POST"])
def get_labels():
    
    #on recupère les labels de certaines images avec leur ids
    logging.info('get labels')

    try :
        req = request.get_json()
        logging.debug(" message from main %s",req)
        
        id_images = req['images']

        # CouchDB
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['user']
        
        labels_dic = {}
    
        for id in id_images: 
            labels_dic[id] = list(db.get(id) ['labels'].keys())

        logging.debug("nb images %s",len(labels_dic))
        logging.debug("labels images %s",labels_dic)
        
        response = {
            "labels" : labels_dic
        }

    except Exception as e:
        logging.error(traceback.format_exc())
        response = {
            "labels" : {},
            "confirm": False,
            "error": repr(e)
        }
    finally :
        return jsonify(response)

# # Get labels de toutes les images de la bdd
# @app.route("/all_labels", methods=["GET"])
# def get_all_labels():
#     try :
#         # Get JSON request
#         req = request.get_json()

#         images = req['images']

#         # CouchDB
#         couch = couchdb.Server("http://user:user@localhost:5984")
#         db = couch['user']
        
#         labels_dic = {}

#         for image in images:
#             # Mango query
#             mango = ({  'selector': {'_id': image},
#                         'fields': ['labels']})
#             query_result = list(db.find(mango)) 
#             labels_image = query_result[0]['labels'] 
#             labels_dic[image] = labels_image

#         response = {
#             "title": "AnswerSrV",
#             "user": req['user'],
#             "id_partie": req['id_partie'],
#             "answer": {"labels" : labels_dic},
#             "confirm": True
#         }

#     except Exception as e:
#         response = {
#             "title": "AnswerSrV",
#             "user": req['user'],
#             "id_partie": req['id_partie'],
#             "answer": {"labels" : {}},
#             "confirm": False,
#             "error": repr(e)
#         }
#     finally :
#         return jsonify(response)

#on recupère le images de la bdd user en fonction des ids
@app.route("/images_by_id", methods=["POST"])
def get_images_by_id():

    logging.info("Get images de user by id")

    try :
        
        # Get JSON request
        req = request.get_json()
        logging.debug("messafge from main %s",req)
        
        id_images = req['id_images_user']

        # CouchDB
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['user']
         

        images = []
        for id in id_images:
            logging.debug('id %s',id)
            images.append(base64.b64encode(db.get_attachment(id, list(db.get(id) ['_attachments'].keys())).read()).decode('utf-8'))
            
        logging.debug("images %s",images)

        response = {
            "title": "AnswerSrV",
            "user": req['user'],
            "id_partie": req['id_partie'],
            "answer": {"images": images,"ids":id_images},
            "confirm": True
        }
        
    except Exception as e:
        logging.error(traceback.format_exc())
        response = {
            "title": "AnswerSrV",
            "user": req['user'],
            "id_partie": req['id_partie'],
            "answer": {"images": [], "ids":[]},
            "confirm": False,
            "error": repr(e)
        }
    finally :
        return jsonify(response)

@app.route("/labels_by_id", methods=["POST"])
def get_labels_by_id():

    logging.info("Get labels  d'une image by id")

    try :
        
        # Get JSON request
        req = request.get_json()
        logging.debug("message from main %s",req)
        
        id_image = req['id_image_user']

        # CouchDB
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['user']

        labels_dic = {}

        query_result = db.get(id_image)

        logging.debug("result query %s",query_result)
    
        labels_dic = query_result['labels']
         
        logging.debug("labels dic %s",labels_dic)

        response = {
            "title": "AnswerSrV",
            "user": req['user'],
            "id_partie": req['id_partie'],
            "answer": {"labels": labels_dic,"id":id_image},
            "confirm": True
        }
        
    except Exception as e:
        logging.error(traceback.format_exc())
        response = {
            "title": "AnswerSrV",
            "user": req['user'],
            "id_partie": req['id_partie'],
            "answer": {"labels": [], 'id':""},
            "confirm": False,
            "error": repr(e)
        }
    finally :
        return jsonify(response)

# Running app
if __name__ == '__main__':
    app.run(debug=True, port=8000)