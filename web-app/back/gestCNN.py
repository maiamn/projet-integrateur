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

  
# Initializing flask app
app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.secret_key = "123"
cors.init_app(app)

sess = {}

@app.route("/", methods=["GET"])
def get_labels():
    return jsonify("gestCNN OK on port 7000")

@app.route("/get_labels", methods=["POST"])
def get_label():
    global sess
    print("get labels")
    infos = request.get_json()
    print(infos)
    session['message']=infos
    sess['message']=infos
    print("sess_send", sess)
    print(session.get('message'))
    return jsonify(infos)

@app.route("/answer", methods=["GET"])
def answer():
    global sess
    print('answer')
    answer = {"msg":"session is empty"}
    print("sess_answer", sess)
    print(session.get('message'))
    if "message" in sess :
        answer = {"msg":"session is here"}
        message = sess['message']
        print(message)
        if message["title"]=="get_labels" :
            try :
                print(" in try")
                df = get_labels_images()
                labels_list = df.values.tolist()
                print('labels_list',labels_list)
                answer = {'title':'AnswerSrv','answer':{'labels':labels_list}, 'confirm':True}
            except Exception as e :
                logging.error("pb recup images %s",e.__cause__)
                logging.error(traceback.format_exc())
                answer = {'title':'AnswerSrv','answer':{'labels':None}, 'confirm':False,'error':repr(e)}
        print("message :", message)
        #answer["message"] = message
    return jsonify(answer)
      
def get_labels_images() :
    #au lieu d'utiliser le path des images on fait appel au microservice pour récupérer le dossier des images 
    #path à adapter en fonction de l'emplacement
    df = predicted('C:/Users/fifid/Documents/saved_model_50000/cp.h5','C:/Users/fifid/Pictures/test')
    
    return df

# Running app
if __name__ == '__main__':
    app.run(debug=True, port=7000)