from datetime import datetime
from flask import current_app
from flask.ext.login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db
from ..utils.database import CRUDMixin
from ..main.models import Fridge

BCRYPT_ROUNDS = 12

class User(UserMixin, CRUDMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    groceries = db.relationship('Fridge',
            foreign_keys=[Fridge.user_id],
            backref=db.backref('owner', lazy='joined'),
            lazy='dynamic',
            cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password.encode('utf-8'))

    def verify_password(self, password):
        return check_password_hash(self.password_hash,
                                          password.encode('utf-8'))

    def __repr__(self):
        return '<User %r>' % self.username

class AnonymousUser(AnonymousUserMixin):
    pass
