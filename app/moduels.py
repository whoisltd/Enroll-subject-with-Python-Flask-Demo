from flask_login import current_user
from flask import request, render_template, redirect
from functools import wraps
def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.role == 'admin':
            return func(*args, **kwargs)
        return render_template("error.html", message="You cannot access this page")
    return decorated_view
