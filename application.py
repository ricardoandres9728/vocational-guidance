from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_mail import Mail
from flask_login import LoginManager

uploaded_images = UploadSet('images', IMAGES)
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
mail = Mail()
login = LoginManager()


def registrar_blueprints(app):
    from foro.views import foro_app
    from aspirante.view import aspirante_app
    from colegio.view import colegio_app
    from usuario.view import usuario_app
    app.register_blueprint(foro_app)
    app.register_blueprint(colegio_app)
    app.register_blueprint(aspirante_app)
    app.register_blueprint(usuario_app)


def create_app(**config_overrides):
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')

    app.config.update(config_overrides)
    app.config.update(dict(

    ))
    db.init_app(app)
    migrate.init_app(app=app, db=db)
    csrf.init_app(app)
    mail.init_app(app)
    login.init_app(app)
    configure_uploads(app, uploaded_images)
    registrar_blueprints(app)

    return app
