from flask import Flask, Blueprint

from .config import configs, Config, APPLICATION_ROOT
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'

def create_application(fleet):
    application = Flask(__name__, root_path = APPLICATION_ROOT)

    application.config.from_object(configs.get(fleet))

    login_manager.init_app(application)
    database.init_app(application)

    return application