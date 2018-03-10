from flask import Blueprint, render_template, request
from .model import Usuario, TipoUsuario
from aspirante.model import Aspirante
from colegio.model import Colegio, AspiranteColegio
from application import db
from werkzeug.security import generate_password_hash

usuario_app = Blueprint("usuario", __name__)





@usuario_app.route('/registro', methods=["GET", "POST"])
def registro_usuario():
    message = None
    error = None
    tipos = TipoUsuario.query.all()
    colegios = Colegio.query.all()
    if request.method == "POST":
        form = request.form
        if not Usuario.query.filter_by(correo=form["correo"]).first():
            hashed_pass = generate_password_hash(form["password"])
            if form["tipo_usuario"] == '1':
                usuario = Usuario(
                    correo = form["correo"],
                    password = hashed_pass,
                    id_tipo_usuario =  form["tipo_usuario"]
                )
                db.session.add(usuario)
                usuario = Usuario.query.filter_by(correo=form["correo"]).first()
                aspirante = Aspirante(
                    nombre = form["nombre"],
                    documento = form["documento"],
                    id_usuario = usuario.id
                )
                db.session.add(aspirante)
                if form["colegio"] != '0':
                    aspirante = Aspirante.query.filter_by(id_usuario = usuario.id).first()
                    asp_col = AspiranteColegio(
                        id_colegio = form["colegio"],
                        id_aspirante = aspirante.id
                    )
                    db.session.add(asp_col)
                message = "Aspirante registrado con éxito"
                db.session.commit()
            if form["tipo_usuario"] == '2':
                usuario = Usuario(
                    correo = form["correo"],
                    password = hashed_pass,
                    id_tipo_usuario =  form["tipo_usuario"]
                )
                db.session.add(usuario)
                usuario = Usuario.query.filter_by(correo=form["correo"]).first()
                colegio = Colegio(
                    nombre = form["nombre_colegio"],
                    documento = form["nit"],
                    id_usuario = usuario.id
                )
                db.session.add(colegio)
                message = "Colegio registrado con éxito"
                db.session.commit()
            if form["tipo_usuario"] == '3':
                usuario = Usuario(
                    correo = form["correo"],
                    password = hashed_pass,
                    id_tipo_usuario =  form["tipo_usuario"]
                )
                db.session.add(usuario)
                message = "Usuario registrado con éxito"
                db.session.commit()
        else:
            error = "Error, correo existente"

    return render_template('usuario/registro_usuario.html', tipos=tipos, colegios=colegios, error=error, message=message)

