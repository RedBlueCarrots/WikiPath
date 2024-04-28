from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
import time
from flask_login import UserMixin
from .utilities import *

class User(db.Model, UserMixin):
    # Integer column type with primary_key=True will enable auto-increment
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    points = db.Column(db.Integer, nullable=False)
    # I believe there are more secure ways of implementing this
    password_hash = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f'User({self.id}, "{self.username}", {self.points}, "{self.password_hash}")'

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.Text, nullable=False)
    path = db.Column(db.Text, nullable=False)
    # storing datetime as an integer as epoch as the datetime object makes dealing with time zones very frustrating
    dt_submit = db.Column(db.Integer, nullable=False)
    dt_finish = db.Column(db.Integer, nullable=False)
    finished = db.Column(db.Boolean, nullable=False)
    winner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creator = db.relationship("User", foreign_keys=[creator_id])
    winner = db.relationship("User", foreign_keys=[winner_id])
    attempts = db.relationship("Submission", backref="challenge")
    
    def toDict(self):
        pathArticles= self.path.split("|")
        challengeDict = {
            "id": self.id,
            "creator_id": self.creator_id,
            "creator": User.query.get(self.creator_id).username,
            "title": self.title,
            "startArticle": pathArticles[0],
            "endArticle": pathArticles[1],
            "timeLeft" : secondsToTime(self.dt_finish-int(time.time())),
            "guesses" : len(self.attempts),
            "finished": self.finished,
            "winner_id": self.winner_id
        }
        return challengeDict

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'))
    path = db.Column(db.Text, nullable=False)
    dt_submit = db.Column(db.Integer, nullable=False)
    article_no = db.Column(db.Integer, nullable=False)
    # was this submission the winner of the challenge?
    win = db.Column(db.Boolean, nullable=False)
    creator = db.relationship("User", foreign_keys=[creator_id])
    
    

    