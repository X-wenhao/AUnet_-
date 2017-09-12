from flask import Blueprint
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os

admin={
    'account':'admin',
    'password':'hardtoguess'
}

basedir = os.path.abspath(os.path.dirname(__file__))


db = SQLAlchemy()
bootstrap=Bootstrap()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']= 'easy to guess'
    app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///' \
                              + os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

    db.init_app(app)
    bootstrap.init_app(app)
    from . import fd as fd_blueprint
    app.register_blueprint(fd_blueprint)

    return app

fd=Blueprint('fd',__name__)

from . import views,api

