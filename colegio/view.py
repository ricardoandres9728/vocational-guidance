from flask import Blueprint, jsonify, request, session, render_template
from .model import Colegio, AspiranteColegio
from usuario.model import Usuario
from aspirante.model import Aspirante
from application import csrf, db
from werkzeug.security import generate_password_hash, check_password_hash


colegio_app = Blueprint("colegio", __name__, url_prefix="/colegio")


@colegio_app.route("/administrar/aspirantes")
def administrar_aspirantes():
    return render_template("colegio/administrar_aspirantes.html")


@colegio_app.route("/cargar/aspirantes", methods=["POST"])
def cargar_aspirantes():
    if request.method == "POST":
        data = []
        colegio = Colegio.query.filter_by(id_usuario = session["id"]).first()
        aspirantes = AspiranteColegio.query.filter_by(id_colegio=colegio.id).all()
        for aspirante in aspirantes:
            asp = Aspirante.query.filter_by(id=aspirante.id_aspirante).first()
            usuario = Usuario.query.filter_by(id=asp.id_usuario,live=True).first()
            if usuario:
                data.append({
                    "nombres":asp.nombres,
                    "apellidos":asp.apellidos,
                    "correo":usuario.correo,
                    "perfil":asp.perfil
                })
        return jsonify(data)

@colegio_app.route("/cambiar/password", methods=["POST"])
def cambiar_pass():
    if request.method == "POST":
        data = request.json
        usuario = Usuario.query.filter_by(id=session["id"]).first()
        if check_password_hash(usuario.password, data.get("password").get("anterior")):
            hashed_pass = generate_password_hash(data.get("password").get("nueva"))
            usuario.password = hashed_pass
            db.session.commit()
            return "ok"
        return "no"


@colegio_app.route("/modificar", methods=["POST"])
def modificar_perfil():
    if request.method == "POST":
        data = request.json
        usuario = Usuario.query.filter_by(id=session["id"]).first()
        usuario.correo = data.get("colegio").get("correo")
        colegio = Colegio.query.filter_by(id_usuario=usuario.id).first()
        colegio.nombre= data.get("colegio").get("nombre")
        db.session.commit()
        session["nombre"] = colegio.nombre
        return "ok"


@colegio_app.route("/perfil")
def perfil():
    return render_template("colegio/perfil_colegio.html")


@colegio_app.route("/cargar", methods=["POST"])
def cargar_aspirante():
    if request.method == "POST":
        usuario = Usuario.query.filter_by(id=session["id"]).first()
        colegio = Colegio.query.filter_by(id_usuario=usuario.id).first()
        col = {
            "nombre":colegio.nombre,
            "correo":usuario.correo,
            "password":{
                "anterior":'',
                "nueva":''
            },
        }
        session["nombre"] = colegio.nombre
        return jsonify(col)



