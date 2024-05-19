from flask import render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_user, logout_user
from app.blueprints import main
from .database import *
from .forms import *
import time
from datetime import datetime
from app.wikipedia import *

#Home page

@main.route('/', methods=['GET'])
@main.route('/index', methods=['GET'])
def index(search_string=None):
    checkChallengesCompleted()
    form = LoginForm()
    search_form = SearchForm()
    active_nav = "play"
    challengeList = []
    search_string = request.args.get("search")
    page_num = request.args.get("page")
    if page_num is None:
        page_num = 1
    page_num = int(page_num)
    total_pages = 1
    if search_string is None:
        total_pages = getTotalChallengePages()
        challenges = getChallengesByPage(page_num)
    else:
        challenges = getChallengesByTitleOrCreator(search_string, page_num)
        total_pages = challenges[1]
        challenges = challenges[0]
        if challenges == []:
            flash("Your search did not return any results.")
    for challenge in challenges:
        challengeList.append(challenge.toDict())
    return render_template('index.html', challenges=challengeList, form=form, search_form=search_form, nav=active_nav, current_page=page_num, total_pages=total_pages)

@main.route('/search', methods=['POST'])
def search():
    search_form = SearchForm()
    return redirect(url_for('main.index', search=search_form.search.data))

#Create challenge page
@main.route('/create', methods=['GET', 'POST'])
def create():
    form = LoginForm()
    create_form = ChallengeCreationForm()
    errors = []
    active_nav = "create"
    if create_form.validate_on_submit():
        if current_user.is_anonymous:
            errors.append("Login before creating a challenge!")
        if (create_form.start.data == create_form.destination.data):
            errors.append("The starting article cannot be the same as the destination article!")
        articlesInfo = checkArticlesExists([create_form.start.data, create_form.destination.data])
        for article in articlesInfo:
            if not articlesInfo[article]:
                errors.append(article + " is not a valid article")
        path = create_form.start.data + "|" + create_form.destination.data
        try:
            datetime_object = int(datetime.fromisoformat(str(create_form.time.data)).timestamp())
            if datetime_object < int(time.time()):
                errors.append("The submission close date must be in the future.")
        except:
            errors.append("The submission close date must be in the future.")
        if len(errors) > 0:
            return render_template('create.html', form=form, create_form=create_form, errors=errors, nav=active_nav)
        createNewChallenge(current_user.id, create_form.title.data, path, int(time.time()), datetime_object)
        return redirect(url_for('main.index'))
    return render_template('create.html', form=form, create_form=create_form, errors=errors, nav=active_nav)

#Challenge submission
#Submit should always include an id parameter
@main.route('/submit', methods=['POST'])
def submit():
    checkChallengesCompleted()
    submitForm = SubmitForm()
    form = LoginForm()
    challenge = getChallenge(int(submitForm.challenge_id.data)).toDict()
    if challenge["finished"]:
        return redirect(url_for('main.view', id=int(submitForm.challenge_id.data)))
    #if validation errored, this means there is a path failure
    #Include the submitted path in the return URL, so form stays populated
    pathString = ""
    pathString = challenge["startArticle"] + "|"
    for i in submitForm.path.data:
        if i.strip() != "":
            pathString += i + "|"
    pathString += challenge["endArticle"]
    if submitForm.validate_on_submit():
        createNewSubmission(current_user.id, challenge["id"], pathString, int(time.time()))
        return redirect(url_for('main.view', id=int(submitForm.challenge_id.data)))
    #submitform["path][0] has been raised as ["article errors", "path errors"]
    return redirect(url_for('main.view', id=int(submitForm.challenge_id.data), article_errors=submitForm.errors["path"][0][0], path=pathString, path_errors=submitForm.errors["path"][0][1]))

#Challenge view
#View should always include an id parameter
@main.route('/view', methods=['GET'])
def view():
    checkChallengesCompleted()
    form = LoginForm()
    submitForm = SubmitForm()
    challenge_id = int(request.args.get("id", default=-1, type=int))
    if(getChallenge(challenge_id) is None ):
        return redirect(url_for('main.index'))
    challenge = getChallenge(challenge_id).toDict()
    isFinished = getChallenge(challenge_id).finished
    if current_user.is_anonymous:
        if isFinished:
            submissions = getSubmissionsByChallenge(challenge_id)
            return render_template('view.html', form=form, submitted=True, challenge=challenge, submissions=submissions)
        return render_template('view.html', form=form, submitted=True, challenge=challenge, submissions=[])
    isCreator = getChallenge(challenge_id).creator_id == current_user.id
    isSubmitted = getSubmissionByChallengeAndCreator(getChallenge(challenge_id).id, current_user.id) != None
    isFinished = getChallenge(challenge_id).finished
    
    if isCreator or isFinished:
        submissions = getSubmissionsByChallenge(challenge_id).copy()
        for s in submissions:
            s.dt_submit = time.strftime('%d/%m/%Y %I:%M %p', time.localtime(s.dt_submit))
        return render_template('view.html', form=form, submitted=True, challenge=challenge, submissions=submissions)
    elif isSubmitted:
        submissions = [getSubmissionByChallengeAndCreator(getChallenge(challenge_id).id, current_user.id)]
        submissions[0].dt_submit = time.strftime('%d/%m/%Y %I:%M %p', time.localtime(submissions[0].dt_submit))
        return render_template('view.html', form=form, submitted=True, challenge=challenge, submissions=submissions)
    submitted_path = request.args.get("path")
    article_errors = request.args.get("article_errors")
    path_errors = request.args.get("path_errors")
    if(submitted_path is not None):
        return render_template('view.html', form=form, submitForm=submitForm, submitted=False, challenge=challenge, article_errors=article_errors, path=submitted_path, path_errors=path_errors)
    
    return render_template('view.html', form=form, submitForm=submitForm, submitted=False, challenge=challenge)

#create account
@main.route('/create_account', methods=["POST"])
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
@main.route('/login', methods=["POST"])
def login():
    form = LoginForm()
    #This is for testing.
    if form.username.data == "root":
        for sub in getSubmissionsByCreator(0):
            db.session.delete(sub)
            db.session.commit()
        #db.session.delete(returnUserViaUsername("testUser"))  
        db.session.commit()
   
    if form.validate_on_submit():
        current_login_user = returnUserViaUsername(form.username.data)
        # Checks if the user exists and the password matches with what's stored in the database
        if current_login_user != None and current_login_user.check_password(form.password.data):
            login_user(current_login_user, remember=form.remember_me.data)
            response = jsonify({"reason": "Login Successful"})
            response.status_code = 200
            return response
        response = jsonify({"reason": "Invalid Username or Password"})
        response.status_code = 401
        return response
    pass

#Logout
@main.route('/logout', methods=["GET"])
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route("/users", methods=["GET"])
def leaderboard():
    form = LoginForm()
    userList = []
    users = db.session.execute(db.select(User).order_by(User.WikiAura)).scalars()
    scores = [usr.WikiAura for usr in db.session.execute(db.select(User)).scalars()]
    scores.sort(reverse=True)
    for user in users:
        userList.append({})
        userList[-1]["rank"] = scores.index(user.WikiAura) + 1
        userList[-1]["username"] = user.username
        userList[-1]["WikiAura"] = user.WikiAura
    active_nav = "leaderboard"
    return render_template('leaderboard.html', users=userList, form=form, nav=active_nav)