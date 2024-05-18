from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, HiddenField, DateTimeLocalField
from wtforms.validators import DataRequired, ValidationError
from .wikipedia import *

def articlesExist(form, field):
    errorsString = ""
    #Will return a dictionary of article names, and true/false if it exists
    articlesInfo = checkArticlesExists(field.data)
    for article in articlesInfo:
        if not articlesInfo[article]:
            errorsString += article + "|"
    errorsString = errorsString.strip("|")
    if errorsString != "":
        raise ValidationError(errorsString)
    
def pathValid(full_path):
    pathInfo = checkValidPath(full_path)
    errorsString = ""
    for article in pathInfo:
        if not pathInfo[article]:
            errorsString += article + "|"
    errorsString = errorsString.strip("|")
    return errorsString

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    login = SubmitField('Login')
    create_account = SubmitField('Create Account')
    
class SubmitForm(FlaskForm):
    path = FieldList(StringField('Path'), min_entries=1, max_entries=50, validators=[articlesExist])
    challenge_id = HiddenField()
    

class ChallengeCreationForm(FlaskForm):
    title = StringField('Challenge Title', validators=[DataRequired()])
    start = StringField('Starting Article', validators=[DataRequired()])
    destination = StringField('Destination Article', validators=[DataRequired()])
    time = DateTimeLocalField('Submission Close', validators=[DataRequired()])
    submit = SubmitField('Create Challenge')

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')