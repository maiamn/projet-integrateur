# Import flask and datetime module for showing date and time
from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
import couchdb
import base64
import logging
import traceback
import json
import tempfile, os
  
# Initializing flask app
app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.secret_key = "123"
cors.init_app(app)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

selectedImage = ""
images_left = 5


#Route pour vérifier que le microservice est bien lancé
@app.route('/', methods=["GET"])
def defaultRoute():
    return jsonify("Dispatcher ok on port 5000")

#Route pour toutes les requests posts
@app.route("/sent", methods=["POST"])
def test_receive():
    global selectedImage, images_left

    logging.info("Post message from react route")
    
    try : 
        content = request.form.to_dict()

        #on check le message qui a été envoyé
        if content!={} :
            #recup images
            infos = request.files
            #recup le message json
            message = json.loads(content["data"])

            logging.debug("images from interface %s",infos)
            logging.debug("message from interface %s",message)

            if message["title"]=="get_labels":
                logging.info("get_labels")

                try :
                    #Envoie les images uploadées au cnn
                    payload = { 'title' : 'get_labels', 'user' : message['user'], 'id_partie' : message['id_partie']}
                    files = []
                    k = list(infos.keys())
                    print(k)
                    for file in range(len(k)) :
                        print(infos[k[file]])
                        files.append((k[file] ,(k[file]+'.jpg', infos[k[file]].read(),'image/jpeg')))

                    #res = requests.post('http://localhost:7000/get_labels', json={ 'title' : 'get_labels', 'user' : message['user'], 'id_partie' : message['id_partie'], 'images':'C:/Users/fifid/Pictures/test'}, timeout=20).json()
                    res = requests.post('http://localhost:7000/get_labels', headers={}, data=payload, files=files, timeout=20).json()
                    logging.debug("message from gestCNN: %s" ,res)

                    
                    value = []
                    payload = {'title' : 'get_labels','hey':'he'}
                    for i in res['answer']['labels'] :
                        value.append(list(i[0].split("."))[0])
                        payload[list(i[0].split("."))[0]] = ' '.join(str(e) for e in i[1:])
                    

                    headers = {}
                    print(payload)
                    files = []
                    k = list(infos.keys())
                    l = value
                    print(k)
                    print(l)
                    for file in range(len(k)) :
                        print(l)
                        print(l[file])
                        print(infos[k[file]])
                        files.append((l[file] ,(l[file]+'.jpg', infos[k[file]].read(),'image/jpeg')))

                    

                    res_upload = requests.post('http://localhost:8000/upload', headers=headers, data=payload, files=files, timeout=20).json()
                    logging.debug("message from upload: %s" ,res_upload)
                    question = {'title':"ConfirmSrv", 'user' : res['user'], 'id_partie' : res['id_partie'], 'confirm':True}
                        
                except Exception as e :
                    logging.error(traceback.format_exc())
                    question = {'title':"ConfirmSrv", 'confirm':False,'error':repr(e)}

        else :
            message = request.get_json()['message']
            title = message["title"]
            
            logging.debug("message from interface %s",message)

            if title=="get_n_celeb_images" :
                logging.info("get_n_celeb_images")

                try :
                    #Recup les images du jeu
                    res = requests.post('http://localhost:9000/celebs', json={ "title": "get_n_celeb_images","user": 3,"id_partie": 4,"nb_images": 20}, timeout=20).json()
                    logging.debug("message from BDDdefault: %s" ,res)

                    if message['questions']==True : 
                        #Si on veut recuperer les questions aussi 
                        logging.info("images + questions")
                        # a modifier en récuperant les questions 
                        questions_ask = ["Are they a Male ?", "Do they have brown hair?", "Do they have a beard ?"]

                        question = {
                            "title": "AnswerSrV",
                            "user": res['user'],
                            "id_partie": res['id_partie'],
                            "nb_images": res['nb_images'],
                            "answer": {"images": res['answer']['images'], "questions":questions_ask},
                            "confirm": True
                        }
                    else :

                        #Si on recupère que les photos
                        logging.info("images only")

                        question = {
                            "title": "AnswerSrV",
                            "user": res['user'],
                            "id_partie": res['id_partie'],
                            "nb_images": res['nb_images'],
                            "answer": {"images": res['answer']['images']},
                            "confirm": True
                        }
                        
                except Exception as e :
                    logging.error(traceback.format_exc())
                    question = res

            elif title=="get_answer_computer" :
                logging.info("get_answer_computer")

                try : 
                    #Recup la réponse à la question du user
                    answer = True

                    question = {
                            'title' : 'AnswerSrV',
                            'user' : message['user'],
                            'id_partie' : message['id_partie'],
                            'question' : message['question'],
                            'answer' : {
                                        'answer_computer': answer
                                        },
                            'confirm' : True
                            }

                except Exception as e :
                    logging.error(traceback.format_exc())
                    question = {
                            'title' : 'AnswerSrV',
                            'user' : message['user'],
                            'id_partie' : message['id_partie'],
                            'question' : message['question'],
                            'answer' : {
                                        'answer_computer': ""
                                        },
                            "error" : repr(e),  
                            'confirm' : False
                            }

            elif title=="check_answer" :
                logging.info("check_answer")

                try : 
                    #TO DO : A retirer après avoir relié les microservices
                    selectedImage = message['final_image']

                    #TO DO : Recup answer du computer une fois qu'il a check la rep
                    answer = True

                    question = {
                            'title' : 'AnswerSrV',
                            'user' : message['user'],
                            'id_partie' : message['id_partie'],
                            'final_image' : message['final_image'],
                            'answer' : {
                                        'answer_check': answer
                                        },
                            'confirm' : True
                            }

                except Exception as e :
                    logging.error(traceback.format_exc())
                    question = {
                            'title' : 'AnswerSrV',
                            'user' : message['user'],
                            'id_partie' : message['id_partie'],
                            'final_image' : message['final_image'],
                            'answer' : {
                                        'answer_check': ""
                                        },
                            "error" : repr(e),  
                            'confirm' : False
                            }

            # elif title=="add_image_to_guess" :
            #     selectedImage = ""
            #     print(message['image_to_guess'])
            #     selectedImage = message['image_to_guess']
            #     question = {
            #         'title' : 'ConfirmSrV',
            #         'user' : message['user'],
            #         'id_partie' : message['id_partie'],
            #         'image_to_guess' : message['image_to_guess'],
            #         'confirm' : True,
            #     }

            elif title=="get_question_to_ask" :
                logging.info("get_question_to_ask")

                try : 
                    #TO DO : recup la question du computer et enlever le images_left et les 2 messages différents qui vont être renvoyés par le micro service
                    question_to_ask = "Are they a Male ?"
                    
                    logging.debug("images left %s",images_left)

                    if images_left==2 :
                        logging.debug("end of the game")
                        question = {

                            'title' : 'AnswerSrV',
                            'user' : message['user'],
                            'id_partie' : message['id_partie'],
                            'answer' : {
                                        'image': selectedImage, #TO DO: Mettre la vraie image devinée par computer
                                        'images_left' : images_left-1

                                    },
                            'confirm' : True
                        }
                        images_left=5
                    else : 
                        logging.debug("Still asking")

                        images_left-=1
                        question = {
                            'title' : 'AnswerSrV',
                            'user' : message['user'],
                            'id_partie' : message['id_partie'],
                            'answer' : {
                                        'question_to_ask': question_to_ask,
                                        'images_left' : images_left

                                    },
                            'confirm' : True
                        }
                except Exception as e :
                    logging.error(traceback.format_exc())
                    question = {
                            'title' : 'AnswerSrV',
                            'user' : message['user'],
                            'id_partie' : message['id_partie'],
                            'answer' : {},
                            "error" : repr(e),  
                            'confirm' : False
                            }


            elif title=="get_answer_user":
                logging.info("get_answer_user")

                try : 
                    #TO DO : Process la réponse du user

                    question = {
                        
                        'title' : 'ConfirmSrV',
                        'user' : message['user'],
                        'id_partie' : message['id_partie'],
                        'answer_user': message['answer_user'],
                        'confirm' : True
                    }
                except Exception as e :
                    logging.error(traceback.format_exc())
                    question = {
                            'title' : 'ConfirmSrV',
                            'user' : message['user'],
                            'id_partie' : message['id_partie'],
                            'answer_user': message['answer_user'],
                            "error" : repr(e),  
                            'confirm' : False
                            }

    except Exception as e :
        logging.error(traceback.format_exc())
        question = {
                'title' : 'ConfirmSrV',
                "error" : repr(e),  
                'confirm' : False
                }

        
    return jsonify(question)

