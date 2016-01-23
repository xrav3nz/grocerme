import os
import logging.handlers

from flask import Flask, render_template

from config import config

from .main import main_blueprint
from .auth import auth_blueprint
from .users.models import AnonymousUser, User
from .extensions import db, bcrypt, csrf, login_manager

def create_app(config_name):

    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    configure_blueprints(app)
    configure_extensions(app)
    configure_errorhandlers(app)
    configure_logging(app)
    configure_signals(app)

    return app

def configure_extensions(app):

    # Flask-SQLAlchemy
    db.init_app(app)

    # Flask-Login
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth_blueprint.login'
    login_manager.anonymous_user = AnonymousUser

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.init_app(app)

    # Flask-Bcrypt
    bcrypt.init_app(app)

    # Flask-WTF CSRF
    csrf.init_app(app)

def configure_blueprints(app):
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

def configure_errorhandlers(app):

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("errors/forbidden_page.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/page_not_found.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/server_error.html"), 500

def configure_logging(app):

    logs_folder = os.path.join(app.root_path, os.pardir, "logs")
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    info_log = os.path.join(logs_folder, app.config['INFO_LOG'])

    info_file_handler = logging.handlers.RotatingFileHandler(
        info_log,
        maxBytes=100000,
        backupCount=10
    )

    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(formatter)
    app.logger.addHandler(info_file_handler)

    error_log = os.path.join(logs_folder, app.config['ERROR_LOG'])

    error_file_handler = logging.handlers.RotatingFileHandler(
        error_log,
        maxBytes=100000,
        backupCount=10
    )

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)

def configure_signals(app):
    pass