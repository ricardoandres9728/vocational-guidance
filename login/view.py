from flask import Blueprint, render_template

login_app = Blueprint("login", __name__)


@login_app.route('/', methods=["GET", "POST"])
def login():
    return render_template('login/login.html')
