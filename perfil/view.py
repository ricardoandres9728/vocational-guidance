from flask import Blueprint
from .model import Perfil

perfil_app = Blueprint("perfil", __name__, url_prefix="/perfil")
