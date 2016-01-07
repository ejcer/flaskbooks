from flask import Flask
from config import config
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.moment import Moment

db = SQLAlchemy()
mail = Mail()
moment = Moment()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    mail.init_app(app)
    moment = Moment(app)

    from main import main as main_blueprint #TODO it might need to be .main
    app.register_blueprint(main_blueprint)

    return app
