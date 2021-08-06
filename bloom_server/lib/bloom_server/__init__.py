import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from bloom_database.models import db

migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    app.config['FLASK_APP'] = os.environ['FLASK_APP']

    initialize_extensions(app)

    app.app_context().push()

    from bloom_database.models import models

    return app


def initialize_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
