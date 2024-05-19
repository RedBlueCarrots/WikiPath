from .models import *
from .utilities import *
from app import login
import random
import string
from sqlalchemy import func
import math

@login.user_loader
def load_user(id):
    return User.query.get(id)

def returnUserViaUsername(name):
    user = db.session.query(User).filter_by(username=name).first()
    return user

def createUser(username, password):
    # Make the salt
    salt = random.choice(string.ascii_letters)
    user = User(username = username, password_hash = "", WikiAura = 0, password_salt = salt)
    # Hash the password
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
def getChallenge(post_id):
    challenge = db.session.query(Challenge).filter_by(id=post_id).first()
    return challenge

def getChallengesByPage(pageNum):
    if pageNum < 1:
        pageNum = 1
    scores = [chal.id for chal in db.session.execute(db.select(Challenge)).scalars()]
    if pageNum > math.ceil(len(scores)/10.0):
        pageNum = math.ceil(len(scores)/10.0)
    scores.sort(reverse=False)
    scores = scores[(pageNum-1)*10:pageNum*10]
    query = db.session.query(Challenge).filter(Challenge.id.in_(scores))
    return query.all()


def getChallengesByTitleOrCreator(search):
    users = db.session.query(User).filter(User.username.icontains(search)).all()
    ids = [user.id for user in users]
    challenges = db.session.query(Challenge).filter(Challenge.title.icontains(search)).all()
    challenges = challenges + db.session.query(Challenge).filter(Challenge.creator_id.in_(ids)).all()
    challenges = list(dict.fromkeys(challenges))
    return challenges

def getSubmission(submission_id):
    submission = db.session.query(Submission).filter_by(id=submission_id).first()
    return submission

# Most likely don't need this anymore as getSubmission() does the same thing essentially
def checkSubmissionExists(submission_id):
    submission = db.session.query(Submission).filter_by(id=submission_id).first()
    return submission is not None

def getSubmissionByChallengeAndCreator(challenge_id, creator_id):
    submission = db.session.query(Submission).filter_by(challenge_id=challenge_id, creator_id=creator_id).first()
    return submission

#Used to delete all root user submissions for debugging
def getSubmissionsByCreator(creator_id):
    submission = db.session.query(Submission).filter_by(creator_id=creator_id).all()
    return submission

def getSubmissionsByChallenge(challenge_id):
    submission = db.session.query(Submission).filter_by(challenge_id=challenge_id).all()
    return submission

def createNewSubmission(creator_id, challenge_id, path, dt_submit):
    newSubmission = Submission(
        creator_id=creator_id,
        challenge_id=challenge_id,
        path=path,
        dt_submit=dt_submit,
        article_no=path.count("|")+1,
        win=False)
    db.session.add(newSubmission)
    db.session.commit()
    
def createNewChallenge(creator_id, title, path, dt_submit, dt_finish):
    newChallenge = Challenge(
        creator_id = creator_id,
        title=title,
        path=path,
        dt_submit=dt_submit,
        dt_finish=dt_finish,
        finished=False)
    db.session.add(newChallenge)
    db.session.commit()

# Given a Challenge model, find the submission with the fewest articles in its path (the winner of the challenge)
def findWinner(challenge):
    maxArticles = -1 # For what we currently have, each path has a maximum length of 50 articles
    winningSubmission = None
    for submission in challenge.attempts:
        # If there's a tie, the earliest submission should be the winner, and in the database, it automatically sorts via attempt submission
        if submission.article_no < maxArticles or maxArticles == -1:
            maxArticles = submission.article_no
            winningSubmission = submission.id
    return winningSubmission

# Query the database to see if a challenge is finished. If so, update the database to store who won the challenge.
def checkChallengesCompleted():
    challenges = Challenge.query.all()
    for challenge in challenges:
        if ((challenge.dt_finish-int(time.time())) <= 0 and not challenge.finished):
            challenge.finished = True
            winning_submission = getSubmission(findWinner(challenge))
            if winning_submission is not None:
                challenge.winner_id = winning_submission.creator_id
                winner = challenge.winner
                winner.WikiAura += 10
    db.session.commit()
            