# Import flask and datetime module for showing date and time
from flask import Flask, jsonify, request
from flask_cors import CORS
import couchdb
import base64
import logging
import traceback
import requests
  
# Initializing flask app
app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.secret_key = "123"
cors.init_app(app)


  
@app.route('/', methods=["GET"])
def firstRoute():
    return jsonify({"message" : "Hello world"})

@app.route("/sent", methods=["POST"])
def test_receive():
    message = request.get_json()['message']
    print(message)
    title = message["title"]
    print(message, title)
    
    if title=="get_question_to_ask":
        try :
            #images à modifier avec les images uploadés
            res = requests.post('http://localhost:7000/send_pic', json={ 'title' : 'get_question_to_ask', 'user' : message['user'], 'id_partie' : message['id_partie'], 'images':'C:/Users/fifid/Pictures/test'}, timeout=20).json()
            question = {'title':"ConfirmSrv", 'user' : res['user'], 'id_partie' : res['id_partie'], 'confirm':True}

        except Exception as e :
            logging.error(traceback.format_exc())
            question = {'title':"ConfirmSrv", 'confirm':False,'error':repr(e)}
    
    return jsonify(question)


@app.route('/get_question_to_ask', methods=["GET"])
def get_question_to_ask():
    res = {}
    try :
        res = requests.get('http://localhost:7001/get_question_to_ask').json()
        print(res) 
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
      
# Running app
if __name__ == '__main__':
    app.run(debug=True)