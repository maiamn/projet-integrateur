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


  
@app.route('/', methods=["GET"])
def firstRoute():
    return jsonify("Dispatcher ok on port 5000")

@app.route("/sent", methods=["POST"])
def test_receive():
    infos = request.get_json()
    print(infos)
    title = infos["message"]["title"]
    print(title)

    if title=="upload":
        try :
            res = requests.post('http://localhost:7000/get_labels', json={'title':"get_labels"}, timeout=20).json()
            logging.debug("message from PI : %s" ,res)
            question = {'title':"ConfirmSrv", 'confirm':True}
                
        except Exception as e :
            
            logging.error(traceback.format_exc())
            question = {'title':"ConfirmSrv", 'confirm':False,'error':repr(e)}
    return jsonify(question)

@app.route('/return', methods=["GET"])
def returnRoute():
    try :
        res = requests.get('http://localhost:7000/answer').json()
        print(res)
        logging.debug("message from PI : %s" ,res)
            
    except Exception as e :
        
        logging.error(traceback.format_exc())
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
    app.run(debug=True, port=5000)