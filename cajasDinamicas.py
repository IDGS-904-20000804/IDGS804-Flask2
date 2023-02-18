from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField, RadioField

from wtforms.fields import EmailField

class CajasDinamicasForm(Form):
    num1 = StringField('Número 1')
    num2 = StringField('Número 2')
    num3 = StringField('Número 3')
    num4 = StringField('Número 4')
