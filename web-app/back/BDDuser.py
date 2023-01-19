# Import flask and datetime module for showing date and time
from flask import Flask, jsonify, request
from flask_cors import CORS
import couchdb
import base64
import random
import io
import json
  
# Initializing flask app
app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.secret_key = "123"
cors.init_app(app)


# Get images uploadees
@app.route("/img/<id>", methods=["GET"])
def get_images(id):
    
    # CouchDB
    couch = couchdb.Server("http://user:user@localhost:5984")
    db = couch['user']

    db.get_attachment(id, list(db.get(id) ['_attachments'].keys())).read()

    return send_file(
        io.BytesIO(image),
        mimetype='image/jpeg',
        download_name=id)


# Upload Images
## TO DO !
@app.route("/upload", methods=["POST"])
def upload_images():
    try :
        print(request.headers.items)
        #print('data',json.loads(request.data))
        print('data',request.data)
        #print('json',request.json)
        infos = request.files
        content = request.form
        labels = {}
        print("infos",infos)

        print("content",content)
        print("labels",labels)
        # CouchDB
        couch = couchdb.Server("http://user:user@localhost:5984")
        print("b")
        db = couch['user']
        print("a")
        print("keys",content.keys())
        #print("file content",content['file'])

        # for k in content.keys(): 
        #     if k in infps:
        #         lab = content[k]
    
        # print("lab",lab)

        for file in infos.keys():
            print(content[file])
            lab = list(content[file].split(" "))
            lab = [int(e) for e in lab]
            print(lab)
            doc = {'labels': lab}
            db.save(doc)
            print(file)
            print(infos[file])
            f = infos[file].read()
            db.put_attachment(doc=doc, content=f, filename="image", content_type="image/jpg")


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


# Delete Images associated with a party
@app.route("/delete", methods=["DELETE"])
def delete_images():
    try :
        # Get JSON request
        req = request.get_json()

        # CouchDB
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['user']

        id_images = [
            "test"
        ]

        for id in id_images:
            # Mango query
            mango = ({  'selector': {'_id': id},
                        'fields': ['_id']})
            query_result = list(db.find(mango))
            del db[query_result[0].id]

        response = {
            "title": "AnswerSrV",
            "user": req['user'],
            "id_partie": req['id_partie'],
            "confirm": True
        }                      

    
    except Exception as e:
        print(e)
        response = {
            "title": "AnswerSrV",
            "user": req['user'],
            "id_partie": req['id_partie'],
            "confirm": False,
            "error": repr(e)
        }
        
    finally :
        return jsonify(response)

# Running app
if __name__ == '__main__':
    app.run(debug=True, port=8000)