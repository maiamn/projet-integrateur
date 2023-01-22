# Import flask and datetime module for showing date and time
from flask import Flask, jsonify, request
from flask_cors import CORS
import couchdb
import base64
import random
import logging
import traceback
import random
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
    return jsonify("BDD game OK on port 7002")

# Créer une nouvelle partie dans la bdd
@app.route("/new_game", methods=["POST"])
def new_game():
    logging.info("new_game")
    
    try :
        # Get JSON request
        req = request.get_json()
        logging.debug("message from main %s",req)

        # CouchDB
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['game']

        logging.debug("images %s",req['id_images_user']+req['id_images_default'])
        
        #choisit l'image à deviner
        #id_guess = ""

        #if req['mode']=="player" :
        id_guess = random.choice(req['id_images_user']+req['id_images_default'])
            
        logging.debug("id guess %s", id_guess)
        
        # mango = ({  'selector': {'id_user': req['user'], 'id_partie': int(req['id_partie'])},
        #             'fields': ['_id','_rev','id_images_user', 'id_images_default','id_image_to_guess']})

        # query_result = list(db.find(mango))
        
        # for row in query_result :
        #     db.delete(db.find(row['_id']))
        
        # logging.debug("query %s",query_result)
        
        mango = ({  'selector': {'id_user': req['user'], 'id_partie': int(req['id_partie'])},  'fields': ['_id']})            
        query_result = list(db.find(mango))
        if query_result:
            del db[query_result[0].id]

        doc = {
            "id_user": req['user'],
            "id_partie": int(req['id_partie']),
            #"mode": req['mode'],
            "id_images_user": req['id_images_user'],
            "id_images_default": req['id_images_default'],
            "id_image_to_guess": id_guess
        }

        db.save(doc)

        response = {
            "title": "ConfirmSrV",
            "confirm": True
        }
        
    except Exception as e:
        response = {
            "title": "AnswerSrV",
            "confirm": False,
            "error": repr(e)
        }
    finally :
        return jsonify(response)  

# Récupérer l'id de l'image à deviner
@app.route("/img_to_guess/<id_user>/<id_partie>", methods=["GET"])
def get_img_to_guess(id_user, id_partie):
    logging.info("get_img_to_guess")
    
    try :

        logging.debug("id user %s",id_user)
        logging.debug("id partie %s",id_partie)
        
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['game']

        mango = ({  'selector': {'id_user': id_user, 'id_partie': int(id_partie)},
                    'fields': ['id_image_to_guess',"id_images_default", "id_images_user"]})

        query_result = list(db.find(mango))
        
        logging.debug("query result %s",query_result)

        id_image_to_guess = query_result[0]['id_image_to_guess']
        
        logging.debug("id to guess %s",id_image_to_guess)

        if id_image_to_guess in query_result[0]['id_images_default'] : 
            id_from = "default"
        else :
            id_from="user"
            
        logging.debug("id from %s",id_from)
        
        response = {
            "title": "ConfirmSrV",
            "confirm": True,
            "id_image_to_guess": id_image_to_guess,
            "from" : id_from
        }
        
    except Exception as e:
        response = {
            "title": "AnswerSrV",
            "confirm": False,
            "error": repr(e)
        }
    finally :
        return jsonify(response)  



# Checker si l'user a deviné la bonne image
@app.route("/result/<id_user>/<id_partie>/<id_image>", methods=["POST"])
def get_result(id_user, id_partie, id_image):
    
    logging.info("get_result")
    
    try :
        
        logging.debug("id user %s",id_user)
        logging.debug("id partie %s",id_partie)
        logging.debug("id image %s",id_image)

        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['game']

        mango = ({  'selector': {'id_user': id_user, 'id_partie': int(id_partie)},
                    'fields': ['id_image_to_guess']})

        query_result = list(db.find(mango))

        id_image_to_guess = query_result[0]['id_image_to_guess']
        
        logging.debug("id to guess %s",id_image_to_guess)
        logging.debug("id guessed %s",id_image)

        response = {
            "title": "ConfirmSrV",
            "confirm": True,
            "win": id_image_to_guess == id_image
        }
        
    except Exception as e:
        response = {
            "title": "AnswerSrV",
            "confirm": False,
            "win" : False,
            "error": repr(e)
        }
    finally :
        return jsonify(response)  


# Récupérer les ids des images de la partie
@app.route("/images/<id_user>/<id_partie>", methods=["POST"])
def get_imgs(id_user, id_partie):
    logging.info("get imgs")
    
    try :
        
        logging.debug("id user %s",id_user)
        logging.debug("id partie %s",id_partie)

        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['game']

        mango = ({  'selector': {'id_user': id_user, 'id_partie': int(id_partie)},
                    'fields': ['id_images_user', 'id_images_default']})

        query_result = list(db.find(mango))
        
        logging.debug("query %s",query_result)
        
        id_images_default = []
        id_images_user = []

        for row in query_result :
            id_images_default = row['id_images_default']
            id_images_user = row['id_images_user']
        
        logging.debug("images default %s", id_images_default)
        logging.debug("images user %s", id_images_user)

        response = {
            "title": "ConfirmSrV",
            "confirm": True,
            "id_images_default": id_images_default,
            "id_images_user": id_images_user
        }
        
    except Exception as e:
        response = {
            "title": "AnswerSrV",
            "confirm": False,
            "error": repr(e)
        }
    finally :
        return jsonify(response) 

# Delete Images associated with party
@app.route("/delete/<id_user>/<id_partie>", methods=["POST"])
def delete_images(id_user,id_partie):

    logging.info("delete")

    try :
        
        logging.debug("id user %s",id_user)
        logging.debug("id partie %s",id_partie)
        
        # Get JSON request
        req = request.get_json()
        id_list_delete = req['ids']
        logging.debug("message from main %s",req)

        logging.debug("id list delete %s",id_list_delete)

        # CouchDB
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['game']
        
        mango = ({  'selector': {'id_user': id_user, 'id_partie': int(id_partie)},
                    'fields': ['_id','_rev','id_images_user', 'id_images_default','id_image_to_guess']})

        query_result = list(db.find(mango))
    
        ids_user = []
        ids_default = []


        for row in query_result: 
            print(row['_id'],row['id_images_user'],row['id_images_default'])
            
            id_doc = row['_id']
            rev_doc = row['_rev']

            #mode = row['mode']
            im = row['id_image_to_guess']

            for id in row['id_images_user'] :
                if id not in id_list_delete and id not in ids_user:
                    ids_user.append(id) 

            for id in row['id_images_default'] :
                if id not in id_list_delete and id not in ids_default:
                    ids_default.append(id)
                    
        logging.debug("id users left %s",ids_user)
        logging.debug("id default left %s",ids_default)
                
        doc = {
            "_id" : id_doc,
            "_rev" : rev_doc,
            "id_user": id_user,
            "id_partie": int(id_partie),
            #"mode": mode,
            "id_images_user": ids_user,
            "id_images_default": ids_default,
            "id_image_to_guess": im
        }
        
        db.save(doc)

        response = {
            "title": "AnswerSrV",
            "confirm": True
        }                      

    
    except Exception as e:
        logging.error(traceback.format_exc())
        response = {
            "title": "AnswerSrV",
            "confirm": False,
            "error": repr(e)
        }
        
    finally :
        return jsonify(response)

# Running app
if __name__ == '__main__':
    app.run(debug=True, port=7002)