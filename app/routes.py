from flask import render_template, request
from app import app

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    #example challenge below:
    challenges = [
    {
        'title': 'My Test Challenge',
        'startArticle': 'University',
        'endArticle': 'Bottled Water',
        'guesses': 6,
        'creator': 'Joseph',
        'timeLeft': '2 hours 13 minutes'
    },{
        'title': 'My Test Challenge Again!',
        'startArticle': 'Library',
        'endArticle': 'Wisdom Teeth',
        'guesses': 1,
        'creator': 'Not Joseph',
        'timeLeft': '13 minutes'
    }]
    return render_template('index.html', challenges=challenges)

@app.route('/create', methods=['GET', 'PUT'])
def create():
    #TODO
    if request.method == "PUT":
        pass
    else:
        pass

#Submit should always include an id parameter
@app.route('/submit', methods=['GET', 'PUT'])
def submit():
    #TODO
    submission_id = request.args.get("id", default=-1, type=int)
    if request.method == "PUT":
        pass
    else:
        pass
    pass

#View should always include an id parameter
@app.route('/view', methods=['GET'])
def submit():
    #TODO
    #TODO - View should have server-side protection from being viewed by wrong account while challenge is active (not MVP)
    submission_id = request.args.get("id", default=-1, type=int)
    print(submission_id)
    pass

#View should always include an id parameter
@app.route('/view', methods=['GET'])
def submit():
    #TODO
    #TODO - View should have server-side protection from being viewed by wrong account while challenge is active (not MVP)
    submission_id = request.args.get("id", default=-1, type=int)
    print(submission_id)
    pass

@app.route('/login', methods=["POST"])
def login():
    #TODO - unsure of implementation/parameters currently, because of security concerns
    pass