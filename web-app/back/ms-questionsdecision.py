# Import flask and datetime module for showing date and time
from flask import Flask, jsonify, request
from flask_cors import CORS
from os import system
from subprocess import check_output
import couchdb
import base64
import questiondecision
  
# Initializing flask app
app = Flask(__name__)
cors = CORS(app, supports_credentials=True)
app.secret_key = "123"
cors.init_app(app)

@app.route('/get_question_to_ask', methods=["POST"])
def get_question_to_ask() : 
    json = request.get_json()
    print(json)

    excluded = []

    for ex in json['excluded'] :
        for i in questiondecision.questions.keys() :
            if questiondecision.questions[i]==ex :
                excluded.append(i)
            
    result = questiondecision.get_question_to_ask(json['images'],excluded)
    print(result)
    return(jsonify({"question" : result}))
     
@app.route('/get_possible_question', methods=["GET"])
def get_possible_question() : 
    result = questiondecision.questions
    return(jsonify({"questions" : result}))

# Running app
if __name__ == '__main__':
    app.run(debug=True, port=7001)