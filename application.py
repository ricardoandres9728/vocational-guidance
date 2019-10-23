from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_mail import Mail
from flask_login import LoginManager
from utilities.json_encoder import AlchemyEncoder
from sqlalchemy import event

uploaded_images = UploadSet('images', IMAGES)
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
mail = Mail()
login = LoginManager()


def crear_perfiles():
    from sklearn.ensemble import GradientBoostingClassifier
    import json
    import pickle
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import log_loss
    with open('codebeautify.json', 'rb') as encuestas:
        data = json.load(encuestas)
    diccionaro = data["dict"]
    data = data["data"]
    features = []
    labels = []
    model = GradientBoostingClassifier(
        n_estimators=100, max_depth=3, learning_rate=0.1,)
    for value in data:
        tupla = ()
        labels.append(int(value["carrera"]))
        for dic in diccionaro:
            if not dic == "genero":
                tupla = tupla + tuple([float(value[dic])])
            else:
                if value["genero"] == "MASCULINO":
                    tupla = tupla + tuple([0])
                else:
                    tupla = tupla + tuple([1])
        features.append(tupla)
    model.fit(features, labels)
    filename = "1.sav"
    pickle.dump(model, open(filename, 'wb'))


def insertar_datos_iniciales():
    from usuario.model import TipoUsuario
    from usuario.model import Usuario
    from encuesta.model import Encuesta, Pregunta, Respuesta, Recomendacion, Muestra, MuestraRespuesta
    from perfil.model import Perfil

    @event.listens_for(MuestraRespuesta.__table__, 'after_create')
    def insetar_muestras(*args, **kwargs):
        import json
        with open('codebeautify.json', 'rb') as encuestas:
            data = json.load(encuestas)
        diccionaro = data["dict"]
        data = data["data"]
        dict_ids = {
            "funcionamiento": 1,
            "personas-maquinas": 2,
            "ultima-generacion": 3,
            "lenguaje": 4,
            "lenguajes-conocidos": 5,
            "matematicas": 6,
            "cacharrero": 7,
            "algoritmo": 8,
            "manejar-pc": 9,
            "trabajan": 10,
            "formacion-madre": 11,
            "formacion-padre": 12
        }

        for value in data:
            muestra = Muestra(
            id_encuesta=1,
            live=True)
            if int(value["carrera"]) == 1:
                muestra.id_perfil = 2
            else:
                muestra.id_perfil = 1
            db.session.add(muestra)
            db.session.flush()
            for dic in diccionaro:
                respuesta = MuestraRespuesta(
                    id_muestra=muestra.id,
                    valor=int(value[dic]),
                    id_pregunta=int(dict_ids.get(dic)))
                db.session.add(respuesta)
        db.session.commit()    

    @event.listens_for(TipoUsuario.__table__, 'after_create')
    def insentar_tipos_usuario(*args, **kwargs):
        db.session.add(TipoUsuario(nombre="administrador", id=0))
        db.session.add(TipoUsuario(nombre="aspirante", id=1))
        db.session.add(TipoUsuario(nombre="colegio", id=2))
        db.session.commit()

    @event.listens_for(Usuario.__table__, 'after_create')
    def intertar_administrador(*args, **kwargs):
        from werkzeug.security import generate_password_hash
        db.session.add(Usuario(
            correo="1@1",
            password=generate_password_hash('1234'),
            live=True,
            id_tipo_usuario=0
        ))
        db.session.commit()

    @event.listens_for(Recomendacion.__table__, 'after_create')
    def intertar_encuesta(*args, **kwargs):
        perfil = Perfil(
            nombre="Psicologia"
        )
        db.session.add(perfil)
        db.session.flush()
        perfil = Perfil(
            nombre="Ing. Sistemas"
        )
        db.session.add(perfil)
        db.session.flush()
        encuesta = Encuesta(
            id_perfil=perfil.id
        )
        db.session.add(encuesta)
        db.session.flush()
        pregunta = Pregunta(
            pregunta="¿Qué tanto te gusta saber acerca del funcionamiento interno "
                     "de las máquinas y las computadoras? ",
            id_encuesta=encuesta.id
        )
        db.session.add(pregunta)
        db.session.flush()
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="1",
            valor=1
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="2",
            valor=2
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="3",
            valor=3
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="4",
            valor=4
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="5",
            valor=5
        )
        db.session.add(respuesta)
        recomendacion = Recomendacion(
            recomendacion="Interesate más",
            id_pregunta=pregunta.id
        )
        db.session.add(recomendacion)
        pregunta = Pregunta(
            pregunta="¿Prefieres trabajar con máquinas o con personas? "
                     "(1 para “exclusivamente máquinas”, 5 para “exclusivamente personas”)",
            id_encuesta=encuesta.id
        )
        db.session.add(pregunta)
        db.session.flush()
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="1",
            valor=1
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="2",
            valor=2
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="3",
            valor=3
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="4",
            valor=4
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="5",
            valor=5
        )
        db.session.add(respuesta)
        recomendacion = Recomendacion(
            recomendacion="",
            id_pregunta=pregunta.id
        )
        db.session.add(recomendacion)
        pregunta = Pregunta(
            pregunta="¿Qué tanto te interesa trabajar con tecnología de última generación?",
            id_encuesta=encuesta.id
        )
        db.session.add(pregunta)
        db.session.flush()
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="1",
            valor=1
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="2",
            valor=2
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="3",
            valor=3
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="4",
            valor=4
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="5",
            valor=5
        )
        db.session.add(respuesta)
        recomendacion = Recomendacion(
            recomendacion="Compra PC nuevo",
            id_pregunta=pregunta.id
        )
        db.session.add(recomendacion)
        pregunta = Pregunta(
            pregunta="¿Antes de inscribirte en el programa conocías qué era un lenguaje de programación? ",
            id_encuesta=encuesta.id
        )
        db.session.add(pregunta)
        db.session.flush()
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="1",
            valor=1
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="2",
            valor=2
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="3",
            valor=3
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="4",
            valor=4
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="5",
            valor=5
        )
        db.session.add(respuesta)
        recomendacion = Recomendacion(
            recomendacion="",
            id_pregunta=pregunta.id
        )
        db.session.add(recomendacion)
        pregunta = Pregunta(
            pregunta="¿Cuántos lenguajes de programación conocías?",
            id_encuesta=encuesta.id
        )
        db.session.add(pregunta)
        db.session.flush()
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="Ninguno",
            valor=1
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="1 lenguaje",
            valor=2
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="Entre 1 & 3 lenguajes",
            valor=3
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="Entre 3 & 5 lenguajes",
            valor=4
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="Más de 5 lenguajes",
            valor=5
        )
        db.session.add(respuesta)
        recomendacion = Recomendacion(
            recomendacion="Aprende más",
            id_pregunta=pregunta.id
        )
        db.session.add(recomendacion)
        pregunta = Pregunta(
            pregunta="Tu nota media de matemáticas en el bachillerato fue de:",
            id_encuesta=encuesta.id
        )
        db.session.add(pregunta)
        db.session.flush()
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="1",
            valor=1
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="2",
            valor=2
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="3",
            valor=3
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="4",
            valor=4
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="5",
            valor=5
        )
        db.session.add(respuesta)
        recomendacion = Recomendacion(
            recomendacion="Echale ganas a la matematica",
            id_pregunta=pregunta.id
        )
        db.session.add(recomendacion)
        pregunta = Pregunta(
            pregunta="¿Qué tan “cacharrero” te consideras para arreglar los aparatos electrónicos en tu hogar?",
            id_encuesta=encuesta.id
        )
        db.session.add(pregunta)
        db.session.flush()
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="1",
            valor=1
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="2",
            valor=2
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="3",
            valor=3
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="4",
            valor=4
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="5",
            valor=5
        )
        db.session.add(respuesta)
        recomendacion = Recomendacion(
            recomendacion="Desbarata cosas",
            id_pregunta=pregunta.id
        )
        db.session.add(recomendacion)
        pregunta = Pregunta(
            pregunta="¿Sabías qué era un algoritmo cuando te presentaste al programa?",
            id_encuesta=encuesta.id
        )
        db.session.add(pregunta)
        db.session.flush()
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="1",
            valor=1
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="2",
            valor=2
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="3",
            valor=3
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="4",
            valor=4
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="5",
            valor=5
        )
        db.session.add(respuesta)
        recomendacion = Recomendacion(
            recomendacion="Aprende que es",
            id_pregunta=pregunta.id
        )
        db.session.add(recomendacion)
        pregunta = Pregunta(
            pregunta="¿Qué tan fácil te resultaba manejar la computadora cuando te presentaste al programa?",
            id_encuesta=encuesta.id
        )
        db.session.add(pregunta)
        db.session.flush()
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="1",
            valor=1
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="2",
            valor=2
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="3",
            valor=3
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="4",
            valor=4
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="5",
            valor=5
        )
        db.session.add(respuesta)
        recomendacion = Recomendacion(
            recomendacion="Practica",
            id_pregunta=pregunta.id
        )
        db.session.add(recomendacion)
        pregunta = Pregunta(
            pregunta="Cuando te presentaste al programa, en tu casa trabajaban:",
            id_encuesta=encuesta.id
        )
        db.session.add(pregunta)
        db.session.flush()
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="Nadie",
            valor=1
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="Solo yo",
            valor=2
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="Solo papá y/o mamá",
            valor=3
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="La mayoría ",
            valor=4
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="Todos trabajamos",
            valor=5
        )
        db.session.add(respuesta)
        recomendacion = Recomendacion(
            recomendacion="Asegurate de tener un buen soporte economico",
            id_pregunta=pregunta.id
        )
        db.session.add(recomendacion)
        pregunta = Pregunta(
            pregunta="Qué formación tenía tu madre",
            id_encuesta=encuesta.id
        )
        db.session.add(pregunta)
        db.session.flush()
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="No tenía estudios",
            valor=1
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="Estudios básica primaria",
            valor=2
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="Estudios básica secundaria",
            valor=3
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="Estudios técnicos y tecnólogos",
            valor=4
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="Culminó carrera profesional",
            valor=5
        )
        db.session.add(respuesta)
        pregunta = Pregunta(
            pregunta="Qué formación tenía tu padre:",
            id_encuesta=encuesta.id
        )
        db.session.add(pregunta)
        db.session.flush()
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="No tenía estudios",
            valor=1
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="Estudios básica primaria",
            valor=2
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="Estudios básica secundaria",
            valor=3
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="Estudios técnicos y tecnólogos",
            valor=4
        )
        db.session.add(respuesta)
        respuesta = Respuesta(
            id_pregunta=pregunta.id,
            respuesta="Culminó carrera profesional",
            valor=5
        )
        db.session.add(respuesta)
        db.session.commit()
       


def registrar_blueprints(app):
    from aspirante.view import aspirante_app
    from colegio.view import colegio_app
    from usuario.view import usuario_app
    from login.view import login_app
    from administrador.view import administrador_app
    from perfil.view import perfil_app
    from encuesta.view import encuesta_app
    app.register_blueprint(login_app)
    app.register_blueprint(colegio_app)
    app.register_blueprint(aspirante_app)
    app.register_blueprint(usuario_app)
    app.register_blueprint(administrador_app)
    app.register_blueprint(perfil_app)
    app.register_blueprint(encuesta_app)


def create_app(**config_overrides):
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    app.json_encoder = AlchemyEncoder
    app.config.update(config_overrides)
    app.config.update(dict(

    ))
    db.init_app(app)
    migrate.init_app(app=app, db=db)
    csrf.init_app(app)
    mail.init_app(app)
    login.init_app(app)
    registrar_blueprints(app)
    insertar_datos_iniciales()
    crear_perfiles()
    return app
