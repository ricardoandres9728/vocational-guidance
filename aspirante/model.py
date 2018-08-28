from application import db


class Aspirante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(80))
    apellidos = db.Column(db.String(80))
    documento = db.Column(db.String(80), unique=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), unique=True)
    newsletter = db.Column(db.Boolean, default=True)
