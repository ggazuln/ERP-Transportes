from extensions import db

class Bodega(db.Model):
    __tablename__ = 'bodega'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ubicacion = db.Column(db.String(150))
    tipo = db.Column(db.String(100))

    # relación directa con Persona
    personas_principal = db.relationship('Persona', backref='bodega_principal', lazy=True)

    # relación intermedia con PersonaBodega
    accesos = db.relationship('PersonaBodega', back_populates='bodega')

    empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'))
    empresa = db.relationship('Empresa')
