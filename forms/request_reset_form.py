from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class RequestResetForm(FlaskForm):
    email = StringField('Correo Electrónico',
                        validators=[DataRequired(message="El correo es requerido."), Email(message="Correo electrónico no válido.")])
    submit = SubmitField('Solicitar Reseteo de Contraseña')
