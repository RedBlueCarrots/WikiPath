from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
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
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.Text, nullable=False)
    path = db.Column(db.Text, nullable=False)
    # storing datetime as an integer as epoch as the datetime object makes dealing with time zones very frustrating
    dt_submit = db.Column(db.Integer, nullable=False)
    dt_finish = db.Column(db.Integer, nullable=False)
    finished = db.Column(db.Boolean, nullable=False)
    winner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    poster = db.relationship("User", foreign_keys=[poster_id])
    winner = db.relationship("User", foreign_keys=[winner_id])

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('challenge.id'))
    path = db.Column(db.Text, nullable=False)
    dt_submit = db.Column(db.Integer, nullable=False)
    article_no = db.Column(db.Integer, nullable=False)
    ogpost = db.relationship("Challenge", foreign_keys=[post_id])
    poster = db.relationship("User", foreign_keys=[poster_id])
    

    