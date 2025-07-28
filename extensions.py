from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
# Redirige a la vista de login si un usuario no autenticado intenta acceder a una página protegida
login_manager.login_view = 'auth.login'
# Define la categoría del mensaje flash para la redirección
login_manager.login_message_category = 'info'

mail = Mail()
migrate = Migrate()
