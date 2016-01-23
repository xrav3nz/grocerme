from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.wtf.csrf import CsrfProtect
from flask_admin import Admin

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CsrfProtect()
admin = Admin()