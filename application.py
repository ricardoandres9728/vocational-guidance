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
    with open('codebeautify.json', 'rb') as encuestas:
        data = json.load(encuestas)
    diccionaro = data["dict"]
    data = data["data"]
    features = []
    labels = []
    model = GradientBoostingClassifier()
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
    

    x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, shuffle=True)

    model.fit(x_train, y_train)
    filename = "finalized_model.sav"
    pickle.dump(model, open(filename, 'wb'))


def insertar_datos_iniciales():
    from usuario.model import TipoUsuario
    from usuario.model import Usuario
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
