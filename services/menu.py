from extensions import db
import logging
from models.acceso import Modulo, Permiso, PersonaRol, RolPermiso

def obtener_menu_usuario(usuario_id):
    """
    Obtiene el menú lateral jerárquico para un usuario específico usando el ORM.

    Args:
        usuario_id (int): El ID del usuario.

    Returns:
        list: Una lista de diccionarios que representa el árbol del menú.
    """
    if not isinstance(usuario_id, int):
        logging.error(f"Se intentó obtener el menú con un ID de usuario no válido: {usuario_id}")
        return []

    try:
        # --- Verificación de Administrador Global (Rol ID = 1) ---
        # Se ajusta la consulta para no depender de la columna 'id' que no existe en la BD.
        # En su lugar, se busca el objeto completo. Si existe, la condición será verdadera.
        es_admin_global = PersonaRol.query.filter_by(persona_id=usuario_id, rol_id=1).first()
        modulos = []

        if es_admin_global:
            logging.info(f"Usuario {usuario_id} es Administrador Global. Obteniendo todos los módulos.")
            # Si es admin, obtiene todos los módulos directamente.
            modulos_del_usuario = Modulo.query.order_by(Modulo.padre_id, Modulo.nombre).all()
        else:
            # --- Lógica para usuarios normales ---
            # 1. Obtener los IDs de los módulos a los que el usuario tiene CUALQUIER permiso.
            accessible_modulo_ids_subquery = db.session.query(Permiso.modulo_id)\
                .join(RolPermiso, RolPermiso.permiso_id == Permiso.id)\
                .join(PersonaRol, PersonaRol.rol_id == RolPermiso.rol_id)\
                .filter(PersonaRol.persona_id == usuario_id).distinct().subquery()

            accessible_modulos = Modulo.query.filter(Modulo.id.in_(accessible_modulo_ids_subquery)).all()

            if not accessible_modulos:
                logging.warning(f"El usuario {usuario_id} no tiene permisos sobre ningún módulo. No se generará menú.")
                return []

            # 2. Obtener también los módulos padres para construir el árbol completo.
            modulos_id_necesarios = set()
            a_revisar = {m.id for m in accessible_modulos}

            while a_revisar:
                id_actual = a_revisar.pop()
                if id_actual in modulos_id_necesarios or id_actual is None:
                    continue
                modulos_id_necesarios.add(id_actual)
                modulo = Modulo.query.get(id_actual)
                if modulo and modulo.padre_id:
                    a_revisar.add(modulo.padre_id)

            # 3. Obtener todos los objetos Modulo relevantes.
            modulos_del_usuario = Modulo.query.filter(Modulo.id.in_(modulos_id_necesarios))\
                .order_by(Modulo.padre_id, Modulo.nombre).all()

        # 4. Construir la estructura del menú a partir de los módulos.
        menu_items = {}
        for m in modulos_del_usuario:
            # Se genera un endpoint por convención. Ej: Módulo "Gestion Usuarios" -> "gestion_usuarios.index"
            # Es VITAL que tengas un blueprint llamado 'gestion_usuarios' con una ruta 'index'.
            # Se reemplazan espacios y barras para crear un nombre de blueprint válido.
            endpoint_base = m.nombre.lower().replace(' ', '_').replace('/', '_')
            menu_items[m.id] = {
                'id': m.id, 'nombre': m.nombre, 'icono': m.icono,
                'padre_id': m.padre_id,
                'endpoint': f"{endpoint_base}.index", # Asume una ruta 'index' por módulo.
                'hijos': []
            }

        # 5. Construir el árbol jerárquico.
        menu_arbol = []
        for item_id, item in menu_items.items():
            if item['padre_id'] is None:
                menu_arbol.append(item)
            elif item['padre_id'] in menu_items:
                menu_items[item['padre_id']]['hijos'].append(item)

        logging.info(f"Menú jerárquico generado para el usuario {usuario_id}: {menu_arbol}")
        return menu_arbol

    except Exception as e:
        logging.error(f"Error al construir el menú jerárquico para el usuario {usuario_id}: {e}", exc_info=True)
        return []
