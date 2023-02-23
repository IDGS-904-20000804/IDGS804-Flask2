from wtforms import Form
from wtforms import StringField, RadioField
from wtforms import validators

def mi_validacion(form, field):
    if len(field.data) == 0:
        raise validators.ValidationError('Se deben llenar los datos')

class TraslaterForm(Form):
    spanish = StringField('Español', [
        mi_validacion
    ])
    english = StringField('Ingles', [
        mi_validacion
    ])
    traslater = RadioField('Traducir', choices=[
        ('english','Ingles'),
        ('spanish','Español')
    ])
