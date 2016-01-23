from flask_admin.contrib.sqla import ModelView
from ..extensions import admin, db
from ..users.models import User
from ..main.models import Fridge, Unit, Item

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Fridge, db.session))
admin.add_view(ModelView(Unit, db.session))
admin.add_view(ModelView(Item, db.session))