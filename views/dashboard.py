# Importa Blueprint para crear un módulo independiente de rutas
# Importa render_template para renderizar HTML desde Flask
from flask import Blueprint, render_template

# Importa decorador login_required para proteger rutas
# Importa current_user para acceder al usuario actualmente autenticado
from flask_login import login_required, current_user

# Crea el blueprint para este módulo, llamado 'dashboard'
dashboard = Blueprint('dashboard', __name__)

# Define la ruta /dashboard
@dashboard.route('/dashboard')
@login_required  # Esta ruta requiere que el usuario haya iniciado sesión
def show_dashboard():
    # Renderiza el template dashboard.html y le pasa el usuario actual como contexto
    return render_template('dashboard.html', user=current_user)
