from flask import Blueprint, render_template, request, jsonify
from .model import Usuario, TipoUsuario
from aspirante.model import Aspirante
from colegio.model import Colegio, AspiranteColegio
from application import db, csrf


usuario_app = Blueprint("usuario", __name__, url_prefix="/usuario")


@usuario_app.route('/tipos', methods=["POST"])
@csrf.exempt
def cargar_tipos_usuario():
    tipos = TipoUsuario.query.all()
    return jsonify(tipos)


@usuario_app.route('/administrar/colegios', methods=["POST", "GET"])
def administrar_colegios():
    if request.method == "POST":
        colegios = db.session.query(Colegio, Usuario).join(Usuario).filter(Usuario.live == True).all()
        data = []
        for colegio in colegios:
            data.append({
                'usuario': colegio.Usuario,
                'colegio': colegio.Colegio
            })
        return jsonify({'data': data})
    return render_template('usuario/administracion_colegio.html')
