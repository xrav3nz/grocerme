from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, DateField, ValidationError
from wtforms.validators import Required, Length, Email

class NewItemForm(Form):
    name = StringField('Name', validators=[Required(), Length(1, 100)])
    default_lifespan = IntegerField('Default Lifespan', validators=[Required()])
    submit = SubmitField('Submit')

class NewUnitForm(Form):
    name = StringField('Name', validators=[Required(), Length(1, 20)])
    abbr = StringField('Abbr', validators=[Required(), Length(1, 10)])
    submit = SubmitField('Submit')

class NewFridgeItemForm(Form):
    quantity = IntegerField('Quantity', validators=[Required()])
    unit = SelectField('Unit', validators=[Required()])
    item = SelectField('Name', validators=[Required()])
    expiry_date = DateField('Expiry Date', validators=[Required()])
    submit = SubmitField('Submit')
