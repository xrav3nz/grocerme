from functools import wraps
from flask import redirect, flash, abort
from flask.ext.login import current_user
from .helpers import redirect_url

def anonymous_user_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            flash("You are already logged in")
            return redirect(redirect_url())
        return f(*args, **kwargs)
    return wrapper