#Labelliser les nouvelles images entrées par le user
@app.route('/get_labels', methods=["GET"])
def get_labels():
    logging.info("get_labels route")

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
    logging.info("CouchDB route")


    try : 
        couch = couchdb.Server("http://user:user@localhost:5984")
        db = couch['images']
        for id in db:
            logging.debug(base64.b64encode(db.get_attachment(id, list(db.get(id) ['_attachments'].keys())).read()).decode('utf-8'))
        
        rep = {"data": base64.b64encode(db.get_attachment(id, list(db.get(id) ['_attachments'].keys())).read()).decode('utf-8')}

    except Exception as e :
        logging.error(traceback.format_exc())
        rep = {
                'title' : 'ConfirmSrV',
                "error" : repr(e),  
                'confirm' : False
                }

    return jsonify(rep)
      
# @app.route("/add", methods=["POST"])
# def add_images():
#     infos = request.files
#     print(infos)
#     # CouchDB
#     couch = couchdb.Server("http://user:user@localhost:5984")
#     db = couch['images']

#     for file in infos.keys() :
#         doc = {'labels': "To add"}
#         db.save(doc)
#         f = infos[file].read()
#         db.put_attachment(doc=doc, content=f, filename="image", content_type="image/jpg")

#     return jsonify({"image": "coucou"})
    
# Running app
if __name__ == '__main__':
    app.run(debug=True, port=5000)