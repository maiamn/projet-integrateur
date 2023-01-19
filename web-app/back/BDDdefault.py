# Import flask and datetime module for showing date and time
from flask import Flask, jsonify, request
from flask_cors import CORS
import couchdb
import base64
import random
import logging
import traceback
  
# Initializing flask app
app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.secret_key = "123"
cors.init_app(app)

questions={
    'Male':"Is it a boy?",
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
    'Smiling':"Do they smile?",
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
    'No_Beard':"Do they have no beard?",
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

# Get n images de celebrites
@app.route("/celebs", methods=["POST"])
def get_images():

    logging.info("Get n images de celebrites")

    try :
        
        # Get JSON request
        req = request.get_json()
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
            images.append(base64.b64encode(db.get_attachment(id, list(db.get(id) ['_attachments'].keys())).read()).decode('utf-8'))

        response = {
            "title": "AnswerSrV",
            "user": req['user'],
            "id_partie": req['id_partie'],
            "nb_images": nb_images,
            "answer": {"images": images},
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
      
# Get labels de celebrites
@app.route("/labels", methods=["GET"])
def get_labels():
    logging.info('get labels')

    try :

        ## TO DO : for now we don't get the labels associated to the images of a "partie" but the labels associated to the following images 
        images = [
                "000003.jpg",
                "000004.jpg",
                "000002.jpg"
        ]

        # CouchDB
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['images']
        
        labels_dic = {}

        # Mango query
        mango = ({  'selector': {},
                    'fields': ['labels','_id']})

        query_result = list(db.find(mango)) 

        print(query_result)
    
        for row in query_result: 
            labels_dic[row['_id']] = row['labels']

        print("nb images",len(labels_dic))
        response = {
            "labels" : labels_dic,
            "nb_images" : len(labels_dic)
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

# Delete Images associated with a party
@app.route("/delete", methods=["POST"])
def delete_images():

    logging.info("delete")

    try :
        # Get JSON request
        req = request.get_json()

        logging.debug("req %s",req)

        answer_user = 1 if req['answer_user'] else -1

        for i in questions.keys() :
            if questions[i]==req['question'] :
                question = i

        print(answer_user,question)

        # CouchDB
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['images']


        
        mango = ({ 'selector': {}, 'fields': ['labels','_id']})
        query_result = list(db.find(mango))

        print(query_result)

        id_list_delete = []      
        for row in query_result: 
            print(row['_id'],row['labels'][question])
            if row['labels'][question]!=answer_user :
                id_list_delete.append(row['_id']) 
                db.delete(db.get(row['_id'])) 

        print("id_to_delete",id_list_delete)

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
    app.run(debug=True, port=9000)