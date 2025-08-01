from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Optional, Length
from wtforms_sqlalchemy.fields import QuerySelectField as BaseQuerySelectField
from models.cargo import Cargo
from models.bodega import Bodega
from models.acceso import Rol
from models.usuario import Persona

# --- PARCHE PARA INCOMPATIBILIDAD DE VERSIONES ---
# WTForms moderno espera 4 valores de iter_choices, pero una versión antigua de
# WTForms-SQLAlchemy podría estar devolviendo 3. Esta clase personalizada
# asegura que siempre se devuelvan 4 valores.
class QuerySelectField(BaseQuerySelectField):
    def iter_choices(self):
        if self.allow_blank:
            yield ('__None', self.blank_text, self.data is None, {})

        for pk, obj in self._get_object_list():
            yield (pk, self.get_label(obj), obj == self.data, {})


# --- Factories para los QuerySelectFields ---
def cargo_factory():
    return Cargo.query.order_by(Cargo.nombre).all()

def bodega_factory():
    return Bodega.query.order_by(Bodega.nombre).all()

def rol_factory():
    return Rol.query.order_by(Rol.nombre).all()


class PersonaForm(FlaskForm):
    # Información Personal
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=100)])
    rut = StringField('RUT', validators=[DataRequired(), Length(max=12)])
    direccion = StringField('Dirección', validators=[Optional(), Length(max=255)])

    # Información de Contacto
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    celular_personal = StringField('Celular Personal', validators=[Optional(), Length(max=20)])
    persona_contacto = StringField('Contacto de Emergencia', validators=[Optional(), Length(max=100)])
    celular_contacto = StringField('Celular de Emergencia', validators=[Optional(), Length(max=20)])

    # Información Laboral y Documentos
    cargo_id = QuerySelectField('Cargo',
                                query_factory=cargo_factory,
                                get_label='nombre',
                                allow_blank=True,
                                blank_text='-- Seleccione un Cargo --')
    bodega_id = QuerySelectField('Bodega/Faena',
                                 query_factory=bodega_factory,
                                 get_label='nombre',
                                 allow_blank=True,
                                 blank_text='-- Seleccione una Bodega --')
    firma_imagen = FileField('Firma Digital', validators=[FileAllowed(['jpg', 'png', 'jpeg'], '¡Solo imágenes!')])
    fecha_vencimiento_licencia = DateField('Vencimiento Licencia', format='%Y-%m-%d', validators=[Optional()])
    fecha_vencimiento_cedula = DateField('Vencimiento Cédula', format='%Y-%m-%d', validators=[Optional()])

    # Configuración del Sistema
    activo = BooleanField('Activo', default=True)
    tiene_login = BooleanField('Tiene Login', default=False)

    # Datos de Acceso (condicional)
    username = StringField('Nombre de Usuario', validators=[Optional(), Length(min=4, max=25)])
    password = PasswordField('Contraseña', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[Optional(), EqualTo('password', message='Las contraseñas deben coincidir.')])
    rol_id = QuerySelectField('Rol de Usuario',
                              query_factory=rol_factory,
                              get_label='nombre',
                              allow_blank=True,
                              blank_text='-- Seleccione un Rol --',
                              get_pk=lambda obj: obj.id)

    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        super(PersonaForm, self).__init__(*args, **kwargs)
        # Guardar el objeto original para validaciones de unicidad al editar
        self._obj = kwargs.get('obj')

    def validate_username(self, username):
        if self.tiene_login.data and username.data:
            if hasattr(self, '_obj') and self._obj and self._obj.username == username.data:
                return
            if Persona.query.filter_by(username=username.data).first():
                raise ValidationError('Ese nombre de usuario ya está en uso. Por favor, elige otro.')

    def validate_rut(self, rut):
        if hasattr(self, '_obj') and self._obj and self._obj.rut == rut.data:
            return
        if Persona.query.filter_by(rut=rut.data).first():
            raise ValidationError('Este RUT ya está registrado en el sistema.')