from .models import *
from .utilities import *
from app import login

@login.user_loader
def load_user(id):
    return User.query.get(id)

def returnUserViaUsername(name):
    user = db.session.query(User).filter_by(username=name).first()
    return user
    
def getChallenge(post_id):
    challenge = db.session.query(Challenge).filter_by(id=post_id).first()
    return challenge

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