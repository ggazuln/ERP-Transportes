# models/acceso.py

from extensions import db

class Modulo(db.Model):
    __tablename__ = 'modulo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    # Campo para el icono del módulo (ej: 'fas fa-users')
    icono = db.Column(db.String(50), nullable=False, server_default='fas fa-folder')
    # Campo para la jerarquía: apunta al ID del módulo padre.
    # Se especifica el nombre real de la columna en la BD ('modulo_padre_id')
    padre_id = db.Column('modulo_padre_id', db.Integer, db.ForeignKey('modulo.id'), nullable=True)

    # Relaciones para manejar la jerarquía padre-hijo
    hijos = db.relationship('Modulo', backref=db.backref('padre', remote_side=[id]), cascade='all, delete-orphan')

class Permiso(db.Model):
    __tablename__ = 'permiso'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(150), nullable=False)
    modulo_id = db.Column(db.Integer, db.ForeignKey('modulo.id'), nullable=False)

    modulo = db.relationship('Modulo', backref='permisos')

class Rol(db.Model):
    __tablename__ = 'rol'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)


    permisos = db.relationship('RolPermiso', back_populates='rol', cascade='all, delete-orphan')
    personas = db.relationship('PersonaRol', back_populates='rol', cascade='all, delete-orphan')

class RolPermiso(db.Model):
    __tablename__ = 'rol_permiso'
    # Se define una clave primaria compuesta, que es lo estándar para tablas de asociación.
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), primary_key=True)
    permiso_id = db.Column(db.Integer, db.ForeignKey('permiso.id'), primary_key=True)

    rol = db.relationship('Rol', back_populates='permisos')
    permiso = db.relationship('Permiso')

class PersonaRol(db.Model):
    __tablename__ = 'persona_rol'
    persona_id = db.Column(db.Integer, db.ForeignKey('persona.id'), primary_key=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'), primary_key=True)

    persona = db.relationship('Persona', back_populates='roles')
    rol = db.relationship('Rol', back_populates='personas')
