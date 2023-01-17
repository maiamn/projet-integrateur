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



@app.route('/get_question_to_ask', methods=["GET"])
def get_question_to_ask() : 
    print("bonjour")



@app.route('/', methods=["GET"])
def getQuestionToAsk():
    questiondecision.init() #à appeler une seule fois au début
    variable = questiondecision.test()
    return jsonify({"message" : "Coucou", "variable": variable})

@app.route('/', methods=["POST"])
def getAnswerQuestion():
   questiondecision.get_images_left_df()

     
# Running app
if __name__ == '__main__':
    app.run(debug=True, port=7001)