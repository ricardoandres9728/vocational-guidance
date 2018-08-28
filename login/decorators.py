from functools import wraps
from flask import session, redirect, url_for, request


def unlogged_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id' in session:
            if 'aspirante' in session:
                return redirect(url_for('aspirante.perfil_aspirante'))
        return f(*args, **kwargs)

    return decorated_function
