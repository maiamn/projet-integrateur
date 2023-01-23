# Import flask and datetime module for showing date and time
from flask import Flask, jsonify, request
from flask_cors import CORS
from os import system
from subprocess import check_output
import couchdb
import base64
import questiondecision
import logging
  
# Initializing flask app
app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.secret_key = "123"
cors.init_app(app)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

#Route pour vérifier que le microservice est bien lancé
@app.route("/", methods=["GET"])
def defaultRoute():
    return jsonify("question decision OK on port 7001")

#on recupère la prochaine question que le computer va poser
@app.route('/get_question_to_ask', methods=["POST"])
def get_question_to_ask() : 
    logging.info("get_question_to_ask")
    
    mess = request.get_json()
    logging.debug("message from main %s ",mess)

    #on exclue les questions déjà posées
    excluded = {}
    
    logging.debug("excluded before %s",mess['excluded'])
    
    for ex in mess['excluded'] :
        for i in questiondecision.questions.keys() :
            if questiondecision.questions[i]==ex :
                excluded[i]=mess['excluded'][ex]
                
    logging.debug("excluded %s",excluded)
            
    #recup de la question à poser
    result = questiondecision.get_question_to_ask(mess['images'],excluded)
    logging.debug(" next question %s",result)
    
    return(jsonify({"question" : result}))
     
@app.route('/get_possible_question', methods=["GET"])
def get_possible_question() : 
    logging.info("get_possible_question")
    
    #recup les questions possibles
    result = questiondecision.questions
    logging.debug("possible question %s",result)
    
    return(jsonify({"questions" : result}))

@app.route('/answer_question', methods=["POST"])
def answer_question() : 
    #répond à la question de l'user
    logging.info("answer_question")
    
    message = request.get_json()
    logging.debug("message from main %s",message)

    q = message['question']
    
    logging.debug("question %s",q)
    
    if message['labels'][q]==1:
        answer = True
    elif message['labels'][q]==-1 :
        answer = False

    return(jsonify({"answer" : answer, "question":questiondecision.questions[q]}))

@app.route('/process_question', methods=["POST"])
def process_question() : 
    #process la réponse de l'user
    logging.info("process_question")
    
    message = request.get_json()
    logging.debug("message from main %s",message)

    answer_user = 1 if message['answer_user'] else -1

    for i in questiondecision.questions.keys() :
        if questiondecision.questions[i]==message['question'] :
            question = i
    
    logging.debug("question %s",question)
    logging.debug("answer_user %s",answer_user)

    
    #on fait la liste des images qui ne correspondent pas 
    id_to_delete = []

    for img in message['labels'] :
        if message['labels'][img][question]!=answer_user:
            id_to_delete.append(img)
       
    logging.debug("id to delete %s",id_to_delete)
    
    return(jsonify({"id_to_delete" : id_to_delete}))

# Running app
if __name__ == '__main__':
    app.run(debug=True, port=7001)