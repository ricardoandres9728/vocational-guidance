from application import db


class Encuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_perfil = db.Column(db.Integer, db.ForeignKey("perfil.id"))
    live = db.Column(db.Boolean, default=True)


class Pregunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pregunta = db.Column(db.String())
    live = db.Column(db.Boolean, default=True)


class Respuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_pregunta = db.Column(db.Integer, db.ForeignKey("pregunta.id"))
    respuesta = db.Column(db.String())
    valor = db.Column(db.Integer)
    live = db.Column(db.Boolean, default=True)


class Recomendacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_pregunta = db.Column(db.Integer, db.ForeignKey("pregunta.id"))
    respuestas = db.Column(db.JSON, nullable=False)
    live = db.Column(db.Boolean, default=True)


