from ...extensions import db
from ...utils.database import CRUDMixin
from . import Fridge

class Unit(db.Model, CRUDMixin):
    __tablename__ = 'units'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    abbr = db.Column(db.String(10))

    list = db.relationship('Fridge',
        foreign_keys=[Fridge.unit_id],
        backref=db.backref('unit', lazy='joined'),
        lazy='dynamic',
        cascade='all, delete-orphan')

    def __repr__(self):
        return '<Unit %r>' % self.abbr