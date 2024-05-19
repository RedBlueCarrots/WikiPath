from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, HiddenField, DateTimeLocalField
from wtforms.validators import DataRequired, ValidationError
from .wikipedia import *
from .database import *

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
    
def pathValid(form, field):
    challenge = getChallenge(int(form.challenge_id.data)).toDict()
    data = field.data.copy()
    data.insert(0, challenge["startArticle"])
    data.append(challenge["endArticle"])
    pathInfo = checkValidPath(data)
    errorsString = "#"
    for article in pathInfo:
        print(article, pathInfo[article])
        if not pathInfo[article]:
            errorsString += article + "|"
    errorsString = errorsString.strip("|")
    if errorsString != "#":
        raise ValidationError(errorsString)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    login = SubmitField('Login')
    create_account = SubmitField('Create Account')
    
class SubmitForm(FlaskForm):
    path = FieldList(StringField('Path'), min_entries=1, max_entries=50, validators=[articlesExist, pathValid])
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
