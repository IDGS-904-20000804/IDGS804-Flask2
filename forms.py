from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField, RadioField
from wtforms.fields import EmailField
from wtforms import validators

def mi_validacion(form, field):
    if len(field.data) == 0:
        raise validators.ValidationError('EL campo no tiene datos')

class UserForm(Form):
    matricula = StringField('Matricula', [
        validators.DataRequired(message = 'El matricula es requerida'),
        validators.length(min = 5, max = 10, message = 'Ingresa min 5 y max 10'),
    ])
    nombre = StringField('Nombre',[
        validators.DataRequired(message = 'El nombre es requerido')
    ])
    apaterno = StringField('Apaterno', [
        mi_validacion
    ])
    amaterno = StringField('Amaterno', [
        mi_validacion
    ])
    email = EmailField('Correo', [
        mi_validacion
    ])

class LoginForm(Form):
    username = StringField('usuario', [
        validators.DataRequired(message = 'El usuario es requerido'),
        validators.length(min = 5, max = 10, message = 'Ingresa min 5 y max 10'),
    ])
    password = StringField('Contraseña', [
        validators.DataRequired(message = 'La contraseña es requerida'),
        validators.length(min = 5, max = 10, message = 'Ingresa min 5 y max 10'),
    ])
