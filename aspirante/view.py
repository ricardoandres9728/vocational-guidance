from flask import Blueprint
from .model import Aspirante
from usuario.model import Usuario

aspirante_app = Blueprint("aspirante", __name__, url_prefix="/aspirante")


@aspirante_app.route("/registro")
def registro_aspirante():
    pass
