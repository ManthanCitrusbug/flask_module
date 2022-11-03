from functools import wraps
from flask_login import current_user
from flask import redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):   
        if current_user.is_authenticated is False:
            return redirect(url_for('customadmin.login'))
        return f(*args, **kwargs)
    return decorated_function

def superuser_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.role.name != "Superuser":
                return redirect(url_for('customadmin.dashboard', username=current_user.username))
        return f(*args, **kwargs)
    return decorated_function