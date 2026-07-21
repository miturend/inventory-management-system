from functools import wraps
from flask import session, redirect, url_for, flash


def roles_required(*allowed_roles):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            role = session.get("role")

            if role not in allowed_roles:

                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for("dashboard.view_dashboard"))

            return func(*args, **kwargs)

        return wrapper

    return decorator