from flask import Blueprint, render_template, request, session, redirect, url_for
from werkzeug.security import check_password_hash
from usuario.model import Usuario

login_app = Blueprint("login", __name__)


@login_app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('aspirante', None)
    session.pop('colegio', None)
    return redirect(url_for('.login'))


@login_app.route('/', methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        form = request.form
        if Usuario.query.filter_by(correo=form["correo"]).first():
            usuario = Usuario.query.filter_by(correo=form["correo"]).first()
            if check_password_hash(usuario.password, form["password"]):
                if usuario.id_tipo_usuario == 1:
                    session["id"] = usuario.id
                    session["apirante"] = True
                    return redirect(url_for('aspirante.perfil'))
                if usuario.id_tipo_usuario == 2:
                    session["id"] = usuario.id
                    session["colegio"] = True
                    return redirect(url_for('colegio.perfil'))
                if usuario.id_tipo_usuario == 0:
                    session["id"] = usuario.id
                    session["administrador"] = True
                    return redirect(url_for('administrador.panel_principal'))
            else:
                error = "Correo y/o contraseña incorrectos"
        else:
            error = "Correo y/o contraseña incorrectos"
    return render_template('login/login.html', error=error)
