from flask import Flask, request,jsonify, session
from helper import remove_token, add_token, is_token_found, resizing_vector
from Code import perdict_img

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
    input_data = request.get_json(force=True) 

    token = input_data["token"]
    json_data =input_data["data"]
    if token:

        if is_token_found(token):
            session[token] = token
        else:
            return jsonify({"response": "Invalid token"}) , 401       
    elif "token" in session:
        token = session["token"]   
    else:     
        return jsonify({"response": "Token is required or session is expired"}), 401 # UNAUTHORIZED
    
    # data = request.get_json(force=True) 
    if not json_data:
        return jsonify({"response": "Image file is required"}), 404 # not found
    else:
        try:
            json_data = resizing_vector(json_data)            
            scores = perdict_img(json_data)
            
            return jsonify(scores)
        except:
            return jsonify({"response": "Image file is required"}), 400 # Bad Request

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
