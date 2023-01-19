# Import flask and datetime module for showing date and time
from flask import Flask, jsonify, request, session
from flask_cors import CORS
import base64
import traceback
import logging
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
from Notebook.images_to_labels import predicted
import pandas as pd

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)
  
# Initializing flask app
app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.secret_key = "123"
cors.init_app(app)

sess = {}

#Route pour vérifier que le microservice est bien lancé
@app.route("/", methods=["GET"])
def defaultRoute():
    return jsonify("gestCNN OK on port 7000")

# @app.route("/send_pic", methods=["POST"])
# def send_pic():
#     global sess

#     message = request.get_json()
#     #On enregistre le message pour pouvoir le récupérer dans get_labels
#     sess['message']=message
#     print("sess_send", sess)

#     return jsonify(message)

@app.route("/get_labels", methods=["POST"])
def get_labels():
    global sess

    infos = request.files
    message = request.form

    print("infos",infos)

    print("message",message)

    answer = {"message":"session is empty"}

    print("sess_answer", sess)

    #message = request.get_json()
    #On enregistre le message pour pouvoir le récupérer dans get_labels
    sess['message']=message


    if "message" in sess :

        message = sess['message']
        print(message)

        if message["title"]=="get_labels" :
            try :
                images = 'C:/Users/fifid/Pictures/test'
                df = get_labels_images(images)
                labels_list = df.values.tolist()

                answer = {'title':'AnswerSrv','user':message['user'],'id_partie':message['id_partie'],'answer':{'labels':labels_list}, 'confirm':True}

            except Exception as e :
                logging.error("pb recup images %s",e.__cause__)
                logging.error(traceback.format_exc())
                answer = {'title':'AnswerSrv','user':message['user'],'id_partie':message['id_partie'],'answer':{'labels':None}, 'confirm':False,'error':repr(e)}

    return jsonify(answer)
      
def get_labels_images(images) :
    #au lieu d'utiliser le path des images on fait appel au microservice pour récupérer le dossier des images 
    #path à adapter en fonction de l'emplacement
    print(images)
    df = predicted('C:/Users/fifid/Documents/saved_model_50000/cp.h5',images)
    return df

# Running app
if __name__ == '__main__':
    app.run(debug=True, port=7000)