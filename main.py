import os
from flask import Flask, session, redirect, url_for, request, current_app
from werkzeug.routing import BuildError
from config import Config
from extensions import db, login_manager, mail, migrate
from models.usuario import Persona
from views.auth import auth as auth_blueprint
from views.dashboard import dashboard as dashboard_blueprint
from views.camiones_tractos import camiones_tractos as camiones_tractos_blueprint
from views.centros_costos import centros_costos as centros_costos_blueprint
from views.personal import personal as personal_blueprint
from context.injectors import register_context_processors


def safe_url_for(endpoint, **values):
    """Genera una URL de forma segura evitando errores si el endpoint no existe."""
    if not endpoint:
        return "#"
    try:
        return url_for(endpoint, **values)
    except BuildError:
        return "#"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.jinja_env.add_extension('jinja2.ext.do')
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    register_context_processors(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Persona.query.get(int(user_id))

    app.jinja_env.globals['safe_url_for'] = safe_url_for

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    app.register_blueprint(auth_blueprint, url_prefix='/')
    app.register_blueprint(dashboard_blueprint)
    app.register_blueprint(camiones_tractos_blueprint)
    app.register_blueprint(centros_costos_blueprint)
    app.register_blueprint(personal_blueprint)

    @app.before_request
    def requerir_bodega_seleccionada():
        if 'usuario_id' in session and not session.get('bodega_id'):
            exempt_endpoints = {
                'auth.login',
                'auth.logout',
                'auth.seleccionar_bodega',
                'auth.reset_request',
                'auth.reset_token',
                'static'
            }
            if request.endpoint and request.endpoint not in exempt_endpoints:
                current_app.logger.info(
                    f"Redirigiendo a 'seleccionar_bodega': {request.path} solicitado sin bodega."
                )
                return redirect(url_for('auth.seleccionar_bodega'))

    return app


# Este bloque asegura que se cree y ejecute la app cuando se ejecuta este archivo directamente
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)  # o cambia a debug=False en producción
