from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FieldList, HiddenField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    login = SubmitField('Login')
    create_account = SubmitField('Create Account')
    
class SubmitForm(FlaskForm):
    path = FieldList(StringField('Path'), min_entries=1, max_entries=50)
    challenge_id = HiddenField()
