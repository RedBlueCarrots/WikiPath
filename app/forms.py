from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, HiddenField, DateTimeLocalField
from wtforms.validators import DataRequired, ValidationError
from .wikipedia import *

def articleExists(form,field):
        print(field.data)
        if not checkArticleExists(field.data):
            raise ValidationError(str(field.data) + " is not a valid article")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    login = SubmitField('Login')
    create_account = SubmitField('Create Account')
    
class SubmitForm(FlaskForm):
    path = FieldList(StringField('Path', validators=[articleExists]), min_entries=1, max_entries=50)
    challenge_id = HiddenField()
    

class ChallengeCreationForm(FlaskForm):
    title = StringField('Challenge Title', validators=[DataRequired()])
    start = StringField('Starting Article', validators=[DataRequired()])
    destination = StringField('Destination Article', validators=[DataRequired()])
    time = DateTimeLocalField('Submission Close', validators=[DataRequired()])
    submit = SubmitField('Create Challenge')