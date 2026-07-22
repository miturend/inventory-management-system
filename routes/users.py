from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from database import get_connection
from utils.auth_helpers import login_required
from utils.permissions import roles_required

users = Blueprint("users", __name__)


@users.route("/users")
@login_required
@roles_required("Admin")
def view_users():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            UserID,
            Username,
            Role,
            CreatedDate
        FROM Users
        ORDER BY Username
    """)

    user_list = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "users.html",
        users=user_list
    )
@users.route("/users/add", methods=["GET", "POST"])
@login_required
@roles_required("Admin")
def add_user():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        role = request.form["role"]

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("add_user.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "warning")
            return render_template("add_user.html")

        password_hash = generate_password_hash(password)

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT UserID
            FROM Users
            WHERE Username = %s
        """, (username,))

        existing_user = cursor.fetchone()

        if existing_user:
            cursor.close()
            connection.close()
            flash("Username already exists.", "danger")
            return render_template("add_user.html")

        cursor.execute("""
            INSERT INTO Users
            (
                Username,
                PasswordHash,
                Role
            )
            VALUES
            (%s, %s, %s)
        """, (
            username,
            password_hash,
            role
        ))

        connection.commit()
        flash("User created successfully.", "success")

        cursor.close()
        connection.close()

        return redirect(url_for("users.view_users"))

    return render_template("add_user.html")

@users.route("/users/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
@roles_required("Admin")
def edit_user(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":

        username = request.form["username"]
        role = request.form["role"]
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password:

            if password != confirm_password:
                flash("Passwords do not match.", "danger")
                cursor.close()
                connection.close()
                return render_template(
                    "edit_user.html",
                    user={"UserID": user_id, "Username": username, "Role": role}
                )

            if len(password) < 6:
                flash("Password must be at least 6 characters.", "warning")
                cursor.close()
                connection.close()
                return render_template(
                    "edit_user.html",
                    user={"UserID": user_id, "Username": username, "Role": role}
                )

            password_hash = generate_password_hash(password)

            cursor.execute("""
                UPDATE Users
                SET
                    Username = %s,
                    PasswordHash = %s,
                    Role = %s
                WHERE UserID = %s
            """, (username, password_hash, role, user_id))
        else:
            cursor.execute("""
                UPDATE Users
                SET
                    Username = %s,
                    Role = %s
                WHERE UserID = %s
            """, (username, role, user_id))

        connection.commit()
        flash("User updated successfully.", "success")

        cursor.close()
        connection.close()

        return redirect(url_for("users.view_users"))

    cursor.execute("""
        SELECT *
        FROM Users
        WHERE UserID = %s
    """, (user_id,))

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template("edit_user.html", user=user)
@users.route("/users/delete/<int:user_id>")
@login_required
@roles_required("Admin")
def delete_user(user_id):

    # Prevent an admin from deleting themselves
    if session.get("user_id") == user_id:
        flash("You cannot delete your own account.", "warning")
        return redirect(url_for("users.view_users"))

    connection = get_connection()
    cursor = connection.cursor()

    # Prevent deleting the last Admin account
    cursor.execute("""
        SELECT Role
        FROM Users
        WHERE UserID = %s
    """, (user_id,))

    user = cursor.fetchone()

    if user and user[0] == "Admin":

        cursor.execute("""
            SELECT COUNT(*)
            FROM Users
            WHERE Role = 'Admin'
        """)

        admin_count = cursor.fetchone()[0]

        if admin_count <= 1:

            cursor.close()
            connection.close()

            flash(
                "Cannot delete the last Admin account.",
                "danger"
            )

            return redirect(url_for("users.view_users"))


    # Delete user
    cursor.execute("""
        DELETE FROM Users
        WHERE UserID = %s
    """, (user_id,))

    connection.commit()

    flash("User deleted successfully.", "success")

    cursor.close()
    connection.close()

    return redirect(url_for("users.view_users"))