from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class CheckoutForm(Form):
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name')
    email = StringField('email', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])