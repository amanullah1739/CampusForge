from functools import wraps
from flask import session, redirect, url_for, flash
from database.models.user import User


def admin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "user_id" not in session:
            return redirect(url_for("login"))

        user = User.query.get(session["user_id"])

        if not user:
            session.clear()
            return redirect(url_for("login"))

        if user.role != "admin":
            flash("Admin access required.", "error")
            return redirect(url_for("dashboard"))

        return f(*args, **kwargs)

    return decorated_function