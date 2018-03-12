from application import db
from datetime import datetime


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    live = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now())
    id_tipo_usuario = db.Column(db.Integer, db.ForeignKey('tipo_usuario.id'))

    @staticmethod
    def __json__():
        return ["id", "nombre"]


class TipoUsuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))

    @staticmethod
    def __json__():
        return["id", "nombre"]
