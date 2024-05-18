import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # obviously dont want this permanently - look into it? may not want to push this to the db.
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DeploymentConfig(Config):
    SQLALCHEMY_DATABASE_URI =  os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'testapp.db')