from application import db


class Encuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_perfil = db.Column(db.Integer, db.ForeignKey("perfil.id"))
    live = db.Column(db.Boolean, default=True)
    preguntas = db.relationship("Pregunta", lazy="joined")


class Pregunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pregunta = db.Column(db.String())
    id_encuesta = db.Column(db.Integer, db.ForeignKey("encuesta.id"))
    live = db.Column(db.Boolean, default=True)
    respuestas = db.relationship("Respuesta", lazy="joined")
    recomendacion = db.relationship("Recomendacion", lazy="joined")


class Respuesta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_pregunta = db.Column(db.Integer, db.ForeignKey("pregunta.id"))
    respuesta = db.Column(db.String())
    valor = db.Column(db.Integer)
    live = db.Column(db.Boolean, default=True)


class Recomendacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recomendacion = db.Column(db.String())
    id_pregunta = db.Column(db.Integer, db.ForeignKey("pregunta.id"))
    live = db.Column(db.Boolean, default=True)


aspirante_respuesta = db.Table('aspirante_respuesta',
    db.Column('aspirante_id', db.Integer, db.ForeignKey('aspirante.id'), primary_key=True),
    db.Column('respuesta_id', db.Integer, db.ForeignKey('respuesta.id'), primary_key=True)
)
