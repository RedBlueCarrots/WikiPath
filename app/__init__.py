from flask import Flask
from app.config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
login = LoginManager()

def create_app(config):
	app = Flask(__name__)
	app.config.from_object(config)
	db.init_app(app)
	login.init_app(app)
	from app.blueprints import main
	app.register_blueprint(main)

	return app

from app import routes, models, database