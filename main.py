import os
import bcrypt
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask import Flask, session, jsonify, render_template, request
from game_tools import word_new, is_valid_word, try_solve
if os.path.exists:
    import env

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "somesecret")
app.config["MONGO_DBNAME"] = "wordwar"
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "")
mongo = PyMongo(app)


# ROUTE
@app.route('/')
def index():
    if "word" not in session:
        session["word"] = word_new(5)
        session["letters"] = 5
    return render_template("index.html")
    




@app.route('/try_word', methods=["POST"])
def try_word():
    word = request.form["word"].lower()

    if is_valid_word(word, session["letters"]):
        result = try_solve(session["word"], word)
        return jsonify(validated=True, result=result, text="The server received the word "+request.form["word"])
    else:
        return jsonify(validated=False, result="Not a Valid Word")

@app.route('/new_word', methods=["POST"])
def new_word():
    session["word"] = word_new(5)
    session["letters"] = 5
    return jsonify(result="Success")


# Authentications
@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        old_password = b"request.form.get('password')"
        hash_pass = bcrypt.hashpw(old_password, bcrypt.gensalt())
        fields = request.form.to_dict()
        fields['password'] = hash_pass
        mongo.db.useraccount.insert_one(fields)
    return render_template('sign_up.html')


@app.route('/login', methods=['POST'])
def login():
    unhashed_pwd = b"request.form.get('user_password')"
    this_user = request.form.get('user_username')
    
    if mongo.db.Users.find({"username": this_user}):
        hashed_pwd = mongo.db.useraccount.find({"Username": this_user}, {"Password": 1, "_id":0 })
        print(hashed_pwd)
        if bcrypt.checkpw(unhashed_pwd, hashed_pwd):
            return "FOUND+Hashed"
        else:
            return "FOUND+NOPE"
    else:
        
        return "NOT FOUND"




if __name__ == '__main__':
    app.run(host=os.environ.get('IP', "0.0.0.0"),
            port=int(os.environ.get('PORT', 8000)),
            debug=True)