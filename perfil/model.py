from application import db


class Perfil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    live = db.Column(db.Boolean, default=True)
