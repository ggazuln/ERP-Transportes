import os
import secrets
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_paginate import Pagination, get_page_parameter
from flask_login import login_required
from extensions import db
from forms.persona_form import PersonaForm
from models.usuario import Persona
from models.acceso import PersonaRol
from werkzeug.utils import secure_filename

personal = Blueprint('personal', __name__, url_prefix='/administracion/personal')

def guardar_firma(firma_file):
    random_hex = secrets.token_hex(8)
    filename = secure_filename(firma_file.filename)
    _, ext = os.path.splitext(filename)
    nombre_archivo = random_hex + ext
    ruta_completa = os.path.join(current_app.root_path, 'static/firmas', nombre_archivo)
    os.makedirs(os.path.dirname(ruta_completa), exist_ok=True)
    firma_file.save(ruta_completa)
    return nombre_archivo

@personal.route('/')
@login_required
def index():
    """Muestra la lista de todo el personal."""
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = current_app.config.get('PER_PAGE', 10)
    offset = (page - 1) * per_page

    personal_query = Persona.query.order_by(Persona.nombre)
    total = personal_query.count()
    personal_list = personal_query.offset(offset).limit(per_page).all()

    pagination = Pagination(page=page, total=total, per_page=per_page, css_framework='bootstrap5')

    return render_template('administracion/personal/index.html', personal_list=personal_list,
                           pagination=pagination, title="Administración de Personal")

@personal.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    form = PersonaForm()
    if form.validate_on_submit():
        persona = Persona(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            rut=form.rut.data,
            direccion=form.direccion.data,
            email=form.email.data,
            celular_personal=form.celular_personal.data,
            celular_contacto=form.celular_contacto.data,
            persona_contacto=form.persona_contacto.data,
            cargo_id=form.cargo_id.data.id if form.cargo_id.data else None,
            fecha_vencimiento_licencia=form.fecha_vencimiento_licencia.data,
            fecha_vencimiento_cedula=form.fecha_vencimiento_cedula.data,
            tiene_login=form.tiene_login.data,
            activo=form.activo.data,
        )

        if form.firma_imagen.data:
            persona.firma_imagen = guardar_firma(form.firma_imagen.data)

        if form.tiene_login.data:
            if not form.username.data or not form.password.data:
                flash('Debes ingresar usuario y contraseña si el usuario tendrá login.', 'danger')
                return render_template('administracion/personal/persona.html', form=form, title="Nuevo Personal", legend="Nuevo Personal")

            persona.username = form.username.data
            persona.set_password(form.password.data)

        db.session.add(persona)
        db.session.commit()  # Commit para que la persona obtenga un ID

        # Asignar rol después de que la persona tiene un ID
        if form.tiene_login.data and form.rol_id.data and form.rol_id.data > 0:
            nuevo_rol = PersonaRol(persona_id=persona.id, rol_id=form.rol_id.data)
            db.session.add(nuevo_rol)
            db.session.commit()

        flash('Usuario creado correctamente.', 'success')
        return redirect(url_for('personal.index'))

    return render_template('administracion/personal/persona.html', form=form, title="Nuevo Personal", legend="Nuevo Personal")

@personal.route('/<int:persona_id>/editar', methods=['GET', 'POST'])
@login_required
def editar(persona_id):
    """Página para editar personal existente."""
    persona = Persona.query.get_or_404(persona_id)
    form = PersonaForm(obj=persona)

    if request.method == 'GET' and persona.roles:
        form.rol_id.data = persona.roles[0].rol_id

    if form.validate_on_submit():
        # Actualizar campos del objeto persona
        persona.nombre = form.nombre.data
        persona.apellido = form.apellido.data
        persona.rut = form.rut.data
        persona.direccion = form.direccion.data
        persona.email = form.email.data
        persona.celular_personal = form.celular_personal.data
        persona.celular_contacto = form.celular_contacto.data
        persona.persona_contacto = form.persona_contacto.data
        persona.fecha_vencimiento_licencia = form.fecha_vencimiento_licencia.data
        persona.fecha_vencimiento_cedula = form.fecha_vencimiento_cedula.data
        persona.activo = form.activo.data
        persona.tiene_login = form.tiene_login.data
        persona.cargo_id = form.cargo_id.data.id if form.cargo_id.data else None

        if form.firma_imagen.data:
            persona.firma_imagen = guardar_firma(form.firma_imagen.data)

        if persona.tiene_login:
            persona.username = form.username.data
            # Solo actualizar la contraseña si se ha introducido una nueva
            if form.password.data:
                persona.set_password(form.password.data)
            
            # Actualizar rol
            PersonaRol.query.filter_by(persona_id=persona.id).delete() # Limpiar roles antiguos
            if form.rol_id.data and form.rol_id.data > 0:
                nuevo_rol = PersonaRol(persona_id=persona.id, rol_id=form.rol_id.data)
                db.session.add(nuevo_rol)
        else:
            # Si se quita el login, limpiar los datos de acceso
            persona.username = None
            PersonaRol.query.filter_by(persona_id=persona.id).delete()

        db.session.commit()
        flash('Los datos del personal han sido actualizados.', 'success')
        return redirect(url_for('personal.index'))

    return render_template('administracion/personal/persona.html', form=form, title="Editar Personal", legend=f"Editando a {persona.nombre} {persona.apellido}")
