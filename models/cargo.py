from extensions import db

class Cargo(db.Model):
    __tablename__ = 'cargo'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.String(255))

    def __str__(self):
        return self.nombre
