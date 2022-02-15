import os
import bcrypt
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask import Flask, session, jsonify, render_template, request, redirect, url_for
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
    if not all([key in session for key in ["word","letters", "attempts"]]):
        session["word"] = word_new(5)
        session["letters"] = 5
        session["attempts"] = []
    return render_template("index.html", attempts=session["attempts"])
    

@app.route('/try_word', methods=["POST"])
def try_word():
    word = request.form["word"].lower()
    if ("complete" not in session):
        if is_valid_word(word, session["letters"]): 
            result = try_solve(session["word"], word)
            if 'attempts' in session:
                attempts = session.get("attempts")
                attempts.append([word, result])
                session["attempts"] = attempts
                text_back = "The server received the word "+request.form["word"]
                if result == "y"*session["letters"]:
                    session["complete"] = True
            else:
                session["attempts"] = [word]
            if "user" in session:
                updating = {"word":session["word"], "current_attempts": session["attempts"]}
                mongo.db.useraccount.update_one({"username": session["user"]}, {"$set" : updating})
                if "complete" in session:
                    score = len(session["attempts"])
                    mongo.db.useraccount.update_one({"username": session["user"]},{"$inc": {"score": 5 if score <= 3 else 7-score}})
            
            print(session["word"])
            return jsonify(validated=True, result=result, text_back=text_back)
        else:
            return jsonify(validated=False, text_back="Not a Valid Word")
    else:
        text_back = "You have already completed this word"
    return jsonify(validated=False, text_back=text_back)

@app.route('/new_word', methods=["POST"])
def new_word():
    # if "user" in session:
    #     updating = { "$inc": {"num_words": 1}}
    #     mongo.db.useraccount.update_one({"username": session["user"]}, updating)
    new_word = word_new(5)
    session["letters"] = 5
    if "user" in session:
        # updating = { "$inc": {"num_words": 1, "num_attempts": len(session["attempts"])}}
        user = mongo.db.useraccount.find_one({"username": session["user"]})
        updating = {"$set" : { 
            "num_attempts" : user.get("num_attempts", 0) + len(session["attempts"]),
            "num_words": user.get("num_words", 0) + 1,
            "word": new_word,
            "current_attempts": []
        }}
        mongo.db.useraccount.update_one({"username": session["user"]}, updating)
    session["attempts"] = []
    session["word"] = new_word
    session["letters"] = 5
    if "complete" in session:
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
            fields["num_words"] = 1
            fields["score"] = 0
            mongo.db.useraccount.insert_one(fields)
        return redirect(url_for("index"))
    return render_template('sign_up.html')


@app.route('/login', methods=['POST'])
def login():
    unhashed_pwd = request.form.get('password').encode('utf-8')
    this_user = request.form.get('username')
    user = mongo.db.useraccount.find_one({"username": this_user})
    if user:
        hashed_pwd = user["password"]
        if bcrypt.checkpw(unhashed_pwd, hashed_pwd):
            session["user"] = user["username"]
            session["word"] = user.get("word", word_new(5))
            session["letters"] = user.get("letters", 5)
            session["attempts"] = user.get("attempts", [])
            return redirect(url_for('index'))
        else:
            return "Account Found but Wrong Hash/PWD"
    else:
        return "No Account Found"

@app.route('/logout')
def logout():
    if "user" in session:
        session.pop("user")
        
    return redirect(url_for('index'))


@app.route('/leaderboard')
def leaderboard():
    top_scores = mongo.db.useraccount.find().sort("score", -1).limit(5)
  
    
    return render_template("leaderboard.html", leaderboard=top_scores)





if __name__ == '__main__':
    app.run(host=os.environ.get('IP', "0.0.0.0"),
            port=int(os.environ.get('PORT', 8000)),
            debug=True)