from flask import Blueprint, render_template
from database import get_connection

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/dashboard")
def view_dashboard():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total_products FROM Products")
    total_products = cursor.fetchone()["total_products"]

    cursor.execute("SELECT COUNT(*) AS total_customers FROM Customers")
    total_customers = cursor.fetchone()["total_customers"]

    cursor.execute("SELECT COUNT(*) AS total_suppliers FROM Suppliers")
    total_suppliers = cursor.fetchone()["total_suppliers"]

    cursor.execute("SELECT SUM(Stock) AS total_stock FROM Products")
    total_stock = cursor.fetchone()["total_stock"]

    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",
        total_products=total_products,
        total_customers=total_customers,
        total_suppliers=total_suppliers,
        total_stock=total_stock
    )