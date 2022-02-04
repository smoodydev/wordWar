import os
from flask import Flask, session, jsonify
from game_tools import word_new

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "somesecret")

@app.route('/attempt')
def attempt():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=a + b)

@app.route('/new_word')
def new_word():
    session["word"] = word_new(4)
    return "Done"

@app.route('/')
def index():
    if "word" in session:
        return 'Your word is ' + session["word"]
    else:
        session["word"] = word_new(4)
        return "First Timer? - Getting you a new word"
    


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT', 8000)),
            debug=True)