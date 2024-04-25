from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_user, logout_user
from app import app
from .database import *
from .forms import LoginForm

#Home page
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    #Challenges
    challenges = []
    for chal in getAllChallenges():
        challenges.append(chal.toDict())
    form = LoginForm()
    return render_template('index.html', challenges=challenges, form=form)

#Create challenge page
@app.route('/create', methods=['GET', 'PUT'])
def create():
    #TODO
    if request.method == "PUT":
        pass
    else:
        return render_template('create.html') #Extend with parameters as needed

#Challenge submission
#Submit should always include an id parameter
@app.route('/submit', methods=['GET', 'PUT'])
def submit():
    #TODO
    submission_id = request.args.get("id", default=-1, type=int)
    if request.method == "PUT":
        pass
    else:
        return render_template('submit.html') #Extend with parameters as needed

#Challenge view
#View should always include an id parameter
@app.route('/view', methods=['GET'])
def view():
    #TODO - View should have server-side protection from being viewed by wrong account while challenge is active (not MVP)
    submission_id = request.args.get("id", default=-1, type=int)
    return render_template('view.html') #Extend with parameters as needed

#Login
@app.route('/login', methods=["POST"])
def login():
    #TODO - implement password and password checking
    form = LoginForm()
    if form.validate_on_submit():
        if checkUsernameExists(form.username.data):
            login_user(getUserViaName(form.username.data), remember=form.remember_me.data)
            response = jsonify({"reason": "Login Successful"})
            response.status_code = 200
            return response
        response = jsonify({"reason": "Invalid Username or Password"})
        response.status_code = 401
        return response
    pass

#Logout
@app.route('/logout', methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for('index'))
