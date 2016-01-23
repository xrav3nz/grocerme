from ...extensions import db
from ...utils.database import CRUDMixin

class Fridge(db.Model, CRUDMixin):
    __tablename__ = 'fridges'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # eg. 2
    quality = db.Column(db.Float)

    # eg. lbs
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'))

    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    expiry_date = db.Column(db.DateTime)