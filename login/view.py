from flask import Blueprint, render_template, request, session, redirect, url_for
from werkzeug.security import check_password_hash
from usuario.model import Usuario

login_app = Blueprint("login", __name__)


@login_app.route('/', methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        form = request.form
        if Usuario.query.filter_by(correo=form["username"]).first():
            usuario = Usuario.query.filter_by(correo=form["username"]).first()
            if check_password_hash(usuario.password, form["password"]):
                if usuario.id_tipo_usuario == 1:
                    session["usuario"] = usuario.id
                    return redirect(url_for('aspirante.home'))
                if usuario.id_tipo_usuario == 2:
                    session["usuario"] = usuario.id
                    return redirect(url_for('aspirante.home'))
            else:
                error = "Correo y/o contraseña incorrectos"
        else:
            error = "Correo y/o contraseña incorrectos"
    return render_template('login/login.html', error=error)
