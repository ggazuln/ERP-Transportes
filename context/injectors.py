from flask import session
from models import Bodega
from services.menu import obtener_menu_usuario

def register_context_processors(app):
    @app.context_processor
    def inject_bodega_y_logo():
        contexto = {
            'bodega_nombre': None,
            'empresa_logo': None,
            'usuario': None,
            'menu_lateral': {}
        }

        # Obtener bodega y logo
        bodega_id = session.get('bodega_id')
        if bodega_id:
            bodega = Bodega.query.get(bodega_id)
            if bodega and bodega.empresa:
                contexto['bodega_nombre'] = bodega.nombre
                contexto['empresa_logo'] = bodega.empresa.logo

        # Obtener menú lateral según permisos
        usuario_id = session.get('usuario_id')
        if usuario_id:
            contexto['menu_lateral'] = obtener_menu_usuario(usuario_id)
            contexto['usuario'] = usuario_id  # si necesitas el ID del usuario también

        return contexto
