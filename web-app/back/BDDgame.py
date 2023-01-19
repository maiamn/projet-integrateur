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

# Créer une nouvelle partie
@app.route("/new_game", methods=["POST"])
def new_game():
    try :
        # Get JSON request
        req = request.get_json()

        # CouchDB
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['game']

        doc = {
            "id_user": req['user'],
            "id_partie": req['id_partie'],
            "mode": req['mode'],
            "id_images_user": req['id_images_user'],
            "id_images_default": req['id_images_default'],
            "id_image_to_guess": req['id_image_to_guess']
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
    try :

        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['game']

        mango = ({  'selector': {'id_user': id_user, 'id_partie': int(id_partie)},
                    'fields': ['id_image_to_guess']})

        query_result = list(db.find(mango))

        id_image_to_guess = query_result[0]['id_image_to_guess']

        response = {
            "title": "ConfirmSrV",
            "confirm": True,
            "id_image_to_guess": id_image_to_guess
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
@app.route("/result/<id_user>/<id_partie>/<id_image>", methods=["GET"])
def get_result(id_user, id_partie, id_image):
    try :

        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['game']

        mango = ({  'selector': {'id_user': id_user, 'id_partie': int(id_partie)},
                    'fields': ['id_image_to_guess']})

        query_result = list(db.find(mango))

        id_image_to_guess = query_result[0]['id_image_to_guess']

        response = {
            "title": "ConfirmSrV",
            "confirm": True,
            "win": id_image_to_guess == id_image
        }
        
    except Exception as e:
        response = {
            "title": "AnswerSrV",
            "confirm": False,
            "error": repr(e)
        }
    finally :
        return jsonify(response)  

# Récupérer les ids des images de la partie
@app.route("/images/<id_user>/<id_partie>", methods=["GET"])
def get_imgs(id_user, id_partie):
    try :

        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['game']

        mango = ({  'selector': {'id_user': id_user, 'id_partie': int(id_partie)},
                    'fields': ['id_images_user', 'id_images_default']})

        query_result = list(db.find(mango))

        id_images_default = query_result[0]['id_images_default']
        id_images_user = query_result[0]['id_images_user']

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


# Running app
if __name__ == '__main__':
    app.run(debug=True, port=7002)