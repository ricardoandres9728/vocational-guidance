from flask import Blueprint, render_template
from .model import Usuario, TipoUsuario

usuario_app = Blueprint("usuario", __name__)


@usuario_app.route('/usuario/registro')
def registro_usuario():
    return render_template('usuario/registro_usuario.html')
