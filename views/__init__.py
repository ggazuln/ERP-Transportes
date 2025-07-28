from views.auth import auth as auth_blueprint
from views.dashboard import dashboard as dashboard_blueprint

def register_blueprints(app):
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(dashboard_blueprint)
