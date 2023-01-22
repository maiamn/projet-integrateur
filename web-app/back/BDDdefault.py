# Import flask and datetime module for showing date and time
from flask import Flask, jsonify, request
from flask_cors import CORS
import couchdb
import base64
import random
import logging
import traceback
import logging
  
# Initializing flask app
app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.secret_key = "123"
cors.init_app(app)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

questions={
    'Male':"Are they a Male?",
    'Young':"Are they young?",
    'Eyeglasses':"Do they wear eyeglasses?",
    'Wearing_Necktie':"Do they wear a tie?",
    'Wearing_Necklace':"Do they wear a necklace?",
    'Wearing_Earrings':"Do they wear earrings?",
    'Wearing_Hat':"Do they wear a hat?",
    'Big_Lips':"Do they have big lips?",
    'Big_Nose':"Do they have a big nose?",
    'Bags_Under_Eyes':"Do they have bags under their eyes?",
    'Bushy_Eyebrows':"Do they have bushy eyebrows?",
    'Wearing_Lipstick':"Do they wear lipstick?",
    'Heavy_Makeup':"Do they wear heavy makeup?",
    'Smiling':"Are they smiling?",
    'Mouth_Slightly_Open':"Do they have their mouth slightly open?",
    'Receding_Hairline':"Do they have a receding hairline?",
    'Bald':"Are they bald?",
    'Blond_Hair':"Do they have blond hair?",
    'Brown_Hair':"Do they have brown hair?",
    'Black_Hair':"Do they have black hair?",
    'Gray_Hair':"Do they have gray hair?",
    'Bangs':"Do they have bangs?",
    'Wavy_Hair':"Do they have wavy hair?",
    'Straight_Hair':"Do they have straight hair?",
    'No_Beard':"Are they beardless?",
    '5_o_Clock_Shadow':"Do they have a 5 o’clock shadow?",
    'Goatee':"Do they have a goatee?",
    'Mustache':"Do they have a mustache?",
    'Sideburns':"Do they have sideburns?",
    'Pale_Skin':"Do they have pale skin?",
    'Rosy_Cheeks':"Do they have rosy cheeks?",
    'Pointy_Nose':"Do they have a pointy nose?",
    'Chubby':"Are they chubby?",
    'High_Cheekbones':"Do they have high cheekbones?",
    'Oval_Face':"Do they have an oval face?"    
}


#Route pour vérifier que le microservice est bien lancé
@app.route("/", methods=["GET"])
def defaultRoute():
    return jsonify("BDD default OK on port 9000")

# Get n images de celebrites
@app.route("/celebs", methods=["POST"])
def get_images():

    logging.info("Get n images de celebrites")

    try :
        
        # Get JSON request
        req = request.get_json()
        logging.debug("message from main %s", req)
        
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

        images = []
        for id in id_images:
            logging.debug('id %s',id)
            images.append(base64.b64encode(db.get_attachment(id, list(db.get(id) ['_attachments'].keys())).read()).decode('utf-8'))

        response = {
            "title": "AnswerSrV",
            "user": req['user'],
            "id_partie": req['id_partie'],
            "nb_images": nb_images,
            "answer": {"images": images,"ids":id_images},
            "confirm": True
        }
        
    except Exception as e:
        logging.error(traceback.format_exc())
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
    
#Pour recuperer une image en fonction de son id
@app.route("/celeb_by_id", methods=["POST"])
def get_image_by_id():

    logging.info("Get image de celebrite by id")

    try :
        
        # Get JSON request
        req = request.get_json()
        logging.debug(" message from main %s",req)
        
        id_image = req['id']

        # CouchDB
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['images']
         

        
        logging.debug("id %s",id_image)
        image = base64.b64encode(db.get_attachment(id_image, list(db.get(id_image) ['_attachments'].keys())).read()).decode('utf-8')

        logging.debug("image %s",image)
        
        response = {
            "title": "AnswerSrV",
            "user": req['user'],
            "id_partie": req['id_partie'],
            "answer": {"image": image,"id":id_image},
            "confirm": True
        }
        
    except Exception as e:
        logging.error(traceback.format_exc())
        response = {
            "title": "AnswerSrV",
            "user": req['user'],
            "id_partie": req['id_partie'],
            "answer": {"image": "", 'id':""},
            "confirm": False,
            "error": repr(e)
        }
    finally :
        return jsonify(response)

#Pour recuperer des images en fonction de leurs ids
@app.route("/celebs_by_id", methods=["POST"])
def get_images_by_id():

    logging.info("Get images de celebrites by id")

    try :
        
        # Get JSON request
        req = request.get_json()
        logging.debug(" message from main %s",req)
        
        id_images = req['id_images_default']

        # CouchDB
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['images']
         

        images = []
        for id in id_images:
            logging.debug("id %s",id)
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
            "answer": {"images": [], 'ids':[]},
            "confirm": False,
            "error": repr(e)
        }
    finally :
        return jsonify(response)


#recup les labels d'une image en fonction de son id
@app.route("/labels_by_id", methods=["POST"])
def get_labels_by_id():

    logging.info("Get labels by id")

    try :
        
        # Get JSON request
        req = request.get_json()
        logging.debug("messafge from main %s",req)
        
        id_image = req['id_image_default']

        # CouchDB
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['images']

        labels_dic = {}

        query_result = db.get(id_image)

        logging.debug("query %s",query_result)
    
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
            "answer": {"labels": [], "id":""},
            "confirm": False,
            "error": repr(e)
        }
    finally :
        return jsonify(response)
      
# # Get labels de celebrites
# @app.route("/all_labels", methods=["GET"])
# def get_all_labels():
#     logging.info('get all labels')

#     try :
#         # CouchDB
#         couch = couchdb.Server("http://user:user@localhost:5984")
#         db = couch['images']
        
#         labels_dic = {}

#         # Mango query
#         mango = ({  'selector': {},
#                     'fields': ['labels','_id']})

#         query_result = list(db.find(mango)) 

#         logging.debug("query %s",query_result)
    
#         for row in query_result: 
#             labels_dic[row['_id']] = row['labels']

#         logging.debug("nb images %s",len(labels_dic))
#         logging.debug("labels images %s",labels_dic)
        
#         response = {
#             "labels" : labels_dic,
#             "nb_images" : len(labels_dic)
#         }

#     except Exception as e:
#         logging.error(traceback.format_exc())
#         response = {
#             "labels" : {},
#             "confirm": False,
#             "error": repr(e)
#         }
#     finally :
#         return jsonify(response)


# Get labels de celebrites par id
@app.route("/labels", methods=["POST"])
def get_labels():
    logging.info('get labels by id')

    try :
        req = request.get_json()
        logging.debug(" message from main %s",req)
        
        id_images = req['images']

        # CouchDB
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['images']
        
        labels_dic = {}
    
        for id in id_images: 
            lab = db.get(id) ['labels']
            print(lab)
            labels_dic[id] = {e:lab[e] for e in list(lab.keys())}

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



# Running app
if __name__ == '__main__':
    app.run(debug=True, port=9000)