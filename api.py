from http.client import UNAUTHORIZED
from flask import Flask, flash, request, redirect, url_for, render_template,jsonify, session
from helper import remove_token, add_token, is_token_found
import os
from werkzeug.utils import secure_filename
from Code import perdict_img

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


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

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
        return jsonify({"respose": "UNAUTHORIZED"}), 401 # UNAUTHORIZED   

# @app.route('/get_data', methods=['POST'])
# def get_data():
#     data = request.data
#     return data

@app.route('/delete_token', methods=['Delete'])
def delete_token():
    data = request.get_json(force=True) 
    token = data['token']
    try:
        key = data['secret_key']
    except:
        key=""    
    if key == secret_key or "secret_key" in session:     
        remove_token(token)
        clear_session(token)
        if token in tokens:
            tokens.remove(token)
        else:
            return jsonify({"respose": "This token does not exist!"}) , 404 # NOT Found
        return jsonify(tokens)
    else:
        return jsonify({"respose": "UNAUTHORIZED"}), 401 # UNAUTHORIZED   




def clear_session(token):
    session.pop(token, None)


@app.route('/', methods=['POST','GET'])
def upload_image():

    if request.method == 'POST':
        token = request.args.get('token')
        if token:
            if is_token_found(token):
                session[token] = token
            else:
                return jsonify({"respose": "Invalid token"}) , 401       
        elif "token" in session:
            token = session["token"]   
        else:     
            return jsonify({"respose": "Token is required or session is expired"}), 401 # UNAUTHORIZED
        
        if 'file' not in request.files:
            return jsonify({"respose": "Image file is requered"}), 404 # not found

        file = request.files['file']
        if file.filename == '':
            return jsonify({"respose": "No image selected for uploading"}), 404 # UNAUTHORIZED

        if file and allowed_file(file.filename):
            print("YES i entered")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            scores = perdict_img(file)
            print (scores)
            return jsonify(scores)
        else:

            return jsonify({"respose": "This file type is not allowed"}), 


    # elif request.method == 'GET':
    #     return render_template('index.html')

##Requests for backend##
# @app.route('/get_token', methods=['GET'])
# def save_token():



if __name__ == "__main__":
    app.run()     

    # TO DO       
# 1)create session with backend, with  a sercret key as an environment variable.
# 2)linking user session with token so when token is deleted the session related to this token is also cleared.
# 3)

############################# API END ###########################
