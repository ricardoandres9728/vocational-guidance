from flask import Blueprint
from .model import Usuario, TipoUsuario

usuario_app = Blueprint("usuario", __name__)
