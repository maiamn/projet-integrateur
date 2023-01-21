# Import flask and datetime module for showing date and time
from flask import Flask, jsonify, request
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

model = '../../Notebook/saved_model/cp.h5'

#Route pour vérifier que le microservice est bien lancé
@app.route("/", methods=["GET"])
def defaultRoute():
    return jsonify("gestCNN OK on port 7000")

@app.route("/get_labels", methods=["POST"])
def get_labels():
    #labellise les images uploadées
    logging.info("get labels")

    infos = request.files
    message = request.form

    logging.debug("files %s",infos)
    logging.debug("message %s",message)

    answer = {}

    if message["title"]=="get_labels" :
        try :
            df = predicted(model,infos)
            labels_list = df.values.tolist()
            
            answer = {'title':'AnswerSrv','user':message['user'],'id_partie':message['id_partie'],'answer':{'labels':labels_list}, 'confirm':True}

        except Exception as e :
            logging.error("pb recup images %s",e.__cause__)
            logging.error(traceback.format_exc())
            answer = {'title':'AnswerSrv','user':message['user'],'id_partie':message['id_partie'],'answer':{'labels':None}, 'confirm':False,'error':repr(e)}

    return jsonify(answer)

# Running app
if __name__ == '__main__':
    app.run(debug=True, port=7000)