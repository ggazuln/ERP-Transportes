# models/acceso.py

from extensions import db

class Modulo(db.Model):
    __tablename__ = 'modulo'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

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
    id = db.Column(db.Integer, primary_key=True)
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'))
    permiso_id = db.Column(db.Integer, db.ForeignKey('permiso.id'))

    __table_args__ = (db.UniqueConstraint('rol_id', 'permiso_id', name='unique_rol_permiso'),)
    rol = db.relationship('Rol', back_populates='permisos')
    permiso = db.relationship('Permiso')

class PersonaRol(db.Model):
    __tablename__ = 'persona_rol'
    id = db.Column(db.Integer, primary_key=True)
    persona_id = db.Column(db.Integer, db.ForeignKey('persona.id'))
    rol_id = db.Column(db.Integer, db.ForeignKey('rol.id'))

    __table_args__ = (db.UniqueConstraint('persona_id', 'rol_id', name='unique_persona_rol'),)
    persona = db.relationship('Persona', back_populates='roles')
    rol = db.relationship('Rol', back_populates='personas')
