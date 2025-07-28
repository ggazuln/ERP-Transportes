from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField(
        'Usuario',
        validators=[
            DataRequired(message="El nombre de usuario es obligatorio."),
            Length(min=3, max=50, message="Debe tener entre 3 y 50 caracteres.")
        ]
    )
    
    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(message="La contraseña es obligatoria."),
            Length(min=6, message="Debe tener al menos 6 caracteres.")
        ]
    )
    
    submit = SubmitField('Iniciar sesión')
