from flask import Blueprint, render_template
from flask_login import login_required

# 1. Crear el Blueprint
# El nombre 'centros_costos' DEBE coincidir con el que genera el menú.
centros_costos = Blueprint('centros_costos', __name__, template_folder='templates')

# 2. Crear la vista 'index'
# La ruta URL puede ser la que quieras (ej: '/centros-costos').
# El nombre de la función DEBE ser 'index' para que coincida con 'centros_costos.index'.
@centros_costos.route('/centros-costos')
@login_required
def index():
    # Por ahora, solo devolvemos un texto. Más adelante puedes crear una plantilla.
    return "<h1>Página de Centros de Costos</h1>"