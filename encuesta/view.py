from flask import Blueprint
from .model import Encuesta

encuesta_app = Blueprint("encuesta", __name__, url_prefix="/encuesta")
