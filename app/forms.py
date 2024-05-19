from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, HiddenField, DateTimeLocalField
from wtforms.validators import DataRequired, ValidationError
from .wikipedia import *
from .database import *
VALID = 0
MISSING = 1
INVALID = 2

def pathValid(form, field):
    #Add the start and end articles to the list, because needed for path verification
    challenge = getChallenge(int(form.challenge_id.data)).toDict()
    data = field.data.copy()
    data.insert(0, challenge["startArticle"])
    data.append(challenge["endArticle"])
    #Will return a dictionary, with pathIndo["article"] = VALID or MISSING or INVALID
    pathInfo = checkValidPath(data)
    if pathInfo == {}:
        raise ValidationError("WIKI API CALL FAILED")
    # [article errors, path errors]
    errorsStrings = ["", ""]
    for article in pathInfo:
        #if path is not VALID, append to respective error string
        if pathInfo[article] != VALID:
            errorsStrings[pathInfo[article]-1] += article + "|"
    errorsStrings[0] = errorsStrings[0].strip("|")
    errorsStrings[1] = errorsStrings[1].strip("|")
    if errorsStrings[0] != "" or errorsStrings[1] != "":
        raise ValidationError(errorsStrings)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    login = SubmitField('Login')
    create_account = SubmitField('Create Account')
    
class SubmitForm(FlaskForm):
    path = FieldList(StringField('Path'), min_entries=1, max_entries=50, validators=[pathValid])
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
