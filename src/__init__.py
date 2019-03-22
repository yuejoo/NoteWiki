from flask import Flask
from .config import configs, Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()
login_manager = LoginManager()


def create_application(fleet):
    application = Flask(__name__, root_path = Config.APPLICATION_ROOT)

    application.config.from_object(configs.get(fleet))

    login_manager.init_app(application)
    database.init_app(application)

    return application