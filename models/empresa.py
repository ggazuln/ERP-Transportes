from extensions import db

class Empresa(db.Model):
    __tablename__ = 'empresa'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    rut = db.Column(db.String(50))
    direccion = db.Column(db.String(255))
    telefono = db.Column(db.String(50))
    ciudad = db.Column(db.String(100))
    logo = db.Column('logo', db.String(255))   
    estado = db.Column(db.Integer)
    giro = db.Column(db.String(255))
    # Relación inversa (si tus bodegas tienen empresa_id como ForeignKey)
 
