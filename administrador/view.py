from flask import Blueprint, jsonify, render_template, request, url_for, redirect, session
from colegio.model import Colegio
from usuario.model import Usuario
from usuario.model import Feedback
from perfil.model import Perfil
from aspirante.model import Aspirante
from encuesta.model import Encuesta, Pregunta, Respuesta, Recomendacion, Muestra, MuestraRespuesta
from colegio.model import AspiranteColegio
from application import db
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import joinedload


administrador_app = Blueprint(
    "administrador", __name__, url_prefix="/administrador")


@administrador_app.route('/cambiar/pass', methods=["POST"])
def cambiar_pass():
    print("Entró a cambiar pass")


@administrador_app.route('/principal/cargar', methods=["POST"])
def principal_cargar():
    if request.method == "POST":
        adm = Usuario.query.filter_by(id=session["id"]).first()
        aspirantes = Usuario.query.filter_by(
            id_tipo_usuario=1, live=True).all()
        colegios = Usuario.query.filter_by(id_tipo_usuario=2, live=True).all()
        encuestas = Encuesta.query.filter_by(live=True).all()
        perfiles = Perfil.query.filter_by(live=True).all()
        feedback = Feedback.query.order_by(Feedback.fecha.desc()).all()
        comentarios = []
        for feed in feedback:
            usuario = Usuario.query.filter_by(
                id=feed.id_usuario, live=True).first()
            if usuario:
                user = {}
                if usuario.id_tipo_usuario == 1:
                    aspirante = Aspirante.query.filter_by(
                        id_usuario=usuario.id).first()
                    user = {
                        "nombre": aspirante.nombres+" "+aspirante.apellidos,
                        "tipo_usuario": 1,
                    }
                if usuario.id_tipo_usuario == 2:
                    colegio = Colegio.query.filter_by(
                        id_usuario=usuario.id).first()
                    user = {
                        "nombre": colegio.nombre,
                        "tipo_usuario": 2,
                    }
                comentarios.append({
                    "usuario": user,
                    "comentario": feed.comentario,
                    "fecha": feed.fecha
                })
        data = {
            "aspirantes": len(aspirantes),
            "colegios": len(colegios),
            "perfiles": len(perfiles),
            "encuestas": len(encuestas),
            "feedback": comentarios,
            "correo": adm.correo
        }
        return jsonify(data)


@administrador_app.route('/principal')
def panel_principal():
    return render_template('administrador/panel_principal.html')


@administrador_app.route('/aspirante/desactivar', methods=["POST"])
def desactivar_aspirante():
    if request.method == "POST":
        data = request.json
        usuario = Usuario.query.filter_by(
            id=data.get("aspirante").get("id_usuario")).first()
        usuario.live = False
        db.session.commit()
        return "ok"


