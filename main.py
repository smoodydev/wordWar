import os
import bcrypt
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask import Flask, session, jsonify, render_template, request
from game_tools import word_new, is_valid_word, try_solve
if os.path.exists("env.py"):
    import env
else:
    print("not there")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "somesecret")
app.config["MONGO_DBNAME"] = "wordwar"
app.config["MONGO_URI"] = os.environ.get("MONGO_URI", "")
mongo = PyMongo(app)


# ROUTE
@app.route('/')
def index():
    # session["attempts"] = []
    if "word" not in session:
        session["word"] = word_new(5)
    if "letters" not in session:
        session["letters"] = 5
    if "attempts" not in session:
        session["attempts"] = []

    print(session["attempts"])
    return render_template("index.html", attempts=session["attempts"])
    

@app.route('/try_word', methods=["POST"])
def try_word():
    word = request.form["word"].lower()
    if ("complete" not in session):
        if is_valid_word(word, session["letters"]): 
            result = try_solve(session["word"], word)
            if 'attempts' in session:
                print(session["attempts"], "blah")
                attempts = session.get("attempts")
                attempts.append([word, result])
                session["attempts"] = attempts
                text_back = "The server received the word "+request.form["word"]
                if result == "y"*session["letters"]:
                    session["complete"] = True
            else:
                session["attempts"] = [word]
            return jsonify(validated=True, result=result, text_back=text_back)
        else:
            return jsonify(validated=False, text_back="Not a Valid Word")
    else:
        text_back = "You have already completed this word"
    return jsonify(validated=False, text_back=text_back)

@app.route('/new_word', methods=["POST"])
def new_word():
    session["word"] = word_new(5)
    session["letters"] = 5
    session["attempts"] = []
    session.pop("complete")
    return jsonify(result="Success")


# Authentications
@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        fields = request.form.to_dict()
        if fields["password1"] == fields["password2"]:
            hashing_password = request.form.get('password1').encode('utf-8')
            fields['password'] = bcrypt.hashpw(hashing_password, bcrypt.gensalt())
            [fields.pop(key) for key in ['password1', 'password2']]
        
        mongo.db.useraccount.insert_one(fields)
    return render_template('sign_up.html')


@app.route('/login', methods=['POST'])
def login():

    unhashed_pwd = request.form.get('password').encode('utf-8')
    this_user = request.form.get('username')
    if mongo.db.useraccount.find({"username": this_user}):
        hashed_pwd = mongo.db.useraccount.find_one({"username": this_user})["password"]
        print(unhashed_pwd, hashed_pwd)
        if bcrypt.checkpw(unhashed_pwd, hashed_pwd):
            return "Can Log In"
        else:
            return "Account Found but Wrong Hash/PWD"
    else:
        return "No Account Found"




if __name__ == '__main__':
    app.run(host=os.environ.get('IP', "0.0.0.0"),
            port=int(os.environ.get('PORT', 8000)),
            debug=True)