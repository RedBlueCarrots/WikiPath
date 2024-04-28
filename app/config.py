import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # obviously dont want this permanently - look into it? may not want to push this to the db.
    SECRET_KEY = 'REPLACE THIS WITH SECRET KEY'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False