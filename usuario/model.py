from application import db
from datetime import datetime


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    live = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now())
    id_tipo_usuario = db.Column(db.Integer, db.ForeignKey('tipo_usuario.id'))


class TipoUsuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comentario = db.Column(db.String(500))
    fecha = db.Column(db.DateTime, default=datetime.now())
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
