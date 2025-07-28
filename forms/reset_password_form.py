from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nueva Contraseña', validators=[
        DataRequired(message="La nueva contraseña es requerida."),
        Length(min=8, message="La contraseña debe tener al menos 8 caracteres.")
    ])
    confirm_password = PasswordField('Confirmar Nueva Contraseña',
                                     validators=[DataRequired(message="Por favor, confirma la contraseña."), EqualTo('password', message='Las contraseñas deben coincidir.')])
    submit = SubmitField('Resetear Contraseña')
