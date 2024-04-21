from flask import render_template, request, flash, redirect
from app import app
from app.forms import LoginForm
from app.database import checkUsernameExists

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

    form = LoginForm()
    # Should pass "is logged in" here, which will change a conditional in base.html
    return render_template("index.html", challenges=challenges, form=form)

@app.route('/create', methods=['GET', 'PUT'])
def create():
    #TODO
    if request.method == "PUT":
        pass
    else:
        return render_template('create.html') #Extend with parameters as needed

#Submit should always include an id parameter
@app.route('/submit', methods=['GET', 'PUT'])
def submit():
    #TODO
    submission_id = request.args.get("id", default=-1, type=int)
    if request.method == "PUT":
        pass
    else:
        return render_template('submit.html') #Extend with parameters as needed

#View should always include an id parameter
@app.route('/view', methods=['GET'])
def view():
    #TODO - View should have server-side protection from being viewed by wrong account while challenge is active (not MVP)
    submission_id = request.args.get("id", default=-1, type=int)
    return render_template('view.html') #Extend with parameters as needed

@app.route('/login', methods=["POST"])
def login():
    #TODO - unsure of implementation/parameters currently, because of security concerns
    form = LoginForm()
    if form.validate_on_submit():
        if checkUsernameExists(form.username.data):
            flash("ThisGuyExists!")
            return redirect("\index")
        flash("no exist")
        return ('', 204)
    pass
