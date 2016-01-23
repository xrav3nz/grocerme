from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from flask.ext.wtf.csrf import CsrfProtect

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
csrf = CsrfProtect()