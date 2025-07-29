from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from extensions import db
from flask import current_app
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from models.bodega import Bodega  # Asegúrate que este import funcione

# --- Clase Persona (usuario + datos personales) ---
class Persona(UserMixin, db.Model):
    __tablename__ = 'persona'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    rut = db.Column(db.String(20), unique=True, nullable=False)
    direccion = db.Column(db.String(200))
    email = db.Column(db.String(150), unique=True)

    # Relaciones clave foránea
    cargo_id = db.Column(db.Integer, db.ForeignKey('cargo.id'), nullable=True)
    bodega_id = db.Column(db.Integer, db.ForeignKey('bodega.id'), nullable=True)

    # Campos de acceso
    username = db.Column(db.String(150), unique=True)
    password_hash = db.Column(db.String(150))
    tiene_login = db.Column(db.Boolean, default=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Datos personales y de contacto
    celular_personal = db.Column(db.String(20))
    celular_contacto = db.Column(db.String(20))
    persona_contacto = db.Column(db.String(150))

    # Documentación
    fecha_vencimiento_licencia = db.Column(db.Date)
    fecha_vencimiento_cedula = db.Column(db.Date)
    firma_imagen = db.Column(db.String(255))  # Ruta del archivo de firma

    # Relaciones
    roles = db.relationship('PersonaRol', back_populates='persona', cascade='all, delete-orphan')
    bodegas = db.relationship('PersonaBodega', back_populates='persona')

    # Métodos de autenticación
    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=expires_sec)
            return Persona.query.get(data['user_id'])
        except Exception:
            return None


# --- Clase intermedia: relación Persona - Bodega ---
class PersonaBodega(db.Model):
    __tablename__ = 'persona_bodega'

    __table_args__ = (
        db.Index('ix_persona_bodega_persona_id', 'persona_id'),
        db.Index('ix_persona_bodega_bodega_id', 'bodega_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    persona_id = db.Column(db.Integer, db.ForeignKey('persona.id'))
    bodega_id = db.Column(db.Integer, db.ForeignKey('bodega.id'))
    permiso = db.Column(db.String(50))

    # Relaciones
    persona = db.relationship('Persona', back_populates='bodegas')
    bodega = db.relationship('Bodega', back_populates='accesos')