from sqlalchemy import text
from extensions import db
import logging

def obtener_menu_usuario(usuario_id):
    """
    Obtiene el menú lateral para un usuario específico.

    Args:
        usuario_id (int): El ID del usuario.

    Returns:
        dict: Un diccionario que representa el menú lateral.
    """
    if not isinstance(usuario_id, int):
        logging.error(f"Se intentó obtener el menú con un ID de usuario no válido: {usuario_id}")
        return {}

    logging.debug(f"Obteniendo menú para el usuario ID: {usuario_id}")
    menu = {}
    try:
        query = text("SELECT * FROM obtener_menu_usuario(:usuario_id)")
        resultado = db.session.execute(query, {"usuario_id": usuario_id})
    except Exception as e:
        logging.error(f"Error al obtener el menú para el usuario {usuario_id}: {e}")
        return {}

    for row in resultado:
        fila = row._mapping
        logging.debug(f"Fila de menú procesada: {dict(fila)}")

        modulo = fila["modulo"]
        submodulo = fila["submodulo"]
        permiso = fila["permiso"]
        icono = fila.get("icono", "far fa-circle")

        if modulo not in menu:
            menu[modulo] = []

        menu[modulo].append({
            "nombre": submodulo,
            "permiso": permiso,
            "icono": icono or "far fa-circle"
        })

 
    return menu
