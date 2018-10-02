from flask import Blueprint, jsonify, render_template, request,url_for, redirect
from colegio.model import Colegio
from usuario.model import Usuario
from perfil.model import Perfil
from aspirante.model import Aspirante
from encuesta.model import Encuesta
from colegio.model import AspiranteColegio
from application import csrf, db
from werkzeug.security import generate_password_hash


administrador_app = Blueprint("administrador", __name__, url_prefix="/administrador")


@administrador_app.route('/principal')
def panel_principal():
    return render_template('administrador/modificar_encuesta.html')

@administrador_app.route('/aspirante/desactivar', methods=["POST"])
def desactivar_aspirante():
    if request.method == "POST":
        data = request.json
        usuario = Usuario.query.filter_by(id=data.get("aspirante").get("id_usuario")).first()
        usuario.live = False
        db.session.commit()
        return "ok"


@administrador_app.route('/aspirante/cargar/todos', methods=["POST"])
def cargar_aspirantes():
    usuarios = Usuario.query.filter_by(live=True, id_tipo_usuario=1).all()
    data = []
    for usuario in usuarios:
        aspirante = Aspirante.query.filter_by(id_usuario=usuario.id).first()
        id_colegio = AspiranteColegio.query.filter_by(id_aspirante=aspirante.id).first()
        if id_colegio:
            colegio = db.session.query(Colegio.nombre).filter(Colegio.id==id_colegio.id_colegio).first()
            colegio = colegio.nombre
        else:
            colegio = "No registra."
        data.append(
            {
                "nombres":aspirante.nombres,
                "apellidos":aspirante.apellidos,
                "documento":aspirante.documento,
                "correo":usuario.correo,
                "colegio":colegio,
                "fecha": usuario.fecha_creacion,
                "id_usuario": usuario.id
            }
        )
    return jsonify(data)


@administrador_app.route('/aspirante/administrar')
def administrar_aspirante():
    return render_template('administrador/administrar_aspirantes.html')

@administrador_app.route('/colegio/desactivar', methods=["POST"])
def desactivar_colegio():
    if request.method == "POST":
        data = request.json
        usuario = Usuario.query.filter_by(id=data.get("colegio").get("id_usuario")).first()
        usuario.live = False
        db.session.commit()
        return "ok"


@administrador_app.route('/colegio/modificar', methods=["POST"])
def modificar_colegio():
    if request.method == "POST":
        data = request.json
        usuario = Usuario.query.filter_by(id=data.get("colegio").get("id_usuario")).first()
        colegio = Colegio.query.filter_by(id=data.get("colegio").get("id_colegio")).first()
        usuario.correo = data.get("colegio").get("correo")
        colegio.nombre = data.get("colegio").get("nombre")
        colegio.documento = data.get("colegio").get("documento")
        db.session.commit()
        return "ok"


@administrador_app.route('/colegio/cargar/todos', methods=["POST"])
def cargar_colegios():
    if request.method == "POST":
        colegios = Colegio.query.all()
        data = []
        for colegio in colegios:
            usuario = Usuario.query.filter_by(id=colegio.id_usuario).first()
            if usuario.live:
                data.append(
                    {
                        "correo":usuario.correo,
                        "nombre":colegio.nombre,
                        "documento":colegio.documento,
                        "id_usuario":usuario.id,
                        "id_colegio":colegio.id
                    }
                )
        return jsonify(data)


@administrador_app.route('/colegio/administrar')
def administrar_colegio():
    return render_template('administrador/administrar_colegios.html')

@administrador_app.route('/colegio/registrar', methods=["POST"])
def registrar_colegio():
    if request.method == "POST":
        data = request.json
        if not Usuario.query.filter_by(correo=data.get("colegio").get("correo")).first() or Usuario.query.filter_by(documento=Usuario.query.filter_by(correo=data.get("colegio").get("documento")).first()):
            hashed_pass = generate_password_hash(data.get("colegio").get("password"))
            usuario = Usuario(
                correo=data.get("colegio").get("correo"),
                password=hashed_pass,
                id_tipo_usuario=2
            )
            db.session.add(usuario)
            db.session.flush()
            colegio = Colegio(
                nombre=data.get("colegio").get("nombre"),
                documento=data.get("colegio").get("documento"),
                id_usuario=usuario.id
            )
            db.session.add(colegio)
            db.session.commit()
            return "ok"
        else:
            return "Correo y/o documento ya registrado en el sistema."


@administrador_app.route('/perfil/agregar', methods=["POST"])
def agregar_perfil():
    if request.method == "POST":
        data = request.json
        perfil_existente = Perfil.query.filter_by(nombre=data.get("perfil").get("nombre")).first()
        if not perfil_existente:
            perfil = Perfil(
                nombre=data.get("perfil").get("nombre")
            )
            db.session.add(perfil)
            db.session.commit()
            return "ok"
        else:
            return "Perfil ya registrado en el sistema."


@administrador_app.route('/perfil/desactivar', methods=["POST"])
def desactivar_perfil():
    if request.method == "POST":
        data = request.json
        perfil = Perfil.query.filter_by(id=data.get("perfil").get("id")).first()
        perfil.live = False
        db.session.commit()
        return "ok"


@administrador_app.route('/perfil/modificar', methods=["POST"])
def modificar_perfil():
    if request.method == "POST":
        data = request.json
        perfil = Perfil.query.filter_by(id=data.get("perfil").get("id")).first()
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
