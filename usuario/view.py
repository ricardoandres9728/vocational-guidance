from flask import Blueprint, render_template, request, jsonify
from .model import Usuario, TipoUsuario
from aspirante.model import Aspirante
from colegio.model import Colegio, AspiranteColegio
from application import db, csrf
from werkzeug.security import generate_password_hash


usuario_app = Blueprint("usuario", __name__, url_prefix="/usuario")


@usuario_app.route('/tipos', methods=["POST"])
@csrf.exempt
def cargar_tipos_usuario():
    tipos = TipoUsuario.query.all()
    print(tipos)
    return jsonify(tipos)
