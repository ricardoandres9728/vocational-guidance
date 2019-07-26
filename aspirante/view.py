import pickle
import math
from flask import Blueprint, request, render_template, session, jsonify, redirect, url_for
from .model import Aspirante
from usuario.model import Usuario, Feedback
from colegio.model import Colegio, AspiranteColegio
from encuesta.model import Respuesta, Pregunta, Recomendacion
from application import db
from werkzeug.security import generate_password_hash, check_password_hash

aspirante_app = Blueprint("aspirante", __name__, url_prefix="/aspirante")


@aspirante_app.route('/encuesta/responder', methods=["GET"])
def encuesta():
    return render_template("aspirante/encuesta_aspirante.html")


@aspirante_app.route('/encuesta/guardar', methods=["POST"])
def encuesta_guardar():
    form = request.json
    usuario = Usuario.query.filter_by(id=session["id"]).first()
    aspirante = Aspirante.query.filter_by(id_usuario=usuario.id).first()
    aspirante.respuestas = []
    db.session.commit()
    recomendaciones = []
    valores = []
    if len(form) > 0:
        respuestas_form = form
        perfect_model = [4.967, 1.002, 4.949, 4.989, 3.795, 4.118, 4.979, 2.097, 4.897, 3.529, 3.048, 4.997]
        for (index, respuesta_form) in enumerate(respuestas_form):
            respuesta = Respuesta.query.filter_by(id=respuesta_form).first()
            distancia = math.sqrt(math.pow((respuesta.valor - perfect_model[index]), 2))
            if distancia > 2:
                recomendacion = Recomendacion.query.filter_by(id=respuesta.id_pregunta).first()
                if recomendacion:
                    recomendaciones.append(recomendacion.recomendacion)
            valores.append(respuesta.valor)
            aspirante.respuestas.append(respuesta)

    db.session.commit()
    filename = "finalized_model.sav"
    model = pickle.load(open(filename, 'rb'))
    respuesta = model.predict([valores])
    if respuesta[0] == 1:
        mensaje = True
    else:
        mensaje = False
    return jsonify({
        "respuesta": mensaje,
        "recomendaciones": recomendaciones
    }), 200


@aspirante_app.route('/comentarios', methods=["GET", "POST"])
def comentario():
    if request.method == "POST":
        form = request.form
        comentario = Feedback(
            id_usuario=session["id"],
            comentario=form["comentario"],
        )
        db.session.add(comentario)
        db.session.commit()

    return redirect(url_for('aspirante.perfil'))


@aspirante_app.route("/newsletter", methods=["POST"])
def newsletter():
    if request.method == "POST":
        aspirante = Aspirante.query.filter_by(id_usuario=session["id"]).first()
        aspirante.newsletter = not aspirante.newsletter
        db.session.commit()
    return "ok"


@aspirante_app.route("/cambiar/password", methods=["POST"])
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


@aspirante_app.route("/modificar", methods=["POST"])
def modificar_perfil():
    if request.method == "POST":
        data = request.json
        usuario = Usuario.query.filter_by(id=session["id"]).first()
        usuario.correo = data.get("aspirante").get("correo")
        aspirante = Aspirante.query.filter_by(id_usuario=usuario.id).first()
        aspirante.nombres = data.get("aspirante").get("nombres")
        aspirante.apellidos = data.get("aspirante").get("apellidos")
        db.session.commit()
        session["nombres"] = aspirante.nombres
        session["apellidos"] = aspirante.apellidos
        return "ok"


@aspirante_app.route("/perfil")
def perfil():
    return render_template("aspirante/perfil_aspirante.html")


@aspirante_app.route("/cargar", methods=["POST"])
def cargar_aspirante():
    if request.method == "POST":
        usuario = Usuario.query.filter_by(id=session["id"]).first()
        aspirante = Aspirante.query.filter_by(id_usuario=usuario.id).first()
        aspirante_colegio = AspiranteColegio.query.filter_by(id_aspirante=aspirante.id).first()
        if aspirante_colegio:
            colegio = Colegio.query.filter_by(id=aspirante_colegio.id_colegio).first()
            colegio = colegio.nombre
        else:
            colegio = None
        asp = {
            "nombres": aspirante.nombres,
            "apellidos": aspirante.apellidos,
            "correo": usuario.correo,
            "colegio": colegio,
            "password": {
                "anterior": '',
                "nueva": ''
            },
            "newsletter": aspirante.newsletter
        }
        session["nombres"] = aspirante.nombres
        session["apellidos"] = aspirante.apellidos
        return jsonify(asp)


@aspirante_app.route("/registro", methods=["GET", "POST"])
def registro_aspirante():
    error = None
    mensaje = None
    colegios = db.session.query(Colegio, Usuario).filter(Colegio.id_usuario == Usuario.id, Usuario.live == True,
                                                         Usuario.id_tipo_usuario == 2).all()
    if request.method == "POST":
        form = request.form
        usuario = Usuario.query.filter_by(correo=form["correo"]).first()
        if usuario:
            error = "Usuario ya registrado."
        else:
            hashed_pass = generate_password_hash(form["password"])
            usuario = Usuario(
                correo=form["correo"],
                password=hashed_pass,
                id_tipo_usuario=1
            )
            db.session.add(usuario)
            db.session.flush()
            aspirante = Aspirante(
                nombres=form["nombres"],
                apellidos=form["apellidos"],
                id_usuario=usuario.id
            )
            db.session.add(aspirante)
            db.session.flush()
            if form["colegio"] != '0':
                colegio = Colegio.query.filter_by(id=form["colegio"]).first()
                aspirante_colegio = AspiranteColegio(
                    id_colegio=colegio.id,
                    id_aspirante=aspirante.id
                )
                db.session.add(aspirante_colegio)
                db.session.flush()
            mensaje = "Datos guardados en el sistema."
            db.session.commit()
    return render_template('aspirante/registro_aspirante.html', mensaje=mensaje, error=error, colegios=colegios)
