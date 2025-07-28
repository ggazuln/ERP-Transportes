import os
from flask import Flask, session, redirect, url_for, request
from werkzeug.routing import BuildError
from config import Config
from extensions import db, login_manager, mail, migrate
from models.usuario import Persona
from views.auth import auth as auth_blueprint
from views.dashboard import dashboard as dashboard_blueprint
from views.camiones_tractos import camiones_tractos as camiones_tractos_blueprint
from views.centros_costos import centros_costos as centros_costos_blueprint
from context.injectors import register_context_processors

def safe_url_for(endpoint, **values):
    """
    Genera una URL de forma segura. Si el endpoint no existe o no se puede construir,
    en lugar de lanzar un error y detener la aplicación, devuelve '#'.
    Esto permite que el menú se dibuje incluso si las páginas de destino
    aún no han sido creadas.
    """
    if not endpoint:
        return "#"
    try:
        return url_for(endpoint, **values)
    except BuildError:
        return "#"

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

    # Registra la función safe_url_for para que esté disponible en todas las plantillas.
    app.jinja_env.globals['safe_url_for'] = safe_url_for

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    app.register_blueprint(auth_blueprint, url_prefix='/')
    app.register_blueprint(dashboard_blueprint)
    app.register_blueprint(camiones_tractos_blueprint)
    app.register_blueprint(centros_costos_blueprint)

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
