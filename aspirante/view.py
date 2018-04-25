from flask import Blueprint, request, render_template
from .model import Aspirante
from usuario.model import Usuario
from colegio.model import Colegio, AspiranteColegio
from application import db
from werkzeug.security import generate_password_hash

aspirante_app = Blueprint("aspirante", __name__, url_prefix="/aspirante")


@aspirante_app.route('/')
def home():
    return render_template('aspirante/home.html')


@aspirante_app.route("/registro", methods=["GET", "POST"])
def registro_aspirante():
    if request.method == "POST":
        form = request.form
        if not Usuario.query.filter_by(correo=form["email"]).first():
            hashed_pass = generate_password_hash(form["password"])
            usuario = Usuario(
                correo=form["email"],
                password=hashed_pass,
                id_tipo_usuario=1
            )
            db.session.add(usuario)
            db.session.flush()
            aspirante = Aspirante(
                nombre=form["fullname"],
                documento=form["document"],
                id_usuario=usuario.id
            )

            db.session.add(aspirante)
            if form["colegio"] != "0":
                colegio = Colegio.query.join(Usuario).filter(Colegio.id == form["colegio"],
                                                             Usuario.live == True).first_or_404()
                aspirante_colegio = AspiranteColegio(
                    id_colegio=colegio.id,
                    id_aspirante=aspirante.id
                )
                db.session.add(aspirante_colegio)
            db.session.commit()
        else:
            usuario = Usuario.query.filter_by(correo=form["email"]).first()
            if usuario.live:
                return "Correo existente", 202
            else:
                usuario.live = True
                db.session.commit()
                return "Usuario Reactivado", 200
        return "Usuario Registrado", 200
    return render_template('aspirante/registro_aspirante.html')
