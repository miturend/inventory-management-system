from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from database import get_connection

auth = Blueprint("auth", __name__)


@auth.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM users
            WHERE Username = %s
        """, (username,))

        user = cursor.fetchone()

        cursor.close()
        connection.close()


        if user and check_password_hash(
            user["PasswordHash"],
            password
        ):

            session["user_id"] = user["UserID"]
            session["username"] = user["Username"]
            session["role"] = user["Role"]

            return redirect(
                url_for("dashboard.view_dashboard")
            )


        else:

            return render_template(
                "login.html",
                error="Invalid username or password."
            )


    return render_template("login.html")



@auth.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("auth.login")
    )