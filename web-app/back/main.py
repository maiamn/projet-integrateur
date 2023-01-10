# Import flask and datetime module for showing date and time
from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
import couchdb
import base64
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


#Route pour vérifier que le microservice est bien lancé
@app.route('/', methods=["GET"])
def defaultRoute():
    return jsonify("Dispatcher ok on port 5000")

#Route pour toutes les requests posts
@app.route("/sent", methods=["POST"])
def test_receive():
    message = request.get_json()['message']
    print(message)
    title = message["title"]
    print(message,title)

    #on check le message qui a été envoyé
    if title=="get_labels":
        try :
            #images à modifier avec les images uploadés
            res = requests.post('http://localhost:7000/send_pic', json={ 'title' : 'get_labels', 'user' : message['user'], 'id_partie' : message['id_partie'], 'images':'C:/Users/fifid/Pictures/test'}, timeout=20).json()
            logging.debug("message from gestCNN: %s" ,res)
            question = {'title':"ConfirmSrv", 'user' : res['user'], 'id_partie' : res['id_partie'], 'confirm':True}
                
        except Exception as e :
            logging.error(traceback.format_exc())
            question = {'title':"ConfirmSrv", 'confirm':False,'error':repr(e)}
    return jsonify(question)

#Labelliser les nouvelles images entrées par le user
@app.route('/get_labels', methods=["GET"])
def get_labels():
    res = {}
    try :
        res = requests.get('http://localhost:7000/get_labels').json()
        print(res)
        logging.debug("message from gestCNN : %s" ,res)   
    except Exception as e :
        res = {'title':'AnswerSrv','confirm':False,'error':repr(e)}
        logging.error(traceback.format_exc())

    #on renvoie directement le message renvoyé par gestCNN
    return jsonify(res)



@app.route("/db", methods=["GET"])
def test_DB():
    # CouchDB
    couch = couchdb.Server("http://user:user@localhost:5984")
    db = couch['images']
    for id in db:
        print(base64.b64encode(db.get_attachment(id, list(db.get(id) ['_attachments'].keys())).read()).decode('utf-8'))
    return jsonify({"data": base64.b64encode(db.get_attachment(id, list(db.get(id) ['_attachments'].keys())).read()).decode('utf-8')})
      
@app.route("/add", methods=["POST"])
def add_images():
    infos = request.files
    print(infos)
    # CouchDB
    couch = couchdb.Server("http://user:user@localhost:5984")
    db = couch['images']

    for file in infos.keys() :
        doc = {'labels': "To add"}
        db.save(doc)
        f = infos[file].read()
        db.put_attachment(doc=doc, content=f, filename="image", content_type="image/jpg")

    return jsonify({"image": "coucou"})
    
# Running app
if __name__ == '__main__':
    app.run(debug=True, port=5000)