from main import app as flask_app  # Ya no hay conflicto de nombres
from extensions import db
from models.usuario import Persona
from werkzeug.security import generate_password_hash

with flask_app.app_context():
    usuario = Persona.query.filter_by(username="lquintanilla").first()
    if usuario:
        usuario.password_hash = generate_password_hash("123456")
        db.session.commit()
        print(f"Contraseña asignada para {usuario.username}")
    else:
        print("Usuario no encontrado.")
