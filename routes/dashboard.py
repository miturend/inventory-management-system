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
        FROM products
    """)
    total_products = cursor.fetchone()["total_products"]

    cursor.execute("""
        SELECT COUNT(*) AS total_customers
        FROM customers
    """)
    total_customers = cursor.fetchone()["total_customers"]

    cursor.execute("""
        SELECT COUNT(*) AS total_suppliers
        FROM suppliers
    """)
    total_suppliers = cursor.fetchone()["total_suppliers"]

    cursor.execute("""
        SELECT IFNULL(SUM(Stock),0) AS total_stock
        FROM products
    """)
    total_stock = cursor.fetchone()["total_stock"]

    cursor.execute("""
        SELECT
            ProductName,
            Stock
        FROM products
        WHERE Stock <= 5
        ORDER BY Stock ASC
    """)

    low_stock = cursor.fetchall()

    # ==========================
    # Today's Sales
    # ==========================

    cursor.execute("""
        SELECT IFNULL(SUM(TotalAmount),0) AS today_sales
        FROM saleitems
        INNER JOIN sales
        ON SaleItems.SaleID = Sales.SaleID
        WHERE Sales.SaleDate = CURDATE()
    """)

    today_sales = cursor.fetchone()["today_sales"]

    # ==========================
    # Today's Purchases
    # ==========================

    cursor.execute("""
        SELECT IFNULL(SUM(TotalAmount),0) AS today_purchases
        FROM purchaseitems
        INNER JOIN purchases
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
        FROM products
        WHERE Stock <= 10
    """)

    low_stock = cursor.fetchone()["low_stock"]

    # Today's Sales
    cursor.execute("""
        SELECT IFNULL(SUM(SaleItems.TotalAmount),0) AS today_sales
        FROM sales
        INNER JOIN saleitems
            ON Sales.SaleID = SaleItems.SaleID
        WHERE SaleDate = CURDATE()
    """)
    today_sales = cursor.fetchone()["today_sales"]

    # Monthly Sales
    cursor.execute("""
        SELECT IFNULL(SUM(SaleItems.TotalAmount),0) AS monthly_sales
        FROM sales
        INNER JOIN saleitems
            ON Sales.SaleID = SaleItems.SaleID
        WHERE MONTH(SaleDate)=MONTH(CURDATE())
          AND YEAR(SaleDate)=YEAR(CURDATE())
    """)
    monthly_sales = cursor.fetchone()["monthly_sales"]

    # Monthly Expenses
    cursor.execute("""
        SELECT IFNULL(SUM(Amount),0) AS monthly_expenses
        FROM Expenses
        WHERE MONTH(ExpenseDate)=MONTH(CURDATE())
          AND YEAR(ExpenseDate)=YEAR(CURDATE())
    """)
    monthly_expenses = cursor.fetchone()["monthly_expenses"]

    # Top 5 Best Selling Products
    cursor.execute("""
        SELECT
            Products.ProductName,
            SUM(SaleItems.Quantity) AS TotalSold
        FROM saleitems
        INNER JOIN products
            ON SaleItems.ProductID = Products.ProductID
        GROUP BY Products.ProductID
        ORDER BY TotalSold DESC
        LIMIT 5
    """)
    top_products = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template(
        "dashboard.html",

        total_products=total_products,
        total_customers=total_customers,
        total_suppliers=total_suppliers,
        total_stock=total_stock,

        today_purchases=today_purchases,
        today_expenses=today_expenses,
        today_profit=today_profit,
        low_stock=low_stock,
        today_sales=today_sales,
        monthly_sales=monthly_sales,
        monthly_expenses=monthly_expenses,
        top_products=top_products
)