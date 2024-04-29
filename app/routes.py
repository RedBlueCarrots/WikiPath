from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_user, logout_user
from app import app
from .database import *
from .forms import *
import time

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
@app.route('/create', methods=['GET', 'PUT'])
def create():
    #TODO
    if request.method == "PUT":
        pass
    else:
        return render_template('create.html') #Extend with parameters as needed

#Challenge submission
#Submit should always include an id parameter
@app.route('/submit', methods=['POST'])
def submit():
    submitForm = SubmitForm()
    form = LoginForm()
    pathString = ""
    challenge = getChallenge(int(submitForm.challenge_id.data)).toDict()
    print(challenge)
    pathString = challenge["startArticle"] + "|"
    for i in submitForm.path.data:
        if i.strip() != "":
            pathString += i + "|"
    pathString += challenge["endArticle"]
    createNewSubmission(current_user.id, challenge["id"], pathString, int(time.time()))
    return redirect(url_for('view', id=int(submitForm.challenge_id.data)))

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

#Login
@app.route('/login', methods=["POST"])
def login():
    #TODO - implement password and password checking
    form = LoginForm()
    if form.username.data == "root":
        for sub in getSubmissionsByCreator(0):
            db.session.delete(sub)
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
