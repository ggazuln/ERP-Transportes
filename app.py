import os
from flask import Flask, session, redirect, url_for, request
from config import Config
from extensions import db, login_manager, mail, migrate
from models.usuario import Persona
from views.auth import auth as auth_blueprint
from views.dashboard import dashboard as dashboard_blueprint
from context.injectors import register_context_processors

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    register_context_processors(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Persona.query.get(int(user_id))

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    app.register_blueprint(auth_blueprint, url_prefix='/')
    app.register_blueprint(dashboard_blueprint)

    # 🔒 Validación global: bloquear acceso si no hay bodega seleccionada
    @app.before_request
    def requerir_bodega_seleccionada():
        if 'usuario_id' in session and not session.get('bodega_id'):
            rutas_permitidas = [
                '/', 
                '/login', 
                '/logout', 
                '/reset_password',
                '/seleccionar_bodega'
            ]
            if request.path.startswith('/static'):
                return  # permitir recursos estáticos
            if any(request.path.startswith(ruta) for ruta in rutas_permitidas):
                return  # permitir rutas públicas
            print(f"🚫 Bloqueado: {request.path} sin bodega seleccionada")
            return redirect(url_for('auth.seleccionar_bodega'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
