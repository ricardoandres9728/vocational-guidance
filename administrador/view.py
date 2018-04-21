from flask import Blueprint, jsonify, render_template, request,url_for, redirect
from colegio.model import Colegio
from usuario.model import Usuario
from perfil.model import Perfil
from encuesta.model import Encuesta
from application import csrf, db

administrador_app = Blueprint("administrador", __name__, url_prefix="/administrador")


@administrador_app.route('/perfil/desactivar', methods=["POST"])
def desactivar_perfil():
    if request.method == "POST":
        data = request.json
        perfil = Perfil.query.filter_by(id=data.get("perfil").get("id"))
        perfil.live = False
        db.session.commit()
        return "ok"


@administrador_app.route('/perfil/modificar', methods=["POST"])
def modificar_perfil():
    if request.method == "POST":
        data = request.json
        perfil = Perfil.query.filter_by(id=data.get("perfil").get("id"))
        perfil.nombre = data.get("perfil").get("nombre")
        db.session.commit()
        return "ok"


@administrador_app.route('/perfil/administrar')
def administrar_perfiles():
    return render_template("administrador/administrar_perfiles.html")


@administrador_app.route('/encuesta/desactivar', methods=["POST"])
def desactivar_encuesta():
    if request.method == "POST":
        data = request.json
        encuesta = Encuesta.query.filter_by(id=data.get("id")).first()
        encuesta.live = False
        db.session.commit()
        return "ok"


@administrador_app.route('/encuesta/modificar', methods=["POST"])
def modificar_encuesta():
    if request.method == "POST":
        data = request.json
        encuesta = Encuesta.query.filter_by(id=data.get("encuesta").get("id")).first_or_404()
        db.session.delete(encuesta)
        db.session.commit()
        perfil = Perfil.query.filter_by(nombre=data.get("encuesta").get("perfil")).first()
        evaluacion = Encuesta(
            id = data.get("encuesta").get("id"),
            id_perfil=perfil.id,
            preguntas=data.get("encuesta").get("preguntas")
        )
        db.session.add(evaluacion)
        db.session.commit()
        return redirect(url_for(".administrar_encuesta"))


@administrador_app.route('/encuesta/cargar/todos', methods=["POST"])
def cargar_encuestas():
    encuestas = Encuesta.query.filter_by(live=True).all()
    data = []
    for encuesta in encuestas:
        perfil = Perfil.query.filter_by(id=encuesta.id_perfil).first()
        data.append({
            "id":encuesta.id,
            "perfil":perfil.nombre,
            "preguntas":encuesta.preguntas
        })
    return jsonify(data)


@administrador_app.route('/encuesta/modificar')
def administrar_encuesta():
    return render_template("administrador/modificar_encuesta.html")


@administrador_app.route('/encuesta/guardar', methods=["POST"])
def guardar_encuesta():
    mensaje = None
    if request.method == "POST":
        data = request.json
        perfil = Perfil.query.filter_by(nombre=data.get("encuesta").get("perfil")).first()
        encuesta_existente = Encuesta.query.filter_by(id_perfil=perfil.id, live=True).first()
        if not encuesta_existente:
            encuesta = Encuesta(
                id_perfil=perfil.id,
                preguntas=data.get("encuesta").get("preguntas")
            )
            db.session.add(encuesta)
            db.session.commit()
            mensaje = "ok"
            return mensaje
        else:
            mensaje = "Ya existe una encuesta para este perfil vocacional, por favor desactiva la encuesta anterior para guardar esta."
            return mensaje




@administrador_app.route('/perfil/cargar/todos', methods=["POST"])
def cargar_perfiles():
    perfiles = Perfil.query.filter_by(live=True).all()
    data = []
    for perfil in perfiles:
        data.append({
            "id": perfil.id,
            "nombre":perfil.nombre,
            "live":perfil.live,
        })
    return jsonify(data)


@administrador_app.route('/encuesta/crear')
def crear_encuesta():
    return render_template('administrador/crear_encuesta.html')
