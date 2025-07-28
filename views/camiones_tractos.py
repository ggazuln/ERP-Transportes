from flask import Blueprint, render_template
from flask_login import login_required

# 1. Crear el Blueprint
# El nombre 'camiones_tractos' DEBE coincidir con el que genera el menú.
camiones_tractos = Blueprint('camiones_tractos', __name__, template_folder='templates')

# 2. Crear la vista 'index'
# La ruta URL puede ser la que quieras (ej: '/camiones-tractos').
# El nombre de la función DEBE ser 'index' para que coincida con 'camiones_tractos.index'.
@camiones_tractos.route('/camiones-tractos')
@login_required
def index():
    # Por ahora, solo devolvemos un texto. Más adelante puedes crear una plantilla.
    return "<h1>Página de Camiones y Tractos</h1>"