@administrador_app.route('/aspirante/cargar/todos', methods=["POST"])
def cargar_aspirantes():
    usuarios = Usuario.query.filter_by(live=True, id_tipo_usuario=1).all()
    data = []
    for usuario in usuarios:
        aspirante = Aspirante.query.filter_by(id_usuario=usuario.id).first()
        id_colegio = AspiranteColegio.query.filter_by(
            id_aspirante=aspirante.id).first()
        if id_colegio:
            colegio = db.session.query(Colegio.nombre).filter(
                Colegio.id == id_colegio.id_colegio).first()
            colegio = colegio.nombre
        else:
            colegio = "No registra."
        data.append(
            {
                "nombres": aspirante.nombres,
                "apellidos": aspirante.apellidos,
                "correo": usuario.correo,
                "colegio": colegio,
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
        usuario = Usuario.query.filter_by(
            id=data.get("colegio").get("id_usuario")).first()
        usuario.live = False
        db.session.commit()
        return "ok"


@administrador_app.route('/colegio/modificar', methods=["POST"])
def modificar_colegio():
    if request.method == "POST":
        data = request.json
        usuario = Usuario.query.filter_by(
            id=data.get("colegio").get("id_usuario")).first()
        colegio = Colegio.query.filter_by(
            id=data.get("colegio").get("id_colegio")).first()
        usuario.correo = data.get("colegio").get("correo")
        colegio.nombre = data.get("colegio").get("nombre")
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
                        "correo": usuario.correo,
                        "nombre": colegio.nombre,
                        "id_usuario": usuario.id,
                        "id_colegio": colegio.id
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
        usuario = Usuario.query.filter_by(
            correo=data.get("colegio").get("correo")).first()
        if usuario:
            return "Correo ya registrado en el sistema."
        else:
            hashed_pass = generate_password_hash(
                data.get("colegio").get("password"))
            usuario = Usuario(
                correo=data.get("colegio").get("correo"),
                password=hashed_pass,
                id_tipo_usuario=2
            )
            db.session.add(usuario)
            db.session.flush()
            colegio = Colegio(
                nombre=data.get("colegio").get("nombre"),
                id_usuario=usuario.id
            )
            db.session.add(colegio)
            db.session.commit()
            return "ok"


@administrador_app.route('/perfil/agregar', methods=["POST"])
def agregar_perfil():
    if request.method == "POST":
        data = request.json
        perfil_existente = Perfil.query.filter_by(
            nombre=data.get("perfil").get("nombre")).first()
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
        perfil = Perfil.query.filter_by(
            id=data.get("perfil").get("id")).first()
        perfil.live = False
        db.session.commit()
        return "ok"


@administrador_app.route('/perfil/modificar', methods=["POST"])
def modificar_perfil():
    if request.method == "POST":
        data = request.json
        perfil = Perfil.query.filter_by(
            id=data.get("perfil").get("id")).first()
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
        encuesta = Encuesta.query.filter_by(
            id=data.get("encuesta").get("id")).first_or_404()
        db.session.delete(encuesta)
        perfil = Perfil.query.filter_by(
            nombre=data.get("encuesta").get("perfil")).first()
        encuesta = Encuesta(
            id_perfil=perfil.id,
        )
        db.session.add(encuesta)
        db.session.flush()
        preguntas = data.get("encuesta").get("preguntas")
        for pregunta in preguntas:
            new_pregunta = Pregunta(
                pregunta=pregunta.get("pregunta"),
                id_encuesta=encuesta.id
            )
            db.session.add(new_pregunta)
            db.session.flush()
            if not isinstance(pregunta.get("recomendacion"), list):
                recomendacion = Recomendacion(
                    recomendacion=pregunta.get("recomendacion"),
                    id_pregunta=new_pregunta.id
                )
                db.session.add(recomendacion)
            else:
                recomendacion = Recomendacion(
                    recomendacion=pregunta.get("recomendacion")[
                        0].get("recomendacion"),
                    id_pregunta=new_pregunta.id
                )
                db.session.add(recomendacion)
            respuestas = pregunta.get("respuestas")
            if not pregunta.get("id"):
                for key, respuesta in respuestas.items():
                    new_respuesta = Respuesta(
                        id_pregunta=new_pregunta.id,
                        valor=int(key),
                        respuesta=respuesta
                    )
                    db.session.add(new_respuesta)
            else:
                for respuesta in respuestas:
                    new_respuesta = Respuesta(
                        id_pregunta=new_pregunta.id,
                        valor=respuesta.get("valor"),
                        respuesta=respuesta.get("respuesta")
                    )
                    db.session.add(new_respuesta)
        db.session.commit()
        return redirect(url_for(".administrar_encuesta"))


@administrador_app.route('/encuesta/cargar/todos', methods=["POST"])
def cargar_encuestas():
    encuestas = Encuesta.query.options(joinedload(Encuesta.preguntas).joinedload(Pregunta.respuestas), joinedload(
        Encuesta.preguntas).joinedload(Pregunta.recomendacion)).filter_by(live=True).all()
    data = []
    for encuesta in encuestas:
        perfil = Perfil.query.filter_by(id=encuesta.id_perfil).first()
        data.append({
            "id": encuesta.id,
            "perfil": perfil.nombre,
            "preguntas": encuesta.preguntas
        })
    return jsonify(data)


@administrador_app.route('/encuesta/modificar')
def administrar_encuesta():
    return render_template("administrador/modificar_encuesta.html")


@administrador_app.route('/encuesta/guardar', methods=["POST"])
def guardar_encuesta():
    if request.method == "POST":
        data = request.json
        perfil = Perfil.query.filter_by(
            nombre=data.get("encuesta").get("perfil")).first()
        encuesta_existente = Encuesta.query.filter_by(
            id_perfil=perfil.id, live=True).first()
        if not encuesta_existente:
            encuesta = Encuesta(
                id_perfil=perfil.id,
            )
            db.session.add(encuesta)
            db.session.flush()
            preguntas = data.get("encuesta").get("preguntas")
            for pregunta in preguntas:
                new_pregunta = Pregunta(
                    pregunta=pregunta.get("pregunta"),
                    id_encuesta=encuesta.id
                )
                db.session.add(new_pregunta)
                db.session.flush()
                recomendacion = Recomendacion(
                    recomendacion=pregunta.get("recomendacion"),
                    id_pregunta=new_pregunta.id
                )
                db.session.add(recomendacion)
                respuestas = pregunta.get("respuestas")
                for key, respuesta in respuestas.items():
                    new_respuesta = Respuesta(
                        id_pregunta=new_pregunta.id,
                        valor=int(key),
                        respuesta=respuesta
                    )
                    db.session.add(new_respuesta)
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
            "nombre": perfil.nombre,
            "live": perfil.live,
        })
    return jsonify(data)


