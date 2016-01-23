from ...extensions import db
from ...utils.database import CRUDMixin

class Fridge(db.Model, CRUDMixin):
    __tablename__ = 'fridges'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # eg. 2
    quantity = db.Column(db.Float)

    # eg. lbs
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'))

    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    expiry_date = db.Column(db.DateTime)

    @property
    def item_name(self):
        return self.detail.name

    @item_name.setter
    def item_name(self, item_name):
        from . import Item
        new_item = Item.query.filter_by(name=item_name).first()
        if new_item is None:
            new_item = Item(name=item_name)
            new_item.save()
        self.item_id = new_item.id

    def __repr__(self):
        return '<Fridge %r>' % self.id