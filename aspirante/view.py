from flask import Blueprint, request
from .model import Aspirante
from usuario.model import Usuario

aspirante_app = Blueprint("aspirante", __name__, url_prefix="/aspirante")


@aspirante_app.route("/registro", methods=["POST"])
def registro_aspirante():
    form = request.form
    print(form)
    return "ok"
