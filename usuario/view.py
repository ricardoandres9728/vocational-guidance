from flask import Blueprint, render_template, request, jsonify
from .model import Usuario, TipoUsuario
from aspirante.model import Aspirante
from colegio.model import Colegio, AspiranteColegio
from application import db, csrf


usuario_app = Blueprint("usuario", __name__, url_prefix="/usuario")


