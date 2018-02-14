from flask import Blueprint, render_template

foro_app = Blueprint("foro", __name__)


@foro_app.route("/foro")
def foro():
    return render_template("foro/foro.html")
