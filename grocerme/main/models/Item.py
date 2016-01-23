from ...extensions import db
from ...utils.database import CRUDMixin
from . import Fridge

class Item(db.Model, CRUDMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    default_lifespan = db.Column(db.DateTime)

    list = db.relationship('Fridge',
                foreign_keys=[Fridge.item_id],
                backref=db.backref('detail', lazy='joined'),
                lazy='dynamic',
                cascade='all, delete-orphan')
