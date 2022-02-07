import os
from flask import Flask, session, jsonify, render_template, request
from game_tools import word_new, is_valid_word, try_solve

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "somesecret")

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

@app.route('/')
def index():
    if "word" not in session:
        session["word"] = word_new(5)
        session["letters"] = 5
    return render_template("index.html")
    


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', 8000)),
            debug=True)