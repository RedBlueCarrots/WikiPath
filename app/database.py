from .models import *
from .utilities import *
from app import login

@login.user_loader
def load_user(id):
    return getUser(id)

def checkUsernameExists(name):
    user = db.session.query(User).filter_by(username=name).first()
    return user is not None

def checkChallengeExists(post_id):
    challenge = db.session.query(Challenge).filter_by(id=post_id).first()
    return challenge is not None

def checkSubmissionExists(submission_id):
    submission = db.session.query(Submission).filter_by(id=submission_id).first()
    return submission is not None