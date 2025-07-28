from flask import Blueprint, render_template, redirect, session, url_for, flash, request, current_app
from flask_login import current_user, login_required, login_user, logout_user
from forms.login_form import LoginForm
from models.usuario import Persona, PersonaBodega
from models.empresa import Empresa
from forms.request_reset_form import RequestResetForm
from forms.reset_password_form import ResetPasswordForm
from flask_mail import Message
from extensions import db, mail

auth = Blueprint('auth', __name__)

def _get_bodegas_context(usuario_id):
    """
    Obtiene el contexto de bodegas (principal, virtuales y por empresa) 
    para la página de selección.
    """
    accesos = PersonaBodega.query.filter_by(persona_id=usuario_id).all()
    bodegas = [a.bodega for a in accesos]

    # Usar una comparación más estricta y robusta para los tipos de bodega
    bodega_principal = [b for b in bodegas if b.tipo.strip().lower() == 'principal']
    bodegas_virtuales = [b for b in bodegas if b.tipo.strip().lower() == 'virtual']
    
    empresas = Empresa.query.all()
    bodegas_por_empresa = {}

    for empresa in empresas:
        bodegas_empresa = [
            b for b in bodegas
            if b.empresa_id == empresa.id and b not in bodega_principal and b not in bodegas_virtuales
        ]
        if bodegas_empresa:
            bodegas_por_empresa[empresa] = bodegas_empresa
            
    return {
        "bodega_principal": bodega_principal,
        "bodegas_virtuales": bodegas_virtuales,
        "bodegas_por_empresa": bodegas_por_empresa,
    }

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Solicitud de Reseteo de Contraseña - Transportes Artisa',
                  sender=current_app.config['MAIL_DEFAULT_SENDER'],
                  recipients=[user.email])
    msg.body = f'''Para resetear tu contraseña, visita el siguiente enlace:
{url_for('auth.reset_token', token=token, _external=True)}

Si no solicitaste este cambio, simplemente ignora este correo.
'''
    mail.send(msg)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.show_dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        usuario = Persona.query.filter_by(username=form.username.data).first()

        if usuario and usuario.check_password(form.password.data):
            session.clear()  # Limpiar todo
            login_user(usuario)
            session.permanent = True
            session['usuario_id'] = usuario.id

            accesos = PersonaBodega.query.filter_by(persona_id=usuario.id).all()
            bodegas = [a.bodega for a in accesos]

            if len(bodegas) == 1:
                session['bodega_id'] = bodegas[0].id
                next_page = request.args.get('next')
                return redirect(next_page or url_for('dashboard.show_dashboard'))

            session.pop('bodega_id', None)
            context = _get_bodegas_context(usuario.id)
            return render_template('seleccionar_bodega.html', **context)
        else:
            flash("Usuario o contraseña incorrectos.", "danger")

    return render_template('login.html', form=form)

@auth.route('/seleccionar_bodega', methods=['GET', 'POST'])
@login_required
def seleccionar_bodega():
    if request.method == 'POST':
        bodega_id = request.form['bodega_id']
        acceso = PersonaBodega.query.filter_by(persona_id=current_user.id, bodega_id=bodega_id).first()
        if not acceso:
            flash("No tienes acceso a esta bodega.", "danger")
            return redirect(url_for('auth.login'))

        session['bodega_id'] = bodega_id
        return redirect(url_for('dashboard.show_dashboard'))

    # Si viene por GET (redirección automática), volver a mostrar selección
    usuario_id = session.get('usuario_id')
    context = _get_bodegas_context(usuario_id)
    return render_template('seleccionar_bodega.html', **context)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('auth.login'))

@auth.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.show_dashboard'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Persona.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash('Si tu correo está en nuestro sistema, recibirás un email con las instrucciones.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title='Resetear Contraseña', form=form)

@auth.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.show_dashboard'))
    user = Persona.verify_reset_token(token)
    if user is None:
        flash('El token es inválido o ha expirado.', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('¡Tu contraseña ha sido actualizada! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_with_token.html', title='Resetear Contraseña', form=form)
