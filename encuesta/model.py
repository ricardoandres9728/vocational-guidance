from application import db


class Encuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_perfil = db.Column(db.Integer, db.ForeignKey("perfil.id"))
    preguntas = db.Column(db.JSON)
    live = db.Column(db.Boolean, default=True)

