from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_user, logout_user
from app import app
from .database import *
from .forms import *
import time
from datetime import datetime

#Home page
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    #Challenges
    challengeList = []
    challenges = Challenge.query.all()
    for challenge in challenges:
        challengeList.append(challenge.toDict())
    form = LoginForm()
    return render_template('index.html', challenges=challengeList, form=form)

#Create challenge page
@app.route('/create', methods=['GET', 'POST'])
def create():
    form = LoginForm()
    create_form = ChallengeCreationForm()
    errors = []
    if create_form.validate_on_submit():
        if current_user.is_anonymous:
            errors.append("Login before creating a challenge!")
        path = create_form.start.data + "|" + create_form.destination.data
        try:
            datetime_object = int(datetime.fromisoformat(str(create_form.time.data)).timestamp())
            if datetime_object < int(time.time()):
                errors.append("The submission close date must be in the future.")
        except:
            errors.append("The submission close date must be in the future.")
        if len(errors) > 0:
            return render_template('create.html', form=form, create_form=create_form, errors=errors)
        createNewChallenge(current_user.id, create_form.title.data, path, int(time.time()), datetime_object)
        return redirect(url_for('index'))
    return render_template('create.html', form=form, create_form=create_form, errors=errors)

#Challenge submission
#Submit should always include an id parameter
@app.route('/submit', methods=['POST'])
def submit():
    submitForm = SubmitForm()
    form = LoginForm()
    challenge = getChallenge(int(submitForm.challenge_id.data)).toDict()
    pathString = ""
    print(challenge)
    pathString = challenge["startArticle"] + "|"
    for i in submitForm.path.data:
        if i.strip() != "":
            pathString += i + "|"
    pathString += challenge["endArticle"]
    if submitForm.validate_on_submit():
        createNewSubmission(current_user.id, challenge["id"], pathString, int(time.time()))
        return redirect(url_for('view', id=int(submitForm.challenge_id.data)))
    return render_template('view.html', form=form, submitForm=submitForm, submitted=False, challenge=challenge, errors=submitForm.errors["path"][0], path=pathString)

#Challenge view
#View should always include an id parameter
@app.route('/view', methods=['GET'])
def view():
    form = LoginForm()
    challenge_id = int(request.args.get("id", default=-1, type=int))
    challenge = getChallenge(challenge_id).toDict()
    if current_user.is_anonymous:
        return render_template('view.html', form=form, submitted=True, challenge=challenge, submissions=[])
    isCreator = getChallenge(challenge_id).creator_id == current_user.id
    isSubmitted = getSubmissionByChallengeAndCreator(getChallenge(challenge_id).id, current_user.id) != None
    isFinished = getChallenge(challenge_id).finished
    
    if isCreator or isFinished:
        submissions = getSubmissionsByChallenge(challenge_id)
        return render_template('view.html', form=form, submitted=True, challenge=challenge, submissions=submissions)
    elif isSubmitted:
        submissions = [getSubmissionByChallengeAndCreator(getChallenge(challenge_id).id, current_user.id)]
        return render_template('view.html', form=form, submitted=True, challenge=challenge, submissions=submissions)
    submitForm = SubmitForm()
    return render_template('view.html', form=form, submitForm=submitForm, submitted=False, challenge=challenge)

#create account
@app.route('/create_account', methods=["POST"])
def create_account():
    form = LoginForm()
    if returnUserViaUsername(form.username.data) == None:
        createUser(form.username.data, form.password.data)
        login_user(returnUserViaUsername(form.username.data), remember=form.remember_me.data)
        response = jsonify({"reason": "Account successful"})
        response.status_code = 200
        return response
    response = jsonify({"reason": "Username already exists"})
    response.status_code = 401
    return response

#Login
@app.route('/login', methods=["POST"])
def login():
    #TODO - implement password and password checking
    form = LoginForm()
    #This is for testing.
    if form.username.data == "root":
        for sub in getSubmissionsByCreator(0):
            db.session.delete(sub)
            db.session.commit()
        db.session.delete(returnUserViaUsername("testUser"))  
        db.session.commit()
   
    if form.validate_on_submit():
        if returnUserViaUsername(form.username.data) != None:
            login_user(returnUserViaUsername(form.username.data), remember=form.remember_me.data)
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
