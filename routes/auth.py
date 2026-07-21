from flask import Blueprint, render_template, request, redirect, url_for
from database import get_connection

auth = Blueprint("auth", __name__)

@auth.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        sql = """
        SELECT *
        FROM Users
        WHERE Username = %s
        AND Password = %s
        """

        cursor.execute(sql, (username, password))

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            return redirect(url_for("auth.dashboard"))

        return render_template(
            "login.html",
            error="Invalid username or password."
        )

    return render_template("login.html")


@auth.route("/dashboard")
def dashboard():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM Products")
    total_products = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Customers")
    total_customers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Suppliers")
    total_suppliers = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",
        total_products=total_products,
        total_customers=total_customers,
        total_suppliers=total_suppliers,
    )