@administrador_app.route('/encuesta/crear')
def crear_encuesta():
    return render_template('administrador/crear_encuesta.html')


@administrador_app.route('/encuesta/muestras')
def muestras_perfiles():
    return render_template('administrador/muestras_perfiles.html')


@administrador_app.route('/encuesta/cargar/muestras',  methods=["POST"])
def cargar_muestras():
    data = request.json
    encuestas = Muestra.query.filter_by(id_encuesta=data["encuesta"]).all()
    for encuesta in encuestas:
        encuesta.perfil = Perfil.query.filter_by(id=encuesta.id_perfil).first()
    return jsonify(encuestas)


@administrador_app.route('/encuesta/eliminar/muestras',  methods=["POST"])
def eliminar_muestras():
    data = request.json
    encuesta = Muestra.query.filter_by(id_encuesta=data["encuesta"]).first()
    db.session.delete(encuesta)
    db.session.commit()
    return jsonify(encuesta), 200


@administrador_app.route('/encuesta/crear/muestras',  methods=["POST"])
def crear_muestra():
    data = request.json
    muestra = Muestra(
        id_encuesta=data["encuesta_id"],
        id_perfil=data["perfil_id"],
        live=True
    )
    db.session.add(muestra)
    db.session.flush()
    for key, respuesta in data.get("respuestas").items():
        respuesta = MuestraRespuesta(
            id_muestra=muestra.id,
            id_pregunta=(int(key)),
            valor=(int(respuesta))
        )
        db.session.add(respuesta)
        db.session.flush()
    db.session.commit()
    return "Ok", 200


@administrador_app.route('/encuesta/entrenar/muestras',  methods=["POST"])
def entrenar_encuesta():
    from sklearn.ensemble import GradientBoostingClassifier
    import pickle
    data = request.json
    muestras = Muestra.query.filter_by(id_encuesta=data["encuesta"]).all()
    features = []
    labels= []
    model = GradientBoostingClassifier(
        n_estimators=100, max_depth=3, learning_rate=0.1,)
    for muestra in muestras:
        tupla = ()
        labels.append(muestra.id_perfil)
        respuestas = MuestraRespuesta.query.filter_by(id_muestra=muestra.id).all()
        for respuesta in respuestas:
            tupla = tupla + tuple([int(respuesta.valor)])
        features.append(tupla)   
    model.fit(features, labels)
    filename = str(data["encuesta"]) + ".sav"
    pickle.dump(model, open(filename, 'wb'))
    return "Ok", 200
