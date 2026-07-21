from flask import Blueprint, render_template
from database import get_connection
from utils.auth_helpers import login_required

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/dashboard")
@login_required
def view_dashboard():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # ==========================
    # Dashboard Totals
    # ==========================

    cursor.execute("""
        SELECT COUNT(*) AS total_products
        FROM Products
    """)
    total_products = cursor.fetchone()["total_products"]

    cursor.execute("""
        SELECT COUNT(*) AS total_customers
        FROM Customers
    """)
    total_customers = cursor.fetchone()["total_customers"]

    cursor.execute("""
        SELECT COUNT(*) AS total_suppliers
        FROM Suppliers
    """)
    total_suppliers = cursor.fetchone()["total_suppliers"]

    cursor.execute("""
        SELECT IFNULL(SUM(Stock),0) AS total_stock
        FROM Products
    """)
    total_stock = cursor.fetchone()["total_stock"]

    # ==========================
    # Today's Sales
    # ==========================

    cursor.execute("""
        SELECT IFNULL(SUM(TotalAmount),0) AS today_sales
        FROM SaleItems
        INNER JOIN Sales
        ON SaleItems.SaleID = Sales.SaleID
        WHERE Sales.SaleDate = CURDATE()
    """)

    today_sales = cursor.fetchone()["today_sales"]

    # ==========================
    # Today's Purchases
    # ==========================

    cursor.execute("""
        SELECT IFNULL(SUM(TotalAmount),0) AS today_purchases
        FROM PurchaseItems
        INNER JOIN Purchases
        ON PurchaseItems.PurchaseID = Purchases.PurchaseID
        WHERE Purchases.PurchaseDate = CURDATE()
    """)

    today_purchases = cursor.fetchone()["today_purchases"]

    # ==========================
    # Today's Expenses
    # ==========================

    cursor.execute("""
        SELECT IFNULL(SUM(Amount),0) AS today_expenses
        FROM Expenses
        WHERE ExpenseDate = CURDATE()
    """)

    today_expenses = cursor.fetchone()["today_expenses"]

    # ==========================
    # Today's Profit
    # ==========================

    today_profit = (
        today_sales
        - today_purchases
        - today_expenses
    )

    # ==========================
    # Low Stock Items
    # ==========================

    cursor.execute("""
        SELECT COUNT(*) AS low_stock
        FROM Products
        WHERE Stock <= 10
    """)

    low_stock = cursor.fetchone()["low_stock"]

    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",

        total_products=total_products,
        total_customers=total_customers,
        total_suppliers=total_suppliers,
        total_stock=total_stock,

        today_sales=today_sales,
        today_purchases=today_purchases,
        today_expenses=today_expenses,
        today_profit=today_profit,
        low_stock=low_stock
    )