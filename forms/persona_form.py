from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email, Optional, EqualTo
from wtforms_sqlalchemy.fields import QuerySelectField
from models.cargo import Cargo
from models.bodega import Bodega
from models.acceso import Rol  # Asumimos que tienes Rol aquí

def get_cargos():
    return Cargo.query.order_by(Cargo.nombre).all()

def get_bodegas():
    return Bodega.query.order_by(Bodega.nombre).all()

def get_roles():
    return Rol.query.order_by(Rol.nombre).all()

class PersonaForm(FlaskForm):
    # Datos Personales
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(min=2, max=100)])
    rut = StringField('RUT', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[Optional(), Email()])
    direccion = StringField('Dirección', validators=[Optional(), Length(max=200)])
    celular_personal = StringField('Celular Personal', validators=[Optional(), Length(max=20)])
    celular_contacto = StringField('Celular de Contacto', validators=[Optional(), Length(max=20)])
    persona_contacto = StringField('Persona de Contacto', validators=[Optional(), Length(max=150)])

    # Datos Laborales y Documentación
    cargo_id = QuerySelectField('Cargo', query_factory=get_cargos, get_label='nombre', allow_blank=True, blank_text='-- Seleccionar Cargo --', validators=[Optional()])
    bodega_id = QuerySelectField('Faena Principal', query_factory=get_bodegas, get_label='nombre', allow_blank=True, blank_text='-- Seleccionar Faena --', validators=[Optional()])
    fecha_vencimiento_licencia = DateField('Fecha de Vencimiento de Licencia', format='%Y-%m-%d', validators=[Optional()])
    fecha_vencimiento_cedula = DateField('Fecha de Vencimiento de Cédula', format='%Y-%m-%d', validators=[Optional()])
    firma_imagen = FileField('Imagen de Firma', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Solo imágenes permitidas (JPG, PNG)')])

    # Sistema
    activo = BooleanField('¿Activo?')
    tiene_login = BooleanField('¿Puede acceder al sistema?')
    username = StringField('Nombre de Usuario', validators=[Optional(), Length(min=4, max=150)])
    password = PasswordField('Contraseña', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[EqualTo('password', message='Las contraseñas deben coincidir.')])
    rol_id = SelectField('Rol', coerce=int, validators=[Optional()])

    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)
        # Cargar roles
        self.rol_id.choices = [(0, '-- Asignar Rol --')] + [(r.id, r.nombre) for r in get_roles()]
