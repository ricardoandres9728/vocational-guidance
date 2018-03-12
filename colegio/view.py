from flask import Blueprint, jsonify
from .model import Colegio
from usuario.model import Usuario
from application import csrf, db

colegio_app = Blueprint("colegio", __name__, url_prefix="/colegio")


@colegio_app.route('/lista', methods=["POST"])
@csrf.exempt
def cargar_tipos_usuario():
    colegios = Colegio.query.all()
    return jsonify(colegios)
