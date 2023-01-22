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

#config
ad_bdd_default = 'http://localhost:9000/'
ad_bdd_game = 'http://localhost:7002/'
ad_bdd_user = 'http://localhost:8000/'
ad_gest_cnn = 'http://localhost:7000/'
ad_ms = 'http://localhost:7001/'
nb_images_jeu = 20


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
                    files_cnn = []
                    k_cnn = list(infos.keys())

                    #recup les fichiers uploadés par user
                    for file in range(len(k_cnn)) :
                        logging.debug("file_cnn %s",infos[k_cnn[file]])
                        files_cnn.append((k_cnn[file] ,(k_cnn[file]+'.jpg', infos[k_cnn[file]].read(),'image/jpeg')))

                    #labellise les fichiers avec gest cnn
                    res = requests.post(ad_gest_cnn+'get_labels', data=payload, files=files_cnn, timeout=20).json()
                    logging.debug("message from gestCNN: %s" ,res)

                    
                    #Mise en forme des labels des images récupérées du CNN
                    name_images = []

                    logging.debug('labels %s', res['answer']['labels'])

                    #mise en forme des labels
                    for i in res['answer']['labels'] :
                        name_images.append(i[0])
                        logging.debug(name_images)
                        payload[i[0]] = ' '.join(str(e) for e in i[1:])
                    
                    logging.debug("payload %s",payload)

                    #on upload et on récupère les ids des images uploadées par le user
                    res_upload = requests.post(ad_bdd_user +'upload', data=payload, files=files_cnn, timeout=20).json()
                    id_images_user = res_upload['id_images']
                    logging.debug("message from bdd user: %s" ,res_upload)

                    res_celeb = []
                    if len(res_upload['id_images'])<nb_images_jeu : 
                        #on recupère des images de la bdd default pour compléter
                        res_celeb = requests.post(ad_bdd_default + 'celebs', json={ "title": "get_n_celeb_images","user": message['user'],"id_partie": message['id_partie'],"nb_images": nb_images_jeu-len(res_upload['id_images'])}, timeout=20).json()['answer']['ids']
                        logging.debug("message from BDD default: %s" ,res)
                    elif len(res_upload['id_images'])>nb_images_jeu :
                        id_images_user = res_upload['id_images'][:nb_images_jeu]

                    #on crée la bdd associée à la partie
                    res_game = requests.post(ad_bdd_game+'new_game', json={ "user": message['user'],"id_partie": message['id_partie'],'id_images_user':id_images_user,'id_images_default':res_celeb}, timeout=20).json()
                    logging.debug("message from BDD game: %s" ,res_game)
                    
                    question = {'title':"ConfirmSrv", 'user' : res['user'], 'id_partie' : res['id_partie'], 'confirm':True}
                        
                except Exception as e :
                    logging.error(traceback.format_exc())
                    question = {'title':"ConfirmSrv", 'user' : message['user'], 'id_partie' : message['id_partie'], 'confirm':False,'error':repr(e)}

        else :
            
            message = request.get_json()['message']
            title = message["title"]
            
            logging.debug("message from interface %s",message)

            if title=="get_images" :
                #recupère les images de la partie pour les afficher
                
                logging.info("get_images")

                try :
                    if message['mode_image']=="random" :
                        #on joue avec des images random
                        
                        #on recup 20 images random
                        res = requests.post(ad_bdd_default + 'celebs', json={ "title": "get_n_celeb_images","user": message['user'],"id_partie": message['id_partie'],"nb_images": message['nb_images']}, timeout=20).json()
                        logging.debug("message from BDD default: %s" ,res)

                        #on ajoute les ids des images dans la bdd de la partie
                        res_game = requests.post(ad_bdd_game+'/new_game', json={ "user": message['user'],"id_partie": message['id_partie'],'id_images_user':[],'id_images_default':res['answer']['ids']}, timeout=20).json()
                        logging.debug("message from BDD game: %s" ,res_game)
                        
                        if message['questions'] : 
                            #on veut recuperer les questions possibles
                            questions_ask = requests.get(ad_ms+'get_possible_question', timeout=20).json()
                            logging.debug(" possible question to ask %s", question_to_ask)
                            
                            question = {
                                "title": "AnswerSrV",
                                "user": res['user'],
                                "id_partie": res['id_partie'],
                                "nb_images": res['nb_images'],
                                "answer": {"images": res['answer']['images'], "questions":questions_ask['questions'],'ids':res['answer']['ids']},
                                "confirm": True
                            }
                        else :
                            question = {
                                "title": "AnswerSrV",
                                "user": res['user'],
                                "id_partie": res['id_partie'],
                                "nb_images": res['nb_images'],
                                "answer": {"images": res['answer']['images'],'ids':res['answer']['ids']},
                                "confirm": True
                            }
                    else :
                        
                        #on joue avec des images uploadées 
                        logging.info('joue avec uopload')
                        #on récupère les ids des images de la partie
                        res_game = requests.post(ad_bdd_game+'images/'+message['user']+'/'+ message['id_partie'], timeout=20).json()
                        logging.debug("message bdd game %s",res_game)
                        
                        #on recupère les images associées à ces ids dans default
                        res = requests.post(ad_bdd_default+'celebs_by_id', json={ "user": message['user'],"id_partie": message['id_partie'],"id_images_default": res_game['id_images_default']}, timeout=20).json()
                        logging.debug("message bdd default %s",res)
                        
                        #on recupère les images associées à ces ids dans user
                        res_user = requests.post(ad_bdd_user+'images_by_id', json={ "user": message['user'],"id_partie": message['id_partie'],"id_images_user": res_game['id_images_user']}, timeout=20).json()
                        logging.debug("message bdd user %s",res_user)
                        
                        if message['questions'] :
                            #si on veut recup les questions possibles 
                            questions_ask = requests.get(ad_ms+'get_possible_question', timeout=20).json()
                            
                            logging.debug("possible questions to ask %s",questions_ask)
                            
                            logging.debug(res['answer']['images']+res_user['answer']['images'])
                            logging.debug(res['answer']['ids']+res_user['answer']['ids'])

                            question = {
                                "title": "AnswerSrV",
                                "user": message['user'],
                                "id_partie": message['id_partie'],
                                "nb_images": message['nb_images'],
                                "answer": {"images": res['answer']['images']+res_user['answer']['images'], "questions":questions_ask['questions'], 'ids':res['answer']['ids']+res_user['answer']['ids']},
                                "confirm": True
                            }
                        else :
                            question = {
                                "title": "AnswerSrV",
                                "user": message['user'],
                                "id_partie": message['id_partie'],
                                "nb_images": message['nb_images'],
                                "answer": {"images": res['answer']['images']+res_user['answer']['images']},
                                "confirm": True
                            }

                        
                except Exception as e :
                    logging.error(traceback.format_exc())
                    question = res

            elif title=="get_questions" :
                #on récupère juste les questions possibles que le player peut poser
                
                logging.info("get_questions")

                questions_ask = requests.get(ad_ms+'get_possible_question', timeout=20).json()
                logging.debug("questions ask %s",questions_ask)
                
                question = {
                    "title": "AnswerSrV",
                    "user": message['user'],
                    "id_partie": message['id_partie'],
                    "answer": {"questions":questions_ask['questions']},
                    "confirm": True
                }

            elif title=="get_answer_computer" :
                #on recupère la reponse de l'ordi à une question du user
                
                logging.info("get_answer_computer")

                try : 
                    logging.debug("asked question on %s",message['question'])

                    #on recupère l'image que l'ordi e choisie
                    image_to_guess = requests.get(ad_bdd_game+'img_to_guess/'+message['user']+'/'+ message['id_partie'], timeout=20).json()
                    logging.debug('image to guess %s',image_to_guess)
                    
                    answer = ''
                    
                    #recup les labels de l'image to guess en fonction de la bdd d'ou elle vient
                    if image_to_guess['from']=='user':
                        res = requests.post(ad_bdd_user+'labels_by_id', json={ "user": message['user'],"id_partie": message['id_partie'],"id_image_user": image_to_guess['id_image_to_guess']}, timeout=20).json()
                        logging.debug(" bdd user %s",res)
                    elif image_to_guess['from']=='default' :
                        res = requests.post(ad_bdd_default+'labels_by_id', json={ "user": message['user'],"id_partie": message['id_partie'],"id_image_default": image_to_guess['id_image_to_guess']}, timeout=20).json()
                        logging.debug(" bdd default %s",res)

                    #on regarde les labels et on répond à la question
                    res_qd = requests.post(ad_ms +'answer_question', json={'question':message['question'],'labels':res['answer']['labels'] }, timeout=20).json()
                    logging.debug("answer to question %s",res_qd)
                    
                    answer = res_qd['answer']

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
                #on vérifie si la photo trouvée par l'utilisateur est la bonne
                
                logging.info("check_answer")

                try : 
                    #on check dans la bdd du jeu
                    answer = requests.post(ad_bdd_game+'result/'+message['user']+'/' + message['id_partie'] + '/'+message['final_image'], timeout=20).json()
                    logging.debug("check answer %s",answer)
                    
                    win = answer["win"]

                    question = {
                            'title' : 'AnswerSrV',
                            'user' : message['user'],
                            'id_partie' : message['id_partie'],
                            'final_image' : message['final_image'],
                            'answer' : {
                                        'answer_check': win
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

            elif title=="get_question_to_ask" :
                #on choisit la prochaine question que le computer va poser
                
                logging.info("get_question_to_ask")

                try : 

                    labels = {}
                    
                    #on recupère les ids des images de la partie
                    res_game = requests.post(ad_bdd_game+'images/'+message['user']+'/' + message['id_partie'], timeout=20).json()
                    logging.debug("images de la parties %s",res_game)

                    labels_default = {}
                    
                    if res_game['id_images_default']!=[]:
                        #recup les labels des images de la bdd default encore en jeu
                        labels_default = requests.post(ad_bdd_default+'labels', json={ "user": message['user'],"id_partie":  message['id_partie'],"images": res_game['id_images_default']}, timeout=20).json()['labels']
                        logging.debug("labels default %s",labels_default)
                    labels_user = {}

                    if res_game['id_images_user']!=[]:
                        #recup les labels des images de la bdd user encore en jeu
                        labels_user = requests.post(ad_bdd_user+'labels', json={ "user": message['user'],"id_partie":  message['id_partie'],"images": res_game['id_images_user']}, timeout=20).json()['labels']
                        logging.debug("labels user %s",labels_user)
                    
                    #on rassemble les dictionnaires de labels
                    labels = labels_default | labels_user
                    logging.debug("labels %s",labels)

                    #on compte combien il reste d'images dans la partie
                    images_left = len(list(labels.keys()))

                    logging.debug("already asked and excluded questions %s",message['excluded'])
                    logging.debug("images left %s",images_left)

                    if images_left==1 :
                        #le computer a trouvé une image
                        logging.debug("end of the game, found one")

                        for i in labels :
                            selectedImage = i
                            
                        if selectedImage in labels_default :
                            selectedImage = requests.post(ad_bdd_default+'celeb_by_id', json={ "user": message['user'],"id_partie":  message['id_partie'],"id": selectedImage}, timeout=20).json()['answer']['image']
                        else :
                            selectedImage = requests.post(ad_bdd_user+'image_by_id', json={ "user": message['user'],"id_partie":  message['id_partie'],"id": selectedImage}, timeout=20).json()['answer']['image']
                            
                        logging.debug("selected image %s",selectedImage)

                        question = {

                            'title' : 'AnswerSrV',
                            'user' : message['user'],
                            'id_partie' : message['id_partie'],
                            'answer' : {
                                        'image': selectedImage,
                                        'images_left' : images_left

                                    },
                            'confirm' : True
                        }
                        
                    elif images_left==0 : 
                        #le computer n'a trouvé aucune image
                        logging.debug("end of the game, did not find")
                        
                        question = {

                            'title' : 'AnswerSrV',
                            'user' : message['user'],
                            'id_partie' : message['id_partie'],
                            'answer' : {
                                        'images_left' : images_left
                                    },
                            'confirm' : True
                        }
                        

                    else :
                        #le computer cherche encore
                        
                        question_to_ask = requests.post(ad_ms + 'get_question_to_ask', json={"images":{"labels":labels}, "excluded":message['excluded']}, timeout=20).json()
                        logging.debug("message from ms-question: %s" ,question_to_ask)

                        logging.debug("Still asking")

                        question = {
                            'title' : 'AnswerSrV',
                            'user' : message['user'],
                            'id_partie' : message['id_partie'],
                            'answer' : {
                                        'question_to_ask': question_to_ask["question"],
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
                #recup la réponse de user à une question du computer et process la réponse
                
                logging.info("get_answer_user")

                try : 
                  
                    labels = []
                    
                    #recup les ids des images encore en jeu
                    res_game = requests.post(ad_bdd_game+'images/'+message['user']+'/' + message['id_partie'], timeout=20).json()
                    logging.debug("message bdd game %s",res_game)
                    
                    #recup les labels des images default encore en jeu
                    labels_default = {}

                    #recup les labels des images user encore en jeu
                    if res_game['id_images_default']!=[]:
                        res_default = requests.post(ad_bdd_default+'labels', json={ "user": message['user'],"id_partie":  message['id_partie'],"images": res_game['id_images_default']}, timeout=20).json()
                        logging.debug("message bdd default %s",res_default)
                        labels_default= res_default['labels']
                        
                        
                    labels_user = {}

                    #recup les labels des images user encore en jeu
                    if res_game['id_images_user']!=[]:
                        res_user = requests.post(ad_bdd_user+'labels', json={ "user": message['user'],"id_partie":  message['id_partie'],"images": res_game['id_images_user']}, timeout=20).json()
                        labels_user = res_user['labels']
                        logging.debug("message bdd user %s",res_user)
                        
                    #recup les images à supprimer de la bdd (ne correspondant pas à la rep du user)
                    res = requests.post(ad_ms+'process_question', json={"labels":labels_user|labels_default,'answer_user': message['answer_user'], 'question':message['question']}, timeout=20).json()
                    logging.debug("message id to delete %s",res)
                    id_to_delete = res['id_to_delete']
                    
                    #supprime les ids des images de la bdd de la partie
                    res_delete = requests.post(ad_bdd_game+'delete/'+message['user']+'/'+message['id_partie'], json={'ids':id_to_delete}, timeout=20).json()
                    logging.debug("deleted ids message %s",res_delete)
                    
                    question = {
                        
                        'title' : 'ConfirmSrV',
                        'user' : message['user'],
                        'id_partie' : message['id_partie'],
                        'answer_user': message['answer_user'],
                        'question':message['question'],
                        'confirm' : True
                    }
                except Exception as e :
                    logging.error(traceback.format_exc())
                    question = {
                            'title' : 'ConfirmSrV',
                            'user' : message['user'],
                            'id_partie' : message['id_partie'],
                            'answer_user': message['answer_user'],
                            'question':message['question'],
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
      
if __name__ == '__main__':
    app.run(debug=True, port=5000)