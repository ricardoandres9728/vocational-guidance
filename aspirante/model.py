from application import db


class Aspirante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(80))
    apellidos = db.Column(db.String(80))
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), unique=True)
    newsletter = db.Column(db.Boolean, default=True)


class Respuestas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_aspirante = db.Column(db.Integer, db.ForeignKey("aspirante.id"))
    id_encuesta = db.Column(db.Integer, db.ForeignKey("encuesta.id"))
    respuestas = db.Column(db.JSON, nullable=False)
    live = db.Column(db.Boolean, default=True)

