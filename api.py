from http.client import UNAUTHORIZED
from flask import Flask, flash, request, redirect, url_for, render_template,jsonify, session
from numpy import reshape
from helper import remove_token, add_token, is_token_found
import os
from werkzeug.utils import secure_filename
from Code import perdict_img
import math
import numpy as np

################## API ################
#app.py

app = Flask(__name__)

secret_key = "iuenp!m04*hu^@hieih" #secret_key for verifing backend requests 
# (to be added to environment variables)

UPLOAD_FOLDER = 'static'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

tokens=[]


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif','svg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/', methods=['GET'])
# def home():
#     return render_template('index.html')

@app.route('/insert_token', methods=['POST'])
def insert_token():

    data = request.get_json(force=True) 
    token = data['token']
    try:
        key = data['secret_key']
        
    except:
        key=""    
    if key == secret_key or "secret_key" in session: 

        session["secret_key"] = "secret_key"
        add_token(token)
        tokens.append(token)
        return jsonify(tokens), 201
    else:
        return jsonify({"response": "UNAUTHORIZED"}), 401 # UNAUTHORIZED   



@app.route('/delete_token', methods=['Delete'])
def delete_token():
    # The following line to take data in form of json
    data = request.get_json(force=True) 
    token = data['token']
    try:
        key = data['secret_key']
    except:
        key=""    
    if key == secret_key or "secret_key" in session:     
        remove_token(token) #for removing token from file.txt
        clear_session(token)
        if token in tokens:
            tokens.remove(token)
        else:
            return jsonify({"response": "This token does not exist!"}) , 404 # NOT Found
        return jsonify(tokens)
    else:
        return jsonify({"response": "UNAUTHORIZED"}), 401 # UNAUTHORIZED   




def clear_session(token):
    session.pop(token, None)


@app.route('/', methods=['POST'])
def upload_image():


    #The following line is used to get data as parameters in URL
    token = request.args.get('token')
    if token:

        if is_token_found(token):
            session[token] = token
        else:
            return jsonify({"response": "Invalid token"}) , 401       
    elif "token" in session:
        token = session["token"]   
    else:     
        return jsonify({"response": "Token is required or session is expired"}), 401 # UNAUTHORIZED
    
    
    data = request.get_json(force=True) 
    if not data:
        return jsonify({"response": "Image file is required"}), 404 # not found
    else:
        try:
            data = list(data.values()) # to store values only of the input json string

            
            data_inverse = [255 - x for x in data] # inverse 0 --> 1

            size= int(math.sqrt(len(data_inverse)))
            data_inverse =data_inverse[:size*size]
            data_inverse = np.array(data_inverse)  
            data = np.reshape(data_inverse,(size, size)) # rehaping the input data form 1D to 2D list 
            

            scores = perdict_img(data_inverse)
            
            return jsonify(scores)
        except:
            return jsonify({"response": "Image file is required"}), 400 # Bad Request


if __name__ == "__main__":
    app.run()     

    # TO DO       
# 1)create session with backend, with  a sercret key as an environment variable.
# 2)linking user session with token so when token is deleted the session related to this token is also cleared.
# 3)

############################# API END ###########################

# command for running flask app:
# api.py 