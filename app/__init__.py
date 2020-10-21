import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from werkzeug.exceptions import HTTPException

# instantiate extensions
login_manager = LoginManager()
db = SQLAlchemy()
api = Api()
csrf = CSRFProtect()


def create_app(environment='development'):

    from config import config

    from app.apibackend.views import api_blueprint
    from app.auth.models import AnonymousUser, User
    from app.auth.views import auth_blueprint
    from app.views import main_blueprint
    from app.webbackend.views import web_blueprint

    # Instantiate app.
    app = Flask(__name__)

    # Set app config.
    env = os.environ.get('FLASK_ENV', environment)
    app.config.from_object(config[env])
    config[env].configure(app)

    # Set up extensions.
    db.init_app(app)
    api.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register blueprints.
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint)
    app.register_blueprint(web_blueprint)

    # Set up flask login.
    @login_manager.user_loader
    def get_user(id):
        return User.query.get(int(id))

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.anonymous_user = AnonymousUser

    # Error handlers.
    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        return render_template('error.html', error=exc), exc.code

    return app
