from application import db


class Colegio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    documento = db.Column(db.String(80), unique=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), unique=True)


class AspiranteColegio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_colegio = db.Column(db.Integer, db.ForeignKey("colegio.id"))
    id_aspirante = db.Column(db.Integer, db.ForeignKey("aspirante.id"), unique=True)
